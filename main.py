from ga_icon import GAIcon

# 超参数定义、
hyper_param = {
    "n_pops": 16,  # 种群数量
    "cross_rate": 0.86,  # 交叉率
    "mut_rate": 0.1,  # 变异率
    "target_img": "./img/chrome64.png",
    "desired_size": 64,  # 期望的图片大小
    "max_iter": 100000,  # 最大迭代次数
    "knock_rate": 0.2,
    "n_shells": 100,

    # 其他参数
    "desired_dir": "cache/",  # 图片输出路径
}

ga = GAIcon(**hyper_param)
ga.run()