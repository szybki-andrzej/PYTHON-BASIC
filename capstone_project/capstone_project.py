import argparse
import json
import os
import random
import uuid
import time
import re
import logging
import sys
import ast
import multiprocessing
import configparser


def data_schema_values(schema, count):
    """Function that create a content of the line in file based on a
    given schema"""

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(message)s')
    values_tab = schema.items()
    return_values = {}
    for item in values_tab:
        main_val = False
        value_schema = item[1].split(':')
        if len(value_schema) == 1:
            if re.match(r"\[(.*)\]", value_schema[0]):
                # it was said, that user has to deliver the type of the
                # choice, but in some examples it wasn't like that, so
                # I decided to use an option without it to give a
                # chance to choose from different types variables
                main_val = random.choice(ast.literal_eval(value_schema[0]))
            elif value_schema[0] == 'timestamp':
                main_val = time.time()
            else:
                logging.error("Incorrect schema")
                sys.exit(1)

        elif len(value_schema) == 2:
            key = value_schema[0]
            value = value_schema[1]

            if key not in ('int', 'str', 'timestamp'):
                logging.error("The type should be int, str or timestamp")
                sys.exit(1)

            elif key == 'timestamp':
                main_val = time.time()
                if count == 0:
                    # it is said that I have to ignore all the values
                    # after timestamp and in the same time writing an
                    # error if the type is wrong. I decided to ignore
                    # it every time
                    logging.warning("In timestamp type all values after ':'"
                                    " are ignored")
                    logging.info('Continuing...')

            elif value == 'rand':
                if key == 'int':
                    main_val = random.randint(0, 10000)
                elif key == 'str':
                    main_val = str(uuid.uuid4())

            elif re.match(r"(rand)\([-+]?[0-9]+,\s?[-+]?[0-9]+\)", value):
                if key == 'str':
                    logging.error("Incorrect type: integer variable can't be"
                                  " interpreted as string")
                    sys.exit(1)
                elif key == 'int':
                    a, b = value.split(',')
                    main_val = random.randint(int(a[5:]), int(b[:-1]))

            elif value == '':
                if key == 'int':
                    main_val = None
                elif key == 'str':
                    main_val = ''

            elif value.isalpha():
                if key == 'str':
                    main_val = value

                elif key == 'int':
                    logging.error("Incorrect type: that variable can't be"
                                  " interpreted as a integer")
                    sys.exit(1)

            elif value.isdigit():
                if key == 'int':
                    main_val = value
                elif key == 'str':
                    logging.error("Incorrect type: that variable can't be"
                                  " interpreted as a string")
                    sys.exit(1)
            else:
                logging.error('Incorrect type in schema')
                sys.exit(1)

        else:
            break

        return_values[item[0]] = main_val

    return return_values


def creating_file(path_to_save_files, file_name, file_prefix, data_schema,
                  data_lines, i):
    """Function that creates a file on a given arguments."""

    full_file_name = file_name
    if file_prefix == 'count':
        full_file_name = f'{file_name}_{i+1}'
    elif file_prefix == 'random':
        full_file_name = f'{file_name}_{random.randint(1, 10000)}'
    elif file_prefix == 'uuid':
        full_file_name = f'{file_name}_{uuid.uuid4()}'

    full_path = f'{path_to_save_files}/{full_file_name}.jsonl'

    with open(full_path, 'w') as f:
        for j in range(data_lines):
            content = data_schema_values(data_schema, i + j)
            json.dump(content, f)
            f.write('\n')


def data_types(path_to_save_files, files_count, file_name, file_prefix,
               data_schema, data_lines, clear_path, processes_number):
    """Function that checks if arguments are implemented correct."""

    # data_schema
    try:
        data_schema = json.loads(data_schema)
    except json.JSONDecodeError:
        logging.error('Incorrect data schema structure')
        sys.exit(1)

    # files_count
    if files_count < 0:
        logging.error("files_count can't be smaller than 0")
        sys.exit(1)

    elif files_count == 0:
        logging.info("When files_count is equal to 0 every data will be "
                     "printed to the console")
        for j in range(int(data_lines)):
            print(data_schema_values(data_schema, j))
        sys.exit(1)

    # path_to_save_files
    if not os.path.exists(path_to_save_files):
        os.makedirs(path_to_save_files)
    elif not os.path.isdir(path_to_save_files):
        logging.error("Given path exists and it's not a directory")
        sys.exit(1)

    # data_lines
    if data_lines <= 0:
        logging.error('data_lines has to be a positive integer')
        sys.exit(1)

    # processes_number
    if processes_number <= 0:
        logging.error("processes_number has to be a positive integer")
        sys.exit(1)

    elif processes_number > os.cpu_count():
        logging.warning("processes_number is greater than the number of "
                        "system CPUs. Value replaced with number of "
                        "system CPUs.")
        processes_number = os.cpu_count()

    # file_prefix
    if file_prefix not in ['count', 'random', 'uuid']:
        logging.error("file_prefix has to be 'count', 'random' or 'uuid'")
        sys.exit(1)

    # clear_path
    if clear_path is True:
        # It was said to delete the file if the name was the same but
        # the file is overwrited anyway, and it doesn't deal with the
        # problem of additional files in the same
        # directory, so I decided to clear all the path
        [os.remove(f'{path_to_save_files}/{file}')
         for file in os.listdir(path_to_save_files)]

    return path_to_save_files, files_count, file_name, file_prefix, \
        data_schema, data_lines, processes_number


def arguments_parsing():
    """Function that parse the arguments and returns them."""

    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s:%(message)s")
    parser = argparse.ArgumentParser(
        description='Generates data based on the provided data schema',
        prog='Data generator')
    config = configparser.ConfigParser()

    config['DEFAULT'] = {'path_to_save_files': './files',
                         'files_count': 3,
                         'file_name': 'super_data',
                         'file_prefix': 'count',
                         'data_schema':
                             "{\"date\": \"timestamp:\",\"name\": "
                             "\"str:rand\",\"type\": \"['client', 'partner', "
                             "'government']\",\"age\": \"int:rand(1, 90)\"}",
                         'data_lines': 1000,
                         'clear_path': True,
                         'processes_number': 1}

    with open('default_values.ini', 'w') as configfile:
        config.write(configfile)

    config.read('default_values.ini')
    con_def = config['DEFAULT']

    parser.add_argument('--path_to_save_files',
                        help="path where all files need to be save, "
                             "with './files' as default value",
                        default=con_def['path_to_save_files'], type=str)
    parser.add_argument('--files_count',
                        help='number of json files to generate'
                             ' with 3 as default value',
                        default=con_def['files_count'], type=int)
    parser.add_argument('--file_name',
                        help="base file name, with 'super_data' "
                             "as default value", type=str,
                        default=con_def['file_name'])
    parser.add_argument('--file_prefix',
                        help='prefix for the file_name useful when is more '
                             'than 1 file, with consecutive numbers as '
                             'default value',
                        choices=['count', 'random', 'uuid'], type=str,
                        default=con_def['file_prefix'])

    parser.add_argument('--data_schema',
                        help='schema used for the data, with, '
                             '"{\"date\": \"timestamp:\",\"name\": '
                             '\"str:rand\",\"type\": \"[\'client\', '
                             '\'partner\', \'government\']\",\"age\": '
                             '\"int:rand(1, 90)\"}"'
                             " as default", type=str,
                        default=con_def['data_schema'])
    parser.add_argument('--data_lines', help='count of lines for each file, '
                                             'with 1000 as default value',
                        default=con_def['data_lines'], type=int)
    parser.add_argument('--clear_path',
                        help="flag which when it's set on True delete all "
                             "files from the given directory before creating "
                             "new ones, with True as default",
                        default=con_def['clear_path'], type=bool)
    parser.add_argument('--processes_number',
                        help='number of processes used to create files, with '
                             '10 as default',
                        default=con_def['processes_number'], type=int)

    args = parser.parse_args()

    return args.path_to_save_files, args.files_count, args.file_name, \
        args.file_prefix, args.data_schema, args.data_lines, \
        args.clear_path, args.processes_number


def main(path_to_save_files, files_count, file_name, file_prefix, data_schema,
         data_lines, processes_number):
    """Main function that runs other functions using multiprocessing."""

    with multiprocessing.Pool(processes_number) as ex:
        logging.info('Started data generation')
        arguments = [(path_to_save_files, file_name,
                      file_prefix, data_schema, data_lines, i)
                     for i in range(files_count)]

        ex.starmap(creating_file, arguments)
        logging.info('Data generation finished')


if __name__ == '__main__':
    main(*data_types(*arguments_parsing()))
