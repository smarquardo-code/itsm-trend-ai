import webbrowser
from pathlib import Path

from src.config import config
from src.ingest import load_tickets
from src.metrics import weekly_volume, weekly_mttr, mttr_by_service
from src.trends import top_risers
from src.analysis_contract import build_analysis_summary
from src.ai_insights import generate_ai_insights
from src.viz import generate_charts
from src.report import write_report

def main():
    df = load_tickets(config.DATA_PATH)

    volume = weekly_volume(df)
    wmttr = weekly_mttr(df)
    mttr = mttr_by_service(df)
    risers = top_risers(df)

    summary = build_analysis_summary(volume, wmttr, mttr, risers)
    ai_text = generate_ai_insights(summary)

    charts = generate_charts(volume, wmttr, config.REPORT_PATH)
    outputs = write_report(summary, ai_text, config.REPORT_PATH, charts=charts)

    print("Report generated:")
    for k, v in outputs.items():
        print(f" - {k}: {v}")
    for k, v in charts.items():
        print(f" - {k}: {v}")

    # Open HTML report in your default browser
    html_path = Path(outputs["html_report"]).resolve()
    webbrowser.open(html_path.as_uri())

if __name__ == "__main__":
    main()


