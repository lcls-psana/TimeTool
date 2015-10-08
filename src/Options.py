import sys
import psana

class AnalyzeOptions(object):
    '''
    Specify configuration options for the TimeTool Analyze module.
    
    There are many options for TimeTool.Analyze, most can be left
    at their default values. First we document options users may
    want to change, then more specialized options.

    Note that all options are either a Python str, or Python int, or float.
    Even though some options represent a list of numbers, the argument
    must be formatted as a string with only whitespace separating numbers
    (no commas, etc)

    ** Common Options **
    Option    default    data type / explanation
    ------    -------    -----------
    get_key  'TSS_OPAL'  str, this is the psana source for the TimeTool
                         opal camera. The default, 'TSS_OPAL', is a common
                         DAQ alias for this source
    
    eventcode_nobeam 0   int, for BYKICK experiments, where an evr code 
                         specifies when the beam is NOT present, specify that
                         EVR code here. If the beam is always present, keep
                         the default value of 0. Note - there are specialized
                         options to control laser on/off beam on/off logic 
                         below.

    ref_avg_fraction 0.05 float, weight assigned to next reference shot in
                          rolling average. 1.0 means replace reference with
                          next shot (no rolling average). 0.05 means next 
                          shot is 5% of average and all previous is 95%.

    sig_roi_y '425 725' str, signal roi in y, or the rows of the Opal camera
                         that the user may want to adjust based on where signal is.

    sig_roi_x   '0 1023' str, signal roi in x or columns, default is all.


    calib_poly '0 1 0'   str, TimeTool.Analyze returns results as both a pixel
                         location on the Detector, as well as a conversion 
         to femtoseconds by applying this quadratic polynomial. Typically a 
         special calibration run is performed to compute the mapping from 
         position on the detector to femtoseconds and the results of this 
         analysis are passed through this parameter. If calib_poly is 'a b c'
         Then femtosecond_result = a + b*x + c*x^2 wher x is the detector position.

    ** Uncommon Options**
    Option    default    data type / explanation
    ------    -------    -----------
    projectX   True     bool, if true, project down to the X axis of the opal.

    eventcode_skip  0   int, EVR code for events that should be skipped from
                        TimeTool processing.

    ipm_get_key    ''   str, in addition to the evr code above, the timetool 
                        will look at the threshold on a specified ipmb to decide
                        if the beam is present. Default is to not look at a 
                        ipmb. Here one can specify the psana source for the
                        desired ipimb.
                 
    ipm_beam_threshold  float, threshold for determining if beam present from
                        an ipm.
                       
    weights  '0.00940119 ...' str, this defaults to a long string of the 
                        weights that the TimeTool uses when performing signal
                        processing on the normalized, reference divided signal,
                        to turn a sharp drop into a peak. It is unusual for
                        users to modify this string. The full string can be
                        found in the code.

    weights_file ''     str, the weights can be put into a file as well

    use_calib_db_ref  False  bool, get the initial reference from the 
                       calibration database. This reference can be deployed
                       using calibman by making a pedestal for the appropriate
                       opal. Example use case is creating references not by
                       dropping the beam from shots, but rather making 
                       reference runs (dropped shots tend to give better results).
    
    ref_load  ''       str, filename to load reference file from.

    ref_store ''       str, filename to store reference into.

    controlLogic      False,  bool, to bypass the normal mechanism of letting
                      the timetool identify when the beam or laser is on, 
                      the user can control this. If this is set, then for
                      every event, one must call controlLogic before calling
                      process with the TimeTool.Analyze python class.

    proj_cut   -(1<<31), int, after projecting of the opal camera to create the 
                     signal, one can require that at least one value in the signal
                     be greater than this parameter in order to continue processing.
                     Default is int_min, which means one always processes when the
                     laser is on (and a reference is available).

    sb_roi_x   '', str  give something like 1 10 to do sideband analysis and specify
                   the sideband ROI. This feature, while it exists in the code, is not
                   maintained. Experts interested in this feature may need to contact
                   their POC for support.
                   
    sb_roi_y   '', str, see sb_roi_x, this is for the y region (rows)

    sb_avg_fraction 0.05, float, see sb_roi_x and sig_avg_fraction for information on
                    rolling averages.
    
    analyze_event -1, int, special options for analyzing the first few events with respect
                  to a reference - feature not maintained.

    dump         0, int, setting this option is not reccommended. It instructs TimeTool
                 to use the psana root based historgramming method - however the root
                 files interfere with MPI based analysis. See the eventdump option below
                 to access intermediate stages of TimeTool processing.

    eventdump   False, bool, setting this option to True will cause the underlying C++
                Psana TimeTool.Analyze module to return extra data that the Psana PlotAnalyze
                module can use (or users can get directly) but presently, the Python wrapper
                does not expose this, or setup the plotter in a convenient way. However One can
                get the ndarrays directly from the event following a call to PyAnalyze.Process().


    psanaName TimeTool.Analyze, str, the logging name passed to this instance of the
                underlying C++ Psana Module called TimeTool.Analyze. There should be no
                reason to modify this - unless for some reason you want to configure two
                separate instances of the Psana Module.

    put_key TTANA, str, should be little reason to modify this. This is the key used to get
                 results back from the C++ TimeTool.Analyze module.

    beam_on_off_key ControlLogicBeam, str, there should be no reason to modify this.
                if controlLogic is true, this is the internal key string used to 
                communicate beam on/off with the TimeTool.Analyze module.

    laser_on_off_key ControlLogicLaser, str, as above, should be no reason to modify this.

    -------------------
    
    Users migrating older code will need to discard psana config files, or remove 
    the TimeTool.Analyze configuration from the psana config file **AS WELL AS THE**
    TimeTool.Analyze C++ Psana Module from the list of psana modules in the config
    file. If mixing old style Psana modules with PyAnalyze, be advised that PyAnalyze
    will run after any modules listed in the psana config file (so the TimeTool results
    will not be available to Psana modules listed in the config file). It should be easy
    to move Python Psana modules into the new style (C++ modules are not easy to move). 
    '''
    def __init__(self, *args, **kwargs):
        assert len(args)==0, "Options only takes keyword arguments."

        self.argname2defvalue = {'psanaName':'TimeTool.Analyze',
                                 'controlLogic':False,
                                 'beam_on_off_key':"ControlLogicBeam",
                                 'laser_on_off_key':"ControlLogicLaser",
                                 'get_key':'TSS_OPAL',
                                 'put_key':"TTANA",
                                 'eventcode_nobeam':0,
                                 'eventcode_skip':0,
                                 'ipm_get_key':'',
                                 'ipm_beam_threshold':sys.float_info.min,
                                 'calib_poly':'0 1 0',
                                 'proj_cut': -(1<<31),
                                 'projectX':True,
                                 'sb_roi_x':'',
                                 'sb_roi_y':'',
                                 'sig_roi_x':'0 1023',
                                 'sig_roi_y':'425 725',
                                 'sb_avg_fraction': 0.05,
                                 'ref_avg_fraction':0.05,
                                 'weights':'0.00940119 -0.00359135 -0.01681714 -0.03046231 -0.04553042 -0.06090473 -0.07645332 -0.09188818 -0.10765874 -0.1158105  -0.10755824 -0.09916765 -0.09032289 -0.08058788 -0.0705904  -0.06022352 -0.05040479 -0.04144206 -0.03426838 -0.02688114 -0.0215419  -0.01685951 -0.01215143 -0.00853327 -0.00563934 -0.00109415  0.00262359  0.00584445  0.00910484  0.01416929  0.0184887   0.02284319  0.02976289  0.03677404  0.04431778  0.05415214  0.06436626  0.07429347  0.08364909  0.09269116  0.10163601  0.10940983  0.10899065  0.10079016  0.08416471  0.06855799  0.05286105  0.03735241  0.02294275  0.00853613',
                                 'weights_file':'',
                                 'use_calib_db_ref':False,
                                 'ref_load':'',
                                 'dump':0,
                                 'eventdump':False,
                                 'analyze_event':-1,
                                 'ref_store':''}

        self.psanaName = kwargs.pop('psanaName', self.argname2defvalue.pop('psanaName'))

        self.controlLogic = kwargs.pop('controlLogic', self.argname2defvalue.pop('controlLogic'))
        if not self.controlLogic:
            self.argname2defvalue['beam_on_off_key']=''
            self.argname2defvalue['laser_on_off_key']=''
        for argname, defvalue in self.argname2defvalue.iteritems():
            givenvalue = kwargs.pop(argname, defvalue)
            assert isinstance(givenvalue, type(defvalue)), "arg=%s has type=%r which is different than %r. Default value is %r" % \
                (argname, type(givenvalue), type(defvalue), defvalue)
            if isinstance(givenvalue, str):
                givenvalue = givenvalue.strip()
            setattr(self,argname,givenvalue)
            psana.setOption(self.psanaName + '.' + argname, givenvalue)

        assert len(kwargs)==0, "There are unexpected keyword arguments: %r" % kwargs.keys()

    def get_psanaName(self):
        return self.psanaName

    def get_put_key(self):
        return self.put_key

    def get_get_key(self):
        return self.get_key

    def get_laser_on_off_key(self):
        return self.laser_on_off_key

    def get_beam_on_off_key(self):
        return self.beam_on_off_key
