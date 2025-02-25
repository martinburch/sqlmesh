"""Contains all the standard rules included with SQLMesh"""

from __future__ import annotations

import typing as t


from sqlmesh.core.linter.rule import Rule, RuleViolation
from sqlmesh.core.model import Model, SqlModel


class NoSelectStar(Rule):
    def check(self, model: Model) -> t.Optional[RuleViolation]:
        if not isinstance(model, SqlModel):
            return None

        return RuleViolation(rule=self, model=model) if model.query.is_star else None

    @property
    def summary(self) -> str:
        return "Query should not contain SELECT * on its outer most projections, even if it can be expanded."


class InvalidSelectStarExpansion(Rule):
    def check(self, model: Model) -> t.Optional[RuleViolation]:
        if not model._render_violations:
            return None

        deps = model._render_violations.get(InvalidSelectStarExpansion)
        if not deps:
            return None

        self._deps = deps
        self._model_fqn = model.fqn
        return RuleViolation(rule=self, model=model)

    @property
    def summary(self) -> str:
        return (
            f"SELECT * cannot be expanded due to missing schema(s) for model(s): {self._deps}. "
            "Run `sqlmesh create_external_models` and / or make sure that the model "
            f"'{self._model_fqn}' can be rendered at parse time."
        )


class AmbiguousOrInvalidColumn(Rule):
    def check(self, model: Model) -> t.Optional[RuleViolation]:
        if not model._render_violations:
            return None

        sqlglot_err = model._render_violations.get(AmbiguousOrInvalidColumn)
        if not sqlglot_err:
            return None

        self._error = sqlglot_err
        self._model_fqn = model.fqn
        return RuleViolation(rule=self, model=model)

    @property
    def summary(self) -> str:
        return f"{self._error} for model '{self._model_fqn}', the column may not exist or is ambiguous."
