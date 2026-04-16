from __future__ import annotations

import json
from typing import Iterable

import pandas as pd

from config import OPENAI_API_KEY, OPENAI_MODEL

def ask_openai(question: str) -> str:
    qa_context = build_qa_context()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert QA reporting assistant. "
                    "Answer only from the QA context provided. "
                    "Do not make up information that is not present in the context. "
                    "If the answer is not available, say that the information is not present "
                    "in the current dashboard data. "
                    "Highlight risks, blockers, low pass rates, high defect counts, "
                    "pending scope, deferred cycles, and release readiness concerns when relevant."
                ),
            },
            {
                "role": "system",
                "content": f"QA Dashboard Context:\n{qa_context}",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content or "No response returned."

def is_openai_configured(api_key: str | None = None) -> bool:
    return bool((api_key or OPENAI_API_KEY).strip())


def _get_client(api_key: str | None = None):
    from openai import OpenAI

    key = (api_key or OPENAI_API_KEY).strip()
    if not key:
        raise ValueError("OpenAI API key is not configured.")
    return OpenAI(api_key=key)


def dataframe_to_records(df: pd.DataFrame, limit: int = 50) -> list[dict]:
    if df.empty:
        return []
    trimmed = df.head(limit).copy()
    for col in trimmed.columns:
        trimmed[col] = trimmed[col].astype(str)
    return trimmed.to_dict(orient="records")


def build_ai_context(dataset: dict) -> str:
    context = {
        "kpis": dataset["kpis"],
        "cycles": dataframe_to_records(dataset["cycles"]),
        "defects": dataframe_to_records(dataset["defects"], limit=100),
        "defects_per_cycle": dataframe_to_records(dataset["defects_per_cycle"]),
        "defect_status": dataframe_to_records(dataset["defect_status"]),
        "root_cause": dataframe_to_records(dataset["root_cause"]),
        "weekly_discovery": dataframe_to_records(dataset["weekly_discovery"]),
    }
    return json.dumps(context, indent=2)


def generate_program_analysis(dataset: dict, api_key: str | None = None) -> str:
    client = _get_client(api_key)
    context = build_ai_context(dataset)
    system_prompt = (
        "You are a senior QA test director and data analyst. "
        "Analyze QA dashboard data and produce concise executive insights. "
        "Focus on execution, pass rate, defect risk, error discovery trend, coverage, blockers, release readiness, "
        "and specific recommended actions. Use headings and bullets. Avoid hallucinations. Use only the provided data."
    )
    user_prompt = (
        "Analyze this QA reporting dataset. Include: 1) executive summary, 2) key risks, 3) strengths, "
        "4) release-readiness view, 5) recommended next actions, and 6) notable anomalies.\n\n"
        f"DATA:\n{context}"
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.output_text.strip()


def ask_dashboard_chat(
    user_question: str,
    dataset: dict,
    history: Iterable[dict[str, str]] | None = None,
    api_key: str | None = None,
) -> str:
    client = _get_client(api_key)
    context = build_ai_context(dataset)
    messages: list[dict] = [
        {
            "role": "system",
            "content": (
                "You are a QA reporting copilot. Answer questions about the dashboard, explain metrics, compare cycles, "
                "identify risks, and recommend actions based only on the provided data. Be practical and concise."
            ),
        },
        {
            "role": "user",
            "content": f"Here is the current QA dashboard dataset in JSON:\n{context}",
        },
    ]
    if history:
        for item in history:
            role = item.get("role", "user")
            content = item.get("content", "")
            if content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_question})

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=messages,
        temperature=0.2,
    )
    return response.output_text.strip()
