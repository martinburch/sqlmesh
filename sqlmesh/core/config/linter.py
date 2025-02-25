from __future__ import annotations

import typing as t

from sqlmesh.core.config.base import BaseConfig
from sqlmesh.utils.errors import raise_config_error
from sqlmesh.core.linter.rule import RuleSet
from sqlmesh.core.linter.rules.builtin import (
    InvalidSelectStarExpansion,
    AmbiguousOrInvalidColumn,
    NoSelectStar,
)
from sqlmesh.core.model.meta import RuleListType


class LinterConfig(BaseConfig):
    """Configuration for model linting

    Args:
        enabled: Flag indicating whether the linter should run

        rules: A list of error rules to be applied on model
        warn_rules: A list of rules to be applied on models but produce warnings instead of raising errors.
        exclude_rules: A list of rules to be excluded/ignored

    """

    enabled: bool = True

    rules: RuleListType = []
    warn_rules: RuleListType = []
    exclude_rules: RuleListType = []

    @classmethod
    def gather_rules(self, ALL_RULES: RuleSet, rule_names: RuleListType) -> RuleSet:
        if rule_names == "ALL":
            rule_names = list(ALL_RULES.keys())

        rs = RuleSet()

        for rule_name in rule_names:
            if rule_name not in ALL_RULES:
                raise_config_error(f"Rule {rule_name} could not be found")

            rs[rule_name] = ALL_RULES[rule_name]

        return rs

    def fill_rules(self, ALL_RULES: RuleSet) -> t.Tuple[RuleSet, RuleSet]:
        rules = LinterConfig.gather_rules(ALL_RULES, self.rules)
        warn_rules = LinterConfig.gather_rules(ALL_RULES, self.warn_rules)
        exclude_rules = LinterConfig.gather_rules(ALL_RULES, self.exclude_rules)

        if overlapping := rules.intersection(warn_rules):
            raise_config_error(f"Found overlapping rules {overlapping} in lint config.")

        all_defined_rules = rules.union(warn_rules, exclude_rules)

        builtin_warn_rules = RuleSet.from_args(
            AmbiguousOrInvalidColumn, InvalidSelectStarExpansion
        ).difference(all_defined_rules)
        builtin_exclude_rules = RuleSet.from_args(NoSelectStar).difference(all_defined_rules)

        if not warn_rules:
            warn_rules = builtin_warn_rules

        if not exclude_rules:
            exclude_rules = builtin_exclude_rules

        return rules, warn_rules
