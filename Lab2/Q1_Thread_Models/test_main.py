import contextlib
import importlib.util
import io
from pathlib import Path
import threading
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("thread_demo", Path(__file__).with_name("main.py"))
demo = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()) as import_output:
    spec.loader.exec_module(demo)


class ThreadDemoTests(unittest.TestCase):
    def test_import_does_not_run_workload(self):
        self.assertEqual(import_output.getvalue(), "")

    def test_baseline_uses_same_tasks_on_main_thread(self):
        calls = []
        with patch.object(demo, "do_task", side_effect=lambda *args: calls.append(
            (args, threading.get_ident())
        )), contextlib.redirect_stdout(io.StringIO()):
            elapsed = demo.single_threaded_demo()
        self.assertEqual(calls, [(task, threading.get_ident()) for task in demo.TASKS])
        self.assertGreaterEqual(elapsed, 0)

    def test_workers_overlap_and_finish_before_return(self):
        barrier = threading.Barrier(len(demo.TASKS))
        completed = []
        workers = []
        lock = threading.Lock()

        def worker(*task):
            with lock:
                workers.append(threading.current_thread())
            barrier.wait(timeout=3)
            with lock:
                completed.append(task)

        with patch.object(demo, "do_task", side_effect=worker), contextlib.redirect_stdout(io.StringIO()):
            elapsed = demo.multithreaded_demo()
        self.assertCountEqual(completed, demo.TASKS)
        self.assertEqual(len({thread.ident for thread in workers}), len(demo.TASKS))
        self.assertTrue(all(not thread.is_alive() for thread in workers))
        self.assertGreaterEqual(elapsed, 0)


if __name__ == "__main__":
    unittest.main()
