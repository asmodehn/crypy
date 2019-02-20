from dataclasses import dataclass, field
import typing

# TODO : this can be made generic by parametrizing on the type float
# TODO : optimized interval logic ?


@dataclass
class Bounds:
    upper: typing.Optional[float] = None
    lower: typing.Optional[float] = None

    def __post_init__(self):
        assert self.upper is None or self.lower is None or self.upper > self.lower,\
            "Looks like upper and lower bounds have been swapped ?"

    def __call__(self,
                 value: float,
                 on_under: typing.Optional[typing.Callable] = None,
                 on_over: typing.Optional[typing.Callable] = None):
        proceed = True  # proceed by default

        if self.lower and value < self.lower:
            try:
                proceed = on_under(value, self.lower)
            except TypeError:
                if on_under is None:
                    return True  # no action on out of bounds -> keep usual semantics
                raise
        elif self.upper and value > self.upper:
            try:
                proceed = on_over(value, self.upper)
            except TypeError:
                if on_over is None:
                    return True  # no action on out of bounds -> keep usual semantics
                raise
        return proceed




# TODO : PID Controller on top of it ?
