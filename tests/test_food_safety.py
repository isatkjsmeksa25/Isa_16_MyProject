import unittest

from food_safety import (
    ONLY_RISKY_MESSAGE,
    REFERENCES,
    RISKY_GROUPS,
    SAFETY_DISCLAIMER,
    check_ingredient,
    check_ingredients,
    matchable_ingredients,
)


class FoodSafetyTests(unittest.TestCase):
    def test_freshwater_snails_are_risky(self):
        names = (
            "bekicot",
            "keong",
            "tutut",
            "siput",
            "Keong Sawah",
            "SIPUT air tawar",
            "bekicot goreng",
        )

        for name in names:
            check = check_ingredient(name)
            self.assertTrue(check.is_risky, name)
            self.assertEqual(
                [group.id for group in check.groups],
                ["freshwater_snails"],
                name,
            )
            self.assertEqual(
                check.groups[0].reference.url,
                "https://www.cdc.gov/angiostrongylus/about/index.html",
            )

    def test_pufferfish_and_fugu_are_risky(self):
        names = (
            "buntal",
            "ikan buntal",
            "fugu",
            "ikan fugu",
            "pufferfish",
            "Puffer Fish",
        )

        for name in names:
            check = check_ingredient(name)
            self.assertTrue(check.is_risky, name)
            self.assertEqual(
                [group.id for group in check.groups],
                ["pufferfish"],
                name,
            )

    def test_wild_mushrooms_are_risky(self):
        names = (
            "jamur liar",
            "Jamur Hutan",
            "jamur alam",
            "jamur tidak dikenal",
        )

        for name in names:
            check = check_ingredient(name)
            self.assertTrue(check.is_risky, name)
            self.assertEqual(
                [group.id for group in check.groups],
                ["wild_mushrooms"],
                name,
            )
            self.assertNotIn("wild_game", [group.id for group in check.groups])

    def test_wild_game_and_buruan_are_risky(self):
        names = (
            "daging liar",
            "hasil buruan",
            "daging buruan",
            "hewan liar",
            "babi hutan",
            "rusa",
            "kijang",
            "ayam hutan",
            "ikan liar",
        )

        for name in names:
            check = check_ingredient(name)
            self.assertTrue(check.is_risky, name)
            self.assertEqual(
                [group.id for group in check.groups],
                ["wild_game"],
                name,
            )

    def test_regular_ingredients_are_not_risky(self):
        names = (
            "nasi",
            "telur",
            "bawang putih",
            "cabai",
            "mi",
            "kangkung",
            "minyak",
            "garam",
            "kecap",
            "jamur",
            "jamur tiram",
            "jamur kancing",
            "daging sapi",
            "ayam",
            "ikan nila",
            "kelapa",
            "daun pisang",
            "",
            "   ",
        )

        for name in names:
            check = check_ingredient(name)
            self.assertFalse(check.is_risky, repr(name))
            self.assertEqual(check.warnings, (), repr(name))

    def test_aliases_are_normalized_before_safety_check(self):
        self.assertEqual(check_ingredient("cabe").canonical, "cabai")
        self.assertEqual(
            check_ingredient("brambang").canonical,
            "bawang merah",
        )
        self.assertEqual(check_ingredient("telur ayam").canonical, "telur")
        self.assertEqual(check_ingredient("mie").canonical, "mi")

        for name in ("cabe", "brambang", "telur ayam", "mie"):
            self.assertFalse(check_ingredient(name).is_risky, name)

    def test_original_input_is_preserved(self):
        check = check_ingredient("  Keong Sawah  ")
        self.assertEqual(check.ingredient, "Keong Sawah")
        self.assertEqual(check.canonical, "keong sawah")

    def test_empty_input_is_handled(self):
        self.assertEqual(check_ingredient("").canonical, "")
        self.assertEqual(check_ingredient("   ").ingredient, "")
        self.assertFalse(check_ingredient("").is_risky)

        report = check_ingredients([])
        self.assertEqual(report.checks, ())
        self.assertFalse(report.has_risky)
        self.assertFalse(report.has_safe)
        self.assertFalse(report.only_risky)
        self.assertEqual(matchable_ingredients([]), ())

        report = check_ingredients(["", "   "])
        self.assertEqual(report.checks, ())
        self.assertFalse(report.only_risky)

    def test_report_separates_safe_and_risky_ingredients(self):
        report = check_ingredients(
            ["cabai", "keong", "garam", "jamur liar", "fugu"]
        )

        self.assertTrue(report.has_safe)
        self.assertTrue(report.has_risky)
        self.assertFalse(report.only_risky)
        self.assertEqual(report.safe_ingredients, ("cabai", "garam"))
        self.assertEqual(
            report.risky_ingredients,
            ("keong", "jamur liar", "fugu"),
        )
        self.assertEqual(len(report.warnings), 3)
        self.assertEqual(report.checks[1].ingredient, "keong")

    def test_only_risky_ingredients_are_detected(self):
        report = check_ingredients(["keong", "fugu"])

        self.assertTrue(report.only_risky)
        self.assertFalse(report.has_safe)
        self.assertEqual(report.safe_ingredients, ())
        self.assertIn("tidak dapat", ONLY_RISKY_MESSAGE)

    def test_risky_ingredients_are_never_matchable(self):
        self.assertEqual(
            matchable_ingredients(["keong", "cabai", "fugu", "garam"]),
            ("cabai", "garam"),
        )
        self.assertEqual(matchable_ingredients(["keong"]), ())
        self.assertEqual(
            matchable_ingredients(["cabe", "cabai", "CABE"]),
            ("cabai",),
        )

        for group in RISKY_GROUPS:
            for term in group.terms:
                self.assertEqual(matchable_ingredients([term]), (), term)

    def test_every_defined_term_triggers_its_group(self):
        for group in RISKY_GROUPS:
            for term in group.terms:
                check = check_ingredient(term)
                self.assertIn(
                    group.id,
                    [matched.id for matched in check.groups],
                    term,
                )

    def test_matching_uses_whole_terms(self):
        self.assertFalse(check_ingredient("siputan").is_risky)
        self.assertFalse(check_ingredient("keongnya").is_risky)
        self.assertFalse(check_ingredient("pufferfishnya").is_risky)

    def test_every_group_has_a_reference(self):
        for group in RISKY_GROUPS:
            self.assertTrue(group.reference.title, group.id)
            self.assertTrue(
                group.reference.url.startswith("https://"),
                group.id,
            )
            self.assertIn(group.reference, REFERENCES.values(), group.id)

        self.assertEqual(
            REFERENCES["fda_pufferfish"].url,
            (
                "https://www.fda.gov/international-programs/"
                "cooperative-arrangements/"
                "fda-japan-exchange-letters-regarding-puffer-fish"
            ),
        )

    def test_warnings_do_not_claim_risky_food_is_safe(self):
        self.assertIn("tidak lengkap", SAFETY_DISCLAIMER)

        for group in RISKY_GROUPS:
            text = group.warning.lower()
            self.assertIn("tidak dipakai untuk mencocokkan resep", text)
            for phrase in (
                "aman setelah dimasak",
                "aman setelah direbus",
                "pasti aman",
                "bebas risiko",
            ):
                self.assertNotIn(phrase, text, group.id)


if __name__ == "__main__":
    unittest.main()
