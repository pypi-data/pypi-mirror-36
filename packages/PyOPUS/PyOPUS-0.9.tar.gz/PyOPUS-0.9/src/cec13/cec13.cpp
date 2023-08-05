/* (c)2015 Arpad Buermen */
/* Interface to the CEC13 test set. */

/* Note that in Windows we do not use Debug compile because we don't have the debug version
   of Python libraries and interpreter. We use Release version instead where optimizations
   are disabled. Such a Release version can be debugged. 
 */

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include "Python.h"
#include "numpy/arrayobject.h"
#include <math.h>
#include <stdio.h>

/* Debug switch - uncomment to enable debug messages */
/* #undefine PYDEBUG */

/* Debug file */
#define df stdout

#ifdef LINUX
#define __declspec(a) extern
#endif

extern int cec13_func(double *, double *, int, int, int, int); 
extern void initmod(char *);
extern const char *errstr;
extern double *OShift; 
extern double minval[];

/* Safeguard against C++ symbol mangling */
#ifdef __cplusplus
extern "C" {
#endif
	
static char initmod_doc[]=
"CEC13 problems, initialization.\n"
"\n"
"cec13ini(path)\n"
"\n"
"Input\n"
"path -- path to the cec13 folder containing the data files\n"; 

static PyObject *initmod(PyObject *self, PyObject *args) {
	char *str;
	
#ifdef PYDEBUG
	fprintf(df, "cec13: checking arguments\n");
#endif
	if (PyObject_Length(args)!=1) {
		PyErr_SetString(PyExc_Exception, "Function takes exactly one argument.");
		return NULL; 
	}
	
	if (!PyArg_ParseTuple(args, "s", &str)) {
		PyErr_SetString(PyExc_Exception, "Bad input arguments.");
		return NULL; 
	}
	
	initmod(str);
	
	Py_INCREF(Py_None);
	return Py_None; 
}


static char cec13init_doc[]=
"CEC13 problems, initialization.\n"
"\n"
"data=cec13ini(num, n)\n"
"\n"
"Input\n"
"num -- problem number (1-28)\n"
"n   -- problem dimension\n"
"\n"
"Output\n"
"data -- dictionary with problem information\n"
"\n"
"The dictionary has the following members:\n"
"xmin   -- minimum position (NumPy array)\n"
"fmin   -- function value at the minimum\n";

static PyObject *cec13init(PyObject *self, PyObject *args) {
	int i_problem, i_n; 
	int n, problem, err, i;
	double *xmin;
	PyObject *dict, *tmpo; 
	PyArrayObject *Mxmin;
	npy_intp dims[1];
	
#ifdef PYDEBUG
	fprintf(df, "cec13: checking arguments\n");
#endif
	if (PyObject_Length(args)!=2) {
		PyErr_SetString(PyExc_Exception, "Function takes exactly two arguments.");
		return NULL; 
	}
	
	if (!PyArg_ParseTuple(args, "ii", &i_problem, &i_n)) {
		PyErr_SetString(PyExc_Exception, "Bad input arguments.");
		return NULL; 
	}
	
	/* Set problem number */
	problem=i_problem;
	
	/* Set n */
	n=i_n;
	
	/* Call */
	err=cec13_func(NULL, NULL, n, 1, problem, 1);
	
	if (err!=0) {
		PyErr_SetString(PyExc_Exception, errstr);
		return NULL;
	}
	
	/* Allocate vector for xmin */
	dims[0]=n;
	Mxmin=(PyArrayObject *)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
	xmin=(npy_double *)PyArray_DATA(Mxmin);
	
	for(i=0;i<n;i++) {
		xmin[i]=OShift[i];
	}
	
	/* Prepare return value */
	dict=PyDict_New();
	
	PyDict_SetItemString(dict, "xmin", (PyObject *)Mxmin); 
	Py_XDECREF(Mxmin);
	
	tmpo=PyFloat_FromDouble(minval[problem]);
	PyDict_SetItemString(dict, "fmin", tmpo);
	Py_XDECREF(tmpo);
	
	
	/* Check reference count 
	printf("%d\n", Mx0->ob_refcnt); 
	*/
	
	return dict; 
}

static char cec13eval_doc[]=
"CEC13 problems - function values.\n"
"\n"
"f=tffu28(num, x, n, m)\n"
"\n"
"Input\n"
"num -- problem number (0-27)\n"
"x   -- function argument vector of length m*n\n"
"       n consecutive components specify one point\n"
"n   -- dimension\n"
"m   -- number of points\n"
"\n"
"Output\n"
"f   -- 1-dimensional array of length 1 or length m\n";

static PyObject *cec13eval(PyObject *self, PyObject *args) {
	int i_problem; 
	int n, m, problem, err;
	double *f, *x; 
	PyArrayObject *Mx, *Mf; 
	npy_intp dims[1];
	
#ifdef PYDEBUG
	fprintf(df, "tffu28: checking arguments\n");
#endif
	if (PyObject_Length(args)!=4) {
		PyErr_SetString(PyExc_Exception, "Function takes exactly four arguments.");
		return NULL; 
	}
	
	if (!PyArg_ParseTuple(args, "iOii", &i_problem, &Mx, &n, &m)) {
		PyErr_SetString(PyExc_Exception, "Bad input arguments.");
		return NULL; 
	}
	problem=i_problem;
	
	if (!(PyArray_Check(Mx) && PyArray_ISFLOAT(Mx)&& PyArray_TYPE(Mx)==NPY_DOUBLE && PyArray_NDIM(Mx)==1)) {
		PyErr_SetString(PyExc_Exception, "Argument 2 must be a 1D double array");
		return NULL; 
	}
	
	/* Verify n, m, and array length */
	if (PyArray_DIM(Mx, 0)!=(n*m)) {
		PyErr_SetString(PyExc_Exception, "Argument 2 must be of length n*m");
		return NULL; 
	}
	
	/* Get x */
	x=(npy_double *)PyArray_DATA(Mx);
	
	/* Allocate vector for f */
	dims[0]=m;
	Mf=(PyArrayObject *)PyArray_SimpleNew(1, dims, NPY_DOUBLE);
	f=(npy_double *)PyArray_DATA(Mf);
	
	/* Compute */
	err=cec13_func(x, f, n, m, problem, 0);
	
	if (err!=0) {
		Py_XDECREF(Mf);
		PyErr_SetString(PyExc_Exception, errstr);
		return NULL;
	}
	
	return (PyObject *)Mf; 
}



/* Methods table */
static PyMethodDef module_methods[] = {
	{"initmod",   initmod,   METH_VARARGS, initmod_doc},
	{"cec13init", cec13init, METH_VARARGS, cec13init_doc},
	{"cec13eval", cec13eval, METH_VARARGS, cec13eval_doc},
	{NULL, NULL, 0, NULL}     // Marks the end of this structure
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_cec13", /* name of module */
    "CEC13 global optimization test functions.\n", /* module documentation, may be NULL */
    /* TODO: in future set this to 0 so that this module will work with sub-interpreters */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods,
    NULL, /* Slots for multi phase initialization */
    NULL, /* Traversal function for GC */
    NULL, /* Clear function for clearing the module */
    NULL, /* Function for deallocating the module */
};


/* Module initialization 
   Module name must be _cec13 in compile and link */
PyMODINIT_FUNC PyInit__cec13()  {
	PyObject *m=PyModule_Create(&module);
	
	/* For using NumPy */
	import_array(); 
	
	return m;
}


#ifdef __cplusplus
}
#endif
