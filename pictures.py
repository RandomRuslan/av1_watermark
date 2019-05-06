from conversion import *
from math_functions import *
from image_diff import *
import numpy as np
import os


def split_picture(dir, file, blocks_dir, block_side):
    img = Image.open(os.path.join(dir, file))
    width, height = img.size
    img_desc = {    # for return
        'size': img.size,
        'mode': img.mode
    }

    block_desc = {
        'size': (block_side, block_side),
        'mode': img.mode
    }
    pixels = img.load()

    for i in range(height//block_side):
        for j in range(width//block_side):
            rgb = []
            for ii in range(block_side):
                for jj in range(block_side):
                    rgb.append(pixels[j*block_side + jj, i*block_side + ii][:-1])

            draw_image(rgb, os.path.join(blocks_dir, '_'.join(['0', str(i), str(j)]) + '.png'), block_desc)

    img.close()
    return img_desc


def create_blocks(blocks_dir):
    print('_create_blocks_')
    files = os.listdir(blocks_dir)
    for filename in files:
        if filename[0] != '0':
            continue

        img = Image.open(os.path.join(blocks_dir, filename))
        img_desc = {
            'size': img.size,
            'mode': img.mode
        }
        rgb = get_rgb(img)
        img.close()

        old_rgb, new_rgb = code_block(rgb)
        draw_image(old_rgb, os.path.join(blocks_dir, '1' + filename[1:]), img_desc)
        draw_image(new_rgb, os.path.join(blocks_dir, '2' + filename[1:]), img_desc)


def code_block(rgb):
    y, u, v = convert_rgb_to_yuv(rgb)
    params = get_all_params(y, u, v)
    # print(y, u, v, params, sep='\n')

    old_params, new_params = [], []
    for k, b in params:
        old_params.append([np.float16(k), np.float16(b)])   # ??? float32(k)
        new_params.append([inc_float(np.float16(k)), np.float16(b)])

    old_u = [old_params[0][0] * x + old_params[0][1] for x in y]
    old_v = [old_params[1][0] * x + old_params[1][1] for x in y]
    new_u = [new_params[0][0] * x + new_params[0][1] for x in y]
    new_v = [new_params[1][0] * x + new_params[1][1] for x in y]
    # print(u, old_u, new_u, '', v, old_v, new_v, sep='\n')

    old_rgb = convert_yuv_to_rgb(y, old_u, old_v)
    new_rgb = convert_yuv_to_rgb(y, new_u, new_v)
    # print(rgb, old_rgb, new_rgb, sep='\n')
    return [old_rgb, new_rgb]


def compile_pictures(dir, blocks_dir, block_side, img_desc):
    print('_compile_pictures_')
    full_width, full_height = img_desc['size']
    for ind in ['1', '2']:
        full_rgb = [(255, 255, 255)] * (full_height*full_width)

        files = os.listdir(blocks_dir)
        for filename in files:
            if filename[0] != ind:
                continue

            img = Image.open(os.path.join(blocks_dir, filename))
            rgb = get_rgb(img)
            img.close()

            temp = filename.split('.')[0].split('_')
            i, j = int(temp[1]), int(temp[2])

            for ii in range(block_side):
                for jj in range(block_side):
                    full_rgb[i*full_width*block_side + j*block_side + ii*full_width + jj] = rgb[ii*block_side + jj]

        draw_image(full_rgb, os.path.join(dir, str(block_side) + '_' + ind + '.png'), img_desc)
