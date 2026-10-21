# OS Lab — CSE AI/ML

Operating Systems lab assignments. Each question has a standalone `main.py`
directly inside its question folder, alongside its README.

## Progress

| Lab | Question | Program |
| --- | --- | --- |
| Lab1 | Q1 — System calls | [main.py](Lab1/Q1_System_Calls/main.py) |
| Lab1 | Q2 — FCFS and SJF | [main.py](Lab1/Q2_FCFS_SJF/main.py) |
| Lab1 | Q3 — Priority and Round Robin | [main.py](Lab1/Q3_Priority_Round_Robin/main.py) |
| Lab1 | Q4 — Metrics, threads and IPC | [main.py](Lab1/Q4_Metrics_Threads_IPC/main.py) |
| Lab2 | Q1 — Thread Creation, Models and Benefits | [main.py](Lab2/Q1_Thread_Models/main.py) · [Notes](Lab2/Q1_Thread_Models/README.md) |

Remaining Lab2 questions, Lab3, Lab4 and Capstone have not been added yet.

## Run

From the repository root:

```bash
python3 Lab1/Q1_System_Calls/main.py
python3 Lab1/Q2_FCFS_SJF/main.py
python3 Lab1/Q3_Priority_Round_Robin/main.py
python3 Lab1/Q4_Metrics_Threads_IPC/main.py
python3 Lab2/Q1_Thread_Models/main.py
```

Use Ubuntu/WSL for Lab1 Q1 (`fork`, `/dev/null` and `/proc`). Lab2 Q1 also
runs on Windows with `python` in place of `python3`. No external packages
are required.

Lab2 Q1 follows the classroom program with the practical's 2, 3 and 1 second
waits. Run its checks with:

```bash
python3 -m unittest discover -s Lab2/Q1_Thread_Models -p "test_*.py"
```

