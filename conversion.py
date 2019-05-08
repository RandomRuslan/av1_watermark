from PIL import Image


def get_rgb(img):
    width, height = img.size
    pix = img.load()

    rgb = []
    for i in range(height):
        for j in range(width):
            rgb.append(pix[j, i][:3])
    return rgb

def draw_image(rgb, title, img_desc):
    img = Image.new(img_desc['mode'], img_desc['size'])
    width, height = img_desc['size']
    pixels = img.load()
    for i in range(height):
        for j in range(width):
            pixels[j, i] = rgb[i*width+j]
    # img.show()
    img.save(title)
    img.close()

def convert_rgb_to_yuv(rgb):
    # print('rgb to yuv') # BT.601
    kr = 0.299
    kb = 0.114
    y = []
    u = []
    v = []
    for r, g, b in rgb:
        yi = kr*r + kb*b + (1-kr-kb)*g
        ui = b - yi
        vi = r - yi
        y.append(yi)
        u.append(ui)
        v.append(vi)

    return y, u, v

def convert_yuv_to_rgb(y, u, v):
    # print('yuv to rgb') # BT.601
    kr = 0.299
    kb = 0.114
    rgb = []
    for i in range(len(y)):
        r = y[i] + v[i]
        g = y[i] - ((kr*v[i] + kb*u[i]) / (1-kr-kb))
        b = y[i] + u[i]
        rgb.append((int(round(r)), int(round(g)), int(round(b))))

    return rgb
