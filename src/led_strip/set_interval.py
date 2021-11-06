import time, threading


def set_interval(interval):
    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()

            def inner_wrap():
                while not stop.isSet():
                    time.sleep(interval)
                    function(*args, **kwargs)
            threading.Timer(0, inner_wrap).start()
            return stop
        return wrap
    return outer_wrap