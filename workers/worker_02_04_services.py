#!/usr/bin/env python3
"""
Worker Camunda - Modules 02, 03, 04
Gere les Service Tasks des processus commande + credit + conge
Types de jobs : check-stock, calculate-price, send-confirmation,
                evaluate-score, approve-credit, manual-review, reject-credit,
                check-leave-balance, notify-employee
"""
import asyncio
import random
from datetime import datetime
from pyzeebe import ZeebeWorker, create_insecure_channel

channel = create_insecure_channel(hostname="localhost", port=26500)
worker = ZeebeWorker(channel)


# ── Module 02 : Commande ────────────────────────────────────────────
@worker.task(task_type="check-stock", timeout_ms=10000)
async def check_stock(productId: str, **kwargs):
    stock = random.randint(0, 100)
    print(f"[check-stock] Product={productId} | Stock={stock}")
    return {"stockAvailable": stock > 0, "stockQty": stock}


@worker.task(task_type="calculate-price", timeout_ms=10000)
async def calculate_price(quantity: int, unitPrice: float, **kwargs):
    total = round(quantity * unitPrice * 1.20, 2)  # TVA 20%
    print(f"[calculate-price] qty={quantity} x {unitPrice}€ = {total}€ TTC")
    return {"totalPrice": total}


@worker.task(task_type="send-confirmation", timeout_ms=10000)
async def send_confirmation(**kwargs):
    ref = f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"[send-confirmation] Confirmation envoyee : {ref}")
    return {"confirmationRef": ref, "status": "confirmed"}


# ── Module 03 : Credit ──────────────────────────────────────────────
@worker.task(task_type="evaluate-score", timeout_ms=10000)
async def evaluate_score(montant: float, revenu: float, **kwargs):
    ratio = montant / revenu if revenu > 0 else 1
    score = max(300, min(850, int(850 - (ratio * 300))))
    print(f"[evaluate-score] montant={montant} / revenu={revenu} => score={score}")
    return {"score": score}


@worker.task(task_type="approve-credit", timeout_ms=10000)
async def approve_credit(**kwargs):
    print("[approve-credit] Credit APPROUVE automatiquement")
    return {"resultat": "approuve", "tauxInteret": 2.5}


@worker.task(task_type="manual-review", timeout_ms=10000)
async def manual_review(**kwargs):
    print("[manual-review] Dossier transmis pour revue manuelle")
    return {"resultat": "en_revue"}


@worker.task(task_type="reject-credit", timeout_ms=10000)
async def reject_credit(**kwargs):
    print("[reject-credit] Credit REFUSE")
    return {"resultat": "refuse"}


# ── Module 04 : Conge ───────────────────────────────────────────────
@worker.task(task_type="check-leave-balance", timeout_ms=10000)
async def check_leave_balance(employeeId: str, nbJours: int, **kwargs):
    solde = random.randint(5, 30)
    print(f"[check-leave-balance] Employee={employeeId} | Solde={solde}j | Demande={nbJours}j")
    return {"soldeDisponible": solde, "suffisant": solde >= nbJours}


@worker.task(task_type="notify-employee", timeout_ms=10000)
async def notify_employee(**kwargs):
    print(f"[notify-employee] Notification envoyee | Variables: {kwargs}")
    return {"notified": True, "notifiedAt": datetime.now().isoformat()}


async def main():
    print("[Workers 02-04] Demarrage - 9 types de jobs actifs...")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
