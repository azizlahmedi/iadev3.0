#!/usr/bin/env python
import argparse
import os
import sys

import delia_commons
from adl_codegen.adlcodegen import compile_file, compile_schema_file

DEBUG = True
STACK_SIZE = 2 ** 25


def deliac(args=None):
    if args is None:
        args = sys.argv[1:]
    sys.setrecursionlimit(10 ** 6)
    parser = argparse.ArgumentParser(prog='deliac')
    parser.add_argument('--version', action='version', version=delia_commons.__version__)
    parser.add_argument('-n', '--proc_name',
                        action='store',
                        dest='proc_name',
                        help='procedure name',
                        metavar='name')
    parser.add_argument('-s', '--schema_name',
                        action='store',
                        dest='schema_name',
                        help='schema name',
                        metavar='name')
    parser.add_argument('-p', '--project_path',
                        action='store',
                        dest='project_path',
                        help='project path',
                        metavar='path')
    parser.add_argument('-o', '--output_dir',
                        action='store',
                        dest='output_dir',
                        help='output_dir',
                        metavar='directory')
    parser.add_argument('-f', '--file_path',
                        action='store',
                        dest='file_path',
                        help='procedure file path',
                        metavar='path')
    args = parser.parse_args(args)

    if args.file_path is None and args.project_path is None:
        parser.error('Missing REQUIRED parameters: project path not given')

    if args.file_path is None and args.proc_name is None:
        parser.error('Missing REQUIRED parameters: procedure name not given')

    if args.output_dir is None:
        output_dir = os.environ.get('MAGNUM_MAGPY_DIRECTORY', None)
    else:
        output_dir = args.output_dir

    if args.project_path is not None:
        project_path = args.project_path
    else:
        assert (args.file_path.index('adl') > 0)
        project_path = args.file_path[:args.file_path.index('adl')]

    delia_commons.Context().initialize(project_path)

    if args.file_path is not None:
        proc_path = args.file_path
        if args.proc_name is None:
            proc_name = os.path.splitext(os.path.basename(proc_path))[0].replace('_', '.')
    else:
        proc_name = args.proc_name
        proc_path = delia_commons.DeliaFile(delia_commons.Context(), True, args.proc_name).path

    if output_dir is not None:
        output_path = os.path.join(output_dir, proc_name.replace('.', '_') + '.py')
    else:
        output_path = None

    if args.schema_name is None:
        schema_name = delia_commons.Context().schema_name
    else:
        schema_name = args.schema_name

    schema_path = delia_commons.DeliaFile(delia_commons.Context(), True, schema_name).path

    if DEBUG:
        print(
            "Compile project_path='{}' schema='{}' schema_path='{}' procedure='{}' procedure_path='{}' output_path='{}'".format(
                project_path, schema_name, schema_path, proc_name, proc_path, output_path))
        sys.stdout.flush()

    code = compile_file(proc_path, schema_tree=compile_schema_file(schema_path))

    if output_path is None:
        print(code)
    else:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(code)

    sys.exit(0)


if __name__ == '__main__':
    deliac()
