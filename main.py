import time

from pictures import *
from image_diff import *



def start(WORK_FILE, WORK_DIR, sign_place):
    print('Start ' + WORK_FILE)
    for block_side in [32, 16, 8]:
        print('Start ' + str(block_side) + 'x' + str(block_side))
        t1 = time.time()
        blocks_dir = os.path.join(WORK_DIR, WORK_FILE.split('.')[0] + '_blocks_' + str(block_side))
        try:
            os.mkdir(blocks_dir)
        except OSError:
            pass

        img_desc = split_picture(WORK_DIR, WORK_FILE, blocks_dir, block_side)
        create_blocks(blocks_dir, sign_place)
        total_comparison(blocks_dir, sign_place)
        compile_pictures(WORK_DIR, blocks_dir, block_side, img_desc)
        t2 = time.time()
        print('time: ', t2-t1)


if __name__ == '__main__':
    t0 = time.time()
    for sign_place in range(8):
        for i in range(10):
            try:
                file = str(i) + '.png'
                dirr = '../long/' + str(sign_place) + '/' + str(i)
                start(file, dirr, sign_place)
            except Exception as e:
                print(str(i) + '.png is broken:', e)

    print('TOTAL TIME:', time.time()-t0)
