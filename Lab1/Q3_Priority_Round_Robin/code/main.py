def priority_scheduling(processes):
    current_time = 0
    completed = []
    result = []

    while len(completed) < len(processes):
        ready = [p for p in processes if p["arrival"] <= current_time and p["pid"] not in completed]

        if not ready:
            next_time = min(p["arrival"] for p in processes if p["pid"] not in completed)
            result.append({"pid": "Idle", "start": current_time, "end": next_time})
            current_time = next_time
            continue

        p = min(ready, key=lambda x: (x["priority"], x["arrival"], x["pid"]))
        end = current_time + p["burst"]
        result.append({"pid": p["pid"], "start": current_time, "end": end})
        current_time = end
        completed.append(p["pid"])

    return result


print(priority_scheduling([
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]))