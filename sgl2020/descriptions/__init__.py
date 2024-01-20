from ._flt1002 import FLT1002 as _FLT1002
from ._flt1003 import FLT1003 as _FLT1003
from ._flt1004 import FLT1004 as _FLT1004
from ._flt1005 import FLT1005 as _FLT1005
from ._flt1006 import FLT1006 as _FLT1006
from ._flt1007 import FLT1007 as _FLT1007

FLIGHT_DESCRIPTIONS = {
    "1002": _FLT1002,
    "1003": _FLT1003,
    "1004": _FLT1004,
    "1005": _FLT1005,
    "1006": _FLT1006,
    "1007": _FLT1007,
}
from ._sensor import SENSOR_DESCRIPTIONS
