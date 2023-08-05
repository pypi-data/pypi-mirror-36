"""timer3 - Scheduler for Python functions."""
import atexit
import heapq
import sys
import warnings

from threading import Thread, Event
from time import time, sleep, mktime

from datetime import datetime, timedelta

VERSION = (0, 1, 1)
__version__ = ".".join(map(str, VERSION))
__author__ = "Ask Solem"
__contact__ = "ask@celeryproject.org"
__homepage__ = "http://github.com/ask/timer/"
__docformat__ = "restructuredtext"

DEFAULT_MAX_INTERVAL = 3.1415

class TimedFunctionFailed(UserWarning):
    pass


class Entry:
    cancelled = False

    def __init__(self, fun, args, kwargs):
        self.fun = fun
        self.args = args or []
        self.kwargs = kwargs or {}
        self.tref = self

    def __call__(self):
        return self.fun(*self.args, **self.kwargs)

    def cancel(self):
        self.tref.cancelled = True

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return True

    
class Schedule:
    """ETA scheduler."""
    on_error = None

    def __init__(self, max_interval=DEFAULT_MAX_INTERVAL, on_error=None):
        self.max_interval = float(max_interval)
        self.on_error = on_error or self.on_error
        self._queue = []

    def handle_error(self, exc_info):
        if self.on_error:
            self.on_error(exc_info)
            return True

    def enter(self, entry, eta=None, priority=0):
        """Enter function into the scheduler.

        :param entry: Item to enter.
        :keyword eta: Scheduled time as a :class:`datetime.datetime` object.
        :keyword priority: Unused.

        """
        if isinstance(eta, datetime):
            try:
                eta = mktime(eta.timetuple())
            except OverflowError:
                self.handle_error(sys.exc_info())
        eta = eta or time()
        heapq.heappush(self._queue, (eta, priority, entry))
        return entry

    def __iter__(self):
        """The iterator yields the time to sleep for between runs."""

        # localize variable access
        nowfun = time
        pop = heapq.heappop

        while 1:
            if self._queue:
                eta, priority, entry = verify = self._queue[0]
                now = nowfun()

                if now < eta:
                    yield min(eta - now, self.max_interval)
                else:
                    event = pop(self._queue)
                    if event is verify:
                        if not entry.cancelled:
                            try:
                                entry()
                            except Exception as exc:
                                if not self.handle_error(sys.exc_info()):
                                    warnings.warn(repr(exc), TimedFunctionFailed)
                        continue
                    else:
                        heapq.heappush(self._queue, event)
            yield None

    def empty(self):
        """Is the schedule empty?"""
        return not self._queue

    def clear(self):
        self._queue = []

    def info(self):
        return ({"eta": eta, "priority": priority, "item": item}
                for eta, priority, item in self.queue)

    @property
    def queue(self):
        events = list(self._queue)
        return list(map(heapq.heappop, [events]*len(events)))


class Timer(Thread):
    Entry = Entry

    precision = 0.3
    running = False
    on_tick = None

    def __init__(self, schedule=None, precision=None, on_error=None,
                 on_tick=None):
        if precision is not None:
            self.precision = precision
        self.schedule = schedule or Schedule(on_error=on_error)
        self.on_tick = on_tick or self.on_tick

        Thread.__init__(self)
        self._shutdown = Event()
        self._stopped = Event()
        self.setDaemon(True)

    def run(self):
        self.running = True
        scheduler = iter(self.schedule)
        while not self._shutdown.isSet():
            delay = next(scheduler) or self.precision
            if self.on_tick:
                self.on_tick(delay)
            sleep(delay)
        self._stopped.set()

    def stop(self):
        if not self.running:
            return
        self._shutdown.set()
        self._stopped.wait()
        self.join(1e100)

    def enter(self, entry, eta, priority=None):
        if not self.running:
            self.start()
        return self.schedule.enter(entry, eta, priority)

    def apply_at(self, eta, fun, args=(), kwargs={}, priority=0):
        return self.enter(self.Entry(fun, args, kwargs), eta, priority)

    def enter_after(self, msecs, entry, priority=0):
        eta = datetime.now() + timedelta(seconds=msecs / 1000.0)
        return self.enter(entry, eta, priority)

    def apply_after(self, msecs, fun, args=(), kwargs={}, priority=0):
        return self.enter_after(msecs, Entry(fun, args, kwargs), priority)

    def apply_interval(self, msecs, fun, args=(), kwargs={}, priority=0):
        tref = Entry(fun, args, kwargs)

        def _reschedules(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            finally:
                self.enter_after(msecs, tref, priority)

        tref.fun = _reschedules
        return self.enter_after(msecs, tref, priority)

    def exit_after(self, msecs, priority=10):
        self.apply_after(msecs, sys.exit, priority)

    def cancel(self, tref):
        tref.cancel()

    def clear(self):
        self.schedule.clear()

    def empty(self):
        return self.schedule.empty()

    @property
    def queue(self):
        return self.schedule.queue

_default_timer = Timer()
apply_after = _default_timer.apply_after
apply_at = _default_timer.apply_at
apply_interval = _default_timer.apply_interval
enter_after = _default_timer.enter_after
enter = _default_timer.enter
exit_after = _default_timer.exit_after
cancel = _default_timer.cancel
clear = _default_timer.clear

atexit.register(_default_timer.stop)
