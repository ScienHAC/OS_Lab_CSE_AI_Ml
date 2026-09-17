from collections import deque


def priority_round_robin(processes, quantum):
	"""Return scheduling results for (pid, arrival, burst, priority) tuples."""
	if quantum <= 0:
		raise ValueError("time quantum must be positive")

	jobs = sorted(
		[{"pid": p, "arrival": int(a), "burst": int(b), "priority": int(pr),
		  "remaining": int(b)} for p, a, b, pr in processes],
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
		start = time
		run = min(quantum, job["remaining"])
		time += run
		job["remaining"] -= run

		while index < len(jobs) and jobs[index]["arrival"] <= time:
			new_job = jobs[index]
			ready.setdefault(new_job["priority"], deque()).append(new_job)
			index += 1

		if job["remaining"]:
			queue.append(job)
		else:
			job["completion"] = time
			job["turnaround"] = time - job["arrival"]
			job["waiting"] = job["turnaround"] - job["burst"]
			completed.append(job)

	return sorted(completed, key=lambda x: x["pid"])


def main():
	n = int(input("Number of processes: "))
	processes = []
	for _ in range(n):
		pid, arrival, burst, priority = input(
			"PID Arrival Burst Priority: "
		).split()
		processes.append((pid, arrival, burst, priority))
	quantum = int(input("Time quantum: "))

	results = priority_round_robin(processes, quantum)
	print("\nPID\tCT\tTAT\tWT")
	for p in results:
		print(f'{p["pid"]}\t{p["completion"]}\t{p["turnaround"]}\t{p["waiting"]}')

	count = len(results)
	print(f'\nAverage waiting time: {sum(p["waiting"] for p in results) / count:.2f}')
	print(f'Average turnaround time: {sum(p["turnaround"] for p in results) / count:.2f}')


if __name__ == "__main__":
	main()
