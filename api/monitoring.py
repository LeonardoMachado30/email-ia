import psutil
import os
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)


def monitor_resource_usage(interval=5):
    """
    Monitora o uso de CPU e RAM do processo atual em background.
    - interval: segundos entre cada leitura
    """
    process = psutil.Process(os.getpid())

    def _monitor():
        logging.info(f"🔎 Monitorando recursos (PID {process.pid}) a cada {interval}s")
        while True:
            mem_info = process.memory_info()
            rss = mem_info.rss / (1024 * 1024)  # RAM usada em MB
            cpu = process.cpu_percent(interval=0.1)  # Leitura rápida
            logging.info(f"RAM: {rss:.2f} MB | CPU: {cpu:.2f}%")
            time.sleep(interval)

    thread = threading.Thread(target=_monitor, daemon=True)
    thread.start()
