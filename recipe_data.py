"""Data resep MenuKu.

Nilai None berarti informasi tersebut belum tersedia. Jangan menggantinya
dengan angka atau teks yang tidak memiliki sumber.
"""


RECIPES = [
    {
        "id": "nasi-goreng-sederhana",
        "name": "Nasi Goreng Sederhana",
        "description": None,
        "main": ["nasi", "telur"],
        "supporting": ["bawang putih", "bawang merah", "kecap", "garam"],
        "optional": [],
        "steps": [
            "Iris bawang putih dan bawang merah.",
            "Tumis bawang sampai harum.",
            "Masukkan telur, lalu orak-arik.",
            "Masukkan nasi, kecap, dan garam.",
            "Aduk sampai tercampur rata, lalu sajikan.",
        ],
        "quantities": None,
        "cook_time_minutes": None,
        "servings": None,
        "photo": None,
        "tips": None,
        "source": None,
        "safety_notes": [],
    },
    {
        "id": "telur-kecap",
        "name": "Telur Kecap",
        "description": None,
        "main": ["telur"],
        "supporting": ["kecap", "bawang merah", "bawang putih", "garam"],
        "optional": [],
        "steps": [
            "Goreng telur sampai matang.",
            "Tumis bawang merah dan bawang putih.",
            "Tambahkan kecap, sedikit air, dan garam.",
            "Masukkan telur dan masak sampai bumbu meresap.",
        ],
        "quantities": None,
        "cook_time_minutes": None,
        "servings": None,
        "photo": None,
        "tips": None,
        "source": None,
        "safety_notes": [],
    },
    {
        "id": "mi-telur",
        "name": "Mi Telur",
        "description": None,
        "main": ["mi", "telur"],
        "supporting": ["bawang putih", "garam"],
        "optional": [],
        "steps": [
            "Rebus mi sampai matang, lalu tiriskan.",
            "Tumis bawang putih sampai harum.",
            "Masukkan telur dan orak-arik.",
            "Masukkan mi serta bumbu, lalu aduk rata.",
        ],
        "quantities": None,
        "cook_time_minutes": None,
        "servings": None,
        "photo": None,
        "tips": None,
        "source": None,
        "safety_notes": [],
    },
    {
        "id": "tumis-kangkung",
        "name": "Tumis Kangkung",
        "description": None,
        "main": ["kangkung"],
        "supporting": ["bawang putih", "cabai", "garam", "minyak"],
        "optional": [],
        "steps": [
            "Petik dan cuci kangkung.",
            "Iris bawang putih dan cabai.",
            "Panaskan minyak, lalu tumis bawang dan cabai.",
            "Masukkan kangkung dan garam.",
            "Masak sampai kangkung layu dan matang.",
        ],
        "quantities": None,
        "cook_time_minutes": None,
        "servings": None,
        "photo": None,
        "tips": None,
        "source": None,
        "safety_notes": [],
    },
    {
        "id": "telur-dadar",
        "name": "Telur Dadar",
        "description": None,
        "main": ["telur"],
        "supporting": ["garam", "minyak", "bawang merah"],
        "optional": [],
        "steps": [
            "Pecahkan telur ke dalam mangkuk.",
            "Tambahkan garam dan bawang merah iris.",
            "Kocok sampai tercampur.",
            "Goreng dengan minyak panas sampai matang.",
        ],
        "quantities": None,
        "cook_time_minutes": None,
        "servings": None,
        "photo": None,
        "tips": None,
        "source": None,
        "safety_notes": [],
    },
]


def required_ingredients(recipe):
    """Gabungkan bahan utama dan bahan wajib pendukung."""
    return recipe["main"] + recipe["supporting"]
