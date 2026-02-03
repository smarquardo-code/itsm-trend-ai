import json
from openai import OpenAI
from src.config import config

SYSTEM_INSTRUCTIONS = (
    "You are an IT Operations analyst producing an ITSM trend report. "
    "Use ONLY the provided analysis summary JSON. "
    "Do not invent metrics, dates, counts, or root causes. "
    "If the JSON is insufficient, say what additional data would be needed. "
    "Output MUST be valid Markdown using the exact headings below.\n\n"
    "## Key Trends\n"
    "- Provide 3–6 bullet points. Each bullet must reference evidence from the JSON.\n\n"
    "## Emerging Risks\n"
    "- List risks implied by trends (impact, likelihood). Do not claim certainty.\n\n"
    "## Proactive Recommendations\n"
    "For each recommendation provide:\n"
    "- **Action**:\n"
    "- **Why** (tie to evidence):\n"
    "- **Effort** (Low/Med/High):\n"
    "- **Expected Impact** (Low/Med/High):\n"
    "- **Owner** (example team):\n\n"
    "## What to Monitor Next\n"
    "- Provide 3–5 monitoring or leading indicators.\n\n"
    "## Human Review Required\n"
    "- List any items that require validation by a human and why.\n\n"
    "## Confidence Notes\n"
    "- Provide confidence as High/Med/Low for the overall report and for any major trend.\n"
)

def generate_ai_insights(analysis_summary: dict) -> str:
    if not config.ENABLE_AI:
        return "AI insights disabled (ENABLE_AI=false)."

    if not config.OPENAI_API_KEY:
        return "OPENAI_API_KEY not set. Add it to .env to enable AI insights."

    client = OpenAI(api_key=config.OPENAI_API_KEY)

    payload = json.dumps(analysis_summary, indent=2)

    response = client.responses.create(
        model=config.OPENAI_MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": f"Analysis summary JSON:\n{payload}"},
        ],
        max_output_tokens=config.MAX_OUTPUT_TOKENS,
    )

    return response.output_text
