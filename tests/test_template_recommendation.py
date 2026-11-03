import unittest

from food_safety import ONLY_RISKY_MESSAGE
from recipe_data import RECIPES, required_ingredients
from recipe_templates import RECIPE_TEMPLATES
from template_recommendation import (
    recommend_template_recipes,
    recommend_with_fallback,
)


def template_by_id(template_id):
    for template in RECIPE_TEMPLATES:
        if template.id == template_id:
            return template
    raise ValueError(template_id)


class TemplateRecommendationTests(unittest.TestCase):
    def test_all_core_groups_must_be_satisfied(self):
        result = recommend_template_recipes(["tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertEqual(tumis.matched_main, ["tahu", "tempe"])
        self.assertEqual(tumis.missing_main, [])

    def test_one_alternative_in_group_is_enough(self):
        result = recommend_template_recipes(["kangkung"])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].recipe["name"], "Tumis Sayur Sederhana")
        self.assertEqual(result[0].matched_main, ["kangkung"])

    def test_multiple_alternatives_in_group_can_match(self):
        result = recommend_template_recipes(["kangkung", "kol"])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].matched_main, ["kangkung", "kol"])

    def test_missing_required_core_group_returns_no_template(self):
        result = recommend_template_recipes(["tahu"])

        names = [item.recipe["name"] for item in result]
        self.assertNotIn("Tumis Tahu Tempe", names)

    def test_alias_is_used(self):
        result = recommend_template_recipes(["brambang", "tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertIn("bawang merah", tumis.matched_supporting)

    def test_duplicate_input_does_not_duplicate_matches(self):
        result = recommend_template_recipes(["tahu", "tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertEqual(tumis.matched_main, ["tahu", "tempe"])
        self.assertEqual(tumis.matched_ingredients.count("tahu"), 1)

    def test_risky_ingredients_are_never_matched(self):
        result = recommend_template_recipes(["keong", "tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertEqual(tumis.matched_main, ["tahu", "tempe"])
        self.assertNotIn("keong", tumis.matched_ingredients)
        self.assertTrue(result.safety_report.has_risky)

    def test_only_risky_input_returns_empty_result(self):
        result = recommend_template_recipes(["keong", "fugu"])

        self.assertEqual(result, [])
        self.assertTrue(result.only_risky)
        self.assertTrue(result.warnings)
        self.assertEqual(result.message, ONLY_RISKY_MESSAGE)

    def test_missing_supporting_does_not_fail_template(self):
        result = recommend_template_recipes(["tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertTrue(tumis.missing_supporting)

    def test_required_ingredients_include_unavailable_supporting(self):
        result = recommend_template_recipes(["tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )

        self.assertEqual(
            required_ingredients(tumis.recipe),
            tumis.recipe["main"] + tumis.recipe["supporting"],
        )
        self.assertGreater(
            len(tumis.recipe["supporting"]),
            len(tumis.matched_supporting),
        )
        self.assertTrue(tumis.missing_supporting)

    def test_missing_optional_is_not_required(self):
        result = recommend_template_recipes(["tahu", "tempe"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        self.assertEqual(tumis.matched_optional, [])

    def test_dynamic_steps_do_not_require_unavailable_ingredients(self):
        result = recommend_template_recipes(["tahu", "tempe"])
        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        steps_text = " ".join(tumis.recipe["steps"]).lower()

        self.assertNotIn("minyak", steps_text)
        self.assertNotIn("kecap", steps_text)
        self.assertNotIn("garam", steps_text)

    def test_dynamic_steps_include_available_optional(self):
        result = recommend_template_recipes(["tahu", "tempe", "cabai"])
        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Tahu Tempe"
        )
        steps_text = " ".join(tumis.recipe["steps"]).lower()

        self.assertIn("cabai", steps_text)

    def test_template_not_used_when_catalog_has_result(self):
        result = recommend_with_fallback(["nasi", "telur"])

        self.assertEqual(getattr(result, "source", None), "catalog")
        self.assertGreater(len(result), 0)
        self.assertTrue(any("Nasi Goreng" in item.recipe["name"] for item in result))

    def test_template_used_when_catalog_is_empty(self):
        result = recommend_with_fallback(
            ["brambang", "tahu", "tempe", "kecap", "saus"],
            recipes=[],
        )

        self.assertEqual(getattr(result, "source", None), "template")
        self.assertGreater(len(result), 0)

    def test_no_result_when_catalog_and_template_are_empty(self):
        result = recommend_with_fallback(["xyz"])

        self.assertEqual(result, [])
        self.assertFalse(result.only_risky)

    def test_empty_input_preserves_old_behavior(self):
        result = recommend_with_fallback([])

        self.assertEqual(result, [])
        self.assertFalse(result.only_risky)

    def test_safety_information_types(self):
        result = recommend_template_recipes(["tahu", "tempe"])

        self.assertIsInstance(result.warnings, tuple)
        self.assertIsInstance(result.only_risky, bool)
        self.assertIsNotNone(result.safety_report)


if __name__ == "__main__":
    unittest.main()
