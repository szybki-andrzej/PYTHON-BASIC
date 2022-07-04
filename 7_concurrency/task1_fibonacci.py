import glob
import csv
import time
import multiprocessing as mp
import concurrent.futures
from random import randint
import os

output_dir = './output'
result_file = './output/result.csv'

# in my implementation I decided to increase speed by calculating fib function on a different cores for different
# numbers. Other options with saving on other threads and so on were slower because of the data sending between
# the cores


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def func1_normal(ordinal_numbers):  # first 2 functions are implemented normally to compare the speed
    for i in ordinal_numbers:
        with open(output_dir + f'/file {str(i)}.txt', 'w') as f:
            f.write(str(fib(i - 1)))


def func2_normal(folder):
    files = glob.glob(f'{folder}/*.txt')
    with open(result_file, 'w') as f:
        writer = csv.writer(f)
        for file in files:
            with open(file) as input:
                content = input.read()
                writer.writerow((file[14:-4], content))


def func1(array):
    with concurrent.futures.ProcessPoolExecutor(max_workers=10, mp_context=mp.get_context('fork')) as ex:
        ex.map(calc_and_write, array)


def calc_and_write(number):
    with open(output_dir + f'/file {str(number)}.txt', 'w') as f:
        f.write(str(fib(number - 1)))


if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    array = [randint(1000, 100000) for _ in range(100)]

    # normal implementation
    start_normal = time.time()
    func1_normal(array)
    func2_normal(output_dir)
    print(time.time() - start_normal)

    # implementation with concurrency
    start = time.time()
    func1(array)
    func2_normal(output_dir)
    print(time.time() - start)
