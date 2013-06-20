import inspect
from collections import namedtuple

FuncInfo = namedtuple('FuncInfo', ['func','innerscope'])

def parachute (f):
    """Parachute decorator.

    Useful for wrapping parameter checking functions."""
    
    def wrappee(*args, **kwargs):
        """Tests validity of *args[1:], **kwargs for calling function func
        specified by args[0].
        Binds *args[1:], **kwargs to func's paramters and passes them as a
        dictionary mapping to the wrapped function."""

        funcinfo, *args = args
        try:
            if not isinstance(funcinfo.innerscope, bool):
                raise TypeError ('Second element innerscope of funcinfo must be boolean')
        except AttributeError:
            raise TypeError ('Expected FuncInfo(namedtuple) instance as first argument')
        args_name, kwargs_name = inspect.getfullargspec(funcinfo.func)[1:3]
        
        if funcinfo.innerscope:
            args = args[0]
            Sig = inspect.signature(funcinfo.func)
            arg_dict = {k : v for (k,v) in args.items() if k in Sig.parameters}
        else:
            arg_dict = inspect.getcallargs(funcinfo.func, *args, **kwargs)

        arg_dict.update(arg_dict.pop(kwargs_name, {}))
        ret = f(**arg_dict)
        return ret
    return wrappee
