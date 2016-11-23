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
    controlLogic=True,
    calib_poly='0 1 0',
    sig_roi_x='0 1023',
    sig_roi_y='425 724',
    ref_avg_fraction=0.5)
                           
ttAnalyze = TimeTool.PyAnalyze(ttOptions)
ds = psana.DataSource('exp=sxri0214:run=158', module=ttAnalyze)

for idx, evt in enumerate(ds.events()):
    if (numevents > 0) and (idx >= numevents): break
    if idx % 2 == 0:
        laserOn=True
        beamOn=False
    elif idx % 2 == 1:
        laserOn=True
        beamOn=True

    ttAnalyze.controlLogic(evt, laserOn, beamOn)
    if ttAnalyze.isRefShot(evt): 
        print "rank=%3d event %d is ref shot" % (rank, idx)
        ttAnalyze.process(evt)
    if idx % worldsize != rank: 
        continue
    ttdata = ttAnalyze.process(evt)
    if ttdata is None: continue
    print "rank=%3d event %4d has TimeTool results. Peak is at pixel_position=%6.1f with amplitude=%7.5f nxt_amplitude=%7.5f fwhm=%5.1f" % \
                (rank, idx, ttdata.position_pixel(), ttdata.amplitude(), ttdata.nxt_amplitude(), ttdata.position_fwhm())
    

