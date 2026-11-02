"""Normalisasi nama bahan dan alias MenuKu.

Hanya pencocokan nama lengkap yang dipakai. Tidak ada fuzzy matching atau
pencocokan sebagian, supaya istilah ambigu tidak dipetakan sembarangan.
"""

import re


ALIASES = {
    "cabai": ("cabe",),
    "bawang merah": ("brambang",),
    "telur": ("telur ayam",),
    "mi": ("mie",),
}


def normalize_text(text):
    """Rapikan huruf besar/kecil dan spasi berlebih."""
    return re.sub(r"\s+", " ", text.strip().casefold())


def _build_alias_index():
    index = {}
    for canonical, aliases in ALIASES.items():
        canonical_key = normalize_text(canonical)
        if canonical_key in index:
            raise ValueError(f"Alias ganda untuk {canonical!r}")
        index[canonical_key] = canonical

        for alias in aliases:
            alias_key = normalize_text(alias)
            if alias_key in index:
                raise ValueError(f"Alias ganda untuk {alias!r}")
            index[alias_key] = canonical
    return index


_ALIAS_INDEX = _build_alias_index()


def normalize_ingredient(raw):
    """Kembalikan nama standar untuk satu bahan, atau teks aslinya."""
    normalized = normalize_text(raw)
    return _ALIAS_INDEX.get(normalized, normalized)


def deduplicate_ingredients(raw_ingredients):
    """Buang bahan kosong dan duplikat berdasarkan nama standar.

    Nama yang ditampilkan tetap nama pertama yang dimasukkan pengguna.
    """
    result = []
    seen = set()

    for raw in raw_ingredients:
        text = raw.strip()
        if not text:
            continue

        canonical = normalize_ingredient(text)
        if canonical in seen:
            continue

        seen.add(canonical)
        result.append(text)

    return result
