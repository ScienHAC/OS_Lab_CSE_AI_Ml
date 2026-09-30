processes = [
    {"pid": "P1", "arrival": 0, "burst": 7},
    {"pid": "P2", "arrival": 2, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 1},
    {"pid": "P4", "arrival": 5, "burst": 4}
]
Intervals = [
    ("P1",0,2),("P2",2,4),("P1",4,6),
    ("P3",6,7),("P2",7,9),("P4",9,11),
    ("P1",11,13),("P4",13,15),("P1",15,16)
]
print("="*50)
for p in processes:
    print(f"Process {p['pid']}: Arrival={p['arrival']}, Burst={p['burst']}")
print("="*50)
for interval in Intervals:
    print(f"Process {interval[0]}: {interval[1]} - {interval[2]}")
print("="*50)

def calculate_metrics():
    print("\n---Scheduling Metrics---")
    print("PID AT BT CT TAT WT RT")
    global tat_total, wt_total, rt_total
    tat_total = 0
    wt_total = 0
    rt_total = 0
    for p in processes:
        runs = [x for x in Intervals if x[0] == p["pid"]]
        first_start = runs[0][1]
        completion = runs[-1][2]
        tat = completion - p["arrival"]
        wt = tat - p["burst"]
        rt = first_start - p["arrival"]
        tat_total += tat
        wt_total += wt
        rt_total += rt
        print(f"{p['pid']} {p['arrival']} {p['burst']} {completion} {tat} {wt} {rt}")

n = len(processes)
# calculate_metrics()

# print(f"\nAverage TAT: {tat_total/n:.2f}")
# print(f"Average WT: {wt_total/n:.2f}")
# print(f"Average RT: {rt_total/n:.2f}")

def show_gantt_chart():
    print("\n---Round Robin Gantt Chart---")
    print(" | ".join(pip for pip, _, _ in Intervals))
    times = [Intervals[0][1]] + [interval[2] for interval in Intervals]
    print(" | ".join(str(t) for t in times))

# show_gantt_chart()
print("="*50)
from threading import Thread, current_thread
def thread_task(name):
    print(name, "running | thread ID.",current_thread().ident)

def thread_demo():
    print("\n---Threading Demo---")

    t1 = Thread(target=thread_task, args=("Thread 1",))
    t2 = Thread(target=thread_task, args=("Thread 2",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Both threads completed.")

# thread_demo()

from multiprocessing import Pipe, Process

def child_pipe(conn):
    conn.send("Hello Parent - message from Child")
    conn.close()

def pipe_demo():
    print("\n--PIPE IPC DEMO--")
    parent_conn, child_conn = Pipe()
    child = Process(target=child_pipe, args=(child_conn,))
    child.start()
    message = parent_conn.recv()
    child.join()
    print("Parent received:", message)

# pipe_demo()

from multiprocessing import Value

def update_shared(value):
    value.value += 10

def shared_memory_demo():
    print("\n---Shared Memory Demo---")
    shared_value = Value('i', 5)  # 'i' indicates a signed integer
    print("Before Child Process:", shared_value.value)
    child = Process(target=update_shared, args=(shared_value,))
    child.start()
    child.join()
    print("After Child Process:", shared_value.value)

# shared_memory_demo()
if __name__ == "__main__":
    calculate_metrics()
    print(f"\nAverage TAT: {tat_total/n:.2f}")
    print(f"Average WT: {wt_total/n:.2f}")
    print(f"Average RT: {rt_total/n:.2f}")
    show_gantt_chart()
    thread_demo()
    pipe_demo()
    shared_memory_demo()
