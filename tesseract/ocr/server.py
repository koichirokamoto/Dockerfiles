"""Simple OCR server."""

import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
from io import BytesIO
import json
import os
import shutil
import time

from PIL import Image

import ocr
import storage


class ServerConfig:

  def __init__(self, project_id, bucket):
    self.project_id = project_id
    self.bucket = bucket

  @classmethod
  def from_json(cls, dct):
    return ServerConfig(dct['project_id'], dct['bucket'])


class Handler(BaseHTTPRequestHandler):

  def do_GET(self):
    index = 'index.html'
    f = open(index, 'rb')
    self.send_response(HTTPStatus.OK)
    self.send_header("Content-type", 'text/html;charset=utf8')
    fs = os.fstat(f.fileno())
    self.send_header("Content-Length", str(fs[6]))
    self.end_headers()
    shutil.copyfileobj(f, self.wfile)
    f.close()

  def do_POST(self):
    formData = cgi.FieldStorage(
        self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
    content = formData.getvalue('content')
    img = Image.open(BytesIO(content))
    base_name = str(int(time.time()))
    image_name = base_name + '.bmp'
    img.save(image_name)
    ocr_image = ocr.ocr(image_name, base_name)
    ocr_name = base_name + '.png'
    Image.fromarray(ocr_image).save(ocr_name)
    blob = storage.upload(
        CONFIG.project_id,
        CONFIG.buket,
        ocr_name,
        service_account_file='service_account.json')
    signed_url = storage.signed_url_for_png(blob)
    shutil.os.remove(image_name)
    shutil.os.remove(base_name + '.tsv')
    shutil.os.remove(ocr_name)
    self.send_response(HTTPStatus.OK)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    responseBody = json.dumps({'url': signed_url})

    self.wfile.write(responseBody.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Handler):
  server_address = ('0.0.0.0', 8080)
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()


if __name__ == '__main__':
  with open('config.json') as f:
    CONFIG = json.load(f, object_hook=ServerConfig.from_json)
  run()
