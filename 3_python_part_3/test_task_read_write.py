"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import os.path
import tempfile
import pytest


def file_reading_ops():
    files_tab = []

    for i in range(3):
        try:
            with open(os.path.join(os.path.dirname(__file__), f'files/file_{i+1}.txt')) as f:
                files_tab.append(f.read())

        except FileNotFoundError:
            print('message')

    return files_tab


@pytest.fixture(scope='session')
def generate_writing_ops():
    with tempfile.TemporaryDirectory() as test_file:
        test_file_name = os.path.join(test_file, 'result.txt')
        with open(test_file_name, 'w+') as fh:
            fh.write(str(file_reading_ops()))
            fh.seek(0)
            return fh.read()


def test_len_of_tempfile(generate_writing_ops):
    assert len(generate_writing_ops) != 0


def test_content_of_tempfile(generate_writing_ops):
    assert generate_writing_ops == "['23', '78', '3']"


