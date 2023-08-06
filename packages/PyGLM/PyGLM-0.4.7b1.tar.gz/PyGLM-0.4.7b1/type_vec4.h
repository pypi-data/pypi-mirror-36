static void
tvec4_dealloc(tvec4* self)
{
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
tvec4_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	tvec4 *self;

	self = (tvec4 *)type->tp_alloc(type, 0);
	if (self != NULL) {
		self->x = 0;
		self->y = 0;
		self->z = 0;
		self->w = 0;
	}

	return (PyObject *)self;
}

static int
tvec4_init(tvec4 *self, PyObject *args, PyObject *kwds)
{
	static char *kwlist[] = { "x", "y", "z", "w", NULL };

	PyObject * arg1 = NULL;
	PyObject * arg2 = NULL;
	PyObject * arg3 = NULL;
	PyObject * arg4 = NULL;

	if (PyArg_ParseTupleAndKeywords(args, kwds, "|OOOO", kwlist,
		&arg1, &arg2, &arg3, &arg4)) {
		if (arg1 == NULL) {
			return 0;
		}
		if (arg2 == NULL) {
			if (IS_NUMERIC(arg1)) {
				self->x = self->y = self->z = self->w = pyvalue_as_double(arg1);
				return 0;
			}

			ivec4 o;

			if (unpack_ivec4p(arg1, &o)) {
				self->x = o.x;
				self->y = o.y;
				self->z = o.z;
				self->w = o.w;
				return 0;
			}
			PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
			return -1;
		}
		if (arg3 == NULL) {
			if (IS_NUMERIC(arg1)) {
				ivec3 o;
				if (!unpack_ivec3p(arg2, &o)) {
					PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
					return -1;
				}
				self->x = pyvalue_as_double(arg1);
				self->y = o.x;
				self->z = o.y;
				self->w = o.z;
				return 0;
			}
			if (IS_NUMERIC(arg2)) {
				ivec3 o;
				if (!unpack_ivec3p(arg1, &o)) {
					PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
					return -1;
				}
				self->x = o.x;
				self->y = o.y;
				self->z = o.z;
				self->w = pyvalue_as_double(arg2);
				return 0;
			}
			ivec2 o;
			if (!unpack_ivec2p(arg1, &o)) {
				PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
				return -1;
			}
			ivec2 o2;
			if (!unpack_ivec2p(arg2, &o2)) {
				PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
				return -1;
			}
			self->x = o.x;
			self->y = o.y;
			self->z = o2.x;
			self->w = o2.y;
			return 0;
		}
		if (arg4 == NULL) {
			if (IS_NUMERIC(arg1)) {
				if (IS_NUMERIC(arg2)) {
					ivec2 o;
					if (!unpack_ivec2p(arg3, &o)) {
						PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
						return -1;
					}
					self->x = pyvalue_as_double(arg1);
					self->y = pyvalue_as_double(arg2);
					self->z = o.x;
					self->w = o.y;
					return 0;
				}
				if (IS_NUMERIC(arg3)) {
					ivec2 o;
					if (!unpack_ivec2p(arg2, &o)) {
						PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
						return -1;
					}
					self->x = pyvalue_as_double(arg1);
					self->y = o.x;
					self->z = o.y;
					self->w = pyvalue_as_double(arg3);
					return 0;
				}
				PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
				return -1;
			}
			if (IS_NUMERIC(arg2) && IS_NUMERIC(arg3)) {
				ivec2 o;
				if (!unpack_ivec2p(arg1, &o)) {
					PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
					return -1;
				}
				self->x = o.x;
				self->y = o.y;
				self->z = pyvalue_as_double(arg2);
				self->w = pyvalue_as_double(arg3);
				return 0;
			}
			PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
			return -1;
		}
		if (IS_NUMERIC(arg1) && IS_NUMERIC(arg2) && IS_NUMERIC(arg3) && IS_NUMERIC(arg4)) {
			self->x = pyvalue_as_double(arg1);
			self->y = pyvalue_as_double(arg2);
			self->z = pyvalue_as_double(arg3);
			self->w = pyvalue_as_double(arg4);
			return 0;
		}
	}
	PyErr_SetString(PyExc_TypeError, "invalid argument type(s) for vec4()");
	return -1;
}

// unaryfunc
static PyObject *
tvec4_neg(tvec4 *obj)
{
	return pack_tvec4(-obj->x, -obj->y, -obj->z, -obj->w);
}

static PyObject *
tvec4_pos(tvec4 *obj)
{
	return pack_tvec4(obj->x, obj->y, obj->z, obj->w);
}

static PyObject *
tvec4_abs(tvec4 *obj)
{
	return pack_tvec4(fabs(obj->x), fabs(obj->y), fabs(obj->z), fabs(obj->w));
}

// binaryfunc
static PyObject *
tvec4_add(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			d + ((tvec4*)obj2)->x,
			d + ((tvec4*)obj2)->y,
			d + ((tvec4*)obj2)->z,
			d + ((tvec4*)obj2)->w
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for +: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			o.x + d,
			o.y + d,
			o.z + d,
			o.w + d
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		o.x + o2.x,
		o.y + o2.y,
		o.z + o2.z,
		o.w + o2.w
	);
	return out;
}

static PyObject *
tvec4_sub(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			d - ((tvec4*)obj2)->x,
			d - ((tvec4*)obj2)->y,
			d - ((tvec4*)obj2)->z,
			d - ((tvec4*)obj2)->w
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for -: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			o.x - d,
			o.y - d,
			o.z - d,
			o.w - d
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		o.x - o2.x,
		o.y - o2.y,
		o.z - o2.z,
		o.w - o2.w
	);
	return out;
}

static PyObject *
tvec4_mul(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			d * ((tvec4*)obj2)->x,
			d * ((tvec4*)obj2)->y,
			d * ((tvec4*)obj2)->z,
			d * ((tvec4*)obj2)->w
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for *: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			o.x * d,
			o.y * d,
			o.z * d,
			o.w * d
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		o.x * o2.x,
		o.y * o2.y,
		o.z * o2.z,
		o.w * o2.w
	);
	return out;
}

static PyObject *
tvec4_div(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			d / ((tvec4*)obj2)->x,
			d / ((tvec4*)obj2)->y,
			d / ((tvec4*)obj2)->z,
			d / ((tvec4*)obj2)->w
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for /: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			o.x / d,
			o.y / d,
			o.z / d,
			o.w / d
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		o.x / o2.x,
		o.y / o2.y,
		o.z / o2.z,
		o.w / o2.w
	);
	return out;
}

static PyObject *
tvec4_mod(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			fmod(d, ((tvec4*)obj2)->x),
			fmod(d, ((tvec4*)obj2)->y),
			fmod(d, ((tvec4*)obj2)->z),
			fmod(d, ((tvec4*)obj2)->w)
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for %: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			fmod(o.x, d),
			fmod(o.y, d),
			fmod(o.z, d),
			fmod(o.w, d)
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		fmod(o.x, o2.x),
		fmod(o.y, o2.y),
		fmod(o.z, o2.z),
		fmod(o.w, o2.w)
	);
	return out;
}

static PyObject *
tvec4_floordiv(PyObject *obj1, PyObject *obj2)
{
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		return pack_tvec4(
			floor(d / ((tvec4*)obj2)->x),
			floor(d / ((tvec4*)obj2)->y),
			floor(d / ((tvec4*)obj2)->z),
			floor(d / ((tvec4*)obj2)->w)
		);
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for //: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);
		PyObject* out = pack_tvec4(
			floor(o.x / d),
			floor(o.y / d),
			floor(o.z / d),
			floor(o.w / d)
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}

	// obj1 and obj2 can be interpreted as a tvec4
	PyObject* out = pack_tvec4(
		floor(o.x / o2.x),
		floor(o.y / o2.y),
		floor(o.z / o2.z),
		floor(o.w / o2.w)
	);
	return out;
}

static PyObject *
tvec4_divmod(PyObject * obj1, PyObject * obj2) {
	PyObject *arg1, *arg2;
	arg1 = tvec4_floordiv(obj1, obj2);
	arg2 = tvec4_mod(obj1, obj2);
	if (arg1 == NULL || arg2 == NULL) {
		return NULL;
	}
	PyObject* out = PyTuple_Pack(2, arg1, arg2);
	Py_DECREF(arg1);
	Py_DECREF(arg2);
	return out;
}

// ternaryfunc
static PyObject *
tvec4_pow(PyObject * obj1, PyObject * obj2, PyObject * obj3) {
	if (IS_NUMERIC(obj1)) { // obj1 is a scalar, obj2 is self
		double d = pyvalue_as_double(obj1);

		if (obj3 == Py_None) {
			return pack_tvec4(
				pow(d, ((tvec4*)obj2)->x),
				pow(d, ((tvec4*)obj2)->y),
				pow(d, ((tvec4*)obj2)->z),
				pow(d, ((tvec4*)obj2)->w)
			);
		}

		if (IS_NUMERIC(obj3)) {
			double d2 = pyvalue_as_double(obj3);
			return pack_tvec4(
				fmod(pow(d, ((tvec4*)obj2)->x), d2),
				fmod(pow(d, ((tvec4*)obj2)->y), d2),
				fmod(pow(d, ((tvec4*)obj2)->z), d2),
				fmod(pow(d, ((tvec4*)obj2)->w), d2)
			);
		}

		ivec4 o3;

		if (!unpack_ivec4p(obj3, &o3)) {
			PY_TYPEERROR("unsupported operand type(s) for **: ", obj3);
			return NULL;
		}

		PyObject* out = pack_tvec4(
			fmod(pow(d, ((tvec4*)obj2)->x), o3.x),
			fmod(pow(d, ((tvec4*)obj2)->y), o3.y),
			fmod(pow(d, ((tvec4*)obj2)->z), o3.z),
			fmod(pow(d, ((tvec4*)obj2)->w), o3.w)
		);
		return out;
	}

	ivec4 o;

	if (!unpack_ivec4p(obj1, &o)) { // obj1 is not supported.
		PY_TYPEERROR("unsupported operand type(s) for **: 'glm::detail::tvec4' and ", obj1);
		return NULL;
	}

	if (IS_NUMERIC(obj2)) { // obj1 is self, obj2 is a scalar
		double d = pyvalue_as_double(obj2);

		if (obj3 == Py_None) {
			PyObject* out = pack_tvec4(
				pow(o.x, d),
				pow(o.y, d),
				pow(o.z, d),
				pow(o.w, d)
			);
			return out;
		}

		if (IS_NUMERIC(obj3)) {
			double d2 = pyvalue_as_double(obj3);
			PyObject* out = pack_tvec4(
				fmod(pow(o.x, d), d2),
				fmod(pow(o.y, d), d2),
				fmod(pow(o.z, d), d2),
				fmod(pow(o.w, d), d2)
			);
			return out;
		}

		ivec4 o3;

		if (!unpack_ivec4p(obj3, &o3)) {
			PY_TYPEERROR("unsupported operand type(s) for **: ", obj3);
			return NULL;
		}

		PyObject* out = pack_tvec4(
			fmod(pow(o.x, d), o3.x),
			fmod(pow(o.y, d), o3.y),
			fmod(pow(o.z, d), o3.z),
			fmod(pow(o.w, d), o3.w)
		);
		return out;
	}

	ivec4 o2;

	if (!unpack_ivec4p(obj2, &o2)) { // obj1 is self, obj2 is something else (maybe it knows how to do the operation)
		Py_RETURN_NOTIMPLEMENTED;
	}



	// obj1 and obj2 can be interpreted as a tvec4
	if (obj3 == Py_None) {
		PyObject* out = pack_tvec4(
			pow(o.x, o2.x),
			pow(o.y, o2.y),
			pow(o.z, o2.z),
			pow(o.w, o2.w)
		);
		return out;
	}

	if (IS_NUMERIC(obj3)) {
		double d2 = pyvalue_as_double(obj3);
		PyObject* out = pack_tvec4(
			fmod(pow(o.x, o2.x), d2),
			fmod(pow(o.y, o2.y), d2),
			fmod(pow(o.z, o2.z), d2),
			fmod(pow(o.w, o2.w), d2)
		);
		return out;
	}

	ivec4 o3;

	if (!unpack_ivec4p(obj3, &o3)) {
		PY_TYPEERROR("unsupported operand type(s) for **: ", obj3);
		return NULL;
	}

	PyObject* out = pack_tvec4(
		fmod(pow(o.x, o2.x), o3.x),
		fmod(pow(o.y, o2.y), o3.y),
		fmod(pow(o.z, o2.z), o3.z),
		fmod(pow(o.w, o2.w), o3.w)
	);
	return out;
}

// inplace
// binaryfunc
static PyObject *
tvec4_iadd(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_add((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyObject *
tvec4_isub(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_sub((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyObject *
tvec4_imul(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_mul((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyObject *
tvec4_idiv(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_div((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyObject *
tvec4_imod(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_mod((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyObject *
tvec4_ifloordiv(tvec4 *self, PyObject *obj)
{
	tvec4 * temp = (tvec4*)tvec4_floordiv((PyObject*)self, obj);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

// ternaryfunc
static PyObject *
tvec4_ipow(tvec4 *self, PyObject *obj1, PyObject * obj2)
{
	tvec4 * temp = (tvec4*)tvec4_pow((PyObject*)self, obj1, Py_None);

	if (PY_IS_NOTIMPLEMENTED(temp)) return (PyObject*)temp;

	self->x = temp->x;
	self->y = temp->y;
	self->z = temp->z;
	self->w = temp->w;

	Py_DECREF(temp);
	Py_INCREF(self);
	return (PyObject*)self;
}

static PyMemberDef tvec4_members[] = {
	{ "x", T_DOUBLE, offsetof(tvec4, x), 0,
	"vec x" },
{ "y", T_DOUBLE, offsetof(tvec4, y), 0,
"vec y" },
{ "z", T_DOUBLE, offsetof(tvec4, z), 0,
"vec z" },
{ "w", T_DOUBLE, offsetof(tvec4, w), 0,
"vec z" },
{ NULL }  /* Sentinel */
};

static PyObject *
tvec4_str(tvec4* self)
{
	char * out = (char*)malloc((64) * sizeof(char));
	snprintf(out, 64, "tvec4( %12.6g, %12.6g, %12.6g, %12.6g )", self->x, self->y, self->z, self->w);
	PyObject* po = PyUnicode_FromString(out);
	free(out);
	return po;
}

static Py_ssize_t tvec4_len(tvec4 * self) {
	return (Py_ssize_t)4;
}

static PyObject* tvec4_sq_item(tvec4 * self, Py_ssize_t index) {
	switch (index) {
	case 0:
		return PyFloat_FromDouble(self->x);
	case 1:
		return PyFloat_FromDouble(self->y);
	case 2:
		return PyFloat_FromDouble(self->z);
	case 3:
		return PyFloat_FromDouble(self->w);
	default:
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return NULL;
	}
}

static int tvec4_sq_ass_item(tvec4 * self, Py_ssize_t index, PyObject * value) {
	double d;
	if (IS_NUMERIC(value)) {
		d = pyvalue_as_double(value);
	}
	else {
		PY_TYPEERROR("must be real number, not ", value);
		return -1;
	}
	switch (index) {
	case 0:
		self->x = d;
		return 0;
	case 1:
		self->y = d;
		return 0;
	case 2:
		self->z = d;
		return 0;
	case 3:
		self->w = d;
		return 0;
	default:
		PyErr_SetString(PyExc_IndexError, "index out of range");
		return -1;
	}
}

static int tvec4_contains(tvec4 * self, PyObject * value) {
	double d;
	if (IS_NUMERIC(value)) {
		d = pyvalue_as_double(value);
		return (int)(d == self->x || d == self->y || d == self->z || d == self->w);
	}
	return 0;
	
}

static PyObject * tvec4_richcompare(tvec4 * self, PyObject * other, int comp_type) {
	ivec4 o2;

	if (!unpack_ivec4p(other, &o2)) {
		if (comp_type == Py_EQ) {
			Py_RETURN_FALSE;
		}
		if (comp_type == Py_NE) {
			Py_RETURN_TRUE;
		}
		Py_RETURN_NOTIMPLEMENTED;
	}

	switch (comp_type) {
	case Py_EQ:
		if ((self->x == o2.x) && (self->y == o2.y) && (self->z == o2.z) && (self->w == o2.w)) Py_RETURN_TRUE;
		else Py_RETURN_FALSE;
		break;
	case Py_NE:
		if ((self->x != o2.x) || (self->y != o2.y) || (self->z != o2.z) || (self->w != o2.w)) Py_RETURN_TRUE;
		else Py_RETURN_FALSE;
		break;
	case Py_LT:
		return pack_tvec4((double)(self->x < o2.x), (double)(self->y < o2.y), (double)(self->z < o2.z), (double)(self->w < o2.w));
		break;
	case Py_LE:
		return pack_tvec4((double)(self->x <= o2.x), (double)(self->y <= o2.y), (double)(self->z <= o2.z), (double)(self->w <= o2.w));
		break;
	case Py_GT:
		return pack_tvec4((double)(self->x > o2.x), (double)(self->y > o2.y), (double)(self->z > o2.z), (double)(self->w > o2.w));
		break;
	case Py_GE:
		return pack_tvec4((double)(self->x >= o2.x), (double)(self->y >= o2.y), (double)(self->z >= o2.z), (double)(self->w >= o2.w));
		break;
	default:
		Py_RETURN_NOTIMPLEMENTED;
	}
}

static bool unswizzle_tvec4(tvec4 * self, char c, double * out) {
	if (c == 'x' || c == 'r' || c == 's') {
		*out = self->x;
		return true;
	}
	if (c == 'y' || c == 'g' || c == 't') {
		*out = self->y;
		return true;
	}
	if (c == 'z' || c == 'b' || c == 'q') {
		*out = self->z;
		return true;
	}
	if (c == 'w' || c == 'a' || c == 'p') {
		*out = self->w;
		return true;
	}
	return false;
}

static PyObject * tvec4_getattr(PyObject * obj, PyObject * name) {
	char * name_as_ccp = attr_name_to_cstr(name);
	size_t len = strlen(name_as_ccp);

	if ((len >= 4 && name_as_ccp[0] == '_' && name_as_ccp[1] == '_' && name_as_ccp[len - 1] == '_' && name_as_ccp[len - 2] == '_')
		|| strcmp(name_as_ccp, "x") == 0 || strcmp(name_as_ccp, "y") == 0 || strcmp(name_as_ccp, "z") == 0 || strcmp(name_as_ccp, "w") == 0) {
		return PyObject_GenericGetAttr(obj, name);
	}
	
	if (len == 1) {
		double x;
		if (unswizzle_tvec4((tvec4 *)obj, name_as_ccp[0], &x)) {
			return PyFloat_FromDouble(x);
		}
	}
	else if (len == 2) {
		double x;
		double y;
		if (unswizzle_tvec4((tvec4 *)obj, name_as_ccp[0], &x) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[1], &y)) {
			return pack_tvec2(x, y);
		}
	}
	else if (len == 3) {
		double x; 
		double y;
		double z;
		if (unswizzle_tvec4((tvec4 *)obj, name_as_ccp[0], &x) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[1], &y) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[2], &z)) {
			return pack_tvec3(x, y, z);
		}
	}
	else if (len == 4) {
		double x;
		double y;
		double z;
		double w;
		if (unswizzle_tvec4((tvec4 *)obj, name_as_ccp[0], &x) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[1], &y) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[2], &z) && unswizzle_tvec4((tvec4 *)obj, name_as_ccp[3], &w)) {
			return pack_tvec4(x, y, z, w);
		}
	}
	return PyObject_GenericGetAttr(obj, name);
}

// iterator

static PyObject *
tvec4Iter_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
	tvec4 *sequence;

	if (!PyArg_UnpackTuple(args, "__iter__", 1, 1, &sequence))
		return NULL;

	/* Create a new tvec4Iter and initialize its state - pointing to the last
	* index in the sequence.
	*/
	tvec4Iter *rgstate = (tvec4Iter *)type->tp_alloc(type, 0);
	if (!rgstate)
		return NULL;

	rgstate->sequence = sequence;
	Py_INCREF(sequence);
	rgstate->seq_index = 0;

	return (PyObject *)rgstate;
}

static void
tvec4Iter_dealloc(tvec4Iter *rgstate)
{
	Py_XDECREF(rgstate->sequence);
	Py_TYPE(rgstate)->tp_free(rgstate);
}

static PyObject *
tvec4Iter_next(tvec4Iter *rgstate)
{
	if (rgstate->seq_index < 4) {
		switch (rgstate->seq_index) {
		case 0:
			rgstate->seq_index++;
			return PyFloat_FromDouble(rgstate->sequence->x);
		case 1:
			rgstate->seq_index++;
			return PyFloat_FromDouble(rgstate->sequence->y);
		case 2:
			rgstate->seq_index++;
			return PyFloat_FromDouble(rgstate->sequence->z);
		case 3:
			rgstate->seq_index++;
			return PyFloat_FromDouble(rgstate->sequence->w);
		}
	}
	rgstate->seq_index = 4;
	Py_CLEAR(rgstate->sequence);
	return NULL;
}

static PyObject * tvec4_geniter(tvec4 * self) {
	/* Create a new tvec4Iter and initialize its state - pointing to the last
	* index in the sequence.
	*/
	tvec4Iter *rgstate = (tvec4Iter *)((&tvec4IterType)->tp_alloc(&tvec4IterType, 0));
	if (!rgstate)
		return NULL;

	rgstate->sequence = self;
	Py_INCREF(self);
	rgstate->seq_index = 0;

	return (PyObject *)rgstate;
}

static PySequenceMethods tvec4SeqMethods = {
	(lenfunc)tvec4_len, // sq_length
	0, // sq_concat
	0, // sq_repeat
	(ssizeargfunc)tvec4_sq_item, // sq_item
	0,
	(ssizeobjargproc)tvec4_sq_ass_item, // sq_ass_item
	0,
	(objobjproc)tvec4_contains, // sq_contains
	0, // sq_inplace_concat
	0, // sq_inplace_repeat
};

#if PY3K
static PyNumberMethods tvec4NumMethods = {
	(binaryfunc)tvec4_add,
	(binaryfunc)tvec4_sub,
	(binaryfunc)tvec4_mul,
	(binaryfunc)tvec4_mod, //nb_remainder
	(binaryfunc)tvec4_divmod, //nb_divmod
	(ternaryfunc)tvec4_pow, //nb_power
	(unaryfunc)tvec4_neg, //nb_negative
	(unaryfunc)tvec4_pos, //nb_positive
	(unaryfunc)tvec4_abs, //nb_absolute
	0, //nb_bool
	0, //nb_invert
	0, //nb_lshift
	0, //nb_rshift
	0, //nb_and
	0, //nb_xor
	0, //nb_or
	0, //nb_int
	0, //nb_reserved
	0, //nb_float

	(binaryfunc)tvec4_iadd, //nb_inplace_add
	(binaryfunc)tvec4_isub, //nb_inplace_subtract
	(binaryfunc)tvec4_imul, //nb_inplace_multiply
	(binaryfunc)tvec4_imod, //nb_inplace_remainder
	(ternaryfunc)tvec4_ipow, //nb_inplace_power
	0, //nb_inplace_lshift
	0, //nb_inplace_rshift
	0, //nb_inplace_and
	0, //nb_inplace_xor
	0, //nb_inplace_or

	(binaryfunc)tvec4_floordiv, //nb_floor_divide
	(binaryfunc)tvec4_div,
	(binaryfunc)tvec4_ifloordiv, //nb_inplace_floor_divide
	(binaryfunc)tvec4_idiv, //nb_inplace_true_divide

	0, //nb_index
};
#else
static PyNumberMethods tvec4NumMethods = {
	(binaryfunc)tvec4_add, //nb_add;
	(binaryfunc)tvec4_sub, //nb_subtract;
	(binaryfunc)tvec4_mul, //nb_multiply;
	(binaryfunc)tvec4_div, //nb_divide;
	(binaryfunc)tvec4_mod, //nb_remainder;
	(binaryfunc)tvec4_divmod, //nb_divmod;
	(ternaryfunc)tvec4_pow, //nb_power;
	(unaryfunc)tvec4_neg, //nb_negative;
	(unaryfunc)tvec4_pos, //nb_positive;
	(unaryfunc)tvec4_abs, //nb_absolute;
	0, //nb_nonzero;       /* Used by PyObject_IsTrue */
	0, //nb_invert;
	0, //nb_lshift;
	0, //nb_rshift;
	0, //nb_and;
	0, //nb_xor;
	0, //nb_or;
	0, //nb_coerce;       /* Used by the coerce() function */
	0, //nb_int;
	0, //nb_long;
	0, //nb_float;
	0, //nb_oct;
	0, //nb_hex;

	   /* Added in release 2.0 */
	   (binaryfunc)tvec4_iadd, //nb_inplace_add;
	   (binaryfunc)tvec4_isub, //nb_inplace_subtract;
	   (binaryfunc)tvec4_imul, //nb_inplace_multiply;
	   (binaryfunc)tvec4_idiv, //nb_inplace_divide;
	   (binaryfunc)tvec4_imod, //nb_inplace_remainder;
	   (ternaryfunc)tvec4_ipow, //nb_inplace_power;
	   0, //nb_inplace_lshift;
	   0, //nb_inplace_rshift;
	   0, //nb_inplace_and;
	   0, //nb_inplace_xor;
	   0, //nb_inplace_or;

		  /* Added in release 2.2 */
		  (binaryfunc)tvec4_floordiv, //nb_floor_divide;
		  (binaryfunc)tvec4_div, //nb_true_divide;
		  (binaryfunc)tvec4_ifloordiv, //nb_inplace_floor_divide;
		  (binaryfunc)tvec4_idiv, //nb_inplace_true_divide;
};
#endif

static PyTypeObject tvec4Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"glm::detail::tvec4",             /* tp_name */
	sizeof(tvec4),             /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)tvec4_dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	(reprfunc)tvec4_str,                         /* tp_repr */
	&tvec4NumMethods,             /* tp_as_number */
	&tvec4SeqMethods,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	(reprfunc)tvec4_str,                         /* tp_str */
	(getattrofunc)tvec4_getattr,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT |
	Py_TPFLAGS_BASETYPE |
	Py_TPFLAGS_CHECKTYPES,   /* tp_flags */
	"tvec4( <tvec4 compatible type(s)> )\n4 components vector of medium double-qualifier floating-point numbers.",            /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	(richcmpfunc)tvec4_richcompare,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	(getiterfunc)tvec4_geniter,                         /* tp_iter */
	0,                         /* tp_iternext */
	0,             /* tp_methods */
	tvec4_members,             /* tp_members */
	0,           			/* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)tvec4_init,      /* tp_init */
	0,                         /* tp_alloc */
	(newfunc)tvec4_new,                 /* tp_new */
};

static PyTypeObject tvec4IterType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"tvec4Iter",             /* tp_name */
	sizeof(tvec4Iter),             /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)tvec4Iter_dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	0,                         /* tp_repr */
	0,             /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,   /* tp_flags */
	"tvec4 iterator",           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	(iternextfunc)tvec4Iter_next,                         /* tp_iternext */
	0,             /* tp_methods */
	0,             /* tp_members */
	0,           			/* tp_getset */
	0,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	0,      /* tp_init */
	0,                         /* tp_alloc */
	(newfunc)tvec4Iter_new,                 /* tp_new */
};
