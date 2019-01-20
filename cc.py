#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:51:55 2019

@author: alexv
"""

import cryptocompare.cryptocompare as crcomp # https://github.com/lagerfeuer/cryptocompare


#print(cryptocompare.get_coin_list(format=False))
#print(cryptocompare.get_price('BTC'))
print( crcomp.get_price(['BTC', 'ETH'], ['USD', 'EUR'], 'Kraken' ) )


import matplotlib.pyplot as plt   # https://github.com/matplotlib/matplotlib
import numpy as np

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

# plot violin plot
axes[0].violinplot(all_data,
                   showmeans=False,
                   showmedians=True)
axes[0].set_title('violin plot')

# plot box plot
axes[1].boxplot(all_data)
axes[1].set_title('box plot')

# adding horizontal grid lines
for ax in axes:
    ax.yaxis.grid(True)
    ax.set_xticks([y+1 for y in range(len(all_data))])
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')

# add x-tick labels
plt.setp(axes, xticks=[y+1 for y in range(len(all_data))],
         xticklabels=['x1', 'x2', 'x3', 'x4'])
plt.show()



