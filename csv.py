import os

BASE_DIR = '../csv'

def get_avg_ssim():
    result_file = open(os.path.join(BASE_DIR, 'avg_ssim.csv'), 'w')
    for img_dir in range(10):
        if img_dir == 4:
            continue

        for block_side in [32, 16, 8]:
            file_name = '_'.join([str(img_dir), 'blocks', str(block_side), '0', 'comp']) + '.csv'
            file_name = os.path.join(BASE_DIR, '0', str(img_dir), file_name)

            total_line = 0
            sum_ssim = 0

            with open(file_name) as csv_file:
                for line in csv_file:
                    cols = line.strip().split(';')
                    total_line += 1
                    ssim = float(cols[1])
                    sum_ssim += ssim

            result_file.write(str(sum_ssim/total_line) + ';;')

        result_file.write('\n')
    result_file.close()


def count_success_blocks():
    result_file = open(os.path.join(BASE_DIR, 'result.csv'), 'w')
    for sign_dir in range(8):
        for img_dir in range(10):
            if img_dir == 4:
                continue
            
            part = ''
            for block_side in [32, 16, 8]:
                file_name = '_'.join([str(img_dir), 'blocks', str(block_side), str(sign_dir), 'comp']) + '.csv'
                file_name = os.path.join(BASE_DIR, str(sign_dir), str(img_dir), file_name)

                total_line = 0
                min_ssim = max_ssim = None
                av1_rgb = 0

                rgb_u = 0
                rgb_v = 0
                rgb_both = 0
                rgb_wm = 0

                success_ssim = 0
                success_rgb = 0
                secure = 0

                with open(file_name) as csv_file:
                    for line in csv_file:
                        total_line += 1
                        cols = line.strip().split(';')

                        ssim = float(cols[1])
                        if min_ssim is None or ssim < min_ssim:
                            min_ssim = ssim
                        # if max_ssim is None or ssim > max_ssim:
                        #     max_ssim = ssim
                        if cols[2] == 'True':
                            av1_rgb += 1

                        if cols[4] == 'True':
                            rgb_u += 1
                        if cols[6] == 'True':
                            rgb_v += 1
                        if cols[8] == 'True':
                            rgb_both += 1

                        if 'True' in [cols[4], cols[6], cols[8]]:
                            rgb_wm += 1

                            if ssim >= 0.99:
                                success_ssim += 1
                            if cols[2] == 'True':
                                success_rgb += 1

                            if ssim >= 0.99 and cols[2] == 'False':
                                secure += 1


                # values = [total_line, min_ssim, av1_rgb, rgb_u, rgb_v, rgb_both, rgb_wm, success_ssim, success_rgb]
                values = [total_line, success_rgb, secure]
                part += ';'.join([str(x) for x in values]) + ';;'

            result_file.write(part + '\n')
        result_file.write('\n')
    result_file.close()


if __name__ == '__main__':
    count_success_blocks()
    get_avg_ssim()
