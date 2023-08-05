#!/usr/bin/env python
from typing import List
from nbuild import nbuild
from nbexec import nbexec
import argparse


def nbless(filenames: List[str],
           input_path: str = './',
           nbuild_name: str = 'unexecuted.ipynb',
           nbuild_path: str = './',
           nbexec_name: str = 'executed.ipynb',
           nbexec_path: str = './',
           kernel_name: str = 'python3') -> None:

    nbuild(filenames=filenames,
           input_path=input_path,
           output_name=nbuild_name,
           output_path=nbuild_path)

    print(f'Created {nbuild_name} in {nbuild_path}.')

    if any('.R' in name for name in filenames) and kernel_name != 'ir':
        print('For nbless or nbexec to execute a notebook containing R code, '
              'you must first select the R kernel (IRkernel) '
              'by passing "ir" as the kernel_name argument.')
    else:
        nbexec(input_name=nbuild_name,
               input_path=nbuild_path,
               output_name=nbexec_name,
               output_path=nbexec_path,
               kernel_name=kernel_name)
        print(f'Created {nbexec_name} in {nbexec_path} from {nbuild_name} '
              f'using the {kernel_name} kernel.')


def command_line_runner():

    parser = argparse.ArgumentParser(
          description='Create and execute a notebook from the command line.')

    parser.add_argument('names', nargs='+', help='A series of filenames.')

    parser.add_argument('--input_path', '-i', default='./',
                        help='The filepath to the source files.')

    parser.add_argument('--unexecuted', '-u', default='unexecuted.ipynb',
                        help='The filename of the unexecuted output notebook.')

    parser.add_argument('--executed', '-e', default='executed.ipynb',
                        help='The filename of the executed output notebook.')

    parser.add_argument('--output_path', '-o', default='./',
                        help='The filepath where the notebooks are saved.')

    parser.add_argument('--kernel', '-k', default='python3',
                        help='The Jupyter kernel used to execute the notebook.')

    args = parser.parse_args()
    names = args.names
    in_path = args.input_path
    raw_name = args.unexecuted
    out_path = args.output_path
    out_name = args.executed
    kernel = args.kernel

    nbless(filenames=names,
           input_path=in_path,
           nbuild_name=raw_name,
           nbuild_path=out_path,
           nbexec_name=out_name,
           nbexec_path=out_path,
           kernel_name=kernel)


if __name__ == "__main__":
    command_line_runner()
