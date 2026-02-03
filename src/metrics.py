import pandas as pd

def weekly_volume(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["week"] = d["opened_at"].dt.to_period("W").astype(str)
    return d.groupby("week").size().reset_index(name="ticket_count")

def weekly_mttr(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["week"] = d["opened_at"].dt.to_period("W").astype(str)
    return (
        d.groupby("week")["mttr_minutes"]
        .mean()
        .reset_index(name="avg_mttr_minutes")
        .sort_values("week")
    )

def mttr_by_service(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("service")["mttr_minutes"]
        .mean()
        .reset_index()
        .sort_values("mttr_minutes", ascending=False)
    )
