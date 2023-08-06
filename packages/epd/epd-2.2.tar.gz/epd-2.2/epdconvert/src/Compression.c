#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "lz.h"

PyObject* compress(PyObject* self, PyObject *args, PyObject *keywds)
{
   unsigned char *in;
   unsigned char *out;
   Py_ssize_t insize;
   int outpos;

   PyObject* result;

   static char *kwlist[] = {"data", NULL};

   if (!PyArg_ParseTupleAndKeywords(args, keywds, "s#", kwlist, &in, &insize)) return NULL;

   out = malloc( (unsigned int) ((float)insize*0.5) ); // docs says 0.4+1, but ...
   outpos = LZ_Compress(in, out, insize);

   result = Py_BuildValue("y#", out, outpos);

   free(out);
   return result;
}

