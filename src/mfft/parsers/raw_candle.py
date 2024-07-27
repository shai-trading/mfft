from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class RawCandle:

    dt: datetime
    o: float
    h: float
    l: float
    c: float
