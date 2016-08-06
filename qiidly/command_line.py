# -*- coding: utf-8 -*-
"""dummy docstring."""
import argparse
from qiidly.main import Qiidly


def _arg_parser():
    parser = argparse.ArgumentParser(description='qiidly: Sync following tag feeds at Qiita to Feedly.')
    parser.add_argument('-q', '--qiita-token',
                        required=True,
                        help='Qiita access token')
    parser.add_argument('-f', '--feedly-token',
                        required=True,
                        help='Feedly developer access token')
    return parser


# http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def _query_yes_no(question, default=None):
    valid = {'yes': True, 'y': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == "yes":
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError("invalid default answer: '{default}'".format(default=default))

    while True:
        print(question + prompt, end='')
        choice = input().lower()
        if choice == '' and default is not None:
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'y' or 'n'.")


def main():
    """dummy."""
    args = _arg_parser().parse_args()
    q = Qiidly(args.qiita_token, args.feedly_token)

    if q.up_to_date():
        print('Already up-to-date.')
        exit(0)
    q.print_todo()
    # sync to Feedly
    print('')
    if not _query_yes_no('Sync following tag feeds at Qiita to Feedly?', default=None):
        print('Did nothing.')
        exit(0)
    q.sync()
    print('Done!')


if __name__ == '__main__':
    main()
