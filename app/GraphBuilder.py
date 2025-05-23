import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine


def graph():
    plt.style.use('dark_background')
    
    engine = create_engine('sqlite:///prices.db')
    try:
        data = pd.read_sql_table('table', con=engine)
    except Exception as e:
        print(f"Ошибка чтения из БД: {e}")
        return

    os.makedirs('static', exist_ok=True)

    for currency in data.columns:
        if currency == 'index':
            continue

        try:
            values = pd.to_numeric(data[currency].values)
            if len(values) < 2:
                continue

            fig, ax = plt.subplots(figsize=(1.5, 1), dpi=100)
            fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
            ax.axis("off")

            x = np.linspace(0, 10, num=len(values))
            diffs = np.diff(values)

            for i in range(len(x) - 1):
                color = '#50B33B' if diffs[i] >= 0 else '#FF3B3B'
                ax.plot(
                    [x[i], x[i+1]], 
                    [values[i], values[i+1]], 
                    color=color,
                    linewidth=1,
                    antialiased=False,
                    solid_capstyle='butt'
                )

            filename = f'{currency.replace("/", "-")}-small.png'
            save_path = os.path.join('app/static', filename)
            fig.savefig(
                save_path,
                dpi=100,
                transparent=True,
                bbox_inches='tight',
                pad_inches=0
            )
            plt.close(fig)

        except Exception as e:
            print(f"Ошибка при обработке {currency}: {e}")

    print("Все маленькие графики созданы")

