#include "../misc/common.h"
#include "../misc/options.h"
#include "../misc/trace.h"
#include "../misc/timer.h"
#include <math.h>
#include "gap_list.h"

gap_list::gap_list() 
{
}

//initial the list.
void gap_list::initial(double st_, double et_, size_t gn_)
{
	startt = st_;
	endt = et_;
	gn = gn_;
	
	gapdata.clear();
	gapstruct tempgap;
	tempgap.starttime = startt;
	tempgap.endtime = endt;
	tempgap.gapnum = gn;
	gapdata.push_back(tempgap);
}

void gap_list::init(size_t count, double in[])
{
	gapdata.clear();
	gapstruct tempgap;
	for(size_t i = 0; i < count; ++i)
	{
		tempgap.gapnum = in[3*i];
		tempgap.endtime = in[3*i+1];
		tempgap.starttime = in[3*i+2];
		gapdata.push_back(tempgap);
	}
}


double gap_list::findgap(int jnum, double jtime)
{
   //find gap in the list, and return the start time
	// gap list need to be update
	// if the process = 0, delete that gap. If process > 0 but duration time less than the gap duration time
	// split the list element. Then check if need to be merge
	double duration = 0;         //the gap duration time
	double ts = 0;               // temp start time
	double te = 0;               // temp end time
	int tn = 0;                  // temp job number
	std::list<gapstruct>::iterator it, it1, it2;
	
	for(it = gapdata.begin(); it!= gapdata.end(); ++it)
	{
		int jobdone = 0;
		ts = it->starttime;
		te = it->endtime;
		tn = it->gapnum;
		duration = te - ts;
	
		if(tn == jnum) //this have two case delete or update
		{  
		   if(jtime == duration)
		   {
				 gapdata.erase(it);
				 jobdone =1;
		   }
		   else if(jtime < duration) 
		   {
				 it->starttime += jtime;  
				 jobdone =1;
		   }
		}
		else if(tn > jnum)
		{
			if(jtime < duration)
			{
				it->starttime = ts + jtime;
				gapstruct tempgap;
				tempgap.starttime = ts;
				tempgap.endtime = ts + jtime;
				tempgap.gapnum = tn - jnum;
				gapdata.insert(it, tempgap); //here devide and add a new element of gap in list
				
				--it;
				if(it != gapdata.begin())
				{
					it1 = it;
					
					--it1;
					if((it1->gapnum == it->gapnum )&& (it1->endtime == it->starttime))     //merge front one since only the front one had the chance been merged
					{	
						it->starttime = it1->starttime;
						gapdata.erase(it1);
					}
				}
				jobdone = 1;
			}
			else if(jtime == duration)
			{
				if(it == gapdata.begin())
				{
					if(it == gapdata.end())
						it->gapnum -= jnum;
					else
					{
						it1 = it;
					
						++it1;
						it->gapnum -= jnum; 
						if((it1->gapnum == it->gapnum )&& (it1->starttime == it->endtime))     //merge back one
						{	
							it->endtime = it1->endtime;
							gapdata.erase(it1);
					    }
					}

				}
				else if (it == gapdata.end())
				{
					it1 = it;
					--it1;
					it->gapnum -= jnum; 
					
					if((it1->gapnum == it->gapnum )&& (it1->endtime == it->starttime))     //merge back one
					{	
						it->starttime = it1->starttime;
						gapdata.erase(it1);
				    }	
				}
				else
				{
					it1 = it;
					it2 = it;
					++it1;
					--it2;
					it->gapnum -= jnum;

					if((it1->gapnum == it->gapnum )&& (it1->starttime == it->endtime))     //merge back one
					{	
							it->endtime = it1->endtime;
							gapdata.erase(it1);
					}
					if((it2->gapnum == it->gapnum )&& (it2->endtime == it->starttime))     //merge back one
				    {	
							it->starttime = it2->starttime;
							gapdata.erase(it2);
					}
				
				}
				jobdone =1;
			}
		}
		 
		if(jobdone == 1)
		{
		   return ts;
		}
	}


}

double gap_list::go(int jnum, double jtime)
{

	data_1.clear();
	data_2.clear();
	data_1 = gapdata;
	data_2 = gapdata;
	double temp1, temp2;
	temp1 = 0;
	temp2 = 0;
	temp1 = findcon(jnum, jtime);
	temp2 = findmul(jnum, jtime);
	/*if(temp1 < temp2)
	{
		gapdata.clear();
		gapdata = data_1;
		if(!merge())
			printf("error accoured");
		return temp1;
	}
	else
	{
		gapdata.clear();
		gapdata = data_2;
		if(!merge())
			printf("error accoured");
		return temp2;
	}*/
	gapdata.clear();
	gapdata = data_1;
	if(!merge())
			printf("error accoured");
	return temp1;

}

double gap_list::findcon(int jnum, double jtime)
{
	if(!merge())
		printf("error occured");
	double duration = 0;         //the gap duration time
	double ts = 0;               // temp start time
	double te = 0;               // temp end time
	int tn = 0;                  // temp job number

	std::list<gapstruct>::iterator it;
	
	for(it = gapdata.begin(); it!= gapdata.end(); ++it)
	{
	    ts = it->starttime;
		te = it->endtime;
		tn = it->gapnum;
		duration = te - ts;

		if(tn >= jnum) //this have two case delete or update
		{  
		   if(duration >= jtime)
		   {
			    it->starttime = ts + jtime;
				gapstruct tempgap;
				tempgap.starttime = ts;
				tempgap.endtime = ts + jtime;
				tempgap.gapnum = tn - jnum;
				gapdata.insert(it, tempgap); //here divide and add a new element of gap in list
				return ts;
			}
		}	
	}
}

double gap_list::findmul(int jnum, double jtime)
{
	if(!merge())
		printf("error occured");
	double duration = 0;         //the gap duration time
	double ts = 0;               // temp start time
	double te = 0;               // temp end time
	int tn = 0;                  // temp job number
	size_t temptry;
	double temptime;
	temptry = 0;
	temptime = 0;
	std::list<gapstruct>::iterator it, it1, it2;
	
	for(it = gapdata.begin(); it!= gapdata.end(); ++it)
	{
	    ts = it->starttime;
		te = it->endtime;
		tn = it->gapnum;
		duration = te - ts;

		if(tn >= jnum) //this have two case delete or update
		{  
		   if(temptime == 0)
		   {
				if(duration >= jtime)
				{
					it->starttime = ts + jtime;
					gapstruct tempgap;
					tempgap.starttime = ts;
					tempgap.endtime = ts + jtime;
					tempgap.gapnum = tn - jnum;
					gapdata.insert(it, tempgap); //here divide and add a new element of gap in list
				
					return ts;
				}
				else
				{
					++temptry;
					temptime += duration;
				}
		   }
		   else
		   {
				if(temptime + duration >= jtime)
				{
					assert(temptry!=0);
					it1 = it;
					for(size_t i = 0; i < temptry; ++i)
					{
						--it1;
						it1->gapnum -= jnum;
					}
					it->starttime = jtime-temptime + ts ;
					gapstruct tempgap;
					tempgap.starttime = ts;
					tempgap.endtime = jtime-temptime + ts;
					tempgap.gapnum = tn - jnum;
					gapdata.insert(it, tempgap); //here divide and add a new element of gap in list
				
					return it1->starttime;
					
				}
				else if(duration >= jtime)
				{
					it->starttime = ts + jtime;
					gapstruct tempgap;
					tempgap.starttime = ts;
					tempgap.endtime = ts + jtime;
					tempgap.gapnum = tn - jnum;
					gapdata.insert(it, tempgap); //here divide and add a new element of gap in list
		
					return ts;
				}
				else
				{
					++temptry;
					temptime += duration;
				}
		   }

		   
		   
		}
		else
		{
			temptry = 0;
			temptime = 0;
		}
	}
}

bool gap_list::merge()
{
	std::list<gapstruct>::iterator it, it1, it2;

	for(it = gapdata.begin(); it!= gapdata.end(); ++it)
	{
		if((it->gapnum==0)||(it->endtime-it->starttime == 0))
		{
			it= gapdata.erase(it);
		}
	}

	/*int tn = 0;                  // temp job number

	size_t gapsize = 0;
	for(it = gapdata.begin(); it!= gapdata.end(); ++it)
		++gapsize;

	printf("test gapsize equal to %d   \n", gapsize);
	it2 = gapdata.end();
	--it2;

	if(gapsize == 2)
	{
		it = gapdata.begin();
		it1 = it;
		++it1;
		if(it->endtime == it1->starttime)
		{
			if(it->gapnum == it1->gapnum)
			{
				it->endtime = it1->endtime;
				gapdata.erase(it1);
			}
	     }
		return true;
	}
	else
	{
		for(it = gapdata.begin(); it!=it2;++it)
		{
			if(tn == 1)
			{
				--it;
				tn = 0;
			}

			it1 = it;
			++it1;

			if(it->endtime == it1->starttime)
			{
				if(it->gapnum == it1->gapnum)
				{
					it->endtime = it1->endtime;
					gapdata.erase(it1);
					tn = 1;
				}
			}
		}
	}*/
	return true;
}

size_t gap_list::gapdatasize()
{
	return gapdata.size();
}

void gap_list::copylist(double clist[])
{
}

double gap_list::makes()
{
	std::list<gapstruct>::iterator it1;
	it1 = gapdata.end();
	--it1;
	return it1->endtime;
}