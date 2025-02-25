from __future__ import annotations


from sqlmesh.core.config.linter import LinterConfig

from sqlmesh.core.model import Model

from sqlmesh.utils.errors import raise_config_error
from sqlmesh.core.console import get_console
from sqlmesh.core.linter.rule import RuleSet


class Linter:
    def __init__(self, ALL_RULES: RuleSet, rules: RuleSet, warn_rules: RuleSet) -> None:
        self.ALL_RULES = ALL_RULES
        self.rules = rules
        self.warn_rules = warn_rules

    def lint(self, model: Model) -> None:
        ignored_rules = LinterConfig.gather_rules(self.ALL_RULES, model.ignore_lints)

        rules = self.rules.difference(ignored_rules)
        warn_rules = self.warn_rules.difference(ignored_rules)

        error_violations = rules.check(model)
        warn_violations = warn_rules.check(model)

        if warn_violations:
            warn_msg = "\n".join(warn_violation.message for warn_violation in warn_violations)
            get_console().log_warning(f"Linter warnings for {model._path}:\n{warn_msg}")

        if error_violations:
            error_msg = "\n".join(error_violations.message for error_violations in error_violations)

            raise_config_error(f"Linter error for {model._path}:\n{error_msg}")
