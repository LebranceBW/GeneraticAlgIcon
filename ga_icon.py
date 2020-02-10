# encooding:utf-8
from utils import Chromo, calc_similarity, draw_frame
from PIL import Image
from tqdm import trange
from numpy import ndarray, empty, argmax, argsort
from numpy.random import choice
from numpy.random import uniform as rand
from numpy.random import randint
from matplotlib import pyplot as plt


class GAIcon:
    """

    """

    def __init__(self, **kargs):
        for karg in kargs:
            setattr(self, karg, kargs[karg])
        self.n_genes = Chromo.get_n_gene()
        # 去掉原图中的alpha通道
        img = Image.open(self.target_img).resize(
            (self.desired_size, self.desired_size))
        new_im = Image.new("RGB", img.size, "#FFFFFF")
        new_im.paste(img, mask=img.split()[3])
        self.target_img = new_im
        with open(self.desired_dir + "target.png", 'wb') as fp:
            self.target_img.save(fp)

    def calc_fitness(self, pop: ndarray) -> ndarray:
        '''计算所有种群的适应度'''
        fitness = empty(len(pop))
        for i, shell in enumerate(pop):
            chromos = [Chromo(v) for v in shell]
            im = draw_frame(chromos, self.desired_size)
            fitness[i] = calc_similarity(self.target_img, im)
        return fitness

    def init_pops(self) -> ndarray:
        # 初始种群
        init_pops = rand(size=(self.n_indis, self.n_chromos, self.n_genes))
        return init_pops

    def crossover(self, pop: ndarray) -> ndarray:
        '''交叉'''
        alteres = list(range(len(pop)))
        while len(alteres):
            idx1 = choice(alteres)
            alteres.remove(idx1)
            idx2 = choice(alteres)
            alteres.remove(idx2)
            if rand() < self.cross_rate:
                for chromo_idx in range(self.n_chromos):
                    if rand() >= 0.5:
                        temp = pop[idx1][chromo_idx]
                        pop[idx1][chromo_idx] = pop[idx2][chromo_idx]
                        pop[idx2][chromo_idx] = temp
        return pop

    def mutation(self, pop) -> ndarray:
        ''' 整个染色体变异？或者是基因变异？ '''
        for shell in pop:
            if rand() < self.mut_rate:
                idx = int(rand() * self.n_chromos)
                shell[idx] += rand(-0.3, 0.3, size=self.n_genes)
                shell[idx] = abs(shell[idx])
        return pop

    def selection(self, fitnesses, pop) -> ndarray:
        '''淘汰'''
        n_knock = int(self.knock_rate * self.n_indis)
        indxs = argsort(fitnesses)
        for knock_indx in indxs[:n_knock]:
            indx1 = indxs[-2]
            indx2 = indxs[-1]
            # point = self.n_genes // 2
            for chromo_idx in range(self.n_chromos):
                if rand() < 0.86:
                    pop[knock_indx][chromo_idx] = \
                        pop[indx2][chromo_idx]
                else:
                    pop[knock_indx][chromo_idx] = \
                        pop[indx1][chromo_idx]
        return pop

    def money_num_Gen(self):
        '''生成器，生成类似1, 2, 4, 8 10, 20, 40....的无限长序列'''
        captials = [1, 2, 4, 8]
        while True:
            yield from captials
            captials = [i * 10 for i in captials]

    def run(self):
        fitness_trace = []
        try:
            money_num_gen = self.money_num_Gen()
            catch_time = next(money_num_gen)
            # 初始化种群
            pop = self.init_pops()
            for generation in trange(self.max_iter + 1):
                # 计算fitness
                fitnesses = self.calc_fitness(pop)
                fitness_trace.append(max(fitnesses))
                # 存个点
                if generation == catch_time:
                    if self.mut_rate > 0.1:
                        self.mut_rate *= 0.9
                    catch_time = next(money_num_gen)
                    idx = argmax(fitnesses)
                    chromos = [Chromo(i) for i in pop[idx]]
                    im = draw_frame(chromos, self.desired_size)
                    with open(self.desired_dir + "{}.png".format(generation),
                              'wb') as fp:
                        im.save(fp)
                # 筛选父代
                pop = self.selection(fitnesses, pop)
                # 交叉
                pop = self.crossover(pop)
                # 变异
                pop = self.mutation(pop)

        finally:
            plt.plot(fitness_trace)
            plt.savefig(self.desired_dir + "trace.png")
