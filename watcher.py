import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import WATCH_FOLDER, VALID_EXTENSIONS

QUEUE_FILE = "queue.txt"

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        
        filename = os.path.basename(event.src_path)
        if not any(filename.lower().endswith(ext) for ext in VALID_EXTENSIONS): return
        if filename.startswith((".", "~$")): return

        print(f"🎥 Detectado: {filename}")
        
        with open(QUEUE_FILE, "a", encoding="utf-8") as f:
            f.write(filename + "\n")
        print(f"📥 {filename} adicionado à fila.")

if __name__ == "__main__":
    print(f"👀 Monitorando: {WATCH_FOLDER}")
    observer = Observer()
    observer.schedule(VideoHandler(), WATCH_FOLDER, recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()