import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import os

def big_graph():
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
            values = pd.to_numeric(data[currency].dropna().values)
            if len(values) < 2:
                continue

            fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
            fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
            
            x = np.linspace(0, 10, num=len(values))
            diffs = np.diff(values)

            for i in range(len(x) - 1):
                color = '#50B33B' if diffs[i] >= 0 else '#FF3B3B'
                ax.plot(
                    [x[i], x[i+1]], 
                    [values[i], values[i+1]], 
                    color=color,
                    linewidth=2,
                    antialiased=True,
                    marker='s',
                    markersize=4,
                    solid_capstyle='butt'
                )

            ax.set_title(currency, color='white', pad=20)
            ax.grid(True, color='#333333', linestyle='--', alpha=0.5)
            
            filename = f'{currency.replace("/", "-")}-big.png'
            save_path = os.path.join('static', filename)
            fig.savefig(
                save_path,
                dpi=100,
                transparent=False,
                bbox_inches='tight',
                pad_inches=0.1
            )
            plt.close(fig)

        except Exception as e:
            print(f"Ошибка при обработке {currency}: {e}")

    print("Все большие графики созданы")
