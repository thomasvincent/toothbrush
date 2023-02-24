import os
import subprocess

from sniffer.api import file_validator, runnable, select_runnable

try:
    from pync import Notifier
except ImportError:
    notify = None
else:
    notify = Notifier.notify

WATCH_PATHS = ["toothbrush", "tests"]

class Options:
    group = int(time.time())
    show_coverage = False
    rerun_args = None

    targets = [
        (["make", "test-unit", "DISABLE_COVERAGE=true"], "Unit Tests", True),
        (["make", "test-all"], "Integration Tests", False),
        (["make", "check"], "Static Analysis", True),
        (["make", "docs"], None, True),
    ]

@select_runnable("run_targets")
@file_validator
def python_files(filename):
    return filename.endswith(".py")

@select_runnable("run_targets")
@file_validator
def html_files(filename):
    return filename.split(".")[-1] in ["html", "css", "js"]

@runnable
def run_targets(*args):
    """Run the specified targets."""
    Options.show_coverage = "coverage" in args

    num_failures = 0
    for count, (command, title, retry) in enumerate(Options.targets, start=1):
        success = run_command(command, title, retry)
        if not success:
            num_failures = count
            break

    if num_failures == 0:
        show_notification("✅ " * count, "All Targets")
        show_coverage()
        return True
    else:
        show_notification("✅ " * (num_failures - 1) + "❌", Options.targets[num_failures - 1][1])
        return False

def run_command(command, title, retry):
    """Run a command and display the result."""
    if Options.rerun_args:
        command, title, retry = Options.rerun_args
        Options.rerun_args = None
        success = run_command(command, title, retry)
        if not success:
            return False

    print(f"Running command: {' '.join(command)}")
    failure = subprocess.call(command)

    if failure and retry:
        Options.rerun_args = command, title, retry

    return not failure

def show_notification(message, title):
    """Show a user notification."""
    if notify and title:
        notify(message, title=title, group=Options.group)

def show_coverage():
    """Launch the coverage report."""
    if Options.show_coverage:
        subprocess.call(["make", "read-coverage"])

    Options.show_coverage = False
