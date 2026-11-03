import unittest

from food_safety import ONLY_RISKY_MESSAGE
from recipe_data import RECIPES
from recommendation import (
    RecommendationResult,
    RecipeRecommendation,
    recommend_recipes,
)


def recipe_by_name(name):
    for recipe in RECIPES:
        if recipe["name"] == name:
            return recipe
    raise ValueError(name)


class RecommendationTests(unittest.TestCase):
    def test_one_main_ingredient_matches(self):
        result = recommend_recipes(["nasi"])

        self.assertIsInstance(result, RecommendationResult)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].recipe["name"], "Nasi Goreng Sederhana")
        self.assertEqual(result[0].matched_main, ["nasi"])
        self.assertEqual(result[0].missing_main, ["telur"])
        self.assertEqual(result[0].matched_supporting, [])
        self.assertEqual(
            result[0].missing_supporting,
            ["bawang putih", "bawang merah", "kecap", "garam"],
        )
        self.assertEqual(result[0].matched_optional, [])
        self.assertEqual(result[0].matched_ingredients, ["nasi"])
        self.assertEqual(
            result[0].missing_ingredients,
            ["telur", "bawang putih", "bawang merah", "kecap", "garam"],
        )

    def test_all_main_ingredients_match(self):
        result = recommend_recipes(["nasi", "telur"])

        nasi_goreng = next(
            item for item in result
            if item.recipe["name"] == "Nasi Goreng Sederhana"
        )
        self.assertEqual(nasi_goreng.matched_main, ["nasi", "telur"])
        self.assertEqual(nasi_goreng.missing_main, [])

    def test_partial_main_ingredients_match(self):
        result = recommend_recipes(["telur"])

        names = [item.recipe["name"] for item in result]
        self.assertIn("Telur Kecap", names)
        self.assertIn("Mi Telur", names)
        self.assertIn("Telur Dadar", names)
        self.assertIn("Nasi Goreng Sederhana", names)

        for item in result:
            self.assertEqual(item.matched_main, ["telur"])

        self.assertTrue(
            any(item.missing_main for item in result)
        )

    def test_ranking_by_main_then_supporting(self):
        result = recommend_recipes(["telur", "bawang putih"])

        names = [item.recipe["name"] for item in result]
        self.assertEqual(names[:2], ["Mi Telur", "Mi Goreng"])
        self.assertIn("Telur Kecap", names)
        self.assertIn("Nasi Goreng Sederhana", names)
        self.assertIn("Telur Dadar", names)

        nasi = next(
            item for item in result
            if item.recipe["name"] == "Nasi Goreng Sederhana"
        )
        self.assertEqual(nasi.matched_main, ["telur"])
        self.assertEqual(nasi.matched_supporting, ["bawang putih"])
        self.assertEqual(nasi.missing_ingredients, [
            "nasi", "bawang merah", "kecap", "garam"
        ])

    def test_optional_ingredients_are_bonus_only(self):
        recipes = [
            {
                "id": "resep-a",
                "name": "Resep A",
                "main": ["telur"],
                "supporting": ["garam"],
                "optional": ["daun bawang"],
                "steps": ["Masak."],
            },
            {
                "id": "resep-b",
                "name": "Resep B",
                "main": ["telur"],
                "supporting": ["garam"],
                "optional": [],
                "steps": ["Masak."],
            },
        ]

        result = recommend_recipes(
            ["telur", "garam", "daun bawang"],
            recipes=recipes,
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].recipe["name"], "Resep A")
        self.assertEqual(result[0].matched_optional, ["daun bawang"])
        self.assertEqual(result[1].recipe["name"], "Resep B")
        self.assertEqual(result[1].matched_optional, [])

    def test_recipe_without_matching_main_is_not_recommended(self):
        result = recommend_recipes(["garam"])

        self.assertEqual(result, [])
        self.assertFalse(result.only_risky)
        self.assertEqual(result.warnings, ())

    def test_missing_ingredients_are_calculated(self):
        result = recommend_recipes(["kangkung", "cabai"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Kangkung"
        )
        self.assertEqual(tumis.matched_main, ["kangkung"])
        self.assertEqual(tumis.missing_main, [])
        self.assertEqual(tumis.matched_supporting, ["cabai"])
        self.assertEqual(
            tumis.missing_supporting,
            ["bawang putih", "garam", "minyak"],
        )
        self.assertEqual(
            tumis.missing_ingredients,
            ["bawang putih", "garam", "minyak"],
        )

    def test_aliases_are_used(self):
        result = recommend_recipes(["mie", "telur"])

        mi_telur = next(
            item for item in result
            if item.recipe["name"] == "Mi Telur"
        )
        self.assertEqual(mi_telur.matched_main, ["mi", "telur"])
        self.assertEqual(mi_telur.missing_main, [])

    def test_risky_ingredients_are_never_matched(self):
        result = recommend_recipes(["keong", "kangkung", "cabai"])

        tumis = next(
            item for item in result
            if item.recipe["name"] == "Tumis Kangkung"
        )
        self.assertEqual(tumis.matched_main, ["kangkung"])
        self.assertEqual(tumis.matched_supporting, ["cabai"])
        self.assertNotIn("keong", tumis.matched_ingredients)
        self.assertNotIn("keong", tumis.matched_supporting)
        self.assertTrue(result.safety_report.has_risky)

    def test_only_risky_input_returns_empty_result(self):
        result = recommend_recipes(["keong", "fugu"])

        self.assertEqual(result, [])
        self.assertTrue(result.only_risky)
        self.assertTrue(result.warnings)
        self.assertEqual(result.message, ONLY_RISKY_MESSAGE)

    def test_mixed_safe_and_risky_input_uses_safe_only(self):
        result = recommend_recipes(["keong", "telur"])

        self.assertGreater(len(result), 0)
        for item in result:
            self.assertNotIn("keong", item.matched_ingredients)
        self.assertTrue(result.safety_report.has_risky)
        self.assertTrue(result.safety_report.has_safe)
        self.assertFalse(result.only_risky)

    def test_deterministic_tie_break_by_recipe_name(self):
        recipes = [
            {
                "id": "zeta",
                "name": "Zeta",
                "main": ["telur"],
                "supporting": ["garam"],
                "optional": [],
                "steps": ["Masak."],
            },
            {
                "id": "alpha",
                "name": "Alpha",
                "main": ["telur"],
                "supporting": ["garam"],
                "optional": [],
                "steps": ["Masak."],
            },
        ]

        result = recommend_recipes(["telur", "garam"], recipes=recipes)

        self.assertEqual(
            [item.recipe["name"] for item in result],
            ["Alpha", "Zeta"],
        )

    def test_recommendations_is_same_object_as_result(self):
        result = recommend_recipes(["telur"])

        self.assertIs(result.recommendations, result)

    def test_ranking_by_missing_required_count(self):
        recipes = [
            {
                "id": "sedikit-kurang",
                "name": "Sedikit Kurang",
                "main": ["telur"],
                "supporting": ["garam"],
                "optional": [],
                "steps": ["Masak."],
            },
            {
                "id": "banyak-kurang",
                "name": "Banyak Kurang",
                "main": ["telur"],
                "supporting": ["garam", "kecap"],
                "optional": [],
                "steps": ["Masak."],
            },
        ]

        result = recommend_recipes(["telur", "garam"], recipes=recipes)

        self.assertEqual(
            [item.recipe["name"] for item in result],
            ["Sedikit Kurang", "Banyak Kurang"],
        )

    def test_safety_information_types(self):
        result = recommend_recipes(["telur"])

        self.assertIsInstance(result.warnings, tuple)
        self.assertIsInstance(result.only_risky, bool)
        self.assertIsNotNone(result.safety_report)


if __name__ == "__main__":
    unittest.main()
