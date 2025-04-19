import shutil
import threading
import time
import psutil
import sys

from storm.common.services.logger import Logger
from storm.core.services.helpers import LogColorNoBold as LogColor


class SystemMonitor:
    """
    Monitors and logs system-level metrics like CPU, memory usage,
    and network traffic, updating a single line in the console periodically.
    """

    def __init__(self, interval: int = 3):
        self.logger = Logger(self.__class__.__name__)
        self.interval = interval
        self._shutdown = False
        self._paused = False
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)

        self._last_net = psutil.net_io_counters()
        self._last_time = time.time()

    @property
    def status(self) -> str:
        if self._shutdown:
            return "stopped"
        return "paused" if self._paused else "running"

    def start(self):
        self.logger.info("System monitor started.")
        self._thread.start()

    def shutdown(self):
        with self._lock:
            self._shutdown = True
        self.logger.info("System monitor stopping...")

    def stop(self):
        with self._lock:
            self._paused = True
        self.logger.info("System monitor paused.")

    def continue_(self):
        with self._lock:
            self._paused = False
        self.logger.info("System monitor resumed.")

    def _collect_metrics(self):
        process = psutil.Process()
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_used_mb = mem.used / 1024 / 1024
        mem_total_mb = mem.total / 1024 / 1024
        process_mem = process.memory_info().rss / 1024 / 1024
        proc_cpu = process.cpu_percent(interval=0)
        threads = process.num_threads()

        # Network traffic (delta)
        net_now = psutil.net_io_counters()
        time_now = time.time()
        elapsed = time_now - self._last_time or 1  # avoid div by zero

        net_in = (
            (net_now.bytes_recv - self._last_net.bytes_recv) / elapsed / 1024
        )  # KB/s
        net_out = (
            (net_now.bytes_sent - self._last_net.bytes_sent) / elapsed / 1024
        )  # KB/s

        self._last_net = net_now
        self._last_time = time_now

        return {
            "cpu": cpu_percent,
            "mem_used": mem_used_mb,
            "mem_total": mem_total_mb,
            "app_rss": process_mem,
            "proc_cpu": proc_cpu,
            "threads": threads,
            "network_in": net_in,
            "mem_percent": (mem_used_mb / mem_total_mb) * 100,
            "network_out": net_out,
            "pid": process.pid,
            "timestamp": time.strftime("%Y-%m-%d, %I:%M:%S %p"),
        }

    def _render_line(self, data: dict) -> str:
        return (
            f"{LogColor.HEADER}[Storm] {data['pid']} - {LogColor.RESET}"
            f"{LogColor.TIMESTAMP}{data['timestamp']}{LogColor.RESET} "
            f"{LogColor.INFO}INFO{LogColor.RESET} "
            f"{LogColor.NAME}[SystemMonitor]{LogColor.RESET} "
            f"CPU: {LogColor.INFO}{data['cpu']:.1f}%{LogColor.RESET} | "
            f"RAM: {LogColor.WARNING}{data['mem_used']:.1f}/{data['mem_total']:.1f} MB ({data['mem_percent']:.1f}%){LogColor.RESET} | "
            f"App RSS: {LogColor.DEBUG}{data['app_rss']:.1f} MB{LogColor.RESET} | "
            f"Threads: {LogColor.METRIC_LABEL}{data['threads']}{LogColor.RESET} | "
            f"Net: {LogColor.METRIC_LABEL}↓{data['network_in']:.1f} KB/s ↑{data['network_out']:.1f} KB/s{LogColor.RESET}"
        )

    def _monitor_loop(self):
        while True:
            with self._lock:
                if self._shutdown:
                    break
                if self._paused:
                    time.sleep(0.5)
                    continue

            data = self._collect_metrics()
            line = self._render_line(data)

            width = shutil.get_terminal_size((120, 20)).columns
            sys.stdout.write("\r" + " " * width + "\r")
            sys.stdout.write(line)
            sys.stdout.flush()

            time.sleep(self.interval)

        sys.stdout.write("\n")
