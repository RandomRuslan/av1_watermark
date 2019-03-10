import matplotlib.pyplot as plt
import scipy as sp

def get_all_params(y, u, v):
    # print('get parametres')
    params = []
    fig, axes = plt.subplots(nrows=1, ncols=2)
    params.append(get_params(axes[0], y, u, 'u'))
    params.append(get_params(axes[1], y, v, 'v'))
    # params.append(get_params(axes[2], y+y, u+v, 'UV'))
    fig.tight_layout()
    # plt.show()
    return params

def get_params(ax, x, y, title):
    ax.set_title(title)
    ax.set_xlabel('luma')
    ax.set_ylabel('chroma')
    ax.autoscale(tight=True)
    ax.scatter(x, y)

    fp, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
    # print("Параметры модели: %s" % fp)
    # функция-полином, если её напечатать, то увидите математическое выражение
    f = sp.poly1d(fp)
    # print('ф-я:', f, sep=' ')
    ax.plot(x, f(x), linewidth=2)
    ax.grid()
    return fp

def inc_float(x):
    lst = list(str(x))[::-1]
    # print(x, lst, end='\n')
    for i in range(len(lst)):
        if '0' <= lst[i] <= '9':
            if lst[i] == '9':
                lst[i] = '0'
            else:
                lst[i] = str(int(lst[i])+1)
                break
    else:
        # print('round:', round(x))
        return round(x)

    # print(float(''.join(lst[::-1])))
    return float(''.join(lst[::-1]))
