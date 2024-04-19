import concurrent.futures

items = []


def append_items():
    items.append("Spam")
    items.append("Eggs")
    items.append("Bacon")


def main():
    print(f"Running 4 threads...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(4):
            executor.submit(append_items)

    print("Items:", items)


if __name__ == "__main__":
    main()
