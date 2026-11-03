"""Rekomendasi alternatif berbasis template MenuKu.

Modul ini hanya digunakan sebagai fallback ketika rekomendasi katalog
tidak menghasilkan resep. Modul ini tidak mengubah mesin rekomendasi
katalog yang sudah disetujui.
"""

from dataclasses import dataclass

from food_safety import (
    ONLY_RISKY_MESSAGE,
    check_ingredients,
    matchable_ingredients,
)
from ingredients import normalize_ingredient
from recommendation import RecipeRecommendation, RecommendationResult
from recipe_templates import RECIPE_TEMPLATES


@dataclass(frozen=True)
class TemplateMatch:
    template_id: str
    matched_core: tuple[str, ...]
    matched_supporting: tuple[str, ...]
    matched_optional: tuple[str, ...]


def _match_core_groups(template, available):
    """Kembalikan bahan inti yang cocok, atau None jika ada kelompok kosong."""
    matched_core = []

    for group in template.core_groups:
        group_matches = [
            normalize_ingredient(item)
            for item in group
            if normalize_ingredient(item) in available
        ]
        if not group_matches:
            return None
        matched_core.extend(group_matches)

    # Hilangkan duplikat tanpa mengubah urutan.
    unique_matches = []
    seen = set()
    for item in matched_core:
        if item not in seen:
            seen.add(item)
            unique_matches.append(item)

    return unique_matches


def _build_steps(template, matched_core, matched_supporting, matched_optional):
    """Bangun langkah dinamis hanya dari bahan yang tersedia."""
    steps = []

    if matched_core:
        steps.append("Siapkan " + ", ".join(matched_core) + ".")

    aromatics = [
        item for item in matched_supporting
        if item in ("bawang merah", "bawang putih", "cabai")
    ]
    if aromatics:
        steps.append("Iris " + ", ".join(aromatics) + ".")

    if "minyak" in matched_supporting:
        steps.append("Panaskan minyak.")

    if matched_core:
        steps.append("Masukkan " + ", ".join(matched_core) + ", aduk rata.")

    seasonings = [
        item for item in matched_supporting
        if item in ("kecap", "garam")
    ]
    if seasonings:
        steps.append("Tambahkan " + ", ".join(seasonings) + ", masak sebentar.")

    if matched_optional:
        steps.append("Jika ada, tambahkan " + ", ".join(matched_optional) + ".")

    steps.append("Sajikan.")
    return steps


def recommend_template_recipes(available_ingredients, templates=RECIPE_TEMPLATES):
    """Rekomendasikan template berdasarkan bahan aman yang tersedia."""
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
        result.source = "template"
        return result

    recommendations = []

    for template in templates:
        matched_core = _match_core_groups(template, available)
        if matched_core is None:
            continue

        matched_supporting = [
            normalize_ingredient(item)
            for item in template.supporting_ingredients
            if normalize_ingredient(item) in available
        ]
        missing_supporting = [
            normalize_ingredient(item)
            for item in template.supporting_ingredients
            if normalize_ingredient(item) not in available
        ]
        matched_optional = [
            normalize_ingredient(item)
            for item in template.optional_ingredients
            if normalize_ingredient(item) in available
        ]

        matched_ingredients = matched_core + matched_supporting
        missing_ingredients = missing_supporting

        recipe = {
            "id": "alternatif-" + template.id,
            "name": template.name,
            "description": None,
            "main": list(matched_core),
            "supporting": list(template.supporting_ingredients),
            "optional": list(matched_optional),
            "steps": _build_steps(
                template,
                matched_core,
                matched_supporting,
                matched_optional,
            ),
            "quantities": None,
            "cook_time_minutes": None,
            "servings": None,
            "photo": None,
            "tips": None,
            "source": None,
            "safety_notes": [],
        }

        recommendations.append(
            RecipeRecommendation(
                recipe=recipe,
                matched_main=list(matched_core),
                missing_main=[],
                matched_supporting=list(matched_supporting),
                missing_supporting=list(missing_supporting),
                matched_optional=list(matched_optional),
                matched_ingredients=list(matched_ingredients),
                missing_ingredients=list(missing_ingredients),
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
    result.source = "template"
    return result


def recommend_with_fallback(available_ingredients, recipes=None, templates=RECIPE_TEMPLATES):
    """Jalankan katalog dulu; template hanya fallback."""
    from recipe_data import RECIPES
    from recommendation import recommend_recipes

    if recipes is None:
        recipes = RECIPES

    catalog_result = recommend_recipes(available_ingredients, recipes=recipes)

    if catalog_result.only_risky:
        catalog_result.source = "catalog"
        return catalog_result

    if catalog_result:
        catalog_result.source = "catalog"
        return catalog_result

    template_result = recommend_template_recipes(
        available_ingredients,
        templates=templates,
    )
    template_result.source = "template"
    return template_result


# Alias untuk kompatibilitas nama fungsi.
recommend_templates = recommend_template_recipes
recommend_alternatives = recommend_template_recipes
recommend_alternative_recipes = recommend_template_recipes
