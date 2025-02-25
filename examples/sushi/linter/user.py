from __future__ import annotations

import typing as t

from sqlmesh.core.linter.rule import Rule, RuleViolation
from sqlmesh.core.model import Model


class NoMissingOwner(Rule):
    def check(self, model: Model) -> t.Optional[RuleViolation]:
        return RuleViolation(rule=self, model=model) if not model.owner else None

    @property
    def summary(self) -> str:
        return "All models should have an owner."
