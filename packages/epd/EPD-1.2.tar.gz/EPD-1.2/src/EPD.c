#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "Type0.h"
#include "Type2.h"
#include "Compression.h"

static PyMethodDef module_methods[] = {
   {"convertToType0_1bit", (PyCFunction)convertToType0_1bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type0 2 bit format. Data is in bytes format as from PIL Image.tobytes()."},
   {"convertToType0_2bit", (PyCFunction)convertToType0_2bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type0 1 bit format. Data is in bytes format as from PIL Image.tobytes(). Image width (X size) is needed."},

   {"convertToType2_1bit", (PyCFunction)convertToType2_1bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type2 1 bit format. Data is in bytes format as from PIL Image.tobytes()."},

   {"compress", (PyCFunction)compress, METH_VARARGS | METH_KEYWORDS, "Method for EPD data compression according to LZ77 algorythm."},
   {NULL}
};

static struct PyModuleDef EPD_mod =
{
    PyModuleDef_HEAD_INIT,
    "EPD", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_EPD(void)
{
    return PyModule_Create(&EPD_mod);
}
