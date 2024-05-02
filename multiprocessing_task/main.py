import re
import logging
from pathlib import Path
from multiprocessing import Process, Queue, RLock

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

files = [parent_dir / "text1.txt", parent_dir / "text2.txt", parent_dir / "text3.txt"]

def search_keywords(filename, keywords, queue, lock):
    matches = {}
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            match = re.findall(keyword, content, re.IGNORECASE)
            for word in match:
                if word not in matches:
                    matches[word] = [filename]
    with lock:
        queue.put(matches)


def process_files_with_processes(files, keywords):
    results = {}
    queue = Queue()
    lock = RLock()
    processes = []
    for file in files:
        process = Process(target=search_keywords, args=(file, keywords, queue, lock))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    while not queue.empty():
        matches = queue.get()
        for key, value in  matches.items():
            if key in results:
                results[key].append(*value)
            else:
                results[key] = value

    return results

def multiprocessing_func():
    keywords = ["Python", "програмування", "всі"]

    results = process_files_with_processes(files, keywords)

    [logging.info(f"{key} : {values}") for key, values in results.items()]


if __name__ == "__main__":
    multiprocessing_func()
