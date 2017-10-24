#ifndef FCFS_PLAN_H
#define FCFS_PLAN_H
#include "gap_list.h"
struct idproc
{ 
	int jobid;      
	int jobnum;    //required node number
	double time;   //required runtime
	double wt;       //previous waittime
};
struct planstruct
{
	double waittime; //here we chose the job in queue, that is the wait time is planed start time
	double jobid;  //the job plan should sort as the increasing wait time fashion
};

class fcfs_plan
{
public:
	fcfs_plan();
	void initial();        //initial the gap list
	void inputjob(size_t count, double in[], size_t inputnumber);       //input the job vector   
	void inputgap(size_t count, double in[]);
	
	double planfirst(idproc pj[]);      //make the plan for every job       here return the total average time
	double plansecond(idproc pj[]);
	void sortplan();       //sort the plan on waiting time 
    void sorttime();         //sort the input on running time
	void sortjob();         //sort the input on required processing
	double findgap(int jnum, double jtime); // input the job number that need to be planed and the job runtime.   Return the start time
	void outputplan(double out[]);
	void outputplan2(double out[]);
	void outputplan3(double out[]);
	void perturbation(); //random get one solution
	void random();
	double besttime, currenttime, prevtime, basictime;
	double bestuti, basicuti;
	double bestmake, basicmake;
	void planbasic();
	std::vector<double> bestlist, basiclist;

protected:
	std::vector<idproc> jobvec, jobvec2;
	std::vector<idproc> bestsol, currentsol, prevsol, basicsol; //these three are for the annealing algorithm
	gap_list gaptest, gapstore;
	std::vector<planstruct> planvect, planvect2;

	std::vector<double> gapvec;


	size_t totalproc;         //total processor number
	size_t totaljob;
	double maxtime;          //add all the runtime of the job
}; // class fcfs_plan

#endif // FCFS_PLAN