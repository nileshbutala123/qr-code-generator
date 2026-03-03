#!/usr/bin/env python3
"""Simple HTTP server for requirements editor

Run: python requirements_server.py --port 8002 --dir .

Endpoints:
  GET /requirements/features.txt   -> serves the file
  POST /save                       -> saves body to requirements/features.txt (text/plain)
  Static files served from provided directory
"""
import argparse
import http.server
import socketserver
import urllib.parse
import os
import json

class ReqHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                target = os.path.join(self.directory, 'requirements', 'features.txt')
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, 'wb') as f:
                    f.write(body)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(port: int = 8002, directory: str = '.'):
    handler = ReqHandler
    os.chdir(directory)
    with socketserver.ThreadingTCPServer(('127.0.0.1', port), handler) as httpd:
        print(f"Serving {directory} at http://127.0.0.1:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down')
            httpd.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=8002)
    parser.add_argument('--dir', '-d', default='.')
    args = parser.parse_args()
    run(port=args.port, directory=args.dir)
