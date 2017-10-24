#include "../misc/common.h"
#include "../misc/options.h"
#include "../misc/trace.h"
#include "../misc/timer.h"
#include "../misc/auto_file.h"
#include "../misc/token_parser.h"
#include <iostream>
#include "fcfs_plan.h"
 
using misc::cstr_t;
using misc::options;
bool load_1d(const std::string &name);
bool load_2d(const std::string &name);

bool save_1d(const std::string &name);

std::vector<double> jobinit, gapinit;
std::vector<double> jobplan, jobplan3;
int jobnum;
fcfs_plan jobsplan;
bool runsim();
bool makegap();

int main(int argc, char *argv[])
{
	jobinit.clear();
	gapinit.clear();

	jobplan.clear();
	if (!load_1d(argv[1]))
		return -1;
	if (!load_2d(argv[2]))
		return -1;
	jobnum = jobinit.size()/4;
	jobplan.clear();
	jobplan.resize(2*jobnum);
	jobplan3.clear();
	jobplan3.resize(jobnum);
	if(!makegap())
		return -1;

	if(!runsim())
		return -1;

	std::string name = "rs_plan";
	
	if (!save_1d(name))
		return -1;
	
	return 0;
}


bool runsim()
{
	jobplan.resize(2*jobnum);
	for(size_t i =0; i < jobnum; ++i)
	{
		jobplan[2*i] = jobinit[4*i];
		jobplan[2*i+1] = jobinit[4*i+2];
	}

	
	jobsplan.inputjob(jobnum, &jobinit[0], 1664); //The 1664 is the total system node number

	size_t tempsize = gapinit.size()/3;
	jobsplan.inputgap(tempsize, &gapinit[0]);
	jobsplan.random();
	
	jobsplan.outputplan(&jobplan3[0]);
	jobsplan.outputplan2(&jobplan[0]);
	
	return true;
}

bool save_1d(const std::string &name)
{
	os::auto_file af;
	if (!af.file_open(name+".txt", "w"))
	{
		fprintf(stderr, "%s: error: cannot write problems\n", name.c_str());
		return false;
	}

	FILE *fp = af.get_fp();

	
	for (size_t i = 0; i < jobnum; ++i)
	{
		fprintf(fp, "%f", jobplan[2*i]);
	    fprintf(fp, "\n");
	}
	return true;
}


bool load_1d(const std::string &name)
{
	misc::cstr_t delimit = " \t\r\n,:";
	misc::delimit_bmp bmp = misc::create_delimit_bmp(delimit);

	os::auto_file af;

	if (!af.file_open(name, "r"))
	{
		fprintf(stderr, "%s: error: cannot read swf\n", name.c_str());
		return false;
	}

	FILE *fp = af.get_fp();

	char line[1024*512];
	size_t line_no = 0;
	std::vector<misc::cstr_t> tokens;
	while (fgets(line, sizeof(line), fp))
	{
		line_no++;
		char *temp = misc::skip_space(line, bmp);
		if ((*temp == 0) || (*temp == '*'))
			continue; // empty line and comments

		tokens.resize(0);
		misc::split_tokens(temp, &tokens, bmp);
		if (tokens.size() == 0)
			continue;

		jobinit.push_back(atoi(tokens[0]));
	}

	return true;
}

bool load_2d(const std::string &name)
{
	misc::cstr_t delimit = " \t\r\n,:";
	misc::delimit_bmp bmp = misc::create_delimit_bmp(delimit);

	os::auto_file af;

	if (!af.file_open(name, "r"))
	{
		fprintf(stderr, "%s: error: cannot read swf\n", name.c_str());
		return false;
	}

	FILE *fp = af.get_fp();

	char line[1024*512];
	size_t line_no = 0;
	std::vector<misc::cstr_t> tokens;
	while (fgets(line, sizeof(line), fp))
	{
		line_no++;
		char *temp = misc::skip_space(line, bmp);
		if ((*temp == 0) || (*temp == '*'))
			continue; // empty line and comments

		tokens.resize(0);
		misc::split_tokens(temp, &tokens, bmp);
		if (tokens.size() == 0)
			continue;

		gapinit.push_back(atoi(tokens[0]));
	}

	return true;
}

bool makegap()
{
	std::vector<double> st, et, gnum;
	st.clear();
	et.clear();
	gnum.clear();

	size_t gapsize = gapinit.size()/3;
	
	for(size_t i = 0; i < gapsize; ++i)
	{
		st.push_back(gapinit[3*i]);
		et.push_back(gapinit[3*i+1]);
		gnum.push_back(gapinit[3*i+2]);
	}

	for(size_t i= 0; i<gapsize; ++i)
	{
		double value;
		int temp=i;
		for(size_t j=i+1; j<gapsize; ++j)
			if(et[j]<et[i])
				temp=j;
		if(temp != i)
		{
			value = et[i];
			et[i] = et[temp];
			et[temp] = value;

			value = gnum[i];
			gnum[i] = gnum[temp];
			gnum[temp] = value;
		}
	}
	
	gapinit.clear();

	double ac = 0;
	for(size_t i = gapsize -1; i !=0; --i)
	{
		if(st[i]!=et[i])
		{
			ac += gnum[i];
			gapinit.push_back(et[i-1]);
			gapinit.push_back(et[i]);
			gapinit.push_back(1664-ac);
		}
	}
	if(st[0]!=et[0])
	{
		ac += gnum[0];
		gapinit.push_back(st[0]);
		gapinit.push_back(et[0]);
		gapinit.push_back(1664-ac);
	}

	

	return true;
}