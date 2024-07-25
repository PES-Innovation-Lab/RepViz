import re
import glob
import itertools
import pandas as pd
import matplotlib.pyplot as plt

class Output:
    def __init__(self, path):
        self.path = path
        self.num_procs = int(re.search(r'.*N\.(\d+)-.*', path).groups()[0])
        self.epsilon = int(re.search(r'.*E\.(\d+)-.*', path).groups()[0])
        self.interval = int(re.search(r'.*I\.(\d+)-.*', path).groups()[0])
        self.delta = int(re.search(r'.*D\.(\d+)-.*', path).groups()[0])
        self.alpha = int(re.search(r'.*A\.(\d+)-.*', path).groups()[0])
        self.max_offset_bits = int(re.search(r'.*M\.(\d+)\.csv', path).groups()[0])
        self.df = pd.read_csv(path)

paths = glob.glob('14-min-results/*.csv')
outputs = list(filter(lambda x: x.df.shape[0] > 0, [Output(path) for path in paths]))

def graph(num_procs, epsilon, interval, delta, alpha):
    pass

num_procs_arr = [16, 32]
epsilon_arr = [100, 200, 400, 800]
interval_arr = [100, 200, 400, 800]
alpha_arr = [1, 4, 16]

combinations = []

NUM_PROCS = 0
ALPHA = 1
INTERVAL = 2
EPSILON = 3
DELTA = 4

for num_procs in num_procs_arr:
    for alpha in alpha_arr:
        for interval in interval_arr:
            for epsilon in epsilon_arr:
                delta = 1
                while delta <= epsilon:
                    combinations.append((num_procs, alpha, interval, epsilon, delta))
                    delta *= 4

def wrt(what):
    combinations.sort(key=lambda x: x[what])
    groups = itertools.groupby(combinations, key=lambda x: x[what])
    for key, group in groups:
        print(key)
        for ele in group:
            print(ele)

wrt(ALPHA)

# num_procs = 16
# while num_procs <= 32:
#     epsilon = 100
#     while epsilon <= 1000:
#         interval = 100
#         while interval <= 1000:
#             delta = 1
#             while delta <= epsilon:
#                 alpha = 1
#                 while alpha <= 32:
#                     graph(num_procs, epsilon, interval, delta, alpha)
#                     alpha *= 4
#                 delta *= 4
#             interval *= 2
#         epsilon *= 2
#     num_procs += 16

# def do(with_what):
#     outputs = []
#     for path in paths:
#         outputs.append(Output(path))
# 
#     x = []
#     y = []
#     ze = []
# 
#     filtered_outputs = list(filter(lambda x: len(x.df[with_what]) > 0, outputs))
#     filtered_outputs.sort(key=lambda x: x.df[with_what][0])
#     grouped = itertools.groupby(filtered_outputs, key=lambda x: x.df[with_what][0])
#     for key, group in grouped:
#         s = []
#         z = []
#         for i in group:
#             s.append(i.df.loc[i.df['REPCL_SIZE'].idxmax()]['REPCL_SIZE'])
#             z.append(i.df.loc[i.df['VECCL_SIZE'].idxmax()]['VECCL_SIZE'])
#         x.append(key)
#         y.append(sum(s) / len(s))
#         ze.append(sum(z) / len(z))
# 
#     plt.xlabel(with_what)
#     plt.ylabel('Size of the clock in bits')
# 
#     plt.plot(x, y, '-b', label='RepCl')
#     plt.plot(x, ze, '-r', label='Vector Clock')
#     plt.legend(loc='upper left')
#     plt.show()
# 
# do('NUM_PROCS')
