from conversion import *
from math_functions import *
from image_diff import *
import numpy as np
import os

global_params = []

def split_picture(dir, file, blocks_dir, block_side=32):
    img = Image.open(os.path.join(dir, file))
    width, height = img.size
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

def create_pictures(dir, file, blocks_dir):
    files = os.listdir(blocks_dir)

    for filename in files:
        if filename[0] != '0':
            continue

        rgb1, rgb2 = code_picture(blocks_dir, filename)
        # y1, u1, v1 = convert_rgb_to_yuv(rgb1)
        # y2, u2, v2 = convert_rgb_to_yuv(rgb2)
        # p = [get_all_params(y1, u1, v1), get_all_params(y2, u2, v2)]
        # print(p)
        # global_params.append(p)


def code_picture(dir, filename):
    img = Image.open(os.path.join(dir, filename))
    img_desc = {
        'size': img.size,
        'mode': img.mode
    }
    rgb = get_rgb(img)
    img.close()

    y, u, v = convert_rgb_to_yuv(rgb)
    # print(y, u, v, sep='\n')

    params = get_all_params(y, u, v)
    # print(params)

    old_params = []
    new_params = []
    for k, b in params:
        old_params.append([np.float16(k), np.float16(b)])   # ??? float32(k)
        new_params.append([inc_float(np.float16(k)), np.float16(b)])
    # global_params.append([old_params, new_params])

    old_u = [old_params[0][0] * x + old_params[0][1] for x in y]
    old_v = [old_params[1][0] * x + old_params[1][1] for x in y]
    new_u = [new_params[0][0] * x + new_params[0][1] for x in y]
    new_v = [new_params[1][0] * x + new_params[1][1] for x in y]
    # print(u, old_u, new_u, '', v, old_v, new_v, sep='\n')

    old_rgb = convert_yuv_to_rgb(y, old_u, old_v)
    new_rgb = convert_yuv_to_rgb(y, new_u, new_v)
    # print('compare rgb:', is_rgb_equal(rgb, old_rgb, show_diff=True), is_rgb_equal(old_rgb, new_rgb, show_diff=True))

    # T = 0
    # F = 0
    # for i in range(len(rgb)):
    #     if new_rgb[i] != old_rgb[i] or abs(new_rgb[i][0] - old_rgb[i][0]) > 1 or abs(new_rgb[i][1] - old_rgb[i][1]) > 1 or abs(new_rgb[i][2] - old_rgb[i][2]) > 1:
    #         F += 1
    #         print(i, new_rgb[i], old_rgb[i])
    #     else:
    #         T += 1
    # print(T, F)

    # print(rgb, old_rgb, new_rgb, sep='\n')
    # y_old = get_luma
    draw_image(old_rgb, os.path.join(dir, '1' + filename[1:]), img_desc)
    draw_image(new_rgb, os.path.join(dir, '2' + filename[1:]), img_desc)
    return [old_rgb, new_rgb]