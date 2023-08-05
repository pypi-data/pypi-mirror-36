/*
 * Summary: compile-time version informations for the XSLT engine
 * Description: compile-time version informations for the XSLT engine
 *              this module is autogenerated.
 *
 * Copy: See Copyright for the status of this software.
 *
 * Author: Daniel Veillard
 */

#ifndef __XML_XSLTCONFIG_H__
#define __XML_XSLTCONFIG_H__

#ifdef __cplusplus
extern "C" {
#endif

/**
 * LIBXSLT_DOTTED_VERSION:
 *
 * the version string like "1.2.3"
 */
#define LIBXSLT_DOTTED_VERSION "1.1.32"

/**
 * LIBXSLT_VERSION:
 *
 * the version number: 1.2.3 value is 10203
 */
#define LIBXSLT_VERSION 10132

/**
 * LIBXSLT_VERSION_STRING:
 *
 * the version number string, 1.2.3 value is "10203"
 */
#define LIBXSLT_VERSION_STRING "10132"

/**
 * LIBXSLT_VERSION_EXTRA:
 *
 * extra version information, used to show a CVS compilation
 */
#define	LIBXSLT_VERSION_EXTRA ""

/**
 * WITH_XSLT_DEBUG:
 *
 * Activate the compilation of the debug reporting. Speed penalty
 * is insignifiant and being able to run xsltpoc -v is useful. On
 * by default unless --without-debug is passed to configure
 */
#if 1
#define WITH_XSLT_DEBUG
#endif

#if 0
/**
 * DEBUG_MEMORY:
 *
 * should be activated only when debugging libxslt. It replaces the
 * allocator with a collect and debug shell to the libc allocator.
 * Use configure --with-mem-debug to activate it on both library
 */
#define DEBUG_MEMORY

/**
 * DEBUG_MEMORY_LOCATION:
 *
 * should be activated only when debugging libxslt.
 * DEBUG_MEMORY_LOCATION should be activated only when libxml has
 * been configured with --with-debug-mem too
 */
#define DEBUG_MEMORY_LOCATION
#endif

/**
 * XSLT_NEED_TRIO:
 *
 * should be activated if the existing libc library lacks some of the
 * string formatting function, in that case reuse the Trio ones already
 * compiled in the libxml2 library.
 */

#if 0
#define XSLT_NEED_TRIO
#endif
#ifdef __VMS
#define HAVE_MATH_H 1
#define HAVE_SYS_STAT_H 1
#ifndef XSLT_NEED_TRIO
#define XSLT_NEED_TRIO
#endif
#endif

#ifdef	XSLT_NEED_TRIO
#define	TRIO_REPLACE_STDIO
#endif

/**
 * WITH_XSLT_DEBUGGER:
 *
 * Activate the compilation of the debugger support. Speed penalty
 * is insignifiant.
 * On by default unless --without-debugger is passed to configure
 */
#if 1
#ifndef WITH_DEBUGGER
#define WITH_DEBUGGER
#endif
#endif

/**
 * WITH_MODULES:
 *
 * Whether module support is configured into libxslt
 * Note: no default module path for win32 platforms
 */
#if 0
#ifndef WITH_MODULES
#define WITH_MODULES
#endif
#define LIBXSLT_DEFAULT_PLUGINS_PATH() "/tmp/pip-req-build-aa9jsia6/build/tmp/libxml2/lib/libxslt-plugins"
#endif

/**
 * ATTRIBUTE_UNUSED:
 *
 * This macro is used to flag unused function parameters to GCC
 */
#ifdef __GNUC__
#ifdef HAVE_ANSIDECL_H
#include <ansidecl.h>
#endif
#ifndef ATTRIBUTE_UNUSED
#define ATTRIBUTE_UNUSED __attribute__((unused))
#endif
#else
#define ATTRIBUTE_UNUSED
#endif

/**
 * LIBXSLT_ATTR_FORMAT:
 *
 * This macro is used to indicate to GCC the parameters are printf-like
 */
#ifdef __GNUC__
#define LIBXSLT_ATTR_FORMAT(fmt,args) __attribute__((__format__(__printf__,fmt,args)))
#else
#define LIBXSLT_ATTR_FORMAT(fmt,args)
#endif

/**
 * LIBXSLT_PUBLIC:
 *
 * This macro is used to declare PUBLIC variables for Cygwin and for MSC on Windows
 */
#if !defined LIBXSLT_PUBLIC
#if (defined(__CYGWIN__) || defined _MSC_VER) && !defined IN_LIBXSLT && !defined LIBXSLT_STATIC
#define LIBXSLT_PUBLIC __declspec(dllimport)
#else
#define LIBXSLT_PUBLIC
#endif
#endif

#ifdef __cplusplus
}
#endif

#endif /* __XML_XSLTCONFIG_H__ */
