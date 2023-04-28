# -*- coding:utf8 -*-
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_name', type=str, required=True, help='file name of predicates')
    args = parser.parse_args()
    print(args)
    with open(args.file_name, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            print(line, end='')


if __name__ == '__main__':
    main()
