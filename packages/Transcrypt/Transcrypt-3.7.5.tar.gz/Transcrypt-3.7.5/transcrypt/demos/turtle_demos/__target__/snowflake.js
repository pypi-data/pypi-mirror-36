// Transcrypt'ed from Python, 2018-09-16 20:42:42
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, format, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {Turtle, _allTurtles, _debug, _defaultElement, _defaultTurtle, _height, _ns, _offset, _rightSize, _svg, _timer, _width, back, begin_fill, bgcolor, circle, color, distance, done, down, end_fill, forward, goto, home, left, ontimer, pensize, pos, position, py_clear, reset, right, setDefaultElement, speed, up} from './turtle.js';
var __name__ = '__main__';
export var josh = Turtle ();
export var draw = function (length) {
	if (length > 9) {
		draw (length / 3);
		josh.left (60);
		draw (length / 3);
		josh.right (120);
		draw (length / 3);
		josh.left (60);
		draw (length / 3);
	}
	else {
		josh.forward (length);
	}
};
export var length = 150;
josh.up ();
josh.forward (length / 2);
josh.left (90);
josh.forward (length / 4);
josh.right (90);
josh.down ();
for (var i = 0; i < 3; i++) {
	josh.right (120);
	draw (length);
}
josh.done ();

//# sourceMappingURL=snowflake.map