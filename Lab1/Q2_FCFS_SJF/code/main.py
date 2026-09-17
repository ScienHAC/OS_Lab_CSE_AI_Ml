from collections import deque


def priority_round_robin(processes, quantum):
    """
    Simulate priority-based Round Robin CPU scheduling.

    processes: list of dicts {"pid", "arrival", "burst", "priority"(optional)}
               or tuples (pid, arrival, burst, priority(optional))
    quantum:   the time slice given to each process per turn

    Higher priority number = runs first. Ties are broken by Round Robin
    (each process in the same priority level gets `quantum` time before
    moving to the back of its queue).
    """
    if quantum <= 0:
        raise ValueError("time quantum must be positive")

    jobs = [_to_job(p) for p in processes]
    jobs.sort(key=lambda job: job["arrival"])

    # One FIFO queue per priority level. queues[3] holds all priority-3 jobs.
    queues = {}
    finished = []

    clock = 0
    next_arrival = 0  # index into `jobs` of the next process that hasn't arrived yet

    def admit_new_arrivals(up_to_time):
        """Move any job that has arrived by `up_to_time` into its queue."""
        nonlocal next_arrival
        while next_arrival < len(jobs) and jobs[next_arrival]["arrival"] <= up_to_time:
            job = jobs[next_arrival]
            queues.setdefault(job["priority"], deque()).append(job)
            next_arrival += 1

    while len(finished) < len(jobs):
        admit_new_arrivals(clock)

        # Nothing ready yet -> fast-forward to the next arrival
        if not queues:
            clock = jobs[next_arrival]["arrival"]
            admit_new_arrivals(clock)

        # Always serve the highest-priority non-empty queue
        top_priority = max(queues)
        queue = queues[top_priority]
        job = queue.popleft()
        if not queue:
            del queues[top_priority]

        # Run the job for one quantum (or until it finishes, if shorter)
        slice_length = min(quantum, job["remaining"])
        clock += slice_length
        job["remaining"] -= slice_length

        # New processes may have arrived while this one was running
        admit_new_arrivals(clock)

        if job["remaining"] > 0:
            # Still has work left -> back of its own priority queue
            queues.setdefault(job["priority"], deque()).append(job)
        else:
            job["completion"] = clock
            job["turnaround"] = clock - job["arrival"]
            job["waiting"] = job["turnaround"] - job["burst"]
            finished.append(job)

    return sorted(finished, key=lambda job: job["pid"])


def _to_job(p):
    """Turn a dict or tuple into a normalized job record."""
    if isinstance(p, dict):
        pid, arrival, burst = p["pid"], int(p["arrival"]), int(p["burst"])
        priority = int(p.get("priority", 0))
    else:
        pid, arrival, burst = p[0], int(p[1]), int(p[2])
        priority = int(p[3]) if len(p) > 3 else 0

    return {
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "priority": priority,
        "remaining": burst,
    }


def print_results(results):
    print("\nPID\tCT\tTAT\tWT")
    for p in results:
        print(f'{p["pid"]}\t{p["completion"]}\t{p["turnaround"]}\t{p["waiting"]}')

    count = len(results)
    avg_wait = sum(p["waiting"] for p in results) / count
    avg_turnaround = sum(p["turnaround"] for p in results) / count
    print(f"\nAverage waiting time: {avg_wait:.2f}")
    print(f"Average turnaround time: {avg_turnaround:.2f}")


def main():
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
        {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
        {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
        {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
    ]
    quantum = 3

    results = priority_round_robin(processes, quantum)
    print_results(results)


if __name__ == "__main__":
    main()