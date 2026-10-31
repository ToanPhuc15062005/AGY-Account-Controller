"""Account-model quota and cooldown tracker according to v1.1 Architecture Spec."""

import datetime
from typing import Optional, List, Dict, Any
from ..storage.repositories.resource_repo import ResourceRepository
from ..config import QuotaConfig


class QuotaTracker:
    """Manages resource cooldown states scoped to (account_id, model_key)."""

    def __init__(self, resource_repo: ResourceRepository, config: Optional[QuotaConfig] = None):
        self.resource_repo = resource_repo
        self.config = config or QuotaConfig()

    def record_quota_exhaustion(
        self,
        account_id: str,
        model_key: str,
        retry_after_seconds: Optional[int] = None,
        reason: str = "Quota limit reached",
        source: str = "structured",
    ) -> str:
        """Sets cooldown for the specific (account_id, model_key) pair."""
        cooldown_sec = retry_after_seconds or self.config.cooldown.fallback_seconds
        until = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=cooldown_sec)
        ).isoformat()

        self.resource_repo.set_account_model_cooldown(
            account_id=account_id,
            model_key=model_key,
            cooldown_until=until,
            cooldown_reason=reason,
            cooldown_source=source,
            retry_after_seconds=retry_after_seconds,
            last_error_code="QUOTA_EXHAUSTED",
        )
        return until

    def is_available(self, account_id: str, model_key: str) -> bool:
        """Checks if the account is currently usable for the requested model."""
        return not self.resource_repo.is_in_cooldown(account_id, model_key)

    def select_eligible_account(
        self,
        model_key: str,
        candidate_accounts: List[str],
    ) -> Optional[str]:
        """Finds the first candidate account that is not under active cooldown for this model."""
        for acc in candidate_accounts:
            if self.is_available(acc, model_key):
                return acc
        return None

    def clear_cooldown(self, account_id: str, model_key: str) -> bool:
        return self.resource_repo.clear_account_model_cooldown(account_id, model_key)
