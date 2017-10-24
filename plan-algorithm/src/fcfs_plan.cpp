#include "../misc/common.h"
#include "../misc/trace.h"
#include "../misc/options.h"
#include "../misc/auto_file.h"

#include "fcfs_plan.h"
#include "gap_list.h"

fcfs_plan::fcfs_plan()
{
}

void fcfs_plan::inputjob(size_t count, double in[], size_t inputnumber)
{
	srand (time(NULL));
	totaljob = count;
	totalproc = inputnumber;
	maxtime = 80000000;
	jobvec.clear();
	jobvec.resize(count);
	for(size_t i = 0; i < count; ++i)
	{
		jobvec[i].jobid = in[4*i];
		jobvec[i].jobnum = in[4*i+1];
		jobvec[i].time = in[4*i+2];
		jobvec[i].wt = in[4*i+3];
		maxtime += in[4*i+2];
	}
	bestsol = jobvec;
	planvect.clear();
	jobvec2.clear();
	jobvec2 = jobvec;
}

void fcfs_plan::inputgap(size_t count, double in[])
{
	gapvec.clear();
	for(size_t i = 0; i < count; ++i)
	{
		gapvec.push_back(in[3*i]);
		gapvec.push_back(in[3*i+1]);
		gapvec.push_back(in[3*i+2]);
	}
	std::reverse(gapvec.begin(), gapvec.end());

	if(count != 0)
	{
		gapvec.push_back(totalproc);
		gapvec.push_back(in[1]+maxtime);
		gapvec.push_back(in[1]);
	}
	else
	{
		gapvec.push_back(totalproc);
		gapvec.push_back(maxtime);
		gapvec.push_back(0);
	}
}

void fcfs_plan::initial()
{
	planvect.clear();

}

double fcfs_plan::planfirst(idproc pj[])
{
	//two major works needs to be done. 
	//1, Find gap in gap list
	//2, Update the plan vector
	/*           1       */

	//here the different function cost. temptime += gap.test.findmul(pj[i].jobnum, pj[i].time); is the average wait time;
	double temptime;
	double tmul;
	tmul = 0;
	temptime = 0;
	
	//gaptest.initial(0, maxtime, totalproc);
	gaptest.init(gapvec.size()/3, &gapvec[0]);
	
	for(size_t i = 0; i < totaljob; ++i) 
	{
		tmul = pj[i].wt;
		tmul += gaptest.findmul(pj[i].jobnum, pj[i].time); // just this is the average wait time;

		tmul += pj[i].time; //here is the response time

		tmul /= pj[i].jobnum; // here is the AWRT

		temptime += tmul;

	}
	return temptime /= totaljob;


	/*for(size_t i = 0; i < totaljob; ++i) 
	{
		tmul = pj[i].wt;
		tmul += gaptest.findmul(pj[i].jobnum, pj[i].time); // just this is the average wait time;
		////tmul = gaptest.findmul(pj[i].jobnum, pj[i].time);
		tmul *= tmul;
		//tmul *= pj[i].wt;       // here is the triple time
		temptime += tmul;

	}
	return temptime /= totaljob;// this is the mean squared wait time
	*/
	/*
	for(size_t i = 0; i < totaljob; ++i) 
	{
		
		tmul = gaptest.findmul(pj[i].jobnum, pj[i].time);
	}
	tmul = gaptest.makes();
	return tmul; // this is the make span constrain

	for(size_t i = 0; i < totaljob; ++i) 
	{
		tmul = pj[i].wt;
		tmul += gaptest.findmul(pj[i].jobnum, pj[i].time); // just this is the average wait time;

		tmul += pj[i].time; //here is the response time

		tmul /= pj[i].time; // here is the bounded slow down

		temptime += tmul;

	}
	*/
}

double fcfs_plan::plansecond(idproc pj[])
{
	//two major works needs to be done. 
	//1, Find gap in gap list
	//2, Update the plan vector
	/*           1       */
	double temptime;
	temptime = 0;
	
	//gaptest.initial(0, maxtime, totalproc);
	gaptest.init(gapvec.size()/3, &gapvec[0]);
	for(size_t i = 0; i < totaljob; ++i) 
	{
		planstruct tempplan;
		tempplan.jobid = pj[i].jobid;
		
		tempplan.waittime = gaptest.findmul(pj[i].jobnum, pj[i].time);
		temptime += tempplan.waittime;
		planvect.push_back(tempplan);
	}

	return temptime /= totaljob;
	
}


void fcfs_plan::sortplan()
{
	std::vector<planstruct> sortvec;
	sortvec.clear();
	sortvec.resize(totaljob);
	sortvec.assign(planvect.begin(), planvect.end());
	for(size_t i= 0; i<totaljob; ++i)
	{
		double mt=sortvec[i].waittime;
		double mtid=sortvec[i].jobid;
		int temp=i;
		for(size_t j=i+1; j<totaljob; ++j)
		{
			if(sortvec[j].waittime<mt)
			{
				mt=sortvec[j].waittime;
				temp=j;
			}
		}
		if(temp != i)
		{
			mt = sortvec[i].waittime;
			mtid = sortvec[i].jobid;
			sortvec[i].waittime = sortvec[temp].waittime;
			sortvec[i].jobid = sortvec[temp].jobid;
			sortvec[temp].jobid = mtid;
			sortvec[temp].waittime = mt;
		}
	}
	
	for(size_t i = 0 ; i<totaljob; ++i)
	{
		planvect[i].jobid = sortvec[i].jobid;
		planvect[i].waittime = sortvec[i].waittime;
	}
		

}

void fcfs_plan::sorttime()
{
	std::vector<idproc> sortvec;
	sortvec.clear();
	sortvec.resize(totaljob);
	sortvec = jobvec;
	for(size_t i= 0; i<totaljob; ++i)
	{
		idproc tempid;
		int temp=i;
		for(size_t j=i+1; j<totaljob; ++j)
			if(sortvec[j].time<sortvec[temp].time)
				temp=j;
		if(temp != i)
		{
			tempid = sortvec[i];
			sortvec[i] = sortvec[temp];
			sortvec[temp] = tempid;
		}
	}
	
	jobvec = sortvec;
	
}


void fcfs_plan::sortjob()
{
	std::vector<idproc> sortvec;
	sortvec.clear();
	sortvec.resize(totaljob);
	sortvec = jobvec;
	for(size_t i= 0; i<totaljob; ++i)
	{
		idproc tempid;
		int temp=i;
		for(size_t j=i+1; j<totaljob; ++j)
			if(sortvec[j].jobnum<sortvec[temp].jobnum)
				temp=j;
		if(temp != i)
		{
			tempid = sortvec[i];
			sortvec[i] = sortvec[temp];
			sortvec[temp] = tempid;
		}
	}
	
	jobvec = sortvec;
	
}

void fcfs_plan::planbasic()
{
	planvect.clear();
//	sorttime();
	basicsol.clear();

	basicsol = jobvec;
}

void fcfs_plan::outputplan(double out[])
{
	/*          2       */

	planvect.clear();
	besttime = plansecond(&bestsol[0]);
	for(size_t i = 0; i < totaljob; ++i)
	{
		out[i] = planvect[i].waittime;
	}

}
void fcfs_plan::outputplan2(double out[])
{
	sortplan();
	for(size_t i = 0; i < totaljob; ++i)
	{
		out[2*i]= planvect[i].jobid;
		out[2*i+1]= planvect[i].waittime;
	}
	
}
void fcfs_plan::outputplan3(double out[])
{
	planvect.clear();
	basicsol.clear();

	basicsol = jobvec;
	basictime = plansecond(&basicsol[0]);
	for(size_t i = 0; i < totaljob; ++i)
	{
		out[i] = planvect[i].waittime;
	}
}


void fcfs_plan::annealing()
{
	//Simple version everything start here
	//1,find base solution
	//2.find neighbor solution 
	//3.check neighbor solution with expectation function
	//4.if better, update. if not, compare with expection function update
	//5. output the best solution
	//sorttime();
	bestsol = jobvec;
	prevsol = jobvec;
	besttime = planfirst(&bestsol[0]);
	prevtime = besttime;

	double T = 1;
    double T_min = 0.9; //T_min = 0.00001 always like this. the T_min = 0.9 is for random search
    double alpha = 0.9;
	while(T > T_min)
	{
		for(size_t i = 0; i < 1000; ++i)
		{
			currentsol.clear();
			currentsol.resize(totaljob);
			perturbation();

			currenttime = planfirst(&currentsol[0]);
			if ((currenttime < prevtime) || double(rand()%100)/100 < exp((prevtime-currenttime)/T))
		    {
				if (currenttime < besttime)
				{
					besttime = currenttime;
					bestsol = currentsol;
					//printf("update best solution %d \n", besttime);     //here is testing
				}
				prevtime = currenttime;
				prevsol = currentsol;
			}
		}
		T *= alpha;
	}
}

void fcfs_plan::perturbation()
{
	currentsol = prevsol;
	//just random change two solution
	int temp1 = 0;
	int temp2 = 0;
	idproc t1;

	temp1 = rand()%totaljob;
	temp2 = 0;
	

	t1 = currentsol[temp1];
	currentsol[temp1] = currentsol[temp2];
	currentsol[temp2] = t1;
}
