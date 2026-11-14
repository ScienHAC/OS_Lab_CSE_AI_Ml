# Lab2 Q2 — Race Condition, Mutex and Binary Semaphore

## Aim

Run the same shared-counter workload three ways — unsafe (no synchronization),
protected by a Mutex, and protected by a Binary Semaphore — then compare
correctness and execution time.

## Run

From the repository root:

```bash
python3 Lab2/Q2_Race_Mutex_semaphore/main.py
```

On Windows, use `python` instead of `python3`.

## Workload

- 4 threads x 1000 increments each, so the expected final counter is **4000**.
- All three versions use the identical workload, which keeps the comparison fair.

## Key concepts

| Term | Meaning |
|------|---------|
| Shared resource | Data used by more than one thread (the counter) |
| Race condition | Result depends on unpredictable thread timing |
| Critical section | Code that reads/changes shared data |
| Lost update | One thread's write is overwritten by a thread that used a stale value |
| Mutex | Lock allowing one thread at a time (`threading.Lock`) |
| Binary semaphore | Semaphore with one permit (`threading.Semaphore(1)`) |

An increment is really READ -> MODIFY (+1) -> WRITE. If threads interleave
between these steps, updates are lost.

## Procedure

1. **Unsafe:** each worker reads the counter, yields with `time.sleep(0)`, then
   writes `old + 1`. The yield deliberately exposes the race.
2. **Mutex:** the same read/yield/write sits inside `with mutex:`, so only one
   thread is in the critical section at a time.
3. **Binary semaphore:** same, but guarded by `with binary_semaphore:`.
4. Each `run_*()` function starts the threads, `join()`s them all, and returns
   `(final_value, elapsed)` using `time.perf_counter()`.
5. `main()` prints expected vs actual, a correctness flag and the time for each
   version, followed by a conclusion.

Do not remove `time.sleep(0)`: in CPython a plain counter loop may not show the
race reliably, and the explicit yield makes it observable.

## Sample output

```
1. WITHOUT SYNCHRONIZATION
Actual value : 1083
Correct?     : False

2. WITH MUTEX
Actual value : 4000
Correct?     : True

3. WITH BINARY SEMAPHORE
Actual value : 4000
Correct?     : True
```

The unsafe value and all timings vary from run to run. The mutex and semaphore
versions must always reach 4000.

## Observations

- Unsafe: usually far below 4000 (lost updates); it may be the fastest, but it
  is wrong.
- Mutex and binary semaphore: always 4000.
- Protected versions are typically a little slower because locking and waiting
  add overhead.
- Correctness matters more than speed.

## Viva questions

- **What is a race condition?** A wrong or unpredictable result caused by
  uncontrolled timing of shared-data access.
- **What is a critical section?** Code that reads or changes shared data.
- **Mutex vs binary semaphore?** A mutex is a mutual-exclusion lock; a semaphore
  is a permit counter. With one permit it behaves like a lock.
- **Why `join()`?** Main waits for all workers before comparing results.
- **Why can synchronization be slower?** Locking and waiting add overhead.
