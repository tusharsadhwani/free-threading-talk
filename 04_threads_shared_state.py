import threading

items = []


def append_items():
    items.append("Spam")
    items.append("Eggs")
    items.append("Bacon")


def main():
    print(f"Running 4 threads...")

    threads = []
    for _ in range(4):
        thread = threading.Thread(target=append_items)
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Items:", items)


if __name__ == "__main__":
    main()
