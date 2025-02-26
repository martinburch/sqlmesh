from __future__ import annotations


from sqlmesh.core.config.linter import LinterConfig

from sqlmesh.core.model import Model

from sqlmesh.utils.errors import raise_config_error
from sqlmesh.core.console import get_console
from sqlmesh.core.linter.rule import RuleSet

from sqlmesh.core.config.linter import RuleListType


def gather_rules(all_rules: RuleSet, rule_names: RuleListType) -> RuleSet:
    if rule_names == "ALL":
        rule_names = list(all_rules.keys())

    rules = set()
    for rule_name in rule_names:
        if rule_name not in all_rules:
            raise_config_error(f"Rule {rule_name} could not be found")

        rules.add(all_rules[rule_name])

    return RuleSet(rules)


class Linter:
    def fill_from_config(self, all_rules: RuleSet, config: LinterConfig) -> Linter:
        self.all_rules = all_rules

        exclude_rules = gather_rules(self.all_rules, config.exclude_rules)
        included_rules = self.all_rules.difference(exclude_rules)

        self.rules = gather_rules(included_rules, config.rules)
        self.warn_rules = gather_rules(included_rules, config.warn_rules)

        if overlapping := self.rules.intersection(self.warn_rules):
            overlapping_rules = ", ".join(rule for rule in overlapping.keys())
            raise_config_error(f"Found overlapping rules [{overlapping_rules}] in lint config.")

        return self

    def lint_model(self, model: Model) -> None:
        ignored_rules = gather_rules(self.all_rules, model.ignore_lints)

        rules = self.rules.difference(ignored_rules)
        warn_rules = self.warn_rules.difference(ignored_rules)

        error_violations = rules.check_model(model)
        warn_violations = warn_rules.check_model(model)

        if warn_violations:
            warn_msg = "\n".join(str(warn_violation) for warn_violation in warn_violations)
            get_console().log_warning(f"Linter warnings for {model._path}:\n{warn_msg}")

        if error_violations:
            error_msg = "\n".join(str(error_violations) for error_violations in error_violations)

            raise_config_error(f"Linter error for {model._path}:\n{error_msg}")
