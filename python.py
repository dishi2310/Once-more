import threading
import queue
import time
import random
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# Fibonacci with memoization
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Producer-Consumer with threading and queue
class Producer(threading.Thread):
    def __init__(self, q, count):
        super().__init__()
        self.q = q
        self.count = count

    def run(self):
        for _ in range(self.count):
            num = random.randint(1, 30)
            print(f"Producer produced: {num}")
            self.q.put(num)
            time.sleep(random.uniform(0.1, 0.5))
        self.q.put(None)  # Sentinel

class Consumer(threading.Thread):
    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            num = self.q.get()
            if num is None:
                self.q.put(None)
                break
            fib = fibonacci(num)
            print(f"Consumer consumed: {num}, Fibonacci: {fib}")
            time.sleep(random.uniform(0.1, 0.5))

# Parallel computation of factorials
def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

def compute_factorials(numbers):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(factorial, numbers))
    return results

def main():
    q = queue.Queue()
    producer = Producer(q, 10)
    consumer = Consumer(q)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    numbers = [random.randint(5, 15) for _ in range(8)]
    print(f"Numbers for factorial: {numbers}")
    results = compute_factorials(numbers)
    for n, res in zip(numbers, results):
        print(f"Factorial of {n} is {res}")

if __name__ == "__main__":
    main()