/*
 * Summary: Locale handling
 * Description: Interfaces for locale handling. Needed for language dependent
 *              sorting.
 *
 * Copy: See Copyright for the status of this software.
 *
 * Author: Nick Wellnhofer
 */

#ifndef __XML_XSLTLOCALE_H__
#define __XML_XSLTLOCALE_H__

#include <libxml/xmlstring.h>
#include "xsltexports.h"

#ifdef XSLT_LOCALE_XLOCALE

#include <locale.h>
#include <xlocale.h>

#ifdef __GLIBC__
/*locale_t is defined only if _GNU_SOURCE is defined*/
typedef __locale_t xsltLocale;
#else
typedef locale_t xsltLocale;
#endif
typedef xmlChar xsltLocaleChar;

#elif defined(XSLT_LOCALE_WINAPI)

#include <windows.h>
#include <winnls.h>

typedef LCID xsltLocale;
typedef wchar_t xsltLocaleChar;

#else

/*
 * XSLT_LOCALE_NONE:
 * Macro indicating that locale are not supported
 */
#ifndef XSLT_LOCALE_NONE
#define XSLT_LOCALE_NONE
#endif

typedef void *xsltLocale;
typedef xmlChar xsltLocaleChar;

#endif

XSLTPUBFUN xsltLocale XSLTCALL
	xsltNewLocale			(const xmlChar *langName);
XSLTPUBFUN void XSLTCALL
	xsltFreeLocale			(xsltLocale locale);
XSLTPUBFUN xsltLocaleChar * XSLTCALL
	xsltStrxfrm			(xsltLocale locale,
					 const xmlChar *string);
XSLTPUBFUN int XSLTCALL
	xsltLocaleStrcmp		(xsltLocale locale,
					 const xsltLocaleChar *str1,
					 const xsltLocaleChar *str2);
XSLTPUBFUN void XSLTCALL
	xsltFreeLocales			(void);

#endif /* __XML_XSLTLOCALE_H__ */
