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
    matches = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        for keyword in keywords:
            matches.extend(re.findall(keyword, content, re.IGNORECASE))
    with lock:
        results.append(matches)


def process_files_with_threads(files, keywords):
    results = []
    lock = RLock()
    threads = []
    for file in files:
        thread = Thread(target=search_keywords, args=(file, keywords, results, lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results


def count_matches(results):
    element_counts = {}
    count = 0
    for matches in results:
        if matches in element_counts:
            element_counts[matches] += 1
        else:
            element_counts[matches] = 1
        count += 1
    return element_counts


if __name__ == "__main__":
    keywords = ["Python", "програмування", "всі"]

    results = process_files_with_threads(files, keywords)

    for file, matches in zip(files, results):
        logging.info(f"File: {file}")
        match = count_matches(matches)
        [logging.info(f"{key} : {value}") for key, value in match.items()]
