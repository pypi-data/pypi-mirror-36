"""Resize and crop images to square, save as tiff."""
# -------------------------------------------------------------------#
# Tool to convert images
# Contact: mrinalhaloi11@gmail.com
# Copyright 2017, Mrinal Haloi
# -------------------------------------------------------------------#
from __future__ import division, print_function

import os
from PIL import Image, ImageFilter
from multiprocessing import cpu_count
from multiprocessing.pool import Pool

import click
import numpy as np

from tefla.da import data

N_PROC = cpu_count()

# pylint: disable=no-value-for-parameter


def convert(fname, target_size=512):
  img = Image.open(fname).convert('RGB')

  blurred = img.filter(ImageFilter.BLUR)
  ba = np.array(blurred)
  h, w, _ = ba.shape

  if w > 1.2 * h:
    left_max = ba[:, :w // 32, :].max(axis=(0, 1)).astype(int)
    right_max = ba[:, -w // 32:, :].max(axis=(0, 1)).astype(int)
    max_bg = np.maximum(left_max, right_max)

    foreground = (ba > max_bg + 10).astype(np.uint8)
    bbox = Image.fromarray(foreground).getbbox()

    if bbox is None:
      print('bbox none for {} (???)'.format(fname))
    else:
      left, upper, right, lower = bbox
      # if we selected less than 80% of the original
      # height, just crop the square
      if right - left < 0.8 * h or lower - upper < 0.8 * h:
        print('bbox too small for {}'.format(fname))
        bbox = None
  else:
    bbox = None

  if bbox is None:
    bbox = square_bbox(img, fname)

  cropped = img.crop(bbox)
  resized = cropped.resize([target_size, target_size])
  return resized


def convert_v2(fname, target_size=512):
  try:
    img = Image.open(fname).convert('RGB')
    resized = img.resize([target_size, target_size])
    return resized
  except Exception:
    print('Corrupted Image file %s' % fname)


def full_bbox(img, fname):
  print("full bbox conversion done for image: %s" % fname)
  w, h = img.size
  left = 0
  upper = 0
  right = w
  lower = h
  return (left, upper, right, lower)


def square_bbox(img, fname):
  print("square bbox conversion done for image: %s" % fname)
  w, h = img.size
  left = max((w - h) // 2, 0)
  upper = 0
  right = min(w - (w - h) // 2, w)
  lower = h
  return (left, upper, right, lower)


def convert_square(fname, target_size):
  img = Image.open(fname)
  bbox = square_bbox(img)
  cropped = img.crop(bbox)
  resized = cropped.resize([target_size, target_size])
  return resized


def get_convert_fname(fname, extension, directory, convert_directory):

  def replace_last(s, o, n):
    return "%s%s" % (s[0:s.rfind(o)], n)

  def replace_first(s, o, n):
    return s.replace(o, n, 1)

  if not directory.endswith("/"):
    directory += "/"

  if not convert_directory.endswith("/"):
    convert_directory += "/"

  extension0 = fname.split("/")[-1].split(".")[-1]
  # print("file: %s, old ext: %s, new ext: %s, old dir: %s, new dir: %s" % (
  #     fname, extension0, extension, directory, convert_directory))
  fname2 = replace_last(fname, extension0, extension)
  return replace_first(fname2, directory, convert_directory)


def process(args):
  fun, arg = args
  directory, convert_directory, fname, crop_size, extension = arg
  convert_fname = get_convert_fname(fname, extension, directory, convert_directory)
  if not os.path.exists(convert_fname):
    img = fun(fname, crop_size)
    try:
      save(img, convert_fname)
    except Exception:
      print('Corrupted Image file %s' % fname)


def save(img, fname):
  img.save(fname, quality=97)


@click.command()
@click.option(
    '--directory', default='data/train', show_default=True, help="Directory with original images.")
@click.option(
    '--convert_directory',
    default='data/train_res',
    show_default=True,
    help="Where to save converted images.")
@click.option(
    '--test',
    is_flag=True,
    default=False,
    show_default=True,
    help="Convert images one by one and examine them on screen.")
@click.option('--crop_size', default=256, show_default=True, help="Size of converted images.")
@click.option('--extension', default='tiff', show_default=True, help="Filetype of converted images.")
def main(directory, convert_directory, test, crop_size, extension):
  try:
    os.mkdir(convert_directory)
  except OSError:
    pass

  supported_extensions = set(['jpg', 'png', 'tiff', 'jpeg', 'tif'])

  filenames = [
      os.path.join(dp, f) for dp, dn, fn in os.walk(directory) for f in fn
      if f.split('.')[-1].lower() in supported_extensions
  ]
  filenames = sorted(filenames)

  if test:
    names = data.get_names(filenames)
    y = data.get_labels(names)
    for f, level in zip(filenames, y):
      if level == 1:
        try:
          img = convert(f, crop_size)
          img.show()
          Image.open(f).show()
          real_raw_input = vars(__builtins__).get('raw_input', input)
          real_raw_input('enter for next')
        except KeyboardInterrupt:
          exit(0)

  print("Resizing images in {} to {}, this takes a while." "".format(directory, convert_directory))

  n = len(filenames)
  # process in batches, sometimes weird things happen with Pool on my machine
  batchsize = 500
  batches = n // batchsize + 1
  pool = Pool(N_PROC)

  args = []

  for f in filenames:
    args.append((convert, (directory, convert_directory, f, crop_size, extension)))

  for i in range(batches):
    print("batch {:>2} / {}".format(i + 1, batches))
    pool.map(process, args[i * batchsize:(i + 1) * batchsize])

  pool.close()

  print('done')


if __name__ == '__main__':
  main()
