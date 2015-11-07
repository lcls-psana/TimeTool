#ifndef PSANA_TIMETOOL_ANALYZEPYPROXY_H
#define PSANA_TIMETOOL_ANALYZEPYPROXY_H

//--------------------------------------------------------------------------
// File and Version Information:
// 	$Id$
//
// Description:
//	Class TimeTool::AnalyzePyProxy.
//
//------------------------------------------------------------------------

//-----------------
// C/C++ Headers --
//-----------------

//----------------------
// Base Class Headers --
//----------------------

//-------------------------------
// Collaborating Class Headers --
//-------------------------------
#include <Python.h>
#include "TimeTool/Analyze.h"
#include "TimeTool/EventDump.h"
#include "psddl_psana/timetool.ddl.h"
#include "PSEvt/EventId.h"

//------------------------------------
// Collaborating Class Declarations --
//------------------------------------

//		---------------------
// 		-- Class Interface --
//		---------------------

namespace TimeTool {


class AnalyzePyProxy {
public:

  // Default constructor
  AnalyzePyProxy (PyObject * options) ;

  // Destructor
  virtual ~AnalyzePyProxy () {};

  /// Method which is called once at the beginning of the job
  virtual void beginJob(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);
  
  /// Method which is called at the beginning of the run
  virtual void beginRun(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);
  
  /// Method which is called at the beginning of the calibration cycle
  virtual void beginCalibCycle(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);

  /// invokes the Analyze event method
  virtual boost::shared_ptr<Psana::TimeTool::DataV2>
    process(boost::shared_ptr<PSEvt::Event> evt);

  /// check if this event is a reference shot (i.e, laser on, but no beam)
  /// does not update reference, call process for that.
  virtual bool isRefShot(boost::shared_ptr<PSEvt::Event> evt);
  
  /// if the TimeTool.Analyze module has been configured so that 
  /// beam and laser logic is under user control, this must be called once
  /// for each event before process is called.
  virtual void controlLogic(boost::shared_ptr<PSEvt::Event> evt, bool laserOn, bool beamOn);

  /// Method which is called at the end of the calibration cycle
  virtual void endCalibCycle(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);

  /// Method which is called at the end of the run
  virtual void endRun(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);

  /// Method which is called once at the end of the job
  virtual void endJob(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env);


protected:

private:

  static boost::shared_ptr<std::string> m_onStr, m_offStr;

  boost::shared_ptr<TimeTool::Analyze> m_analyze;
  boost::shared_ptr<PSEnv::Env> m_env;
  std::string m_psanaName, m_putKey, m_getKey,
    m_beamOnOffKey, m_laserOnOffKey;
  Source m_ttGetSource;

  boost::shared_ptr<PSEvt::EventId> m_cachedEventId;
  boost::shared_ptr<Psana::TimeTool::DataV2> m_cachedTimeToolResult;
};

} // namespace TimeTool

#endif // PSANA_TIMETOOL_ANALYZEPYPROXY_H
