from multiprocessing_task.main import multiprocessing_func
from threading_task.main import thread_func
from time import time

if __name__ == "__main__":
    print("Start threading")
    start = time()
    thread_func()
    thread_time = time() - start

    print("Start multiprocessing")
    start_mp = time()
    multiprocessing_func()
    multiprocessin_time = time() - start_mp

    print(f"Thread time: {thread_time}")
    print(f"Multiprocessing time: {multiprocessin_time}")
    if thread_time < multiprocessin_time:
        print("Thread is faster")
    elif thread_time > multiprocessin_time:
        print("Multiprocessing is faster")
    else:
        print("Both are equal")
