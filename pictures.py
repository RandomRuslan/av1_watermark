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
                    rgb.append(pixels[j*block_side + jj, i*block_side + ii][:3])

            draw_image(rgb, os.path.join(blocks_dir, '_'.join(['0', str(i), str(j)]) + '.png'), block_desc)

    img.close()
    return img_desc


def create_blocks(blocks_dir, sign_place):
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

        counted_rgd = code_block(rgb, sign_place)
        for i in range(4):
            draw_image(counted_rgd[i], os.path.join(blocks_dir, str(i+1) + filename[1:]), img_desc)


def code_block(rgb, sign_place):
    y, u, v = convert_rgb_to_yuv(rgb)
    coef_u, coef_v = get_all_params(y, u, v)

    k_u, b_u = np.float16(coef_u[0]), np.float16(coef_u[1])
    k_v, b_v = np.float16(coef_v[0]), np.float16(coef_v[1])
    inc_k_u = inc_float(np.float16(coef_u[0]), sign_place)  # ??? float32(k)
    inc_k_v = inc_float(np.float16(coef_v[0]), sign_place)

    params_origin = ((k_u, b_u), (k_v, b_v))
    params_change_u = ((inc_k_u, b_u), (k_v, b_v))
    params_change_v = ((k_u, b_u), (inc_k_v, b_v))
    params_change_all = ((inc_k_u, b_u), (inc_k_v, b_v))

    counted_u, counted_v = [0] * 4, [0] * 4
    counted_u[0] = [params_origin[0][0] * x + params_origin[0][1] for x in y]
    counted_v[0] = [params_origin[1][0] * x + params_origin[1][1] for x in y]

    counted_u[1] = [params_change_u[0][0] * x + params_change_u[0][1] for x in y]
    counted_v[1] = [params_change_u[1][0] * x + params_change_u[1][1] for x in y]

    counted_u[2] = [params_change_v[0][0] * x + params_change_v[0][1] for x in y]
    counted_v[2] = [params_change_v[1][0] * x + params_change_v[1][1] for x in y]

    counted_u[3] = [params_change_all[0][0] * x + params_change_all[0][1] for x in y]
    counted_v[3] = [params_change_all[1][0] * x + params_change_all[1][1] for x in y]

    counted_rgb = [convert_yuv_to_rgb(y, counted_u[i], counted_v[i]) for i in range(4)]
    return counted_rgb


def compile_pictures(dir, blocks_dir, block_side, img_desc):
    print('_compile_pictures_')
    full_width, full_height = img_desc['size']
    for ind in ['1', '2', '3', '4']:
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
