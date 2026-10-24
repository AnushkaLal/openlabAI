from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def create_plots(df: pd.DataFrame, output_dir: str) -> list[str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    numeric = df.select_dtypes(include="number")
    generated = []

    if numeric.shape[1] >= 2:
        corr = numeric.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        image = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        ax.set_title("Numeric Correlation Matrix")
        fig.colorbar(image, ax=ax, label="Pearson correlation")
        fig.tight_layout()

        path = out / "correlation.png"
        fig.savefig(path, dpi=140)
        plt.close(fig)
        generated.append(str(path))

    if not numeric.empty:
        columns = list(numeric.columns[:6])
        axes_count = len(columns)
        fig, axes = plt.subplots(
            axes_count, 1, figsize=(8, 3 * axes_count),
            squeeze=False
        )

        for index, col in enumerate(columns):
            axes[index, 0].hist(
                numeric[col].dropna(), bins=25, edgecolor="black"
            )
            axes[index, 0].set_title(f"Distribution: {col}")
            axes[index, 0].set_ylabel("Frequency")

        fig.tight_layout()
        path = out / "distributions.png"
        fig.savefig(path, dpi=140)
        plt.close(fig)
        generated.append(str(path))

    return generated
