from __future__ import annotations

from sqlglot.helper import subclasses

from sqlmesh.core.linter.rule import RuleSet, Rule
from sqlmesh.core.linter.rules.builtin import (
    AmbiguousOrInvalidColumn as AmbiguousOrInvalidColumn,
    InvalidSelectStarExpansion as InvalidSelectStarExpansion,
    NoSelectStar as NoSelectStar,
)

BUILTIN_RULES = RuleSet(subclasses(__name__, Rule, (Rule,)))
