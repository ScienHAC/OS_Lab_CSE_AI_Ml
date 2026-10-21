import threading
import time

TASKS = [
    ("Task 1", 2),
    ("Task 2", 3),
    ("Task 3", 1),
]


def do_task(task_name, wait_time):
    thread_id = threading.get_ident()
    print(f"{task_name} STARTED | Thread ID = {thread_id} | Wait = {wait_time}s")
    time.sleep(wait_time)
    print(f"{task_name} FINISHED | Thread ID = {thread_id}")


def single_threaded_demo():
    print("\n========== SINGLE-THREADED ==========")
    start_time = time.perf_counter()
    for task_name, wait_time in TASKS:
        do_task(task_name, wait_time)
    elapsed = time.perf_counter() - start_time
    print(f"Single-threaded time = {elapsed:.2f} seconds")
    return elapsed


def multithreaded_demo():
    print("\n========== MULTITHREADED ==========")
    start_time = time.perf_counter()
    threads = []
    for task_name, wait_time in TASKS:
        thread = threading.Thread(target=do_task, args=(task_name, wait_time))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.perf_counter() - start_time
    print(f"Multithreaded time = {elapsed:.2f} seconds")
    return elapsed


def main():
    single_time = single_threaded_demo()
    multi_time = multithreaded_demo()
    print("\n========== COMPARISON ==========")
    print(f"Single-threaded: {single_time:.2f} seconds")
    print(f"Multithreaded:   {multi_time:.2f} seconds")
    print(f"Speedup: {single_time / multi_time:.2f}x")
    print("\nAll worker threads completed successfully.")


if __name__ == "__main__":
    main()
