import unittest

from recipe_data import RECIPES, required_ingredients
from tests.legacy_recipe_data import LEGACY_RECIPES


class RecipeDataTests(unittest.TestCase):
    def test_recipe_ids_are_unique(self):
        ids = [recipe["id"] for recipe in RECIPES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_are_present(self):
        fields = {
            "id",
            "name",
            "description",
            "main",
            "supporting",
            "optional",
            "steps",
            "quantities",
            "cook_time_minutes",
            "servings",
            "photo",
            "tips",
            "source",
            "safety_notes",
        }
        for recipe in RECIPES:
            self.assertEqual(set(recipe), fields, recipe["name"])

    def test_ingredient_groups_are_valid(self):
        for recipe in RECIPES:
            main = recipe["main"]
            supporting = recipe["supporting"]
            optional = recipe["optional"]

            self.assertTrue(main, recipe["name"])
            self.assertTrue(supporting, recipe["name"])
            self.assertTrue(
                all(isinstance(item, str) and item.strip() for item in main)
            )
            self.assertTrue(
                all(isinstance(item, str) and item.strip() for item in supporting)
            )
            self.assertTrue(
                all(isinstance(item, str) and item.strip() for item in optional)
            )

            self.assertFalse(set(main) & set(supporting), recipe["name"])
            self.assertFalse(set(main) & set(optional), recipe["name"])
            self.assertFalse(set(supporting) & set(optional), recipe["name"])

    def test_steps_are_available(self):
        for recipe in RECIPES:
            self.assertTrue(recipe["steps"], recipe["name"])
            self.assertTrue(
                all(isinstance(step, str) and step.strip() for step in recipe["steps"])
            )

    def test_unknown_data_is_marked_as_unavailable(self):
        for recipe in RECIPES:
            self.assertIsNone(recipe["description"], recipe["name"])
            self.assertIsNone(recipe["quantities"], recipe["name"])
            self.assertIsNone(recipe["cook_time_minutes"], recipe["name"])
            self.assertIsNone(recipe["servings"], recipe["name"])
            self.assertIsNone(recipe["photo"], recipe["name"])
            self.assertIsNone(recipe["tips"], recipe["name"])
            self.assertIsNone(recipe["source"], recipe["name"])
            self.assertEqual(recipe["safety_notes"], [], recipe["name"])

    def test_required_ingredients_combine_main_and_supporting(self):
        for recipe in RECIPES:
            combined = required_ingredients(recipe)
            self.assertEqual(
                combined,
                recipe["main"] + recipe["supporting"],
                recipe["name"],
            )
            self.assertEqual(len(combined), len(set(combined)), recipe["name"])

    def test_recipes_match_legacy_data(self):
        self.assertEqual(len(RECIPES), len(LEGACY_RECIPES))

        for current, legacy in zip(RECIPES, LEGACY_RECIPES):
            current_ingredients = (
                current["main"] + current["supporting"] + current["optional"]
            )
            self.assertEqual(current["name"], legacy["name"])
            self.assertEqual(
                current_ingredients,
                legacy["ingredients"],
                legacy["name"],
            )
            self.assertEqual(current["steps"], legacy["steps"], legacy["name"])


if __name__ == "__main__":
    unittest.main()
