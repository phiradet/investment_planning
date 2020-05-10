import pandas as pd
import matplotlib.pyplot as plt


def nav_plot(curr_df, x_col="date", y_col="cum_return", ax=None):
    if ax is None:
        ax = plt.gca()
    ax = curr_df.plot(x=x_col, y=y_col, ax=ax, color="purple")
    _ = ax.set_title(curr_df.name.iloc[0])
    _ = ax.axhline(curr_df[y_col].iloc[-1], color="purple", alpha=0.4, linestyle="--", label="latest", linewidth=2);

    mean_nav = curr_df[y_col].mean()
    std_nav = curr_df[y_col].std()
    _ = ax.axhline(mean_nav, color="lime", alpha=0.5, linestyle="-", label="average", linewidth=2);
    _ = ax.fill_between(ax.get_xticks(), mean_nav+std_nav, mean_nav-std_nav, facecolor='lime', alpha=0.07, label="avg ± std")

    ax.get_legend().remove()
    
    return ax