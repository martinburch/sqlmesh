from __future__ import annotations


from sqlmesh.core.config.base import BaseConfig
from sqlmesh.core.model.meta import RuleListType


class LinterConfig(BaseConfig):
    """Configuration for model linting

    Args:
        enabled: Flag indicating whether the linter should run

        rules: A list of error rules to be applied on model
        warn_rules: A list of rules to be applied on models but produce warnings instead of raising errors.
        exclude_rules: A list of rules to be excluded/ignored

    """

    enabled: bool = False

    rules: RuleListType = []
    warn_rules: RuleListType = []
    exclude_rules: RuleListType = []
