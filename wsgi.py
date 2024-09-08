from board import create_app
from waitress import serve
import argparse

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='starts the server.')
    parser.add_argument('-d', '--debug', action='store_true', help='Runs the server in debug mode')
    args = parser.parse_args()
    if args.debug is None:
        serve(app, host='0.0.0.0', port=3000)       
    else: 
        app.run(host='0.0.0.0', port=3000, debug=True)