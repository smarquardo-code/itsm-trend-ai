import json
from pathlib import Path
import pandas as pd
from markdown import markdown

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ITSM Trend Analysis Report</title>
  <style>
    body {{
      max-width: 980px;
      margin: 40px auto;
      padding: 0 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      line-height: 1.55;
      color: #111;
    }}
    h1, h2, h3 {{ line-height: 1.2; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; }}
    code, pre {{
      background: #f6f8fa;
      border-radius: 6px;
      padding: 2px 6px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}
    pre {{ padding: 12px; overflow-x: auto; }}
    hr {{ border: 0; border-top: 1px solid #ddd; margin: 24px 0; }}
    .meta {{ color: #555; font-size: 0.95em; margin-bottom: 18px; }}
    .toc {{ background: #fafafa; border: 1px solid #eee; padding: 12px 16px; border-radius: 10px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0 18px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f6f8fa; }}
  </style>
</head>
<body>
  <div class="meta">Generated locally by itsm-trend-ai</div>
  {content}
</body>
</html>
"""

def _df_from_records(records):
    if not records:
        return pd.DataFrame()
    return pd.DataFrame.from_records(records)

def _md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data available._"
    return df.to_markdown(index=False)

def build_deterministic_section(summary: dict) -> str:
    vol = _df_from_records(summary.get("volume_summary_weekly", []))
    wmttr = _df_from_records(summary.get("weekly_mttr", []))
    mttr = _df_from_records(summary.get("mttr_by_service", []))
    risers = _df_from_records(summary.get("top_risers", []))

    # keep tables compact
    vol_tail = vol.tail(12) if not vol.empty else vol
    wmttr_tail = wmttr.tail(12) if not wmttr.empty else wmttr
    mttr_top = mttr.head(10) if not mttr.empty else mttr
    risers_top = risers.head(10) if not risers.empty else risers

    md = []
    md.append("## Deterministic Summary (from data)\n")
    md.append("### Weekly Volume (last 12 weeks)\n")
    md.append(_md_table(vol_tail))
    md.append("\n\n### Weekly Average MTTR (last 12 weeks)\n")
    md.append(_md_table(wmttr_tail))
    md.append("\n\n### MTTR by Service (top 10)\n")
    md.append(_md_table(mttr_top))
    md.append("\n\n### Top Risers (latest week vs prior)\n")
    md.append(_md_table(risers_top))
    md.append("\n")
    return "\n".join(md)

def write_report(summary: dict, ai_text_md: str, output_dir: str, charts: dict | None = None) -> dict:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    analysis_path = out_dir / "analysis_summary.json"
    md_path = out_dir / "report.md"
    html_path = out_dir / "report.html"

    # Save machine-readable summary
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Build markdown with TOC + optional chart embeds + deterministic tables + AI narrative
    parts = []
    parts.append("# ITSM Trend Analysis Report\n")
    parts.append("[TOC]\n")

    if charts:
        # images are saved into the same reports/ folder, so relative links work in HTML
        if "weekly_volume_chart" in charts:
            parts.append("## Charts\n")
            parts.append("### Weekly Ticket Volume\n")
            parts.append("![](weekly_volume.png)\n")
            parts.append("### Weekly Average MTTR\n")
            parts.append("![](weekly_mttr.png)\n")

    parts.append(build_deterministic_section(summary))
    parts.append("## AI Insights\n")
    parts.append(ai_text_md.strip())
    md_text = "\n".join(parts).strip() + "\n"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    # Convert to HTML with TOC + tables
    html_body = markdown(
        md_text,
        extensions=["toc", "tables", "fenced_code"]
    )

    html = HTML_TEMPLATE.format(content=html_body)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return {
        "analysis_summary": str(analysis_path),
        "markdown_report": str(md_path),
        "html_report": str(html_path),
    }

