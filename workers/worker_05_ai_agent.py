#!/usr/bin/env python3
"""
Worker Camunda - Module 05 : AI Agent avec Groq LLM
Types de jobs : extract-text, ai-analyze, auto-process
Configuration : export GROQ_API_KEY=sk-xxxx
"""
import asyncio
import os
import requests
from datetime import datetime
from pyzeebe import ZeebeWorker, create_insecure_channel

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "mixtral-8x7b-32768"

channel = create_insecure_channel(hostname="localhost", port=26500)
worker = ZeebeWorker(channel)


def call_groq(system_prompt: str, user_message: str) -> str:
    """Appel direct API Groq"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,
        "max_tokens": 512
    }
    resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


@worker.task(task_type="extract-text", timeout_ms=30000)
async def extract_text(documentUrl: str, **kwargs):
    """Simule extraction texte depuis une URL"""
    print(f"[extract-text] Extraction depuis : {documentUrl}")
    # En production : utiliser PyPDF2, pdfplumber, ou requests
    texte = f"Document extrait de {documentUrl} - Contenu exemple pour demonstration Camunda AI."
    return {"texte": texte, "nbMots": len(texte.split())}


@worker.task(task_type="ai-analyze", timeout_ms=60000)
async def ai_analyze(texte: str, analyseType: str = "resume", **kwargs):
    """Analyse AI via Groq LLM"""
    print(f"[ai-analyze] Type={analyseType} | Texte ({len(texte)} chars)")

    system = """Tu es un assistant d'analyse documentaire. Reponds en JSON valide avec les champs :
- resume (string, 2 phrases max)
- sentiment (positif|negatif|neutre)
- score_confiance (float entre 0 et 1)
- mots_cles (liste de 3-5 mots)"""

    user = f"Analyse ce texte ({analyseType}) :\n\n{texte}"

    try:
        response = call_groq(system, user)
        # Nettoyer la reponse JSON
        import json
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        result = json.loads(response)
        print(f"[ai-analyze] Sentiment={result.get('sentiment')} | Confiance={result.get('score_confiance')}")
        return result
    except Exception as e:
        print(f"[ai-analyze] Erreur Groq: {e} - Utilisation valeurs par defaut")
        return {
            "resume": "Analyse non disponible",
            "sentiment": "neutre",
            "score_confiance": 0.5,
            "mots_cles": []
        }


@worker.task(task_type="auto-process", timeout_ms=10000)
async def auto_process(**kwargs):
    """Traitement automatique post-analyse"""
    ref = f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"[auto-process] Traitement automatique : {ref}")
    return {"processedRef": ref, "processedAt": datetime.now().isoformat(), "mode": "automatique"}


async def main():
    print("[Worker 05] AI Agent Groq - 3 job types actifs (extract-text, ai-analyze, auto-process)")
    print(f"[Worker 05] Modele LLM : {MODEL}")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
