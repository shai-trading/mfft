import re
from datetime import timedelta, datetime


class TimeFrame:

    M_SUFFIX = 'M'  # Minue
    H_SUFFIX = 'H'  # Hour
    D_SUFFIX = 'D'  # Day
    W_SUFFIX = 'W'  # Week
    MONTH_SUFFIX = 'MONTH'  # Month

    TF_ORDER = [M_SUFFIX, H_SUFFIX, D_SUFFIX, W_SUFFIX, MONTH_SUFFIX]

    __delta = timedelta(microseconds=1)
    __tf = '1M'

    @classmethod
    def parse_tf(cls, tf):
        mr = re.match(r'^\s*(\d?\d?)(M|H|D|W|MONTH)\s*$', tf, re.IGNORECASE)
        if mr is None:
            return None, None

        unit = mr.group(1)
        if unit == '':
            unit = 1

        return int(unit), mr.group(2).upper()

    @classmethod
    def tf(cls, tf):
        if isinstance(tf, str):
            return TimeFrame(tf)
        return tf

    def __init__(self, tf):
        self.__tf = tf

    def __str__(self):
        return f"{self.unit()}{self.suffix()}"

    def __eq__(self, other):
        if not isinstance(other, TimeFrame):
            return NotImplemented

        return self.unit() == other.unit() and self.suffix() == other.suffix()

    def unit(self):
        u, _ = self.parse_tf(self.__tf)
        return u

    def suffix(self):
        _, s = self.parse_tf(self.__tf)
        return s

    def allow_change_order(self, new_tf):
        new_tf = TimeFrame.tf(new_tf)
        u_new = new_tf.unit()
        s_new = new_tf.suffix()

        order_new = self.TF_ORDER.index(s_new)
        order_curr = self.TF_ORDER.index(self.suffix())

        if order_new < order_curr:
            return False
        if order_new == order_curr:
            return u_new > self.unit()
        return True

    def close_period(self, dt):
        u = self.unit()
        s = self.suffix()
        c_dt = self.open_period(dt)
        if s == self.M_SUFFIX:
            c_dt = c_dt + timedelta(minutes=u)
        elif s == self.H_SUFFIX:
            c_dt = c_dt + timedelta(hours=u)
        elif s == self.D_SUFFIX:
            c_dt = c_dt + timedelta(days=u)
        elif s == self.W_SUFFIX:
            c_dt = c_dt - timedelta(days=c_dt.weekday())
            c_dt = c_dt + timedelta(days=7 * u)
        elif s == self.MONTH_SUFFIX:
            month = c_dt.month + u - 1
            year = c_dt.year + month // 12
            month = month % 12 + 1
            c_dt = datetime(year=year, month=month, day=1)
        else:
            raise ValueError('Wrong timestamp suffix')
        return c_dt - self.__delta

    def open_period(self, dt):
        s = self.suffix()
        c_dt = dt
        if s == self.M_SUFFIX:
            pass
        elif s == self.H_SUFFIX:
            c_dt = c_dt.replace(minute=0, second=0, microsecond=0)
        elif s == self.D_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif s == self.W_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            c_dt = c_dt - timedelta(days=c_dt.weekday())
        elif s == self.MONTH_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0, day=1)
        else:
            raise ValueError('Wrong timestamp suffix')
        return c_dt

    def next_period(self, dt):
        return self.close_period(dt) + self.__delta
