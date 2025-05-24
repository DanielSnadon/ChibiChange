import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import os
import matplotlib.ticker as mticker


def big_graph():
    plt.style.use("dark_background")

    engine = create_engine("sqlite:///prices.db")
    try:
        data = pd.read_sql_table("table", con=engine)
    except Exception as e:
        print(f"Error reading from DB: {e}")
        return

    static_dir = "app/static"
    os.makedirs(static_dir, exist_ok=True)

    for currency in data.columns:
        if currency == "index":
            continue

        try:
            values = pd.to_numeric(data[currency].dropna().values)

            if len(values) != 60:
                print(
                    f"Warning: Number of points for {currency} is not 60 ({len(values)})."
                )
                if len(values) < 2:
                    continue

            fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
            fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9)

            x = np.linspace(0, 10, num=len(values))
            diffs = np.diff(values)

            median_val = np.median(values)
            mean_val = np.mean(values)

            Q1 = np.percentile(values, 25)
            Q3 = np.percentile(values, 75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_x = []
            outliers_y = []
            for i, val in enumerate(values):
                if val < lower_bound or val > upper_bound:
                    outliers_x.append(x[i])
                    outliers_y.append(val)

            for i in range(len(x) - 1):
                color = "#50B33B" if diffs[i] >= 0 else "#FF3B3B"
                ax.plot(
                    [x[i], x[i + 1]],
                    [values[i], values[i + 1]],
                    color=color,
                    linewidth=2,
                    antialiased=True,
                    marker="s",
                    markersize=4,
                    solid_capstyle="butt",
                )

            ax.axhline(
                median_val,
                color="#800080",
                linestyle="--",
                linewidth=1.5,
                label=f"Median: {median_val:.2f}",
            )
            ax.axhline(
                mean_val,
                color="#FFFF00",
                linestyle=":",
                linewidth=1.5,
                label=f"Mean: {mean_val:.2f}",
            )

            if outliers_x:
                ax.plot(
                    outliers_x,
                    outliers_y,
                    "o",
                    color="#8B0000",
                    markersize=6,
                    label="Outliers",
                )

            ax.grid(True, color="#333333", linestyle="--", alpha=0.5)
            ax.legend(
                loc="lower center",
                facecolor="#2B2B2B",
                edgecolor="white",
                labelcolor="white",
            )

            ax.tick_params(axis="y", colors="white")
            formatter = mticker.FormatStrFormatter("$%.2f")
            ax.yaxis.set_major_formatter(formatter)

            ax.set_xticks([0, 10])
            ax.set_xticklabels(["Start", "End of Interval"], color="white")
            ax.tick_params(axis="x", colors="white")

            filename = f'{currency.replace("/", "-")}-big.png'
            save_path = os.path.join(static_dir, filename)
            fig.savefig(
                save_path,
                dpi=100,
                transparent=False,
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close(fig)

        except Exception as e:
            print(f"Error processing {currency}: {e}")

    print("Большие графики созданы.")
