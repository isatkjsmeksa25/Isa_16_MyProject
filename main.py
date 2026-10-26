
import random
import re

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle


# Warna utama MenuKu
BG = (0.96, 0.95, 0.91, 1)
SURFACE = (1, 1, 0.98, 1)
GREEN = (0.20, 0.36, 0.25, 1)
GREEN_LIGHT = (0.88, 0.92, 0.85, 1)
TEXT = (0.17, 0.19, 0.16, 1)
MUTED = (0.43, 0.45, 0.40, 1)
BORDER = (0.85, 0.85, 0.80, 1)


# Data resep awal. Bahan ditulis dalam bentuk sederhana.
RECIPES = [
    {
        "name": "Nasi Goreng Sederhana",
        "ingredients": [
            "nasi", "telur", "bawang putih",
            "bawang merah", "kecap", "garam"
        ],
        "steps": [
            "Iris bawang putih dan bawang merah.",
            "Tumis bawang sampai harum.",
            "Masukkan telur, lalu orak-arik.",
            "Masukkan nasi, kecap, dan garam.",
            "Aduk sampai tercampur rata, lalu sajikan."
        ],
    },
    {
        "name": "Telur Kecap",
        "ingredients": [
            "telur", "kecap", "bawang merah",
            "bawang putih", "garam"
        ],
        "steps": [
            "Goreng telur sampai matang.",
            "Tumis bawang merah dan bawang putih.",
            "Tambahkan kecap, sedikit air, dan garam.",
            "Masukkan telur dan masak sampai bumbu meresap."
        ],
    },
    {
        "name": "Mi Telur",
        "ingredients": [
            "mi", "telur", "bawang putih", "garam"
        ],
        "steps": [
            "Rebus mi sampai matang, lalu tiriskan.",
            "Tumis bawang putih sampai harum.",
            "Masukkan telur dan orak-arik.",
            "Masukkan mi serta bumbu, lalu aduk rata."
        ],
    },
    {
        "name": "Tumis Kangkung",
        "ingredients": [
            "kangkung", "bawang putih",
            "cabai", "garam", "minyak"
        ],
        "steps": [
            "Petik dan cuci kangkung.",
            "Iris bawang putih dan cabai.",
            "Panaskan minyak, lalu tumis bawang dan cabai.",
            "Masukkan kangkung dan garam.",
            "Masak sampai kangkung layu dan matang."
        ],
    },
    {
        "name": "Telur Dadar",
        "ingredients": ["telur", "garam", "minyak", "bawang merah"],
        "steps": [
            "Pecahkan telur ke dalam mangkuk.",
            "Tambahkan garam dan bawang merah iris.",
            "Kocok sampai tercampur.",
            "Goreng dengan minyak panas sampai matang."
        ],
    },
]


def normalize(text):
    """Menyamakan huruf dan spasi agar pencarian lebih mudah."""
    return re.sub(r"\s+", " ", text.strip().lower())


class MenuKuApp(App):
    def build(self):
        self.title = "MenuKu"
        Window.size = (1000, 760)
        Window.minimum_width = 360
        Window.minimum_height = 600
        Window.clearcolor = BG

        self.ingredients = []
        self.current_recipes = []

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(18), dp(24), dp(18)],
            spacing=dp(14),
        )

        # Header
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(91),
            spacing=dp(5),
        )

        header.add_widget(self.label(
            "MenuKu",
            size=sp(30),
            color=GREEN,
            bold=True,
            height=dp(42),
        ))
        header.add_widget(self.label(
            "Masak apa hari ini?",
            size=sp(19),
            color=TEXT,
            height=dp(29),
        ))
        header.add_widget(self.label(
            "Masukkan bahan yang tersedia, lalu temukan ide masakan.",
            size=sp(13),
            color=MUTED,
            height=dp(22),
        ))
        root.add_widget(header)

        # Panel input bahan
        input_panel = self.panel()
        input_panel.orientation = "vertical"
        input_panel.size_hint_y = None
        input_panel.height = dp(151)
        input_panel.padding = dp(15)
        input_panel.spacing = dp(9)

        input_panel.add_widget(self.label(
            "BAHAN YANG TERSEDIA",
            size=sp(12),
            color=GREEN,
            bold=True,
            height=dp(22),
        ))

        input_row = BoxLayout(
            size_hint_y=None,
            height=dp(43),
            spacing=dp(8),
        )

        self.ingredient_input = TextInput(
            hint_text="Contoh: nasi, telur, bawang putih",
            multiline=False,
            font_size=sp(14),
            foreground_color=TEXT,
            background_normal="",
            background_active="",
            background_color=BG,
            cursor_color=GREEN,
            padding=[dp(12), dp(11), dp(12), dp(8)],
        )
        self.ingredient_input.bind(
            on_text_validate=lambda *_: self.add_ingredients()
        )
        input_row.add_widget(self.ingredient_input)

        add_button = self.make_button(
            "Tambah",
            GREEN,
            SURFACE,
            self.add_ingredients,
            width=dp(105),
        )
        input_row.add_widget(add_button)
        input_panel.add_widget(input_row)

        self.ingredient_summary = self.label(
            "Belum ada bahan yang ditambahkan.",
            size=sp(12),
            color=MUTED,
            height=dp(24),
        )
        input_panel.add_widget(self.ingredient_summary)
        root.add_widget(input_panel)

        # Daftar bahan dan hasil resep
        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
        )

        self.ingredient_panel = self.panel()
        self.ingredient_panel.orientation = "vertical"
        self.ingredient_panel.size_hint_y = None
        self.ingredient_panel.height = dp(115)
        self.ingredient_panel.padding = dp(13)
        self.ingredient_panel.spacing = dp(7)

        self.ingredient_panel.add_widget(self.label(
            "BAHAN PILIHAN",
            size=sp(12),
            color=GREEN,
            bold=True,
            height=dp(20),
        ))

        self.chips = GridLayout(
            cols=1,
            spacing=dp(5),
            size_hint_y=None,
        )
        self.chips.bind(minimum_height=self.chips.setter("height"))

        chips_scroll = ScrollView(do_scroll_x=False)
        chips_scroll.add_widget(self.chips)
        self.ingredient_panel.add_widget(chips_scroll)
        self.content.add_widget(self.ingredient_panel)

        action_row = BoxLayout(
            size_hint_y=None,
            height=dp(44),
            spacing=dp(9),
        )
        action_row.add_widget(self.make_button(
            "Cari Resep",
            GREEN,
            SURFACE,
            self.search_recipes,
        ))
        action_row.add_widget(self.make_button(
            "Menu Acak",
            GREEN_LIGHT,
            GREEN,
            self.random_menu,
        ))
        self.content.add_widget(action_row)

        self.results_panel = self.panel()
        self.results_panel.orientation = "vertical"
        self.results_panel.padding = dp(15)
        self.results_panel.spacing = dp(10)

        self.results_panel.add_widget(self.label(
            "IDE MASAKAN",
            size=sp(12),
            color=GREEN,
            bold=True,
            height=dp(22),
        ))

        self.result_body = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
        )
        self.result_body.bind(
            minimum_height=self.result_body.setter("height")
        )

        results_scroll = ScrollView(do_scroll_x=False)
        results_scroll.add_widget(self.result_body)
        self.results_panel.add_widget(results_scroll)
        self.content.add_widget(self.results_panel)

        root.add_widget(self.content)

        self.render_ingredients()
        self.show_message(
            "Mulai dari bahan yang ada di dapur. "
            "MenuKu akan membantu mencari ide masakan."
        )

        return root

    def label(
        self, text, size=sp(14), color=TEXT,
        bold=False, height=None
    ):
        widget = Label(
            text=text,
            font_size=size,
            color=color,
            bold=bold,
            halign="left",
            valign="middle",
            size_hint_y=None,
        )
        if height is not None:
            widget.height = height
        else:
            widget.bind(
                texture_size=lambda instance, value:
                setattr(instance, "height", value[1] + dp(8))
            )
        widget.bind(
            width=lambda instance, value:
            setattr(instance, "text_size", (max(value, 1), None))
        )
        return widget

    def panel(self):
        box = BoxLayout()
        with box.canvas.before:
            Color(*SURFACE)
            box.bg_rect = RoundedRectangle(
                pos=box.pos,
                size=box.size,
                radius=[dp(12)],
            )
        box.bind(
            pos=lambda instance, value:
            setattr(instance.bg_rect, "pos", value),
            size=lambda instance, value:
            setattr(instance.bg_rect, "size", value),
        )
        return box

    def make_button(self, text, bg, fg, callback, width=None):
        button = Button(
            text=text,
            font_size=sp(14),
            bold=True,
            color=fg,
            background_normal="",
            background_down="",
            background_color=bg,
            size_hint_x=None if width else 1,
            width=width or 0,
        )
        button.bind(on_release=lambda *_: callback())
        return button

    def add_ingredients(self):
        raw_text = self.ingredient_input.text.strip()
        if not raw_text:
            self.ingredient_summary.text = "Ketik bahan terlebih dahulu."
            return

        # Boleh memasukkan beberapa bahan sekaligus,
        # dipisahkan dengan koma.
        parts = [
            part.strip()
            for part in raw_text.split(",")
            if part.strip()
        ]

        for part in parts:
            normalized = normalize(part)
            if normalized and normalized not in [
                normalize(item) for item in self.ingredients
            ]:
                self.ingredients.append(part)

        self.ingredient_input.text = ""
        self.render_ingredients()

    def render_ingredients(self):
        self.chips.clear_widgets()

        if not self.ingredients:
            self.chips.add_widget(self.label(
                "Bahan yang ditambahkan akan muncul di sini.",
                size=sp(12),
                color=MUTED,
            ))
            self.ingredient_summary.text = (
                "Belum ada bahan yang ditambahkan."
            )
            return

        self.ingredient_summary.text = (
            f"{len(self.ingredients)} bahan sudah ditambahkan."
        )

        for index, ingredient in enumerate(self.ingredients):
            row = BoxLayout(
                size_hint_y=None,
                height=dp(32),
                spacing=dp(8),
            )
            row.add_widget(self.label(
                f"•  {ingredient}",
                size=sp(13),
                height=dp(30),
            ))
            remove_button = self.make_button(
                "Hapus",
                BG,
                GREEN,
                lambda i=index: self.remove_ingredient(i),
                width=dp(72),
            )
            row.add_widget(remove_button)
            self.chips.add_widget(row)

        self.ingredient_panel.height = min(
            dp(115) + max(0, len(self.ingredients) - 2) * dp(27),
            dp(205),
        )

    def remove_ingredient(self, index):
        if 0 <= index < len(self.ingredients):
            self.ingredients.pop(index)
            self.render_ingredients()

    def show_message(self, message):
        self.result_body.clear_widgets()
        self.result_body.add_widget(self.label(
            message,
            size=sp(14),
            color=MUTED,
        ))

    def search_recipes(self):
        if not self.ingredients:
            self.show_message(
                "Tambahkan bahan makanan terlebih dahulu."
            )
            return

        available = {normalize(item) for item in self.ingredients}
        matches = []

        for recipe in RECIPES:
            recipe_ingredients = {
                normalize(item) for item in recipe["ingredients"]
            }
            matched = available & recipe_ingredients

            if matched:
                matches.append((
                    len(matched),
                    recipe,
                    matched,
                ))

        matches.sort(key=lambda item: item[0], reverse=True)
        self.current_recipes = [
            item[1] for item in matches
        ]

        if not matches:
            self.show_message(
                "Belum ada resep yang cocok dengan bahan tersebut. "
                "Coba tambahkan telur, nasi, atau mi."
            )
            return

        self.result_body.clear_widgets()
        self.result_body.add_widget(self.label(
            f"Ditemukan {len(matches)} ide masakan.",
            size=sp(13),
            color=MUTED,
        ))

        for _, recipe, matched in matches:
            self.render_recipe(recipe, matched)

    def random_menu(self):
        if not self.ingredients:
            recipe = random.choice(RECIPES)
            self.result_body.clear_widgets()
            self.result_body.add_widget(self.label(
                "Belum ada bahan yang dimasukkan. "
                "Ini pilihan menu acak untuk inspirasi:",
                size=sp(13),
                color=MUTED,
            ))
            self.render_recipe(recipe, set())
            return

        available = {normalize(item) for item in self.ingredients}
        matches = []

        for recipe in RECIPES:
            recipe_ingredients = {
                normalize(item) for item in recipe["ingredients"]
            }
            matched = available & recipe_ingredients
            if matched:
                matches.append((recipe, matched))

        if not matches:
            self.show_message(
                "Belum ada menu yang cocok. "
                "Coba tambahkan bahan lain."
            )
            return

        recipe, matched = random.choice(matches)
        self.result_body.clear_widgets()
        self.result_body.add_widget(self.label(
            "Pilihan acak untuk hari ini:",
            size=sp(13),
            color=MUTED,
        ))
        self.render_recipe(recipe, matched)

    def render_recipe(self, recipe, matched):
        card = self.panel()
        card.orientation = "vertical"
        card.size_hint_y = None
        card.padding = dp(12)
        card.spacing = dp(7)

        available = {normalize(item) for item in self.ingredients}
        required = {
            normalize(item) for item in recipe["ingredients"]
        }
        missing = sorted(required - available)

        card.add_widget(self.label(
            recipe["name"],
            size=sp(17),
            color=GREEN,
            bold=True,
        ))

        card.add_widget(self.label(
            f"Bahan cocok: {len(matched)} dari "
            f"{len(recipe['ingredients'])}",
            size=sp(12),
            color=MUTED,
        ))

        if self.ingredients:
            missing_text = (
                ", ".join(missing) if missing else "Tidak ada"
            )
            card.add_widget(self.label(
                f"Bahan yang kurang: {missing_text}",
                size=sp(13),
                color=TEXT,
            ))
        else:
            card.add_widget(self.label(
                "Bahan yang diperlukan: "
                + ", ".join(recipe["ingredients"]),
                size=sp(13),
                color=TEXT,
            ))

        card.add_widget(self.label(
            "LANGKAH MEMASAK",
            size=sp(12),
            color=GREEN,
            bold=True,
        ))

        for number, step in enumerate(recipe["steps"], start=1):
            card.add_widget(self.label(
                f"{number}. {step}",
                size=sp(13),
                color=TEXT,
            ))

        card.height = sum(
            child.height for child in card.children
        ) + dp(24) + dp(7) * max(0, len(card.children) - 1)

        self.result_body.add_widget(card)


if __name__ == "__main__":
    MenuKuApp().run()
