#ifndef GAP_LIST_H
#define GAP_LIST_H

// store a 3d vector
struct gapstruct
{
	double starttime;    //gap start time
	double endtime;      //gap end time 
	size_t gapnum;         //avaible node number
};
class gap_list
{
public:
	gap_list();
	void initial(double st_, double et_, size_t c_);
	void init(size_t count, double in[]);

	double findgap(int jnum, double jtime);

	double go(int jnum, double jtime);
	double findcon(int jnum, double jtime);//find the first contiguity gap-->data_1
	double findmul(int jnum, double jtime);//find the multiple gap--->data_2
	bool merge(); //only one list to merge that is gapdata
	void copylist(double clist[]);
	size_t gapdatasize();

	double makes();

protected:
	std::list<gapstruct> gapdata, gapdata1;    //this is the original input list
	std::list<gapstruct> data_1, data_2;  //two list used to comput different situation
	double startt, endt;//here are the initial number
	size_t gn;       //  

}; // class GAP_LIST
#endif // GAP_LIST_H
