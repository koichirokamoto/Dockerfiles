"""OCR."""

import codecs
import os
import shutil
import subprocess

import cv2

LANG = 'eng+jpn'


def ocr(file, output):
  command = [
      'tesseract', file, output, '--oem', '1', '-l', LANG, '-c',
      'tessedit_create_tsv=1'
  ]

  proc = subprocess.Popen(
      command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  errors = proc.stdout.read()
  code = proc.wait()
  if code == 1:
    print('Error:', errors)
    exit(1)

  output_file_name = output + '.tsv'
  image = cv2.imread(file)
  n = 0
  with codecs.open(output_file_name, encoding='utf8') as f:
    l, t = 0, 0
    pl, pt, pw, ph = 0, 0, 0, 0
    word = ''
    while True:
      n += 1
      line = f.readline()
      if n == 1:
        continue
      elif line.strip() == '':
        break
      tsv = line.split('\t')
      left, top, width, height, text = int(tsv[6]), int(tsv[7]), int(
          tsv[8]), int(tsv[9]), tsv[11]
      text = text.strip()
      word += text
      if text == '':
        if word != '':
          cv2.rectangle(image, (l, t), (pl + pw, pt + ph), (0, 255, 0), 2)
          # reset text and point.
          l, t = 0, 0
          pl, pt, pw, ph = 0, 0, 0, 0
          word = ''
        continue

      if l == 0:
        l = left
      if t == 0:
        t = top
      pl = left
      pt = top
      pw = width
      ph = height

  return image
