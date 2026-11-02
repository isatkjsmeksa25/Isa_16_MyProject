"""Pemeriksaan keselamatan bahan MenuKu.

Daftar ini konservatif dan tidak lengkap. Tujuannya hanya menandai bahan yang
tidak boleh dipakai untuk mencocokkan resep, bukan memberi diagnosis atau
jaminan keamanan pangan.

Referensi yang dipakai:
- CDC, Rat Lungworm Disease (Angiostrongylus)
- WHO, Natural toxins in food (poisonous mushrooms)
- FDA, FDA - Japan, Exchange of Letters Regarding Puffer Fish
- CDC, About Trichinellosis
"""

import re
from dataclasses import dataclass

from ingredients import normalize_ingredient, normalize_text


SAFETY_DISCLAIMER = (
    "Daftar ini konservatif dan tidak lengkap. Pemeriksaan ini bukan "
    "pengganti saran tenaga kesehatan atau otoritas keamanan pangan."
)

ONLY_RISKY_MESSAGE = (
    "Semua bahan yang dimasukkan berisiko. MenuKu tidak dapat "
    "merekomendasikan menu untuk dikonsumsi dari bahan-bahan ini."
)


@dataclass(frozen=True)
class Reference:
    title: str
    url: str


REFERENCES = {
    "rat_lungworm": Reference(
        title="CDC - About Rat Lungworm Disease (Angiostrongylus)",
        url="https://www.cdc.gov/angiostrongylus/about/index.html",
    ),
    "who_mushrooms": Reference(
        title="WHO - Natural toxins in food: Poisonous mushrooms",
        url="https://www.who.int/news-room/fact-sheets/detail/natural-toxins-in-food",
    ),
    "fda_pufferfish": Reference(
        title="FDA - Exchange of Letters Regarding Puffer Fish",
        url=(
            "https://www.fda.gov/international-programs/cooperative-arrangements/"
            "fda-japan-exchange-letters-regarding-puffer-fish"
        ),
    ),
    "trichinellosis": Reference(
        title="CDC - About Trichinellosis",
        url="https://www.cdc.gov/trichinellosis/about/index.html",
    ),
}


@dataclass(frozen=True)
class RiskyGroup:
    id: str
    label: str
    terms: tuple[str, ...]
    warning: str
    reference: Reference
    exclude_terms: tuple[str, ...] = ()


RISKY_GROUPS = (
    RiskyGroup(
        id="freshwater_snails",
        label="siput, keong, bekicot, atau tutut",
        terms=("bekicot", "keong", "tutut", "siput"),
        warning=(
            "Siput, keong, bekicot, dan tutut dapat membawa parasit "
            "Angiostrongylus cantonensis. CDC menyarankan tidak memakan "
            "siput atau slug mentah/kurang matang. Aplikasi tidak dapat "
            "memverifikasi identitas bahan dan cara pengolahannya, sehingga "
            "bahan ini tidak dipakai untuk mencocokkan resep."
        ),
        reference=REFERENCES["rat_lungworm"],
    ),
    RiskyGroup(
        id="pufferfish",
        label="ikan buntal atau fugu",
        terms=(
            "buntal",
            "ikan buntal",
            "fugu",
            "ikan fugu",
            "pufferfish",
            "puffer fish",
        ),
        warning=(
            "Ikan buntal dan fugu dapat mengandung tetrodotoxin. FDA "
            "menyatakan setiap ikan dapat mengandung dosis letal dan tidak "
            "ada antidot yang diketahui. Bahan berisiko tidak dipakai untuk "
            "mencocokkan resep."
        ),
        reference=REFERENCES["fda_pufferfish"],
    ),
    RiskyGroup(
        id="wild_mushrooms",
        label="jamur liar",
        terms=(
            "jamur liar",
            "jamur hutan",
            "jamur alam",
            "jamur tidak dikenal",
        ),
        warning=(
            "Jamur liar dapat mengandung racun yang tidak hilang dengan "
            "dimasak atau dikupas (WHO). Bahan berisiko tidak dipakai untuk "
            "mencocokkan resep; hindari jamur liar yang tidak teridentifikasi "
            "pasti."
        ),
        reference=REFERENCES["who_mushrooms"],
    ),
    RiskyGroup(
        id="wild_game",
        label="hewan liar atau hasil buruan",
        terms=(
            "hasil buruan",
            "daging buruan",
            "hewan buruan",
            "buruan",
            "satwa liar",
            "hewan liar",
            "daging liar",
            "babi hutan",
            "babi liar",
            "rusa",
            "kijang",
            "ayam hutan",
            "kelinci hutan",
            "liar",
        ),
        warning=(
            "Hewan liar dan hasil buruan tidak dapat dipastikan jenis, asal, "
            "dan penanganannya dari nama bahan. CDC mencatat daging hewan "
            "liar dapat membawa parasit seperti Trichinella. Bahan berisiko "
            "tidak dipakai untuk mencocokkan resep."
        ),
        reference=REFERENCES["trichinellosis"],
        exclude_terms=("jamur",),
    ),
)


@dataclass(frozen=True)
class SafetyCheck:
    ingredient: str
    canonical: str
    groups: tuple[RiskyGroup, ...]

    @property
    def is_risky(self):
        return bool(self.groups)

    @property
    def warnings(self):
        return tuple(group.warning for group in self.groups)

    @property
    def warning(self):
        return " ".join(self.warnings)


@dataclass(frozen=True)
class SafetyReport:
    checks: tuple[SafetyCheck, ...]

    @property
    def risky_checks(self):
        return tuple(check for check in self.checks if check.is_risky)

    @property
    def safe_checks(self):
        return tuple(check for check in self.checks if not check.is_risky)

    @property
    def safe_ingredients(self):
        return tuple(check.canonical for check in self.safe_checks)

    @property
    def risky_ingredients(self):
        return tuple(check.canonical for check in self.risky_checks)

    @property
    def warnings(self):
        return tuple(
            warning
            for check in self.risky_checks
            for warning in check.warnings
        )

    @property
    def has_safe(self):
        return bool(self.safe_checks)

    @property
    def has_risky(self):
        return bool(self.risky_checks)

    @property
    def only_risky(self):
        return bool(self.checks) and not self.safe_checks


def _contains_term(text, term):
    """Cocokkan satu istilah utuh, bukan potongan kata."""
    pattern = r"(?<!\w)" + re.escape(normalize_text(term)) + r"(?!\w)"
    return re.search(pattern, text) is not None


def _matches_group(group, canonical):
    if any(_contains_term(canonical, term) for term in group.exclude_terms):
        return False

    return any(_contains_term(canonical, term) for term in group.terms)


def check_ingredient(raw):
    """Periksa satu bahan dan kembalikan hasilnya tanpa mengubah input."""
    text = raw.strip()
    canonical = normalize_ingredient(text)
    groups = tuple(
        group
        for group in RISKY_GROUPS
        if _matches_group(group, canonical)
    )
    return SafetyCheck(ingredient=text, canonical=canonical, groups=groups)


def check_ingredients(raw_ingredients):
    """Periksa beberapa bahan sekaligus dan pisahkan yang aman dan berisiko."""
    checks = []

    for raw in raw_ingredients:
        check = check_ingredient(raw)
        if check.ingredient:
            checks.append(check)

    return SafetyReport(checks=tuple(checks))


def matchable_ingredients(raw_ingredients):
    """Nama standar bahan aman yang boleh dipakai untuk mencocokkan resep."""
    result = []
    seen = set()

    for check in check_ingredients(raw_ingredients).safe_checks:
        if check.canonical in seen:
            continue
        seen.add(check.canonical)
        result.append(check.canonical)

    return tuple(result)
