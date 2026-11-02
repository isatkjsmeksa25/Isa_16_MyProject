import unittest

from ingredients import (
    ALIASES,
    deduplicate_ingredients,
    normalize_ingredient,
    normalize_text,
)


class IngredientNormalizationTests(unittest.TestCase):
    def test_case_is_normalized(self):
        self.assertEqual(normalize_text("CABAI"), "cabai")
        self.assertEqual(normalize_ingredient("CaBe"), "cabai")
        self.assertEqual(normalize_ingredient("TELUR AYAM"), "telur")

    def test_extra_spaces_are_normalized(self):
        self.assertEqual(normalize_text("  telur   ayam  "), "telur ayam")
        self.assertEqual(normalize_ingredient("  telur   ayam  "), "telur")
        self.assertEqual(normalize_ingredient("  brambang  "), "bawang merah")

    def test_every_defined_alias(self):
        for canonical, aliases in ALIASES.items():
            self.assertEqual(normalize_ingredient(canonical), canonical)
            for alias in aliases:
                self.assertEqual(
                    normalize_ingredient(alias),
                    canonical,
                    alias,
                )

    def test_standard_names_do_not_change(self):
        names = [
            "cabai",
            "bawang merah",
            "telur",
            "mi",
            "bawang putih",
            "kecap",
            "garam",
            "nasi",
            "kangkung",
            "minyak",
        ]
        for name in names:
            self.assertEqual(normalize_ingredient(name), name)

    def test_unknown_alias_is_not_guessed(self):
        names = [
            "cabe rawit",
            "telur bebek",
            "mie instan",
            "bawang goreng",
        ]
        for name in names:
            self.assertEqual(normalize_ingredient(name), name)

    def test_ambiguous_terms_are_not_mapped(self):
        self.assertEqual(normalize_ingredient("bawang"), "bawang")
        self.assertEqual(
            normalize_ingredient("telur ayam kampung"),
            "telur ayam kampung",
        )

    def test_duplicates_use_standard_name(self):
        self.assertEqual(
            deduplicate_ingredients(["cabe", "cabai", "CABE"]),
            ["cabe"],
        )
        self.assertEqual(
            deduplicate_ingredients(["telur ayam", "telur"]),
            ["telur ayam"],
        )

    def test_ambiguous_terms_are_not_deduplicated(self):
        self.assertEqual(
            deduplicate_ingredients(["bawang", "bawang merah"]),
            ["bawang", "bawang merah"],
        )

    def test_empty_input_is_handled(self):
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_ingredient("   "), "")
        self.assertEqual(deduplicate_ingredients([]), [])
        self.assertEqual(
            deduplicate_ingredients(["", "   ", "cabe", "  "]),
            ["cabe"],
        )


if __name__ == "__main__":
    unittest.main()
