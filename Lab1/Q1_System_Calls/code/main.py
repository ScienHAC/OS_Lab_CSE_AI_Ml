import os


def show_process_info(label):
    print(f"{label} -> PID: {os.getpid()}, Parent PID: {os.getppid()}")


def fork_demo():
    pid = os.fork()

    if pid == 0:
        show_process_info("Child")
        os._exit(0)
    else:
        os.wait()
        show_process_info("Parent")


def exec_demo():
    pid = os.fork()

    if pid == 0:
        os.execlp("echo", "echo", "Hello from execlp, running inside the child")
    else:
        os.wait()


print("FORK DEMO")
fork_demo()

print("\nEXEC DEMO")
exec_demo()
