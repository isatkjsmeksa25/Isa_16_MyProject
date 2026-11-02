"""Mesin rekomendasi resep MenuKu.

Modul ini hanya menentukan resep yang cocok dan urutannya. Tidak mengubah
data resep, alias, atau aturan keselamatan pangan.
"""

from dataclasses import dataclass

from food_safety import (
    ONLY_RISKY_MESSAGE,
    check_ingredients,
    matchable_ingredients,
)
from ingredients import normalize_ingredient
from recipe_data import RECIPES


@dataclass
class RecipeRecommendation:
    recipe: dict
    matched_main: list[str]
    missing_main: list[str]
    matched_supporting: list[str]
    missing_supporting: list[str]
    matched_optional: list[str]
    matched_ingredients: list[str]
    missing_ingredients: list[str]


class RecommendationResult(list):
    def __init__(
        self,
        recommendations=(),
        safety_report=None,
        warnings=(),
        only_risky=False,
        message=None,
    ):
        super().__init__(recommendations)
        self.safety_report = safety_report
        self.warnings = warnings
        self.only_risky = only_risky
        self.message = message

    @property
    def recommendations(self):
        return self

    @property
    def count(self):
        return len(self)


def _group_matches(recipe, group_name, available):
    values = recipe.get(group_name, []) or []
    canonical_values = [normalize_ingredient(item) for item in values]
    matched = [item for item in canonical_values if item in available]
    missing = [item for item in canonical_values if item not in available]
    return matched, missing


def recommend_recipes(available_ingredients, recipes=RECIPES):
    """Rekomendasikan resep berdasarkan bahan aman yang tersedia."""
    safety_report = check_ingredients(available_ingredients)
    available = set(matchable_ingredients(available_ingredients))

    if safety_report.only_risky:
        result = RecommendationResult(
            [],
            safety_report=safety_report,
            warnings=safety_report.warnings,
            only_risky=True,
            message=ONLY_RISKY_MESSAGE,
        )
        return result

    recommendations = []

    for recipe in recipes:
        matched_main, missing_main = _group_matches(
            recipe, "main", available
        )
        matched_supporting, missing_supporting = _group_matches(
            recipe, "supporting", available
        )
        matched_optional, _ = _group_matches(recipe, "optional", available)

        if not matched_main:
            continue

        matched_ingredients = matched_main + matched_supporting
        missing_ingredients = missing_main + missing_supporting

        recommendations.append(
            RecipeRecommendation(
                recipe=recipe,
                matched_main=matched_main,
                missing_main=missing_main,
                matched_supporting=matched_supporting,
                missing_supporting=missing_supporting,
                matched_optional=matched_optional,
                matched_ingredients=matched_ingredients,
                missing_ingredients=missing_ingredients,
            )
        )

    recommendations.sort(
        key=lambda item: (
            -len(item.matched_main),
            -len(item.matched_supporting),
            -len(item.matched_ingredients),
            len(item.missing_ingredients),
            -len(item.matched_optional),
            item.recipe["name"],
        )
    )

    result = RecommendationResult(
        recommendations,
        safety_report=safety_report,
        warnings=safety_report.warnings,
        only_risky=False,
        message=None,
    )
    return result