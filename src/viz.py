from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def _save_line_chart(x, y, title: str, x_label: str, y_label: str, out_path: Path):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

def generate_charts(volume_df: pd.DataFrame, weekly_mttr_df: pd.DataFrame, output_dir: str) -> dict:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    vol_path = out_dir / "weekly_volume.png"
    mttr_path = out_dir / "weekly_mttr.png"

    # Weekly Volume chart
    _save_line_chart(
        x=volume_df["week"],
        y=volume_df["ticket_count"],
        title="Weekly Ticket Volume",
        x_label="Week",
        y_label="Tickets",
        out_path=vol_path
    )

    # Weekly MTTR chart
    _save_line_chart(
        x=weekly_mttr_df["week"],
        y=weekly_mttr_df["avg_mttr_minutes"],
        title="Weekly Average MTTR (minutes)",
        x_label="Week",
        y_label="Avg MTTR (min)",
        out_path=mttr_path
    )

    return {
        "weekly_volume_chart": str(vol_path),
        "weekly_mttr_chart": str(mttr_path),
    }
