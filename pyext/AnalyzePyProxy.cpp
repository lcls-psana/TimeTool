//--------------------------------------------------------------------------
// File and Version Information:
// 	$Id$
//
// Description:
//	Class TimeTool::AnalyzePyProxy
//
//------------------------------------------------------------------------

//-----------------------
// This Class's Header --
//-----------------------
#include "AnalyzePyProxy.h"

//-----------------
// C/C++ Headers --
//-----------------
#include <boost/python.hpp>

//-------------------------------
// Collaborating Class Headers --
//-------------------------------
#include "psddl_psana/timetool.ddl.h"
#include "TimeTool/Exceptions.h"

//-----------------------------------------------------------------------
// Local Macros, Typedefs, Structures, Unions and Forward Declarations --
//-----------------------------------------------------------------------
namespace {

  const char *logger = "TimeTool.AnalyzePyProxy";

}

//		----------------------------------------
// 		-- Public Function Member Definitions --
//		----------------------------------------

namespace TimeTool {

//----------------
// Constructors --
//----------------
AnalyzePyProxy::AnalyzePyProxy (PyObject *options)
{
  m_psanaName = boost::python::call_method<std::string>(options, "get_psanaName");
  m_putKey = boost::python::call_method<std::string>(options, "get_put_key");
  m_getKey = boost::python::call_method<std::string>(options, "get_get_key");
  m_beamOnOffKey = boost::python::call_method<std::string>(options, "get_beam_on_off_key");
  m_laserOnOffKey = boost::python::call_method<std::string>(options, "get_laser_on_off_key");
  MsgLog(logger, trace, "from PyObject options, psanaName=" << m_psanaName
         << " put_key=" << m_putKey
         << " get_key=" << m_getKey
         << " beam_on_off_key=" << m_beamOnOffKey
         << " laser_on_off_key=" << m_laserOnOffKey); 
}

/// Method which is called once at the beginning of the job
void 
AnalyzePyProxy::beginJob(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  m_ttGetSource = Source(m_getKey);
  m_analyze = boost::make_shared<Analyze>(m_psanaName);
  m_env = env;
  m_analyze->beginJob(*evt, *env);
}

/// Method which is called at the beginning of the run
void 
AnalyzePyProxy::beginRun(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  m_analyze->beginRun(*evt, *env);
}

/// Method which is called at the beginning of the calibration cycle
void 
AnalyzePyProxy::beginCalibCycle(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  m_analyze->beginCalibCycle(*evt, *env);
}


boost::shared_ptr<Psana::TimeTool::DataV2>
AnalyzePyProxy::process(boost::shared_ptr<PSEvt::Event> evt)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }

  boost::shared_ptr<PSEvt::EventId> curEventId = evt->get();
  if (m_cachedEventId and (*curEventId == *m_cachedEventId)) return m_cachedTimeToolResult;
  
  m_analyze->event(*evt, *m_env);
  boost::shared_ptr<Psana::TimeTool::DataV2> datav2 = evt->get(m_putKey);
  m_cachedEventId = curEventId;
  m_cachedTimeToolResult = datav2;
  return datav2;
}

 
bool 
AnalyzePyProxy::isRefShot(boost::shared_ptr<PSEvt::Event> evt)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  return m_analyze->isRefShot(*evt);
}

void 
AnalyzePyProxy::controlLogic(boost::shared_ptr<PSEvt::Event> evt, bool laserOn, bool beamOn)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  if ((m_laserOnOffKey.size()==0) or (m_beamOnOffKey.size()==0)) {
    throw ControlLogicError(ERR_LOC);
  }

  boost::shared_ptr<PSEvt::AliasMap> aMap = m_env->aliasMap();
  if (laserOn) {
    evt->put(m_onStr, m_ttGetSource.srcMatch(*aMap).src(), m_laserOnOffKey);
  } else {
    evt->put(m_offStr, m_ttGetSource.srcMatch(*aMap).src(), m_laserOnOffKey);
  }
  
  if (beamOn) {
    evt->put(m_onStr, m_ttGetSource.srcMatch(*aMap).src(), m_beamOnOffKey);
  } else {
    evt->put(m_offStr, m_ttGetSource.srcMatch(*aMap).src(), m_beamOnOffKey);
  }
}

 
/// Method which is called at the end of the calibration cycle
void 
AnalyzePyProxy::endCalibCycle(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  m_analyze->endCalibCycle(*evt, *m_env);
}

/// Method which is called at the end of the run
void 
AnalyzePyProxy::endRun(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  m_analyze->endRun(*evt, *m_env);
}

/// Method which is called once at the end of the job
void 
AnalyzePyProxy::endJob(boost::shared_ptr<PSEvt::Event> evt, boost::shared_ptr<PSEnv::Env> env)
{
  if (not m_analyze) {
    throw ProxyInitError(ERR_LOC);
  }
  m_analyze->endJob(*evt, *env);
}

boost::shared_ptr<std::string> AnalyzePyProxy::m_onStr( new std::string("on"));
boost::shared_ptr<std::string> AnalyzePyProxy::m_offStr(new std::string("off"));

} // namespace TimeTool

