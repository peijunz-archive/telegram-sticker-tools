"""Example usage:

python sticker_conv.py input_path output_path
"""

import os
import sys
from PIL import Image


WEBP = 'webp'
WEBM = 'webm'

format_map = {"png": WEBP, "jpg": WEBP, "gif": WEBM}


def get_format(filename):
    if '.' in filename:
        return filename.split('.')[-1]


def scale_to_box(w, h, box=(512, 512)):
    if w >= h:
        return box[0], box[0]*h//w
    else:
        return box[1]*w//h, box[1]


def convert_single(fmt, input_file, output_file):
    img = Image.open(input_file)
    w, h = scale_to_box(*img.size)
    if fmt == WEBM:
        cmd = f'ffmpeg -y -i {input_file} -t 00:00:03 -c vp9 -b:v 0 -crf 40 -vf scale={w}:{h} {output_file}'
        os.system(cmd)
    else:
        img_resized = img.resize((w, h))
        img_resized.save(output_file)
        

def process(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for i, f in enumerate(os.listdir(input_path)):
        new_fmt = format_map.get(get_format(f))
        if not new_fmt:
            continue
        input_file = os.path.join(input_path, f)
        output_file = os.path.join(output_path, f.lstrip('-') + '.' + new_fmt)
        convert_single(new_fmt, input_file, output_file)


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process(input_path, output_path)

if __name__ == '__main__':
    main()

