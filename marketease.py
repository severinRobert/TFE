#!/usr/bin/python3
import argparse
import os
import sys
import time
from subprocess import DEVNULL, Popen

DIRECTORY = '~/Documents/EPHEC/TFE/TFE'
parser = argparse.ArgumentParser('marketease')


if __name__ == '__main__':
    parser.add_argument('-p', '--project', help='Name of project to use with docker-compose.', default='marketease')
    parser.add_argument('action', choices=['up', 'restart', 'recreate', 'build', 'down', 'exec', 'logs', 'test', 'start'], help='Action to perform on the docker-compose project.')
    parser.add_argument('service', help='Service to perform action on.', nargs='*')
    parser.add_argument('-prod', '--production', help='Launch marketease to production.', action='store_true')

    args = parser.parse_args()
    arguments = ['docker-compose', '-f', f'{DIRECTORY}/docker-compose{"-production" if args.production else ""}.yml', '-p', args.project]

    if args.action == 'up':
        arguments.extend(['up', '-d'])

    elif args.action == 'recreate':
        arguments.extend(['up', '--force-recreate', '-d'])

    elif args.action in ['down', 'build', 'exec', 'restart', 'start']:
        arguments.extend([args.action])

    elif args.action == 'logs':
        arguments.extend(['logs', '-ft'])

    elif args.action == 'test':
        print('Test environment not implemented yet.')
        exit()

    arguments.extend([' '.join(args.service) if args.service else ''])
    print(' '.join(arguments))
    sys.exit(os.system(' '.join(arguments)))
