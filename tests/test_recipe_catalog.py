import unittest

from food_safety import check_ingredient
from ingredients import normalize_ingredient, normalize_text
from recipe_data import RECIPES, required_ingredients
from recipe_templates import RECIPE_TEMPLATES
from tests.legacy_recipe_data import LEGACY_RECIPES


class RecipeCatalogTests(unittest.TestCase):
    def test_legacy_recipes_are_still_present(self):
        self.assertGreaterEqual(len(RECIPES), len(LEGACY_RECIPES))

        for current, legacy in zip(RECIPES, LEGACY_RECIPES):
            current_ingredients = (
                current["main"] + current["supporting"] + current["optional"]
            )
            self.assertEqual(current["name"], legacy["name"])
            self.assertEqual(current_ingredients, legacy["ingredients"])
            self.assertEqual(current["steps"], legacy["steps"])

    def test_legacy_recipe_ids_are_preserved(self):
        self.assertEqual(
            [recipe["id"] for recipe in RECIPES[:5]],
            [
                "nasi-goreng-sederhana",
                "telur-kecap",
                "mi-telur",
                "tumis-kangkung",
                "telur-dadar",
            ],
        )

    def test_catalog_has_expected_size(self):
        self.assertEqual(len(RECIPES), 25)

    def test_recipe_ids_are_unique(self):
        ids = [recipe["id"] for recipe in RECIPES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_recipe_names_are_unique(self):
        names = [recipe["name"] for recipe in RECIPES]
        self.assertEqual(len(names), len(set(names)))

    def test_no_duplicate_ingredients_across_groups(self):
        for recipe in RECIPES:
            combined = recipe["main"] + recipe["supporting"] + recipe["optional"]
            self.assertEqual(
                len(combined),
                len(set(combined)),
                recipe["name"],
            )

        for template in RECIPE_TEMPLATES:
            combined = (
                list(template.core_ingredients)
                + list(template.supporting_ingredients)
                + list(template.optional_ingredients)
            )
            self.assertEqual(
                len(combined),
                len(set(combined)),
                template.id,
            )

    def test_every_recipe_has_valid_structure(self):
        for recipe in RECIPES:
            self.assertTrue(recipe["id"])
            self.assertTrue(recipe["name"])
            self.assertIsInstance(recipe["main"], list)
            self.assertIsInstance(recipe["supporting"], list)
            self.assertIsInstance(recipe["optional"], list)
            self.assertTrue(recipe["steps"])
            self.assertTrue(all(isinstance(step, str) and step for step in recipe["steps"]))
            self.assertTrue(all(isinstance(item, str) and item for item in recipe["main"]))
            self.assertTrue(all(isinstance(item, str) and item for item in recipe["supporting"]))
            self.assertTrue(all(isinstance(item, str) and item for item in recipe["optional"]))

    def test_required_ingredients_still_works(self):
        for recipe in RECIPES:
            required = required_ingredients(recipe)
            self.assertEqual(required, recipe["main"] + recipe["supporting"])

    def test_catalog_does_not_contain_risky_ingredients(self):
        for recipe in RECIPES:
            for group_name in ("main", "supporting", "optional"):
                for ingredient in recipe[group_name]:
                    self.assertFalse(
                        check_ingredient(ingredient).is_risky,
                        (recipe["name"], ingredient),
                    )

    def test_template_ids_are_unique(self):
        ids = [template.id for template in RECIPE_TEMPLATES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_templates_have_valid_structure(self):
        for template in RECIPE_TEMPLATES:
            self.assertTrue(template.id)
            self.assertTrue(template.name)
            self.assertTrue(template.category)
            self.assertTrue(template.core_groups)
            self.assertTrue(template.core_ingredients)
            self.assertTrue(template.supporting_ingredients)
            self.assertTrue(template.steps)
            self.assertTrue(all(isinstance(group, tuple) and group for group in template.core_groups))
            self.assertTrue(all(isinstance(item, str) and item for group in template.core_groups for item in group))
            self.assertTrue(all(isinstance(item, str) and item for item in template.core_ingredients))
            self.assertTrue(all(isinstance(item, str) and item for item in template.supporting_ingredients))
            self.assertTrue(all(isinstance(item, str) and item for item in template.optional_ingredients))
            self.assertTrue(all(isinstance(step, str) and step for step in template.steps))

    def test_templates_do_not_contain_risky_ingredients(self):
        for template in RECIPE_TEMPLATES:
            for ingredient in (
                template.core_ingredients
                + template.supporting_ingredients
                + template.optional_ingredients
            ):
                self.assertFalse(
                    check_ingredient(ingredient).is_risky,
                    (template.id, ingredient),
                )

    def test_template_ingredients_are_normalized(self):
        for template in RECIPE_TEMPLATES:
            for ingredient in (
                template.core_ingredients
                + template.supporting_ingredients
                + template.optional_ingredients
            ):
                self.assertEqual(
                    normalize_ingredient(ingredient),
                    normalize_text(ingredient),
                    (template.id, ingredient),
                )

    def test_optional_ingredients_are_not_required_in_steps(self):
        for recipe in RECIPES:
            for ingredient in recipe["optional"]:
                for step in recipe["steps"]:
                    self.assertNotIn(
                        ingredient.lower(),
                        step.lower(),
                        (recipe["name"], ingredient, step),
                    )

        for template in RECIPE_TEMPLATES:
            for ingredient in template.optional_ingredients:
                for step in template.steps:
                    self.assertNotIn(
                        ingredient.lower(),
                        step.lower(),
                        (template.id, ingredient, step),
                    )


if __name__ == "__main__":
    unittest.main()
