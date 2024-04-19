import sys
import threading


def primes(start, end):
    # Special cases for 0 and 1
    if start <= 1:
        start = 2

    count = 0
    first_prime = None
    last_prime = None

    for num in range(start, end + 1):
        if num > 1:
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    break
            else:
                count += 1
                if first_prime is None:
                    first_prime = num
                last_prime = num

    return count, first_prime, last_prime


def lots_of_primes(thread_number):
    start, end = 1_000_000, 1_500_000
    count, first_prime, last_prime = primes(start, end)
    print(
        f"Thread #{thread_number}: "
        f"{count} primes between 500k and 1 million,"
        f" first: {first_prime}, last: {last_prime}"
    )


def main():
    thread_count = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    print(f"Running {thread_count} thread(s)...")

    threads = []
    for thread_num in range(thread_count):
        thread = threading.Thread(target=lots_of_primes, args=(thread_num,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # # Same code but with concurrent.futures:
    # import concurrent.futures
    #
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for thread_num in range(thread_count):
    #         executor.submit(lots_of_primes, thread_num)


if __name__ == "__main__":
    main()
