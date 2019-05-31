'''
Шифрование:
random_num = random.randint(0, 255)
key = get_bin_view(random_num)
print(random_num, key, sep=' ')

def get_bin_view(x):
    bn = bin(x)[2:]
    return '0' * (8 - len(bn)) + bn

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

# From code_block
# old_params, new_params = [], []
# for k, b in params:
#     old_params.append([np.float16(k), np.float16(b)])   # ??? float32(k)
#     new_params.append([inc_float(np.float16(k)), np.float16(b)])
# old_u = [old_params[0][0] * x + old_params[0][1] for x in y]
# old_v = [old_params[1][0] * x + old_params[1][1] for x in y]
# new_u = [new_params[0][0] * x + new_params[0][1] for x in y]
# new_v = [new_params[1][0] * x + new_params[1][1] for x in y]
# old_rgb = convert_yuv_to_rgb(y, old_u, old_v)
# new_rgb = convert_yuv_to_rgb(y, new_u, new_v)


# for i in range(0, 5-lst.index('.')):
#     lst.insert(0, '0')