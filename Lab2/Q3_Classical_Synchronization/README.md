# Lab2 Q3 — Classical Synchronization Problems

## Aim

Implement three classical synchronization problems with Python threads, locks
and semaphores: Producer-Consumer, Readers-Writers and Dining Philosophers.
Every demo uses finite iterations so the program terminates normally.

## Run

From the repository root:

```bash
python3 Lab2/Q3_Classical_Synchronization/main.py
```

On Windows, use `python` instead of `python3`.

## 1. Producer-Consumer (bounded buffer)

- Circular buffer of 3 slots with `in_index` / `out_index` (wrap with `%`).
- `empty = Semaphore(3)` counts free slots, `full = Semaphore(0)` counts items,
  `buffer_lock` protects the buffer and indexes.
- Producer: `wait(empty) -> lock -> insert -> unlock -> signal(full)`.
- Consumer: `wait(full) -> lock -> remove -> unlock -> signal(empty)`.
- The producer makes 4 items and the consumer takes 4, so the demo ends.

## 2. Readers-Writers

- `read_count` is protected by `read_count_lock`.
- The first reader locks `resource_lock`; the last reader releases it, so many
  readers can read together while writers are kept out.
- A writer holds `resource_lock`, which gives it exclusive access.
- Starvation note: this is reader-preference. If readers keep arriving, a writer
  could wait indefinitely. The finite demo cannot deadlock, but deadlock-free
  does not mean fair.

## 3. Dining Philosophers

- 5 philosophers, 5 fork `Lock`s.
- `waiter = Semaphore(4)` lets at most four philosophers try to pick up forks at
  once, so all five cannot hold one fork each (no circular wait, no deadlock).
- `try/finally` always releases both forks.

## Expected output

Line order for readers/writers and philosophers can change between runs because
of thread scheduling. That is normal. Success means every section finishes and
the last line is `PROGRAM 3 COMPLETED SUCCESSFULLY`.

## Viva questions

- **Why does the producer wait on `empty`?** It must not insert when no slot is free.
- **Why does the consumer wait on `full`?** It must not remove when nothing is stored.
- **Why `buffer_lock`?** It protects the shared buffer and index updates.
- **Why must a writer be exclusive?** It modifies shared data.
- **What is deadlock?** Threads wait forever for resources held by each other.
- **How is it prevented here?** The waiter semaphore admits at most four philosophers.
- **What is starvation?** A thread waits too long while others keep progressing.
