from ga_icon import GAIcon

# 超参数定义、
hyper_param = {
    "n_indis": 32,  # 贝壳数量
    "cross_rate": 0.86,  # 交叉率
    "mut_rate": 0.8,  # 变异率
    "target_img": "./img/bird.png",
    "desired_size": 32,  # 期望的图片大小
    "max_iter": 1000,  # 最大迭代次数
    "knock_rate": 0.25,  # 淘汰率
    # "knock_rate": 0.125,
    "n_chromos": 80,  # 一个贝壳的染色体数量

    # 其他参数
    "desired_dir": "./bird/",  # 图片输出路径
}

ga = GAIcon(**hyper_param)
ga.run()
