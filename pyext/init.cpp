#include <boost/python.hpp>
#include <iostream>
#include "TimeTool/AnalyzePyProxy.h"

using namespace TimeTool;

BOOST_PYTHON_MODULE(_TimeTool)
{    
  bool userDefinedDocStrings = true;
  bool pythonSignatures = false;
  bool cppSignatures = false;
  boost::python::docstring_options local_docstring_options(userDefinedDocStrings, pythonSignatures, cppSignatures);
  boost::python::class_<AnalyzePyProxy>("PyAnalyze", boost::python::init<PyObject *>())
    .def("beginJob",&AnalyzePyProxy::beginJob, 
         "beginJob(self, evt, env):\n"
         "  called by psana framework when datasource is created")
    .def("beginRun",&AnalyzePyProxy::beginRun, 
         "beginRun(self, evt, env):\n"
         "  called by psana framework for each new run during\n"
         "  event iteration.")
    .def("beginCalibCycle",&AnalyzePyProxy::beginCalibCycle, 
         "beginCalibCycle(self, evt, env):\n"
         "  called by psana framework for each new calibcycle during\n"
         "  event iteration.")
    .def("process",&AnalyzePyProxy::process, 
         "process(self, evt):\n"
         "  invokes TimeTool.Analyze to process a event.\n"
         "  It is important to call this on reference shots to update TimeTool's\n"
         "  internal reference.\n"
         "\n"
         "  Returns: None or instance of Psana.TimeTool.DataV2 with Analyze results.")
    .def("isRefShot", &AnalyzePyProxy::isRefShot, 
         "isRefShot(self, evt):\n"
         "  returns True if this is a reference shot - meaning laser is on, but beam is off.")
    .def("controlLogic", &AnalyzePyProxy::controlLogic, 
         "controlLogic(self, laserOn, beamOn):\n"
         "  this is for unusal cases when one wants to directly define\n"
         "  if the beam and/or laser is on. To use this function, one must\n"
         "  initialize the the AnalyzeOptions object with the parameter controlLogic=True")
    .def("endCalibCycle",&AnalyzePyProxy::endCalibCycle,
         "endCalibCycle(self, evt, env):\n"
         "  called by psana framework when an end calibcycle is found during\n"
         "  event iteration.")
    .def("endRun",&AnalyzePyProxy::endRun,
         "beginCalibCycle(self, evt, env):\n"
         "  called by psana framework when an end run is found during\n"
         "  event iteration.")
    .def("endJob",&AnalyzePyProxy::endJob, 
         "beginCalibCycle(self, evt, env):\n"
         "  called by psana framework if/after all datasource events have been processed")
    ;
}
