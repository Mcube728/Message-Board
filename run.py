#!/usr/bin/env python

import subprocess

if __name__ == '__main__':
    subprocess.run(["waitress-serve", "--port=8080", "wsgi:app"], check=True)