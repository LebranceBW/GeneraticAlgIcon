from utils import Shell, calc_similarity, draw_frame
from PIL import Image
from tqdm import trange
from numpy import ndarray, empty, argmax, argsort
from numpy.random import choice
from numpy.random import uniform as rand
from matplotlib import pyplot as plt


class GAIcon:
    """

    """

    def __init__(self, **kargs):
        for karg in kargs:
            setattr(self, karg, kargs[karg])
        self.n_genes = Shell.get_n_gene()
        # 去掉原图中的alpha通道
        img = Image.open(self.target_img).resize(
            (self.desired_size, self.desired_size))
        new_im = Image.new("RGB", img.size, "#FFFFFF")
        new_im.paste(img, mask=img.split()[3])
        self.target_img = new_im
        with open(self.desired_dir + "target.png", 'wb') as fp:
            self.target_img.save(fp)

    def calc_fitness(self, pops: ndarray) -> ndarray:
        '''计算所有种群的适应度'''
        fitness = empty(len(pops))
        for i, pop in enumerate(pops):
            shells = [Shell(v) for v in pop]
            im = draw_frame(shells, self.desired_size)
            fitness[i] = calc_similarity(self.target_img, im)
        return fitness

    def init_pops(self) -> ndarray:
        # 初始种群
        init_pops = rand(size=(self.n_pops, self.n_shells, self.n_genes))
        return init_pops

    def crossover(self, pops: ndarray) -> ndarray:
        '''交叉'''
        alteres = list(range(len(pops)))
        while len(alteres):
            idx1 = choice(alteres)
            alteres.remove(idx1)
            idx2 = choice(alteres)
            alteres.remove(idx2)
            if rand() < self.cross_rate:
                for shell_idx in range(self.n_shells):
                    if rand() >= 0.5:
                        pops[idx1][shell_idx], pops[idx2][shell_idx] = \
                            pops[idx2][shell_idx], pops[idx1][shell_idx]
        return pops

    def mutation(self, pops) -> ndarray:
        ''' 变异 '''
        for pop in pops:
            if rand() < self.mut_rate:
                for idx in choice(list(range(len(pop))), size=6):
                    pop[idx] = rand(size=pop[idx].size)
        return pops

    def selection(self, fitnesses, pops) -> ndarray:
        '''淘汰'''
        n_knock = int(self.knock_rate * self.n_pops)
        indxs = argsort(fitnesses)
        for knock_indx in indxs[:n_knock]:
            [indx1, indx2] = indxs[-2:]
            point = int(self.n_genes * rand())
            for shell_idx in range(self.n_shells):
                pops[knock_indx][shell_idx][:point] = \
                    pops[indx1][shell_idx][:point]
                pops[knock_indx][shell_idx][point:] = \
                    pops[indx2][shell_idx][point:]
        return pops

    def money_num_Gen(self):
        '''生成器，生成类似1, 2, 5, 10, 20, 50....的无限长序列'''
        captials = [1, 2, 5]
        while True:
            yield from captials
            captials = [i * 10 for i in captials]

    def run(self):
        fitness_trace = []
        try:
            money_num_gen = self.money_num_Gen()
            catch_time = next(money_num_gen)
            # 初始化种群
            pops = self.init_pops()
            for generation in trange(self.max_iter):
                # 计算fitness
                fitnesses = self.calc_fitness(pops)
                fitness_trace.append(max(fitnesses))
                # 存个点
                if generation == catch_time:
                    catch_time = next(money_num_gen)
                    idx = argmax(fitnesses)
                    shells = [Shell(i) for i in pops[idx]]
                    im = draw_frame(shells, self.desired_size)
                    with open(self.desired_dir + "第{}代.png".format(
                            generation), 'wb') as fp:
                        im.save(fp)
                # 筛选父代
                pops = self.selection(fitnesses, pops)
                # 交叉
                pops = self.crossover(pops)
                # 变异
                pops = self.mutation(pops)
                plt.plot(fitness_trace, 'b')
                plt.pause(0.01)

        finally:
            plt.savefig(self.desired_dir + "trace.png")
