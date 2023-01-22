import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move
from time import sleep
from os import scandir, rename
from os.path import splitext, exists, join


source_folder = "/Users/SamirA/Downloads"
destination_folder_sfx = "/Users/SamirA/Desktop/Sound"
destination_folder_music = "/Users/SamirA/Desktop/Sound/music"
destination_folder_video = "/Users/SamirA/Desktop/Videos Downloaded"
destination_folder_image = "/Users/SamirA/Desktop/Images Downloaded"
destination_folder_documents = "/Users/SamirA/Documents"


document_types = [".doc", ".docx", ".odt",
                  ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

video_types = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
               ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

image_types = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
               ".raw", ".arw", ".cr2", ".nrw",
               ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf",
               ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

audio_types = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]


def make_unique(destination, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(destination, entry, name):
    if exists(f"{destination}/{name}"):
        unique_name = make_unique(destination, name)
        oldName = join(destination, name)
        newName = join(destination, unique_name)
        rename(oldName, newName)
    move(entry, destination)


class MoverHandler(FileSystemEventHandler):
    # This function runs when there is a change in source_folder
    def on_modified(self, event):
        with scandir(source_folder) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in audio_types:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:
                    destination = destination_folder_sfx
                else:
                    destination = destination_folder_music
                move_file(destination, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        for video_type in video_types:
            if name.endswith(video_type) or name.endswith(video_type.upper()):
                move_file(destination_folder_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        for image_type in image_types:
            if name.endswith(image_type) or name.endswith(image_type.upper()):
                move_file(destination_folder_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        for documents_type in document_types:
            if name.endswith(documents_type) or name.endswith(documents_type.upper()):
                move_file(destination_folder_documents, entry, name)
                logging.info(f"Moved document file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_folder
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
