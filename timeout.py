import threading


class TimeoutException(Exception):
    pass

def function_with_timeout(timeout, function, *args, **kwargs):
    stop_event = threading.Event()
    shared_data = {
        'min_path': None,
        'min_distance': None
    }

    class FunctionThread(threading.Thread):
        def run(self):
            try:
                function(shared_data, stop_event, *args, **kwargs)
            except Exception as e:
                self.error = e

    thread = FunctionThread()
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        stop_event.set()
        thread.join()  # Wait for the thread to acknowledge the stop event and exit
        print("Function timed out, returning best result so far.")

    return shared_data

