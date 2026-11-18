import threading
import time

# ---------- Part 1: Producer-Consumer (bounded buffer) ----------
BUFFER_SIZE = 3
buffer = [None] * BUFFER_SIZE
in_index = 0
out_index = 0
empty = threading.Semaphore(BUFFER_SIZE)  # free slots
full = threading.Semaphore(0)             # filled slots
buffer_lock = threading.Lock()


def producer():
    global in_index
    for item in range(1, 5):
        empty.acquire()
        with buffer_lock:
            buffer[in_index] = item
            print(f"Producer produced {item} at position {in_index}")
            in_index = (in_index + 1) % BUFFER_SIZE
        full.release()
        time.sleep(0.05)


def consumer():
    global out_index
    for _ in range(4):
        full.acquire()
        with buffer_lock:
            item = buffer[out_index]
            buffer[out_index] = None
            print(f"Consumer consumed {item} from position {out_index}")
            out_index = (out_index + 1) % BUFFER_SIZE
        empty.release()
        time.sleep(0.05)


def producer_consumer_demo():
    print("\n========== PRODUCER - CONSUMER ==========")
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()
    print("Producer-Consumer completed safely.")


# ---------- Part 2: Readers-Writers ----------
read_count = 0
read_count_lock = threading.Lock()
resource_lock = threading.Lock()
shared_data = "Initial Data"


def reader(reader_id):
    global read_count
    with read_count_lock:
        read_count += 1
        if read_count == 1:
            resource_lock.acquire()  # first reader locks out writers
    print(f"Reader {reader_id} reads: {shared_data}")
    time.sleep(0.05)
    with read_count_lock:
        read_count -= 1
        if read_count == 0:
            resource_lock.release()  # last reader lets writers in


def writer(writer_id):
    global shared_data
    with resource_lock:
        shared_data = f"Data updated by Writer {writer_id}"
        print(f"Writer {writer_id} writes: {shared_data}")
        time.sleep(0.05)


def readers_writers_demo():
    print("\n========== READERS - WRITERS ==========")
    reader1 = threading.Thread(target=reader, args=(1,))
    reader2 = threading.Thread(target=reader, args=(2,))
    writer1 = threading.Thread(target=writer, args=(1,))
    reader1.start()
    reader2.start()
    writer1.start()
    reader1.join()
    reader2.join()
    writer1.join()
    print("Readers-Writers completed safely.")


# ---------- Part 3: Dining Philosophers ----------
NUMBER_OF_PHILOSOPHERS = 5
forks = [threading.Lock() for _ in range(NUMBER_OF_PHILOSOPHERS)]
# Waiter: at most 4 philosophers compete for forks, so a full circular wait is impossible.
waiter = threading.Semaphore(NUMBER_OF_PHILOSOPHERS - 1)


def philosopher(philosopher_id):
    left_fork = forks[philosopher_id]
    right_fork = forks[(philosopher_id + 1) % NUMBER_OF_PHILOSOPHERS]
    print(f"Philosopher {philosopher_id + 1} is thinking.")
    with waiter:
        left_fork.acquire()
        right_fork.acquire()
        try:
            print(f"Philosopher {philosopher_id + 1} is eating.")
            time.sleep(0.05)
        finally:
            right_fork.release()
            left_fork.release()
    print(f"Philosopher {philosopher_id + 1} finished.")


def dining_philosophers_demo():
    print("\n========== DINING PHILOSOPHERS ==========")
    threads = []
    for i in range(NUMBER_OF_PHILOSOPHERS):
        thread = threading.Thread(target=philosopher, args=(i,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print("Dining Philosophers completed without deadlock.")


def main():
    producer_consumer_demo()
    readers_writers_demo()
    dining_philosophers_demo()
    print("\nPROGRAM 3 COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
