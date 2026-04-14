"""
Skill Registry Module.

Provides dynamic loading and centralized management of agent skills from YAML configurations.
This allows the stateful graph to inject localized expert knowledge (e.g., SQL syntax,
geospatial rules) into the LLM context on-demand, improving modularity and prompt efficiency.
"""

from pathlib import Path

import yaml

SKILLS_DIR = Path(__file__).parent


def load_skill_from_yaml(filename: str) -> dict[str, str]:
    """
    Loads and parses a skill definition from a local YAML file.

    Args:
        filename: The name of the YAML file (e.g., 'sql_query_expert.yaml').

    Returns:
        The parsed skill configuration containing metadata like 'name',
        'description', and 'content'.
    """
    with open(SKILLS_DIR / filename, encoding="utf-8") as f:
        return yaml.safe_load(f)


# Centralized catalog of available skills loaded dynamically into memory.
SKILLS_CATALOG: list[dict[str, str]] = [
    load_skill_from_yaml("sql_query_expert.yaml"),
    load_skill_from_yaml("guadalajara_geo_resolver.yaml"),
]
