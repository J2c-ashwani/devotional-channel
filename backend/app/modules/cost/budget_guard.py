from typing import Dict, Any
from backend.app.config import settings

class BudgetGuard:
    """
    Module Q: Budget Guardrail & Hard Ceiling Enforcer.
    """

    MONTHLY_BUDGET_USD = settings.MONTHLY_BUDGET_USD

    @classmethod
    def check_budget_availability(cls, current_monthly_spend: float, estimated_new_job_cost: float = 0.50) -> Dict[str, Any]:
        projected_spend = current_monthly_spend + estimated_new_job_cost
        pct_used = (current_monthly_spend / cls.MONTHLY_BUDGET_USD) * 100.0
        
        is_allowed = projected_spend <= cls.MONTHLY_BUDGET_USD
        warning_triggered = pct_used >= settings.COST_ALERT_THRESHOLD_PCT

        return {
            "allowed": is_allowed,
            "monthly_budget_usd": cls.MONTHLY_BUDGET_USD,
            "current_spend_usd": round(current_monthly_spend, 2),
            "percentage_used": round(pct_used, 1),
            "warning_threshold_exceeded": warning_triggered,
            "reason": None if is_allowed else f"Monthly spend ceiling of ${cls.MONTHLY_BUDGET_USD} exceeded. Production halted to prevent overruns."
        }
