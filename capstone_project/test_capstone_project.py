import os
import json
from capstone_project import data_types, data_schema_values, creating_file,\
    main
import pytest
from unittest import TestCase
import tempfile
import ast

data_types_correct_product = [
    ['./files', 3, 'super_name', 'count', "{\"name\": \"str:\"}", 10, True, 3],
    ['files', 3, 'super_name', 'random', "{\"name\": \"str:\"}", 10, True, 2],
    [f'{os.getcwd()}/files', 10, '17', 'uuid', "{\"name\": \"str:\"}", 10,
     True, 4],
    ['files', 3, 'super_name', 'count', "{\"name\": \"str:\"}", 10, True, 4]
]


@pytest.mark.parametrize('path_to_save_files, files_count, file_name, '
                         'file_prefix, data_schema, data_lines, clear_path, '
                         'processes_number', data_types_correct_product)
def test_data_types_correct(path_to_save_files, files_count, file_name,
                            file_prefix, data_schema, data_lines, clear_path,
                            processes_number):
    data_schema_loaded = json.loads(data_schema)

    func_result = data_types(path_to_save_files, files_count, file_name,
                             file_prefix, data_schema, data_lines, clear_path,
                             processes_number)
    assert func_result == (path_to_save_files, files_count, file_name,
                           file_prefix, data_schema_loaded, data_lines,
                           processes_number)


# my tests with logging catching
class LogCatcherDataTypes(TestCase):
    def test_zero_files_count(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 0, 'super_name', 'count',
                           "{\"name\": \"str:\"}", 10, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "When files_count is "
                                                      "equal to 0 every data "
                                                      "will be printed to the "
                                                      "console")
        self.assertEqual(sys.exception.code, 1)

    def test_wrong_file_prefix(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'different',
                           "{\"name\": \"str:\"}", 10, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "file_prefix has to be "
                                                      "'count', 'random' or "
                                                      "'uuid'")
        self.assertEqual(sys.exception.code, 1)

    def test_data_lines_too_small(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'count',
                           "{\"name\": \"str:\"}", -5, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "data_lines has to be a "
                                                      "positive integer")
        self.assertEqual(sys.exception.code, 1)

    def test_data_lines_equal_0(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'count',
                           "{\"name\": \"str:\"}", 0, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "data_lines has to be a "
                                                      "positive integer")
        self.assertEqual(sys.exception.code, 1)

    def test_processes_number_negative(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'count',
                           "{\"name\": \"str:\"}", 10, True, -1)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "processes_number has to"
                                                      " be a positive integer")
        self.assertEqual(sys.exception.code, 1)

    def test_processes_number_equal_0(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'count',
                           "{\"name\": \"str:\"}", 10, True, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "processes_number has to"
                                                      " be a positive integer")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_not_dict(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('files', 3, 'super_name', 'count',
                           "{\"name\" \"str:\"}", 10, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect data "
                                                      "schema structure")
        self.assertEqual(sys.exception.code, 1)

    def test_path_not_directory(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_types('capstone_project.py', 3, 'super_name', 'count',
                           "{\"name\": \"str:\"}", 10, True, 4)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Given path exists and "
                                                      "it's not a directory")
        self.assertEqual(sys.exception.code, 1)

    def test_processes_number_cpu_count(self):
        with self.assertLogs() as log:
            data_types('files', 3, 'super_name', 'count',
                       "{\"name\": \"str:\"}", 10, True, 32)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "processes_number is "
                                                      "greater than the number"
                                                      " of system CPUs. Value "
                                                      "replaced with number of"
                                                      " system CPUs.")


data_schema_values_correct_product = [
    {'date': 'timestamp:', 'name': 'str:rand', 'type':
        '["client", "partner", "government"]', 'age': 'int:rand(1, 90)'},
    {'date': 'timestamp', 'name': 'str:', 'type':
        '["client", "partner", "government"]', 'age': 'int:rand'},
    {'name': 'str:bike', 'type': '["client", "partner", "government"]',
     'age': 'int:'}
]


@pytest.mark.parametrize('data_schema_string',
                         data_schema_values_correct_product)
def test_data_schema_values_correct(data_schema_string):
    assert type(data_schema_values(data_schema_string, 0)) != {}


class LogCatcherDataSchemaValues(TestCase):

    def test_data_schema_values_missed_type(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'name': 'str:rand', 'age': '17'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect schema")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_values_missed_value(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'name': 'str:', 'age': 'int'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect schema")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_values_wrong_type(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'name': 'boolean:True'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "The type should be "
                                                      "int, str or timestamp")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_values_value_after_timestamp(self):
        with self.assertLogs() as log:
            data_schema_values({'name': 'timestamp:today'}, 0)
        self.assertEqual(len(log.records), 2)
        self.assertEqual(log.records[0].getMessage(), "In timestamp type all "
                                                      "values after ':' "
                                                      "are ignored")
        self.assertEqual(log.records[1].getMessage(), "Continuing...")

    def test_data_schema_values_str_as_rand_int(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'id': 'str:rand(1,19)'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect type: integer"
                                                      " variable can't be "
                                                      "interpreted as string")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_values_str_as_int(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'id': 'int:dog'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect type: that "
                                                      "variable can't be "
                                                      "interpreted as a "
                                                      "integer")
        self.assertEqual(sys.exception.code, 1)

    def test_data_schema_values_int_as_str(self):
        with self.assertLogs() as log:
            with self.assertRaises(SystemExit) as sys:
                data_schema_values({'id': 'str:17'}, 0)
        self.assertEqual(len(log.records), 1)
        self.assertEqual(log.records[0].getMessage(), "Incorrect type: that "
                                                      "variable can't be "
                                                      "interpreted as a "
                                                      "string")
        self.assertEqual(sys.exception.code, 1)


def file_reading_ops():
    creating_file('files', 'super_file', 'count', {'date': 'timestamp:',
                                                   'name': 'str:rand',
                                                   'type': '["client", '
                                                           '"partner", '
                                                           '"government"]',
                                                   'age': 'int:rand(1, 90)'},
                  10, 0)
    files_tab = []

    try:
        with open(f'files/super_file_1.jsonl') as f:
            content = f.read().split('\n')
            for line in content:
                if len(line) != 0:
                    files_tab.append(line)

    except FileNotFoundError:
        print('message')

    return files_tab


@pytest.fixture(scope='session')
def generate_writing_ops():
    with tempfile.TemporaryDirectory() as test_file:
        test_file_name = os.path.join(test_file, 'test_file.jsonl')
        with open(test_file_name, 'w+') as fh:
            fh.write(str(file_reading_ops()))
            fh.seek(0)
            return ast.literal_eval(fh.read())


def test_len_of_tempfile(generate_writing_ops):
    print(generate_writing_ops)
    assert len(generate_writing_ops) == 10


def test_content_of_tempfile(generate_writing_ops):
    for row in generate_writing_ops:
        assert list(ast.literal_eval(row).keys()) == ['date', 'name', 'type',
                                                      'age']


def test_clear_path_true_and_processes_number():
    main(*data_types('files', 4, 'super_file', 'count',
                     "{\"date\": \"timestamp:\",\"name\": \"str:rand\","
                     "\"type\":\"['client', 'partner', 'government']\","
                     "\"age\": \"int:rand(1, 90)\"}",
         10, True, 4))

    assert len(os.listdir('files')) == 4

    main(*data_types('files', 3, 'super_file', 'count',
                     "{\"date\": \"timestamp:\",\"name\": \"str:rand\","
                     "\"type\":\"['client', 'partner', 'government']\","
                     "\"age\": \"int:rand(1, 90)\"}", 10, True, 4))

    assert len(os.listdir('files')) == 3


def test_clear_path_false_and_processes_number():
    main(*data_types('files', 4, 'super_file', 'count',
                     "{\"date\": \"timestamp:\",\"name\": "
                     "\"str:rand\",\"type\": \"['client', 'partner', "
                     "'government']\",\"age\": \"int:rand(1, 90)\"}",
                     10, True, 4))

    assert len(os.listdir('files')) == 4

    main(*data_types('files', 3, 'super_file', 'count',
                     "{\"date\": \"timestamp:\",\"name\": \"str:rand\","
                     "\"type\": \"['client', 'partner', 'government']\","
                     "\"age\": \"int:rand(1, 90)\"}", 10, 'False', 4))

    assert len(os.listdir('files')) == 4
