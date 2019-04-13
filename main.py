from conversion import *
from math_functions import *
from pictures import *
from image_diff import *

WORK_DIR = 'projectVarya'
WORK_FILE = 'v02.png'

def get_bin_view(x):
    bn = bin(x)[2:]
    return '0' * (8 - len(bn)) + bn

if __name__ == '__main__':
    blocks_dir = os.path.join(WORK_DIR, WORK_FILE.split('.')[0] + '_blocks')

    # split_picture(WORK_DIR, WORK_FILE)
    # create_pictures(WORK_DIR, WORK_FILE)
    total_comparison(blocks_dir)
    # for i in global_params:
    #     print(i)

    '''
    Шифрование:
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
        print('k: ', first_k, second_k, new_k)

        diff_first = abs(first_k[0] - new_k[0]) + abs(first_k[1] - new_k[1])
        diff_second = abs(second_k[0] - new_k[0]) + abs(second_k[1] - new_k[1])
        print(fl, ' diff: ', diff_first, diff_second)

        decrypted_key += 'x' if diff_first == diff_second else '0' if diff_first < diff_second else '1'

    x_count = 0
    same = True
    print('keys: ', key, decrypted_key)
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
    '''