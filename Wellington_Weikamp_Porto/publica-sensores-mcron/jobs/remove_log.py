import os


def remove_log(callback_id, current_time, callback_memory):
  if(os.listdir()[0] == 'log.txt'):
    os.remove('log.txt')