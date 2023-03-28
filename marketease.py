#!/usr/bin/python3
import argparse
import os
import sys
import time
from subprocess import DEVNULL, Popen
from inspect import getsourcefile

DIRECTORY = '~/Documents/EPHEC/TFE/TFE'
parser = argparse.ArgumentParser('marketease')


if __name__ == '__main__':
    parser.add_argument('-p', '--project', help='Name of project to use with docker-compose.', default='marketease')
    parser.add_argument('action', choices=['up', 'restart', 'recreate', 'build', 'down', 'exec', 'logs', 'test', 'start'], help='Action to perform on the docker-compose project.')
    parser.add_argument('service', help='Service to perform action on.', nargs='*')
    parser.add_argument('-prod', '--production', help='Enable production mode.', action='store_true')
    parser.add_argument('-nc', '--no-cache', help='Launch command without cache.', action='store_true')

    args = parser.parse_args()
    arguments = ['docker-compose', '-f', f'{DIRECTORY}/docker-compose{"-production" if args.production else ""}.yml', '-p', args.project]
    services = ' '.join(args.service) if args.service else ''

    if args.action == 'up':
        arguments.extend(['up', '-d'])

    elif args.action == 'recreate':
        arguments.extend(['up', '--force-recreate', '-d'])

    elif args.action in ['down', 'build', 'exec', 'restart', 'start']:
        arguments.extend([args.action])

    elif args.action == 'logs':
        arguments.extend(['logs', '-ft'])

    elif args.action == 'test':
        args.project = f'{args.project}-tests'
        print(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} up -d {services}')
        os.system(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} up -d {services}')
        print(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} logs -ft {services}')
        os.system(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} logs -ft {services}')
        print(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} down {services}')
        os.system(f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project} down')
        exit()

    arguments.extend([f'{"--no-cache" if args.no_cache else ""}', services])
    print(' '.join(arguments))
    sys.exit(os.system(' '.join(arguments)))
