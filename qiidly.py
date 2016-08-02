# -*- coding: utf-8 -*-
"""dummy docstring."""
import argparse
import qiidly.main


def _arg_parser():
    parser = argparse.ArgumentParser(description='qiidly: Qiita to Feedly.')
    parser.add_argument('-q', '--qiita-token',
                        required=True,
                        help='Qiita access token')
    parser.add_argument('-f', '--feedly-token',
                        required=True,
                        help='Feedly developer access token')
    return parser


if __name__ == '__main__':
    args = _arg_parser().parse_args()
    qiidly.main.sync(args.qiita_token, args.feedly_token)
