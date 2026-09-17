from collections import deque


def priority_round_robin(processes, quantum):
    """Return scheduling results for a list of process dictionaries or tuples."""
    if quantum <= 0:
        raise ValueError("time quantum must be positive")

    # Normalize inputs to support dictionaries (with optional priority)
    formatted_processes = []
    for p in processes:
        if isinstance(p, dict):
            pid = p["pid"]
            arrival = int(p["arrival"])
            burst = int(p["burst"])
            priority = int(p.get("priority", 0))  # Default priority is 0 if omitted
        else:
            pid = p[0]
            arrival = int(p[1])
            burst = int(p[2])
            priority = int(p[3]) if len(p) > 3 else 0

        formatted_processes.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "priority": priority,
            "remaining": burst
        })

    jobs = sorted(
        formatted_processes,
        key=lambda x: (x["arrival"], -x["priority"]),
    )
    ready = {}
    completed = []
    time = 0
    index = 0

    while len(completed) < len(jobs):
        while index < len(jobs) and jobs[index]["arrival"] <= time:
            job = jobs[index]
            ready.setdefault(job["priority"], deque()).append(job)
            index += 1

        if not ready:
            time = jobs[index]["arrival"]
            continue

        priority = max(ready)
        queue = ready[priority]
        job = queue.popleft()

        # Clean up empty queue from ready dictionary to prevent IndexError
        if not queue:
            del ready[priority]

        run = min(quantum, job["remaining"])
        time += run
        job["remaining"] -= run

        while index < len(jobs) and jobs[index]["arrival"] <= time:
            new_job = jobs[index]
            ready.setdefault(new_job["priority"], deque()).append(new_job)
            index += 1

        if job["remaining"]:
            ready.setdefault(job["priority"], deque()).append(job)
        else:
            job["completion"] = time
            job["turnaround"] = time - job["arrival"]
            job["waiting"] = job["turnaround"] - job["burst"]
            completed.append(job)

    return sorted(completed, key=lambda x: x["pid"])


def main():
    # Example using your dictionary format
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
        {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
        {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
        {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
    ]
    
    quantum = 3

    results = priority_round_robin(processes, quantum)
    
    print("\nPID\tCT\tTAT\tWT")
    for p in results:
        print(f'{p["pid"]}\t{p["completion"]}\t{p["turnaround"]}\t{p["waiting"]}')

    count = len(results)
    print(f'\nAverage waiting time: {sum(p["waiting"] for p in results) / count:.2f}')
    print(f'Average turnaround time: {sum(p["turnaround"] for p in results) / count:.2f}')


if __name__ == "__main__":
    main()