parachute
=========
A python decorator that helps in encapsulating code-intensive function argument checking into separate functions.
It enables argument validation before calling into the real worker function.

How to use
----------

Move any argument checking code from any function to a dedicated new function and wrap this with the parachute decorator.
When the wrapped function gets called with arbitrary arguments, the decorator will check whether a valid call to the
worker function can be formed from them, and passes the arguments (as a single dictionary) to the argument checking
function.

Example
-------

def worker_function (a, b, c=None, *args, **kwargs):
    start_working_with_the_args()

@parachute
def arg_check(**test_args):
    print (locals())
    # real argument checks should go here instead

arg_check(worker_function, 1, 2, 3, 4, d='another', e='yetanother')

-->  {'test_args': {'a': 1, 'b': 2, 'c': 3, 'args': (4,), 'kwargs': {'d': 'another', 'e': 'yetanother'}}}

arg_check(worker_function, 1, d='another', e='yetanother')

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
