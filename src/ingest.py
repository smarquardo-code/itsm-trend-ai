import pandas as pd

REQUIRED_COLUMNS = {
    "ticket_id", "opened_at", "resolved_at",
    "category", "subcategory", "service", "ci",
    "priority", "assignment_group", "short_description",
    "mttr_minutes"
}

def load_tickets(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["opened_at", "resolved_at"])
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df
