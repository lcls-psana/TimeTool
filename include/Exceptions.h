#ifndef TIMETOOL_EXCEPTIONS_H
#define TIMETOOL_EXCEPTIONS_H

//--------------------------------------------------------------------------
// File and Version Information:
// 	$Id$
//
// Description:
//	Exceptions for TimeTool
//
//------------------------------------------------------------------------

//-----------------
// C/C++ Headers --
//-----------------
#include <string>
#include <boost/lexical_cast.hpp>

//----------------------
// Base Class Headers --
//----------------------
#include "ErrSvc/Issue.h"

//-------------------------------
// Collaborating Class Headers --
//-------------------------------

//------------------------------------
// Collaborating Class Declarations --
//------------------------------------

//		---------------------
// 		-- Class Interface --
//		---------------------

namespace TimeTool {

/// @addtogroup TimeTool

/**
 *  @ingroup TimeTool
 *
 *  @brief Exception classes
 *
 *  This software was developed for the LUSI project.  If you use all or
 *  part of it, please give an appropriate acknowledgement.
 *
 *  @version $Id$
 *
 *  @author David Schneider
 */

class Exception : public ErrSvc::Issue {
public:

  // Constructor
  Exception(const ErrSvc::Context& ctx, const std::string& className, const std::string& what);

};


// thrown when a PyProxy did not get to initialize the underlying Psana module.
// Usually means the DataSource was not constructed with the Proxy module listed.
class ProxyInitError : public Exception {
public:

 ProxyInitError(const ErrSvc::Context& ctx)
   : Exception(ctx, "ProxyInit", "is module listed in psana DataSource module argument?" ) {}

};

// thrown when trying to control the beam logic through a  PyProxy object, but 
// it was not configured to do so.
class ControlLogicError : public Exception {
public:

 ControlLogicError(const ErrSvc::Context& ctx)
   : Exception(ctx, "ControlBeamLogicError", 
               "must set controlBeamLogic to true in the Options argument in order to use this function.")
    {}
};


} // namespace TimeTool

#endif // TIMETOOL_EXCEPTIONS_H
