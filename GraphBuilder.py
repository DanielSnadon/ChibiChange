import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import numpy as np

plt.style.use('dark_background')
engine = create_engine('sqlite:///prices.db')
base = pd.read_sql('table', con=engine)

k = 0
for currency in list(base):
    if currency == 'index':
        continue
    k+=1

    base[currency] = pd.to_numeric(base[currency])

    plt.figure(figsize=(1.5, 1), dpi=100)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis("off")
    y = base[currency].values
    x = np.linspace(0, 10, num=len(y))
    diff = np.diff(y)

    for i in range(len(x) - 1):
        color = '#50B33B' if diff[i] >= 0 else '#FF3B3B'
        plt.plot(
            [x[i], x[i+1]], 
            [y[i], y[i+1]], 
            color=color,
            linewidth=1,
            antialiased=False,
            solid_capstyle='butt'
        )

    plt.savefig(f'{str(currency).replace("/", "-")}-small.png', dpi=100, transparent=True, bbox_inches='tight', pad_inches=0)