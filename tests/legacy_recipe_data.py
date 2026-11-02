"""Data resep sebelum dipisahkan ke recipe_data.py.

Disalin dari commit de037e3, file main.py, variabel RECIPES.
File ini hanya dipakai untuk tes regresi.
"""


LEGACY_RECIPES = [
    {
        "name": "Nasi Goreng Sederhana",
        "ingredients": [
            "nasi",
            "telur",
            "bawang putih",
            "bawang merah",
            "kecap",
            "garam",
        ],
        "steps": [
            "Iris bawang putih dan bawang merah.",
            "Tumis bawang sampai harum.",
            "Masukkan telur, lalu orak-arik.",
            "Masukkan nasi, kecap, dan garam.",
            "Aduk sampai tercampur rata, lalu sajikan.",
        ],
    },
    {
        "name": "Telur Kecap",
        "ingredients": ["telur", "kecap", "bawang merah", "bawang putih", "garam"],
        "steps": [
            "Goreng telur sampai matang.",
            "Tumis bawang merah dan bawang putih.",
            "Tambahkan kecap, sedikit air, dan garam.",
            "Masukkan telur dan masak sampai bumbu meresap.",
        ],
    },
    {
        "name": "Mi Telur",
        "ingredients": ["mi", "telur", "bawang putih", "garam"],
        "steps": [
            "Rebus mi sampai matang, lalu tiriskan.",
            "Tumis bawang putih sampai harum.",
            "Masukkan telur dan orak-arik.",
            "Masukkan mi serta bumbu, lalu aduk rata.",
        ],
    },
    {
        "name": "Tumis Kangkung",
        "ingredients": ["kangkung", "bawang putih", "cabai", "garam", "minyak"],
        "steps": [
            "Petik dan cuci kangkung.",
            "Iris bawang putih dan cabai.",
            "Panaskan minyak, lalu tumis bawang dan cabai.",
            "Masukkan kangkung dan garam.",
            "Masak sampai kangkung layu dan matang.",
        ],
    },
    {
        "name": "Telur Dadar",
        "ingredients": ["telur", "garam", "minyak", "bawang merah"],
        "steps": [
            "Pecahkan telur ke dalam mangkuk.",
            "Tambahkan garam dan bawang merah iris.",
            "Kocok sampai tercampur.",
            "Goreng dengan minyak panas sampai matang.",
        ],
    },
]
