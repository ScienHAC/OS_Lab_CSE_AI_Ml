import threading
import time

NUMBER_OF_THREADS = 4
INCREMENTS_PER_THREAD = 1000

# ---------- Version 1: unsafe (no synchronization) ----------
unsafe_counter = 0


def unsafe_worker():
    global unsafe_counter
    for _ in range(INCREMENTS_PER_THREAD):
        old_value = unsafe_counter      # READ
        time.sleep(0)                   # yield: lets another thread interleave
        unsafe_counter = old_value + 1  # WRITE


def run_unsafe():
    global unsafe_counter
    unsafe_counter = 0
    threads = []
    start_time = time.perf_counter()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=unsafe_worker)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start_time
    return unsafe_counter, elapsed


# ---------- Version 2: Mutex ----------
mutex_counter = 0
mutex = threading.Lock()


def mutex_worker():
    global mutex_counter
    for _ in range(INCREMENTS_PER_THREAD):
        with mutex:  # critical section
            old_value = mutex_counter
            time.sleep(0)
            mutex_counter = old_value + 1


def run_mutex():
    global mutex_counter
    mutex_counter = 0
    threads = []
    start_time = time.perf_counter()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=mutex_worker)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start_time
    return mutex_counter, elapsed


# ---------- Version 3: Binary Semaphore ----------
semaphore_counter = 0
binary_semaphore = threading.Semaphore(1)


def semaphore_worker():
    global semaphore_counter
    for _ in range(INCREMENTS_PER_THREAD):
        with binary_semaphore:  # critical section
            old_value = semaphore_counter
            time.sleep(0)
            semaphore_counter = old_value + 1


def run_semaphore():
    global semaphore_counter
    semaphore_counter = 0
    threads = []
    start_time = time.perf_counter()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=semaphore_worker)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start_time
    return semaphore_counter, elapsed


def main():
    expected = NUMBER_OF_THREADS * INCREMENTS_PER_THREAD
    print("========== SHARED COUNTER EXPERIMENT ==========")
    print("Threads              :", NUMBER_OF_THREADS)
    print("Increments per thread:", INCREMENTS_PER_THREAD)
    print("Expected final value :", expected)

    unsafe_value, unsafe_time = run_unsafe()
    mutex_value, mutex_time = run_mutex()
    semaphore_value, semaphore_time = run_semaphore()

    print("\n========== RESULTS ==========")
    print("\n1. WITHOUT SYNCHRONIZATION")
    print("Actual value :", unsafe_value)
    print("Correct?     :", unsafe_value == expected)
    print(f"Time         : {unsafe_time:.4f} seconds")

    print("\n2. WITH MUTEX")
    print("Actual value :", mutex_value)
    print("Correct?     :", mutex_value == expected)
    print(f"Time         : {mutex_time:.4f} seconds")

    print("\n3. WITH BINARY SEMAPHORE")
    print("Actual value :", semaphore_value)
    print("Correct?     :", semaphore_value == expected)
    print(f"Time         : {semaphore_time:.4f} seconds")

    print("\n========== CONCLUSION ==========")
    print("Unsafe access can lose updates because threads race.")
    print("Mutex and binary semaphore protect the critical section.")
    print("Correctness is more important than a faster but wrong result.")


if __name__ == "__main__":
    main()
