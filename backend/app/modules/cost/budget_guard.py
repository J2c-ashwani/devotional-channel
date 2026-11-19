from typing import Dict, Any, Optional
from backend.app.config import settings
from backend.app.modules.cost.tracker import CostTracker

class BudgetGuard:
    """
    Module Q: Budget Guardrail & Hard Ceiling Enforcer.
    Reads actual persisted monthly spend from CostTracker when not explicitly provided.
    """

    MONTHLY_BUDGET_USD = settings.MONTHLY_BUDGET_USD

    @classmethod
    def check_budget_availability(
        cls,
        current_monthly_spend: Optional[float] = None,
        estimated_new_job_cost: float = 0.50
    ) -> Dict[str, Any]:
        monthly_budget = float(settings.MONTHLY_BUDGET_USD)
        spend = CostTracker.get_monthly_spend() if current_monthly_spend is None else float(current_monthly_spend)
        projected_spend = spend + estimated_new_job_cost
        pct_used = (spend / monthly_budget) * 100.0 if monthly_budget > 0 else 100.0

        is_allowed = projected_spend <= monthly_budget
        warning_triggered = pct_used >= settings.COST_ALERT_THRESHOLD_PCT

        return {
            "allowed": is_allowed,
            "monthly_budget_usd": monthly_budget,
            "current_spend_usd": round(spend, 4),
            "projected_spend_usd": round(projected_spend, 4),
            "percentage_used": round(pct_used, 1),
            "warning_threshold_exceeded": warning_triggered,
            "reason": None if is_allowed else f"Monthly spend ceiling of ${monthly_budget:.2f} exceeded (current: ${spend:.2f}, projected: ${projected_spend:.2f}). Production halted to prevent overruns."
        }
