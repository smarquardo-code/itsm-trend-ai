from datetime import datetime

def build_analysis_summary(volume_df, weekly_mttr_df, mttr_df, risers_list) -> dict:
    return {
        "generated_at_utc": datetime.utcnow().isoformat(),
        "volume_summary_weekly": volume_df.to_dict(orient="records"),
        "weekly_mttr": weekly_mttr_df.to_dict(orient="records"),
        "mttr_by_service": mttr_df.to_dict(orient="records"),
        "top_risers": risers_list,
    }

