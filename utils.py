from PIL import ImageDraw, Image
from PIL.Image import composite
from numpy import asarray, sum, int16
from typing import List


# 定义染色体
class Chromo:
    '''染色体，控制贝壳三角形花纹,每个染色体有9个基因。
    Parameters:
    ----------
    point*: Tuple(float, float)
    color: Tuple(float, float, float)
    注： 所有的浮点数都在0~1之间。
    '''

    def __init__(self, args):
        assert len(args) == Chromo.get_n_gene()
        self.point1 = (args[0], args[1])
        self.point2 = (args[2], args[3])
        self.point3 = (args[4], args[5])
        self.color = tuple(args[6:])

    def get_points(self, size) -> List[float]:
        return [i * size for i in [*self.point1, *self.point2, *self.point3]]

    def get_color(self) -> str:
        return "rgb({:.0%}, {:.0%}, {:.0%})".format(*self.color)

    @classmethod
    def get_n_gene(cls) -> int:
        '''返回一个染色体上的基因数量'''
        return 9


def draw_frame(chromos: List[Chromo], size) -> Image:
    '''综合所有染色体，绘制表现型。'''
    background = Image.new("RGB", (size, size), "#FFFFFF")
    for chromo in chromos:
        chromo_im = Image.new("RGB", background.size, "#000000")
        mask = Image.new("L", background.size, 255)
        imDraw = ImageDraw.Draw(chromo_im)
        imDraw.polygon(chromo.get_points(size), chromo.get_color())
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.polygon(chromo.get_points(size), fill=128)
        background = composite(background, chromo_im, mask)
    return background


def calc_similarity(target: Image, im: Image) -> float:
    '''计算两幅图之间的相似度, 将两幅RGB图各个通道值差值计算'''
    size = im.size[0]
    mat_target = asarray(target, dtype=int16)
    mat_im = asarray(im, dtype=int16)
    return 3 * size * size / sum(abs(mat_target - mat_im))
