from PIL import ImageDraw, Image
from PIL.Image import composite
from numpy import asarray, sum
from typing import List


# 定义shell
class Shell:
    '''三角形的壳
    Parameters:
    ----------
    point*: Tuple(float, float)
    color: Tuple(float, float, float)
    注： 所有的浮点数都在0~1之间
    '''

    def __init__(self, args):
        assert len(args) == Shell.get_n_gene()
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
        return 9


def draw_frame(shells: List[Shell], size) -> Image:
    '''绘制半透明壳叠加在一起后的图形。'''
    background = Image.new("RGB", (size, size), "#FFFFFF")
    for shell in shells:
        # shell = Shell(shell)
        shell_im = Image.new("RGB", background.size, "#FFFFFF")
        mask = Image.new("L", background.size, 255)
        imDraw = ImageDraw.Draw(shell_im)
        imDraw.polygon(shell.get_points(size), shell.get_color())
        maskDraw = ImageDraw.Draw(mask)
        maskDraw.polygon(shell.get_points(size), 128)
        background = composite(background, shell_im, mask)
    return background


def calc_similarity(target: Image, im: Image) -> float:
    '''计算两幅图之间的相似度, 将两幅RGB图各个通道值差值计算'''
    size = im.size[0]
    mat_target = asarray(target)
    mat_im = asarray(im)
    return 3 * size * size / sum(abs(mat_target - mat_im))
