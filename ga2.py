import os
from math import pi, sin, cos
from PIL import Image, ImageDraw
from PIL.Image import alpha_composite, blend
import matplotlib.pyplot as plt
from numpy.random import uniform, choice
from numpy import asarray, sum, array, argmax, argsort, vstack, empty
from tqdm import trange


class triangle:
    dot1x, dot1y = 0, 0
    alpha = 1
    r = 1
    g = 1
    b = 1

    def __init__(self, args):
        assert len(args) == 6
        self.dot1x, self.dot1y = args[0], args[1]
        self.alpha = args[2]
        self.r, self.g, self.b = args[3:]

    def get_position(self):
        l = 0.2
        dot2x, dot2y = self.dot1x + l * cos(2 * self.alpha * pi), \
            self.dot1y + l*sin(2*self.alpha*pi)
        dot3x, dot3y = self.dot1x + l * \
            cos(2 * self.alpha * pi + pi / 3), \
            self.dot1y + l*sin(2*self.alpha*pi + pi / 3)
        return [self.dot1x, self.dot1y, dot2x, dot2y, dot3x, dot3y]

    def get_color(self):
        return "rgb({:d}, {:d}, {:d})".format(
            int(self.r * 255), int(self.g * 255), int(self.b * 255))

    def get_vector(self):
        return [*self.dot1, *self.dot2, *self.dot3, self.r, self.g, self.b]


def draw_frame(units, size):
    canvas = Image.new('RGBA', (size, size), "#FFFFFFFF")
    painter = ImageDraw.Draw(canvas)
    for unit in units:
        canvas2 = Image.new('RGBA', (size, size), "#FFFFFFFF")
        painter = ImageDraw.Draw(canvas2)
        painter.polygon([size * i for i in unit.get_position()],
                        fill=unit.get_color())
        canvas = blend(canvas, canvas2, 0.5)
    return canvas


def fitness_func(img1, img2):
    raw = asarray(img1)
    gene = asarray(img2)
    return img1.size[0] * img1.size[1] * 4 / sum(abs(raw - gene))


img = Image.open("./img/chrome.png")
n_units, l_units = 90, 6
individuals = 8
n_children = 2
n_parents = individuals - n_children
# 创建初始种群
pops = uniform(size=(individuals, n_units, l_units))
with trange(40000) as pbar:
    for g in pbar:
        # 计算适应度
        canvases = [draw_frame([triangle(i) for i in w], img.size[0])
                    for w in pops]
        fitness = array([fitness_func(img, canvas) for canvas in canvases])
        pbar.set_description("fitness:{:.5f}".format(max(fitness)))
        if g % 50 == 0:
            idx = argmax(fitness)
            mat = pops[idx]
            canvas = draw_frame([triangle(jk) for jk in mat], img.size[0])
            plt.imshow(canvas)
            # with open("./cache/{}.png".format(g), 'wb') as fp:
            #     canvas.save(fp)
            plt.pause(0.01)
        # 筛选父代
        idxs = argsort(fitness)[-n_parents:]
        # idxs = choice(individuals, size=n_parents,
        #               p=fitness / sum(fitness))
        # idxs[0] = argmax(fitness)
        parents = pops[idxs]
        # 交叉变异
        offsprings = empty((n_children, n_units, l_units))
        for i in range(n_children):
            idx1, idx2 = choice(n_parents), choice(n_parents)
            for j in range(n_units):
                cross_point = l_units // 3
                offsprings[i][j][:cross_point] = parents[idx1][j][:cross_point]
                offsprings[i][j][cross_point:] = parents[idx2][j][cross_point:]
                if uniform() > 0.3:
                    point = int(uniform() * l_units)
                    offsprings[i][j][point] += uniform(-0.6, 0.6, size=1)
                    if offsprings[i][j][point] < 0:
                        offsprings[i][j][point] = 0
                    if offsprings[i][j][point] > 1:
                        offsprings[i][j][point] = 1
        pops = vstack((parents, offsprings))
    idx = argmax(fitness)
    mat = pops[idx]
    canvas = draw_frame([triangle(jk) for jk in mat], img.size[0])
    with open("./cache/final.png".format(g), 'wb') as fp:
        canvas.save(fp)
os.system("shutdown -s -t 0")
# units = [triangle(uniform(size=10)) for _ in range(3)]
# canvas = draw_frame(units, 96)
# print(fitness_func(img, canvas))
# plt.imshow(canvas)
# plt.show()
