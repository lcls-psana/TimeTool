from Options import AnalyzeOptions
from _TimeTool import *
PyAnalyze.__doc__ = '''
Python interface to the TimeTool.Analyze C++ Psana module
to allow conditional execution.

BASIC USAGE
============

There are several steps to using the module demonstrated in this
example:

        ttOptions = TimeTool.AnalyzeOptions(get_key='TSS_OPAL',
                                            eventcode_nobeam = 162)
        ttAnalyze = TimeTool.PyAnalyze(ttOptions)
        ds = psana.DataSource(self.datasource, module=ttAnalyze)

        for evt in ds.events():
            ttResults = ttAnalyze.process(evt)

The steps are

  * Create an instance of the AnalyzeOptions class. See AnalyzeOptions 
    docstring for detailed documentation on options.

  * Construct an instance of PyAnalyze (called ttAnalyze above) by passing 
    this options object (called ttOptions above).

  * construct your psana DataSource by passing the PyAnalyze instance through 
    to the module argument.

  * call the ttAnalyze.process() method on each event you want to process.

PARALLEL PROCESSING
===================

When doing parallel processing and distributing events among different ranks,
each rank typically processes a fraction of all the events. Howevever it 
is important that each rank also process all events that include reference 
shots for the TimeTool. One can check if a shot is a reference shot or not with
the isRefShot(evt) function. For example, in the above, suppose the variables 
numberOfRanks and rank are defined so that we can implement a round robin
strategy to distribute event processing. One could implement this, while making
sure all ranks process reference shots, as follows:

        for idx, evt in enumerate(ds.events()):
            if ttAnalyze.isRefShot(evt): 
                ttAnalyze.process(evt)
            if idx % numberOfRanks != rank: 
                continue
            ttResults = ttAnalyze.process(evt)

Note that it is Ok to call the PyAnalyze.process(evt) function more than once on the
same event. The PyAnalyze class caches the results of the first call so as to not call the
underlying C++ TimeTool.Analyze module twice.

CONTROLING BEAM LOGIC
=====================
set controlLogic=True in AnalyzeOptions and use the controlLogic(beamOn, laserOn) function
'''
