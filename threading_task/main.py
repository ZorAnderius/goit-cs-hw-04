import re
import logging
from pathlib import Path
from threading import Thread, RLock


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

files = [parent_dir / "text1.txt", parent_dir / "text2.txt", parent_dir / "text3.txt"]

def search_keywords(filename, keywords, results, lock):
    matches = {}
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            match = re.findall(keyword, content, re.IGNORECASE)
            for word in match:
                if word not in matches:
                    matches[word] = [filename]
    with lock:
        for key in matches:
            if key in results:
                results[key].append(*matches[key])
            else:
                results[key] = matches[key]
        


def process_files_with_threads(files, keywords):
    results = {}
    lock = RLock()
    threads = []
    for file in files:
        thread = Thread(target=search_keywords, args=(file, keywords, results, lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    return results

def thread_func():
    keywords = ["Python", "програмування", "всі"]

    results = process_files_with_threads(files, keywords)

    [logging.info(f"{key} : {values}") for key, values in results.items()]


if __name__ == "__main__":
    thread_func()