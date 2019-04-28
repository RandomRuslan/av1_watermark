import time

from pictures import *
from image_diff import *

WORK_DIR = 'pictures/projectVarya'
WORK_FILE = 'v02.png'

def get_bin_view(x):
    bn = bin(x)[2:]
    return '0' * (8 - len(bn)) + bn


if __name__ == '__main__':
    for block_side in [8, 16, 32]:
        print('Start ' + str(block_side) + 'x' + str(block_side))
        t1 = time.time()
        blocks_dir = os.path.join(WORK_DIR, WORK_FILE.split('.')[0] + '_blocks_' + str(block_side))
        try:
            os.mkdir(blocks_dir)
        except OSError:
            pass

        img_desc = split_picture(WORK_DIR, WORK_FILE, blocks_dir, block_side)
        create_blocks(blocks_dir)
        total_comparison(blocks_dir)
        compile_pictures(WORK_DIR, blocks_dir, block_side, img_desc)
        t2 = time.time()
        print('time: ', t2-t1)
