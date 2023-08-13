#!/usr/bin/python3
import argparse
import os
import sys
import time
from subprocess import DEVNULL, Popen
from inspect import getsourcefile
from dotenv import load_dotenv
load_dotenv()


DIRECTORY = os.getenv("ROOT_DIRECTORY")
parser = argparse.ArgumentParser('marketease')


if __name__ == '__main__':
    parser.add_argument('-p', '--project', help='Name of project to use with docker-compose.', default='marketease')
    parser.add_argument('action', choices=['up', 'restart', 'recreate', 'build', 'down', 'exec', 'logs', 'test', 'start', 'ps'], help='Action to perform on the docker-compose project.')
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

    elif args.action == 'ps':
        arguments.extend(['ps', '-a'])

    elif args.action == 'test':
        args.project = f'{args.project}-tests'
        command = f'docker-compose -f {DIRECTORY}/docker-compose-tests.yml -p {args.project}'
        if 'build' in args.service:
            args.service.remove('build')
            services = ' '.join(args.service)
            print(f'[TEST] {command} build --no-cache {services}')
            os.system(f'{command} build --no-cache {services}')
        # Start the database
        print(f'[TEST] {command} up -d db')
        os.system(f'{command} up -d db')
        print(f'[TEST] {command} up -d {services}')
        os.system(f'{command} up -d {services}')
        print(f'[TEST] {command} logs -ft {services}')
        os.system(f'{command} logs -ft {services}')
        print(f'[TEST] {command} down')
        os.system(f'{command} down')
        exit()

    arguments.extend([f'{"--no-cache" if args.no_cache else ""}', services])
    print('[COMMAND]', ' '.join(arguments))
    sys.exit(os.system(' '.join(arguments)))
