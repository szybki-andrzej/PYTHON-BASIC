"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import pytest
import tempfile
import os


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


generated_words = generate_words()

try:
    with open('files/file1.txt', mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(generated_words))

except FileNotFoundError:
    print('message')

try:
    with open('files/file2.txt', mode='w', encoding='CP1252') as f:
        f.write(','.join(reversed(generated_words)))

except FileNotFoundError:
    print('message')


@pytest.fixture(scope='session')
def file1_mock_generation():
    with tempfile.TemporaryDirectory() as test_file:
        test_file_name = os.path.join(test_file, 'file1.txt')
        with open(test_file_name, 'w+', encoding='UTF-8') as fh:
            fh.write('\n'.join(generated_words))
            fh.seek(0)
            return fh.read()


@pytest.fixture(scope='session')
def file2_mock_generation():
    with tempfile.TemporaryDirectory() as test_file:
        test_file_name = os.path.join(test_file, 'file2.txt')
        with open(test_file_name, 'w+',  encoding='CP1252') as fh:
            fh.write(','.join(reversed(generated_words)))
            fh.seek(0)
            return fh.read()


def test_len_file1(file1_mock_generation):
    assert len(file1_mock_generation) != 0


def test_content_file1(file1_mock_generation):
    assert file1_mock_generation == '\n'.join(generated_words)


def test_len_file2(file2_mock_generation):
    assert len(file2_mock_generation) != 0


def test_content_file2(file2_mock_generation):
    assert file2_mock_generation == ','.join(reversed(generated_words))
