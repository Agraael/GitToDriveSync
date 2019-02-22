#!/usr/bin/env python3
import argparse
import subprocess
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8080


class GitDriveHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('Get request received')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_POST(self):
        print('Get request received')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/" + self.server.data:
            update_drive_repo(self.server.data)
        return


class HttpServer:
    def __init__(self, data: any):
        self.server = HTTPServer(('', 8080), GitDriveHandler)
        self.server.data = data
        print("set hook to http://kraken.localhost.run/" + self.server.data)
        self.server.serve_forever()

    def __del__(self):
        self.server.server_close()


def paser_init():
    parser = argparse.ArgumentParser(description="Service who connect every update to a git branch into a Google drive")
    subparsers = parser.add_subparsers(help='', dest='mode')
    subparsers.required = True

    parser_credential = subparsers.add_parser('credential', help='getting json credential for GoogleDrive')

    parser_init = subparsers.add_parser('init', help='init the drive directory and pull the repo')
    parser_init.add_argument('link', type=str, help='link of the git repository')
    parser_init.add_argument('--json', type=str, nargs=1, metavar='json', required=False, help='credential json file')

    parser_start = subparsers.add_parser('start', help='start the GitToDrive" service/server on the directory')
    parser_start.add_argument('dir', type=str, default='.', help='directory to start the git drive service')
    parser_start.add_argument('--hook', help='use web hook to update', action='store_true')

    parser_auto = subparsers.add_parser('auto', help='init and start the GitToDrive service/server')
    parser_auto.add_argument('link', type=str, help='link of the git repository')
    parser_auto.add_argument('--json', type=str, nargs=1, metavar='json', required=False, help='credential json file')
    parser_auto.add_argument('--hook', help='use web hook to update', action='store_true')

    return parser


def update_drive_repo(folder: str):
    print('pull !')
    subprocess.run(['git', 'pull'])
    subprocess.run(['drive push -no-prompt -ignore-conflict -destination ' + folder + ' *'], shell=True)


def check_and_push(repo: str):
    os.chdir(repo)
    folder = os.path.basename(os.getcwd())
    try:
        while 666:
            subprocess.run(['git', 'fetch'])
            upstream = subprocess.run(['echo ${1:-\'@{u}\'}'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
            local = subprocess.run(['echo $(git rev-parse @)'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
            remote = subprocess.run(['echo $(git rev-parse "' + upstream + '")'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]
            base = subprocess.run(['echo $(git merge-base @ "' + upstream + '")'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')[:-1]

            if local == base and local != remote:
                update_drive_repo(folder)
            else:
                print("nothing")
            time.sleep(10)
    except KeyboardInterrupt:
        print('^C received, shutting down the service')


def hook_and_push(repo: str):
    os.chdir(repo)
    folder = os.path.basename(os.getcwd())
    server = None
    try:
        server = HttpServer(data=repo)
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')


def init_git_drive(link: str, json: str):
    folder = os.path.splitext(os.path.basename(link))[0]
    if not os.path.exists(folder):
        ret = subprocess.run(['git', 'clone', link])
        if ret.returncode != 0:
            exit(1)
    else:
        print(folder + " directory allready exist")
    os.chdir(folder)
    if not json:
        subprocess.run(['drive', 'init'])
    else:
        subprocess.run(['mkdir .gd'], shell=True)
        subprocess.run(['cp ../' + json + ' .gd/credentials.json'], shell=True)
    subprocess.run(['drive', 'new', '-folder', folder])
    subprocess.run(['drive push -no-prompt -destination ' + folder + ' *'], shell=True)


def auto_git_drive(link: str, json: str, hook: bool):
    folder = os.path.splitext(os.path.basename(link))[0]
    init_git_drive(link, json)
    os.chdir("..")
    if not hook:
        check_and_push(folder)
    else:
        hook_and_push(folder)


if __name__ == "__main__":

    args = paser_init().parse_args()

    if args.mode == 'init':
        init_git_drive(args.link, args.json[0])
    elif args.mode == 'start':
        if not args.hook:
            check_and_push(args.dir)
        else:
            hook_and_push(args.dir)
    elif args.mode == 'auto':
        auto_git_drive(args.link, args.json[0], args.hook)
    elif args.mode == 'credential':
        subprocess.run(['drive', 'init'])
        subprocess.run(['cp .gd/credentials.json .'], shell=True)
        subprocess.run(['rm .gd/credentials.json'], shell=True)
        subprocess.run(['rmdir .gd'], shell=True)
    else:
        exit(1)
    exit(0)

