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

paths = glob.glob('results/*.csv')

def do(with_what):
    outputs = []
    for path in paths:
        outputs.append(Output(path))

    x = []
    y = []
    ze = []

    filtered_outputs = list(filter(lambda x: len(x.df[with_what]) > 0, outputs))
    filtered_outputs.sort(key=lambda x: x.df[with_what][0])
    grouped = itertools.groupby(filtered_outputs, key=lambda x: x.df[with_what][0])
    for key, group in grouped:
        s = []
        z = []
        for i in group:
            s.append(i.df.loc[i.df['REPCL_SIZE'].idxmax()]['REPCL_SIZE'])
            z.append(i.df.loc[i.df['VECCL_SIZE'].idxmax()]['VECCL_SIZE'])
        x.append(key)
        y.append(sum(s) / len(s))
        ze.append(sum(z) / len(z))

    plt.xlabel(with_what)
    plt.ylabel('Size of the clock in bits')

    plt.plot(x, y, '-b', label='RepCl')
    plt.plot(x, ze, '-r', label='Vector Clock')
    plt.legend(loc='upper left')
    plt.show()

do('NUM_PROCS')
