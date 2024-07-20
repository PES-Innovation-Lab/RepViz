import re
import glob
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

outputs = []
for path in paths:
    outputs.append(Output(path))

outputs.sort(key=lambda x: x.df['NUM_PROCS'][0])

max_sizes = [outputs[i].df.loc[outputs[i].df['CLOCK_SIZE'].idxmax()]['CLOCK_SIZE'] + 64 for i in range(len(outputs))]
min_sizes = [outputs[i].df.loc[outputs[i].df['CLOCK_SIZE'].idxmin()]['CLOCK_SIZE']  + 64 for i in range(len(outputs))]

veccl_sizes = [outputs[i].df['VECCL_SIZE'][0] for i in range(len(outputs))]

plt.plot([0] + max_sizes)
plt.plot([0] + veccl_sizes)
plt.show()
