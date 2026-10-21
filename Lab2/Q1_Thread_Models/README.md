# Lab2 Q1 — Thread Creation, Models and Benefits

**Marks: 5**

## Aim

Create independent worker threads, display their identifiers and progress,
wait for completion, and compare their elapsed time with a single-threaded
baseline using the same workload.

## Run

From the repository root:

```bash
python3 Lab2/Q1_Thread_Models/main.py
```

On Windows, use `python` instead of `python3`.

## Workload and procedure

`TASKS` contains Task 1 (2 seconds), Task 2 (3 seconds) and Task 3 (1 second).
Each task uses `time.sleep()` to simulate waiting for I/O. Tasks are independent
and do not modify shared data.

1. The baseline calls `do_task()` three times sequentially on the main thread.
2. Each worker prints STARTED, its thread identifier and its wait duration,
   then prints FINISHED after waiting.
3. The threaded version creates a `threading.Thread` for each task and starts
   all three before waiting.
4. A separate loop calls `join()` on every worker.
5. Both versions use `time.perf_counter()`; threaded timing includes creation,
   execution and joining. The comparison prints both times and their ratio.

`main()` runs each version once. The entry guard prevents execution on import.
The untimed, top-level threaded batch from the initial draft is unnecessary.

## Expected observations

| Version | Approximate time | Explanation |
| --- | --- | --- |
| Single-threaded | 6 seconds | 2 + 3 + 1 seconds of sequential waiting |
| Multithreaded | 3 seconds | Waits overlap; the longest task takes 3 seconds |
| Speedup | 2x | Single-threaded time divided by multithreaded time |

These are estimates; scheduling, console output and thread creation add
overhead. Thread IDs and output order vary. The baseline uses one ID, while
overlapping workers have separate IDs. IDs may be reused after a thread exits.

## Threads and models

User-level threads are managed by a runtime in user space. Switching can be
cheap; whether blocking stalls other threads depends on their kernel mapping.
Kernel-level threads are scheduled by the OS, allowing other runnable threads
to proceed when one blocks, at the cost of OS scheduling and bookkeeping.

| Model | Mapping and consequence |
| --- | --- |
| Many-to-one | Many user threads share one kernel thread; no multicore execution within that group, and a blocking system call can stall it. |
| One-to-one | Each user thread has a kernel thread; supports independent scheduling and multicore execution, with more kernel resources. |
| Many-to-many | A runtime schedules many user threads over several kernel threads, balancing concurrency and resource use. |
| Two-level | Many-to-many with the option to bind particular user threads to particular kernel threads. |

These models describe scheduling mappings. See the
[university thread-model notes](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/4_Threads).

## Benefits and limitations

- **Responsiveness:** background work can let an interface keep handling input.
  This console demo deliberately waits at `join()` before reporting results.
- **Resource sharing:** threads share process memory and open resources, making
  communication convenient but requiring care with shared mutable state.
- **Concurrency:** tasks make progress during overlapping periods, including
  while other tasks wait. This is what the sleep workload demonstrates.
- **Parallelism:** computations execute simultaneously on multiple cores.
  Overlapping sleeps do not establish CPU parallelism.
- **Race conditions:** unsynchronized shared updates can depend on execution
  order and lose data. Use locks or thread-safe queues where appropriate.
  This program has no shared mutable task results.
- **Deadlocks:** threads can wait forever for resources held by one another.
  Consistent lock ordering helps avoid cycles; this program uses no worker locks.
- **Overhead:** thread stacks, creation, context switches and synchronization
  consume resources. Small tasks or too many threads may make execution slower.

In ordinary CPython builds with the GIL enabled, only one thread executes
Python bytecode at a time. Threads are useful for waiting and I/O; this result
does not promise faster CPU-heavy Python loops. Free-threaded builds can
disable the GIL. See the [Python threading documentation](https://docs.python.org/3/library/threading.html)
and [timing documentation](https://docs.python.org/3/library/time.html#time.perf_counter).

## Result

The same three tasks run sequentially and concurrently. Joining every worker
ensures all tasks finish before the threaded timer stops and the comparison
appears. For this workload, overlapping waits reduce elapsed time from roughly
6 seconds to roughly 3 seconds.
