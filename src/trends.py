import pandas as pd

def top_risers(df: pd.DataFrame, periods: int = 2, top_n: int = 5):
    d = df.copy()
    d["week"] = d["opened_at"].dt.to_period("W").astype(str)

    weekly = d.groupby(["week", "subcategory"]).size().reset_index(name="count")
    pivot = weekly.pivot(index="subcategory", columns="week", values="count").fillna(0)

    if pivot.shape[1] < periods:
        return []

    last_two = pivot.iloc[:, -periods:]
    prev = last_two.iloc[:, 0]
    curr = last_two.iloc[:, 1]

    # avoid divide by zero by treating prev=0 as 1 for pct change computation
    pct_change = ((curr - prev) / prev.replace(0, 1)) * 100

    risers = pct_change.sort_values(ascending=False).head(top_n)

    results = []
    for sub in risers.index:
        results.append({
            "dimension": "subcategory",
            "name": sub,
            "previous_count": int(prev[sub]),
            "current_count": int(curr[sub]),
            "pct_change": round(float(pct_change[sub]), 1),
        })
    return results
