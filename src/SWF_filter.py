import cqsim_path
import Filter_job_SWF

ext = {'ext_job_trace':".swf",'ext_tmp_job':".csv"}
path = []
path.append({'path_in':"Input Files/SWF file/CLEANED/",'path_tmp':"Temp/SWF Formatted/CLEANED/"})
path.append({'path_in':"Input Files/SWF file/ORIGINAL/",'path_tmp':"Temp/SWF Formatted/ORIGINAL/"})


SWF_files=[[],[]]
SWF_files[0].append("CTC-SP2-1996-3.1-cln")
SWF_files[0].append("HPC2N-2002-2.1-cln")
SWF_files[0].append("LANL-CM5-1994-4.1-cln")
SWF_files[0].append("LLNL-Atlas-2006-2.1-cln")
SWF_files[0].append("LLNL-Thunder-2007-1.1-cln")
SWF_files[0].append("LPC-EGEE-2004-1.2-cln")
SWF_files[0].append("NASA-iPSC-1993-3.1-cln")
SWF_files[0].append("OSC-Clust-2000-3.1-cln")
SWF_files[0].append("SDSC-BLUE-2000-4.1-cln")
SWF_files[0].append("SDSC-Par-1995-3.1-cln")
SWF_files[0].append("SDSC-Par-1996-3.1-cln")
SWF_files[0].append("SDSC-SP2-1998-4.1-cln")


SWF_files[1].append("ANL-Intrepid-2009-1")
SWF_files[1].append("CTC-SP2-1995-2")
SWF_files[1].append("DAS2-fs0-2003-1")
SWF_files[1].append("DAS2-fs1-2003-1")
SWF_files[1].append("DAS2-fs2-2003-1")
SWF_files[1].append("DAS2-fs3-2003-1")
SWF_files[1].append("DAS2-fs4-2003-1")
SWF_files[1].append("KTH-SP2-1996-2")
SWF_files[1].append("LANL-O2K-1999-2")
SWF_files[1].append("LCG-2005-1")
SWF_files[1].append("LLNL-T3D-1996-2")
SWF_files[1].append("LLNL-uBGL-2006-2")
SWF_files[1].append("METACENTRUM-2009-2")
SWF_files[1].append("RICC-2010-2")
SWF_files[1].append("Sandia-Ross-2001-1")
SWF_files[1].append("SDSC-DS-2004-1")
SWF_files[1].append("SHARCNET-2005-2")
SWF_files[1].append("SHARCNET-Whale-2005-2")


trace_name=""
save_name=""

filter_job = Filter_job_SWF.Filter_job_SWF(trace=trace_name, save=save_name, sdate=None, debug=0)
for i in SWF_files[0]:
    trace_name=""
    save_name=""
    trace_name = path[0]['path_in'] + i + ext['ext_job_trace'] 
    save_name = path[0]['path_tmp'] + i + ext['ext_tmp_job'] 
    print "=================================================="
    print trace_name
    filter_job.reset(trace=trace_name, save=save_name, sdate=None, debug=0)
    filter_job.read_job_trace()
    filter_job.output_job_data()

for i in SWF_files[1]:
    trace_name=""
    save_name=""
    trace_name = path[1]['path_in'] + i + ext['ext_job_trace'] 
    save_name = path[1]['path_tmp'] + i + ext['ext_tmp_job'] 
    print "=================================================="
    print trace_name
    filter_job.reset(trace=trace_name, save=save_name, sdate=None, debug=0)
    filter_job.read_job_trace()
    filter_job.output_job_data()
