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
    matches = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            matches.extend(re.findall(keyword, content, re.IGNORECASE))
    with lock:
        queue.put(matches)


def process_files_with_processes(files, keywords):
    results = []
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
        results.append(queue.get())

    return results


def count_matches(results):
    element_counts = {}
    count = 0
    for match in results:
        if match in element_counts:
            element_counts[match] += 1
        else:
            element_counts[match] = 1
        count += 1
    return element_counts


if __name__ == "__main__":
    keywords = ["Python", "програмування", "всі"]

    results = process_files_with_processes(files, keywords)

    for file, matches in zip(files, results):
        logging.info(f"File: {file}")
        match = count_matches(matches)
        [logging.info(f"{key} : {value}") for key, value in match.items()]
