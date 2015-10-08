import sys
import os
import psana
import TimeTool
from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()
worldsize = MPI.COMM_WORLD.Get_size()

numevents=50
ttOptions = TimeTool.AnalyzeOptions(
    get_key='TSS_OPAL',
    eventcode_nobeam=0,
    calib_poly='0 1 0',
    sig_roi_x='0 1023',
    sig_roi_y='425 724',
    ref_avg_fraction=0.5,
    use_calib_db_ref=True,
    ref_load='',
    ref_store='')
                           
ttAnalyze = TimeTool.PyAnalyze(ttOptions)
ds = psana.DataSource('exp=sxrd5814:run=150', module=ttAnalyze)

for idx, evt in enumerate(ds.events()):
    if (numevents > 0) and (idx >= numevents): break
    if ttAnalyze.isRefShot(evt): 
        print "is ref shot"
        ttAnalyze.process(evt)
    if idx % worldsize != rank: 
        continue
    ttdata = ttAnalyze.process(evt)
    if ttdata is None: continue
    print "rank=%3d event %4d has TimeTool results. Peak is at pixel_position=%6.1f with amplitude=%7.5f nxt_amplitude=%7.5f fwhm=%5.1f" % \
                (rank, idx, ttdata.position_pixel(), ttdata.amplitude(), ttdata.nxt_amplitude(), ttdata.position_fwhm())
    

