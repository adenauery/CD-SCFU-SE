import os


def remove_log(callback_id, current_time, callback_memory):
    [os.remove(f) for f in os.listdir() if f == "log.txt"]