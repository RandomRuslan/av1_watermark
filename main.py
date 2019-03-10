from conversion import *
from math_functions import *
import numpy as np
import os
import random


def code_picture(filename):
    img = Image.open('pictures/' + filename)
    img_desc = {
        'size': img.size,
        'mode': img.mode
    }
    rgb = get_rgb(img)
    # print(rgb)
    img.close()

    y, u, v = convert_rgb_to_yuv(rgb)
    # print(y, u, v, sep='\n')

    params = get_all_params(y, u, v)
    # print(params)

    old_params = []
    new_params = []
    for k, b in params:
        # old_params.append([np.float32(k), np.float32(b)])
        # new_params.append([inc_float(np.float32(k)), np.float32(b)])
        old_params.append([np.float16(k), np.float16(b)])
        new_params.append([inc_float(np.float16(k)), np.float16(b)])
    global_params.append([old_params, new_params])

    old_u = [old_params[0][0] * x + old_params[0][1] for x in y]
    old_v = [old_params[1][0] * x + old_params[1][1] for x in y]
    new_u = [new_params[0][0] * x + new_params[0][1] for x in y]
    new_v = [new_params[1][0] * x + new_params[1][1] for x in y]
    # print(u, old_u, new_u, '', v, old_v, new_v, sep='\n')

    old_rgb = convert_yuv_to_rgb(y, old_u, old_v)
    new_rgb = convert_yuv_to_rgb(y, new_u, new_v)

    T = 0
    F = 0
    for i in range(len(rgb)):
        if new_rgb[i] != old_rgb[i] or abs(new_rgb[i][0] - old_rgb[i][0]) > 1 or abs(new_rgb[i][1] - old_rgb[i][1]) > 1 or abs(new_rgb[i][2] - old_rgb[i][2]) > 1:
            F += 1
            # print(i, new_rgb[i], old_rgb[i])
        else:
            T += 1
    # print(T, F)

    # print(rgb, old_rgb, new_rgb, sep='\n')
    # y_old = get_luma
    draw_image(old_rgb, 'pictures/' + filename[0] + '_1.png', img_desc)
    draw_image(new_rgb, 'pictures/' + filename[0] + '_2.png', img_desc)
    return [old_rgb, new_rgb]


def create_pictures():
    files = os.listdir('pictures/')
    for filename in files:
        if '_' in filename:
            continue

        print(filename)
        rgb1, rgb2 = code_picture(filename)
        y1, u1, v1 = convert_rgb_to_yuv(rgb1)
        y2, u2, v2 = convert_rgb_to_yuv(rgb2)
        p = [get_all_params(y1, u1, v1), get_all_params(y2, u2, v2)]
        # print(p)
        # global_params.append(p)

def get_bin_view(x):
    bn = bin(x)[2:]
    return '0' * (8 - len(bn)) + bn


global_params = []
if __name__ == '__main__':

    create_pictures()
    # for i in global_params:
    #     print(i)

    random_num = random.randint(0, 255)
    key = get_bin_view(random_num)
    print(random_num, key, sep=' ')

    decrypted_key = ''
    for i in range(8):
        fl = '1' if key[i] == '0' else '2'
        img = Image.open('pictures/' + str(i) + '_' + fl + '.png')
        rgb = get_rgb(img)
        img.close()

        y, u, v = convert_rgb_to_yuv(rgb)
        params = get_all_params(y, u, v)

        new_k = [np.float16(params[0][0]), np.float16(params[1][0])]
        first_k = [global_params[i][0][0][0], global_params[i][0][1][0]]
        second_k = [global_params[i][1][0][0], global_params[i][1][1][0]]
        print(first_k, second_k, new_k)

        diff_first = abs(first_k[0] - new_k[0]) + abs(first_k[1] - new_k[1])
        diff_second = abs(second_k[0] - new_k[0]) + abs(second_k[1] - new_k[1])

        decrypted_key += 'x' if diff_first == diff_second else '0' if diff_first < diff_second else '1'

    x_count = 0
    same = True
    for i in range(len(key)):
        if decrypted_key[i] == 'x':
            x_count += 1
        elif decrypted_key[i] != key[i]:
            same = False
    print('Key:', random_num, sep='\t')
    print('IN:', key, sep='\t')
    print('OUT', decrypted_key, sep='\t')
    if not same:
        print('WRONG')
    else:
        print('SUCCESS: x = ' + str(x_count))
