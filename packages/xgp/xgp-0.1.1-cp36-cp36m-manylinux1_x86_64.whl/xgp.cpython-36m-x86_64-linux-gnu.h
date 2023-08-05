/* Created by "go tool cgo" - DO NOT EDIT. */

/* package github.com/MaxHalford/xgp-python/xgp */


#line 1 "cgo-builtin-prolog"

#include <stddef.h> /* for ptrdiff_t below */

#ifndef GO_CGO_EXPORT_PROLOGUE_H
#define GO_CGO_EXPORT_PROLOGUE_H

typedef struct { const char *p; ptrdiff_t n; } _GoString_;

#endif

/* Start of preamble from import "C" comments.  */




/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */
#line 1 "cgo-gcc-export-header-prolog"

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

typedef _GoString_ GoString;
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


// Fit an Estimator and return the best Program.

extern char* Fit(GoSlice p0, GoSlice p1, GoSlice p2, GoSlice p3, GoSlice p4, GoSlice p5, GoString p6, GoString p7, GoString p8, GoFloat64 p9, GoUint8 p10, GoString p11, GoFloat64 p12, GoFloat64 p13, GoFloat64 p14, GoFloat64 p15, GoFloat64 p16, GoUint p17, GoUint p18, GoUint p19, GoUint p20, GoUint p21, GoFloat64 p22, GoFloat64 p23, GoFloat64 p24, GoFloat64 p25, GoFloat64 p26, GoUint p27, GoUint p28, GoFloat64 p29, GoUint8 p30, GoFloat64 p31, GoFloat64 p32, GoUint8 p33, GoUint p34, GoInt64 p35, GoUint8 p36);

#ifdef __cplusplus
}
#endif
