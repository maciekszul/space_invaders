import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib import gridspec
from scipy.interpolate import interp1d

def resamp_interp(x, y, new_x):
    """
    returns resampled an interpolated data
    """
    resamp = interp1d(x, y, kind='linear', fill_value='extrapolate')
    new_data = resamp(new_x)
    return new_data


data = pd.read_csv("response.csv")
zig_zag = np.load("zigzag.npy")

gs = gridspec.GridSpec(1, 2, wspace=0.25, hspace=0.4, width_ratios=[0.75, 0.25])
figure = plt.figure(figsize=(12, 10))

main = figure.add_subplot(gs[0, 0])

main.plot(zig_zag[:,0], zig_zag[:, 1], lw=2, c="black")

traj = np.flip(data.cur_pos.to_numpy())
pos = data.zig_pos - data.zig_pos.to_numpy()[-1]

main.plot(traj, pos, lw=0.5, c="red")
main.set_xlim([-10.5, 10.5])

side = figure.add_subplot(gs[0, 1])

beg = zig_zag[:,1].max()
end = zig_zag[:,1].min()

beg_ix = np.where(pos <= beg)[0][0]
end_ix = np.where(pos <= end)[0][0]

old_y = zig_zag[:,0]
old_x = zig_zag[:,1]
new_x = np.flip(pos.iloc[beg_ix:end_ix].to_numpy())
new_y = resamp_interp(old_x, old_y, new_x)

perfect_agent = np.zeros(pos.size)
perfect_agent[beg_ix:end_ix] = np.flip(new_y)

result = traj - perfect_agent

side.axvline(0, lw=0.2, c="black")
side.plot(result, pos, lw=0.5, c="blue")
side.set_xlim([-2, 2])


plt.show(block=False)