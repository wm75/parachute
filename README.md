parachute
=========
A python decorator that helps in splitting code into argument checking and worker functions.
It eliminates the need to replicate the worker function signature in the argument checking function definition and
enables argument validation *before* calling into the worker function.

Requirements
------------
Python3

How to use
----------

Move any argument checking code from any function to a dedicated new function and wrap it with the parachute decorator.
When the wrapped function gets called with arbitrary arguments, the decorator checks whether a valid call to the
worker function can be formed from them, then passes the arguments (as a single dictionary with **expression flattened
out) to the argument checking function.
The first argument to the decorated function must be a NamedTuple with field names 'func' and 'innerscope'
(like the FuncInfo class provided with parachute). In it, func holds the name of the worker function and the boolean
value of innerscope specifies whether the decorated function is called from inside or outside func.
If called from inside func, the decorator expects a single positional argument which should be a dictionary including
the arguments passed to func (but may have additional entries).

What it's not
-------------

This is not yet another decorator for checking parameter *types*

Example
-------

    from parachute import parachute, FuncInfo
    
    def worker_function (a, b, c=None, *args, **kwargs):
        start_working_with_the_args()

    @parachute
    def arg_check(**test_args):
        print (locals())
        # real argument checks should go here instead

Example 1: a valid set of parameters for worker_function

    arg_check(FuncInfo(func=worker_function, innerscope=False), 1, 2, 3, 4, d='another', e='yetanother')
    # arg_check gets called with a dictionary of bound arguments


    {'test_args': {'a': 1, 'b': 2, 'c': 3, 'args': (4,), 'e': 'yetanother', 'd': 'another'}}


Example 2: an invalid set of parameters for worker_function

    arg_check(FuncInfo(worker_function, False), 1, d='another', e='yetanother')


    Traceback (most recent call last):
      File "<pyshell#38>", line 1, in <module>
        arg_check(worker_function, None, 1, d='another', e='yetanother')
      File "C:\parachute.py", line 30, in wrappee
        arg_dict = getcallargs(func, *args, **kwargs)
      File "C:\Python33\lib\inspect.py", line 1032, in getcallargs
        _missing_arguments(f_name, req, True, arg2value)
      File "C:\Python33\lib\inspect.py", line 964, in _missing_arguments
        "" if missing == 1 else "s", s))
    TypeError: worker_function() missing 1 required positional argument: 'b'


Example 3: innerscope call

    def worker2 (x, y, z=3, **kwargs):
        # let the decorator determine the set of input arguments from locals() by inspecting worker2's signature
        b = 42 # add something to locals() just to illustrate this
        arg_check(FuncInfo(worker2, innerscope=True), locals())
        
    worker2(3, 7, mode='multiply')


    {'test_args': {'x': 3, 'y': 7, 'z': 3, 'mode': 'multiply'}}
