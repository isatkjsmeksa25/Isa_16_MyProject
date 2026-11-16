"""Template masakan alternatif MenuKu.

Template ini digunakan sebagai fallback ketika katalog resep tidak
menghasilkan rekomendasi. Template bukan resep tetap dan dibangun
berdasarkan bahan aman yang tersedia.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RecipeTemplate:
    id: str
    name: str
    category: str
    core_groups: tuple[tuple[str, ...], ...]
    supporting_ingredients: tuple[str, ...]
    optional_ingredients: tuple[str, ...]
    steps: tuple[str, ...]

    @property
    def core_ingredients(self):
        """Semua bahan inti yang mungkin dipakai, untuk kompatibilitas."""
        return tuple(
            ingredient
            for group in self.core_groups
            for ingredient in group
        )


RECIPE_TEMPLATES = (
    RecipeTemplate(
        id="tumis-tahu-tempe",
        name="Tumis Tahu Tempe",
        category="tumis",
        core_groups=(("tahu",), ("tempe",)),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai",),
        steps=(
            "Potong tahu dan tempe.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan tahu dan tempe, aduk rata.",
            "Tambahkan kecap dan garam, masak sebentar.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-sayur-sederhana",
        name="Tumis Sayur Sederhana",
        category="tumis",
        core_groups=(("kangkung", "kol", "buncis", "wortel", "bayam", "sawi"),),
        supporting_ingredients=("bawang putih", "garam", "minyak"),
        optional_ingredients=("cabai", "bawang merah"),
        steps=(
            "Potong sayur yang tersedia.",
            "Iris bawang putih.",
            "Panaskan minyak, tumis bawang.",
            "Masukkan sayur, aduk rata.",
            "Tambahkan garam, masak hingga sayur layu.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="mi-goreng-sederhana",
        name="Mi Goreng Sederhana",
        category="goreng",
        core_groups=(("mi",), ("telur",)),
        supporting_ingredients=("bawang putih", "kecap", "garam"),
        optional_ingredients=("kol", "wortel", "cabai"),
        steps=(
            "Rebus mi, tiriskan.",
            "Kocok telur.",
            "Panaskan minyak, tumis bawang putih.",
            "Masukkan telur, orak-arik.",
            "Masukkan mi, kecap, dan garam, aduk rata.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-ayam-kecap",
        name="Tumis Ayam Kecap",
        category="tumis",
        core_groups=(("ayam",),),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai", "daun bawang"),
        steps=(
            "Potong ayam sesuai selera.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan ayam, aduk rata.",
            "Tambahkan kecap dan garam, masak hingga matang.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-daging-sapi-kecap",
        name="Tumis Daging Sapi Kecap",
        category="tumis",
        core_groups=(("daging sapi",),),
        supporting_ingredients=("bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai",),
        steps=(
            "Iris daging sapi tipis.",
            "Iris bawang putih.",
            "Panaskan minyak, tumis bawang putih.",
            "Masukkan daging sapi, aduk rata.",
            "Tambahkan kecap dan garam, masak hingga matang.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-ikan-kecap",
        name="Tumis Ikan Kecap",
        category="tumis",
        core_groups=(("ikan",),),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai", "tomat"),
        steps=(
            "Potong ikan sesuai selera.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan ikan, aduk rata.",
            "Tambahkan kecap dan garam, masak hingga matang.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-udang-kecap",
        name="Tumis Udang Kecap",
        category="tumis",
        core_groups=(("udang",),),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai", "daun bawang"),
        steps=(
            "Bersihkan udang.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan udang, aduk rata.",
            "Tambahkan kecap dan garam, masak hingga matang.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-tahu-kecap",
        name="Tumis Tahu Kecap",
        category="tumis",
        core_groups=(("tahu",),),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai",),
        steps=(
            "Potong tahu.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan tahu, aduk rata.",
            "Tambahkan kecap dan garam, masak sebentar.",
            "Sajikan.",
        ),
    ),
    RecipeTemplate(
        id="tumis-tempe-kecap",
        name="Tumis Tempe Kecap",
        category="tumis",
        core_groups=(("tempe",),),
        supporting_ingredients=("bawang merah", "bawang putih", "kecap", "garam", "minyak"),
        optional_ingredients=("cabai",),
        steps=(
            "Potong tempe.",
            "Iris bawang merah dan bawang putih.",
            "Panaskan minyak, tumis bawang sampai harum.",
            "Masukkan tempe, aduk rata.",
            "Tambahkan kecap dan garam, masak sebentar.",
            "Sajikan.",
        ),
    ),
)
