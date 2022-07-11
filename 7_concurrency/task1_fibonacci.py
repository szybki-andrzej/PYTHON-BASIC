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


def func1_one_thread(ordinal_numbers):  # first function is implemented normally to compare the speed
    """Function that writes the files with fibonacci results using one-thread methods"""

    for i in ordinal_numbers:
        with open(output_dir + f'/file {str(i)}.txt', 'w') as f:
            f.write(str(fib(i - 1)))


def func2(folder):
    """Function that reads the files and save results to csv file"""

    files = glob.glob(f'{folder}/*.txt')
    with open(result_file, 'w') as f:
        writer = csv.writer(f)
        for file in files:
            with open(file) as input:
                content = input.read()
                # I'm using file [14:-4] to get only the name of the file without path and extension
                writer.writerow((file[14:-4], content))


def func1_concurrent(array):
    """Function that uses concurrent programming to write and save files with fibonacci results"""

    with concurrent.futures.ProcessPoolExecutor(max_workers=10, mp_context=mp.get_context('fork')) as ex:
        ex.map(calc_and_write, array)


def calc_and_write(number):
    """Function to write the files useful for concurrent implementation"""

    with open(output_dir + f'/file {str(number)}.txt', 'w') as f:
        f.write(str(fib(number - 1)))


if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    array = [randint(1000, 100000) for _ in range(100)]

    # one-thread implementation
    start_one_thread = time.time()
    func1_one_thread(array)
    func2(output_dir)
    print(f'Normal implementation time: {time.time() - start_one_thread}')

    # implementation with concurrency
    start = time.time()
    func1_concurrent(array)
    func2(output_dir)
    print(f'Concurrent implementation time: {time.time() - start}')
