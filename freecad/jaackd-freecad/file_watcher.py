from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, callback, file_path):
        self.callback = callback
        self.file_path = file_path

    def on_modified(self, event):
        print(f"recieved on_modified for: {event.src_path}")
        if event.src_path == self.file_path:
            self.callback(event)

class FileWatcher:
    def __init__(self, file_path, callback):
        self.file_path = file_path
        self.event_handler = FileEventHandler(callback, file_path)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, path=self.file_path, recursive=False)
        self.observer.start()
        print(f"Started watching file: {self.file_path}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print(f"Stopped watching file: {self.file_path}")