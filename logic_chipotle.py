# logic.py
# ─────────────────────────────────────────────────────────────────────────────
# All menu data, step definitions, selection state, and nutrition calculations.
# No tkinter — completely independent of the GUI.
# ─────────────────────────────────────────────────────────────────────────────

# ── Menu data ─────────────────────────────────────────────────────────────────
MENU_DATA = [
    # base
    {"item_name": "Bowl",             "category": "base",    "portion": "1 bowl",      "calories": 0,   "protein": 0,  "carbs": 0,  "fat": 0},
    {"item_name": "Burrito Tortilla", "category": "base",    "portion": "1 tortilla",  "calories": 320, "protein": 8,  "carbs": 50, "fat": 9},
    {"item_name": "Tacos (3 Soft)",   "category": "base",    "portion": "3 tortillas", "calories": 210, "protein": 6,  "carbs": 33, "fat": 6},
    {"item_name": "Tacos (3 Crispy)", "category": "base",    "portion": "3 shells",    "calories": 195, "protein": 3,  "carbs": 27, "fat": 9},
    {"item_name": "Quesadilla",       "category": "base",    "portion": "1 whole",     "calories": 500, "protein": 18, "carbs": 49, "fat": 25},
    # rice
    {"item_name": "White Rice",       "category": "rice",    "portion": "4 oz",        "calories": 210, "protein": 4,  "carbs": 40, "fat": 4},
    {"item_name": "Brown Rice",       "category": "rice",    "portion": "4 oz",        "calories": 210, "protein": 4,  "carbs": 36, "fat": 6},
    # beans
    {"item_name": "Black Beans",      "category": "beans",   "portion": "4 oz",        "calories": 130, "protein": 8,  "carbs": 22, "fat": 1},
    {"item_name": "Pinto Beans",      "category": "beans",   "portion": "4 oz",        "calories": 130, "protein": 8,  "carbs": 21, "fat": 1},
    # protein
    {"item_name": "Chicken",          "category": "protein", "portion": "4 oz",        "calories": 180, "protein": 32, "carbs": 0,  "fat": 7},
    {"item_name": "Steak",            "category": "protein", "portion": "4 oz",        "calories": 150, "protein": 21, "carbs": 1,  "fat": 6},
    {"item_name": "Barbacoa",         "category": "protein", "portion": "4 oz",        "calories": 170, "protein": 24, "carbs": 2,  "fat": 7},
    {"item_name": "Carnitas",         "category": "protein", "portion": "4 oz",        "calories": 210, "protein": 23, "carbs": 0,  "fat": 12},
    {"item_name": "Sofritas",         "category": "protein", "portion": "4 oz",        "calories": 150, "protein": 8,  "carbs": 9,  "fat": 10},
    # veggies
    {"item_name": "Fajita Veggies",   "category": "veggies", "portion": "3 oz",        "calories": 20,  "protein": 1,  "carbs": 4,  "fat": 0},
    # salsa
    {"item_name": "Tomato Salsa",     "category": "salsa",   "portion": "2 oz",        "calories": 25,  "protein": 0,  "carbs": 4,  "fat": 0},
    {"item_name": "Corn Salsa",       "category": "salsa",   "portion": "2 oz",        "calories": 80,  "protein": 3,  "carbs": 16, "fat": 1},
    {"item_name": "Green Salsa",      "category": "salsa",   "portion": "2 oz",        "calories": 15,  "protein": 0,  "carbs": 3,  "fat": 0},
    {"item_name": "Red Salsa",        "category": "salsa",   "portion": "2 oz",        "calories": 30,  "protein": 0,  "carbs": 4,  "fat": 1},
    # dairy
    {"item_name": "Cheese",           "category": "dairy",   "portion": "1 oz",        "calories": 110, "protein": 6,  "carbs": 1,  "fat": 9},
    {"item_name": "Sour Cream",       "category": "dairy",   "portion": "2 oz",        "calories": 120, "protein": 2,  "carbs": 2,  "fat": 10},
    # extras
    {"item_name": "Guacamole",        "category": "extras",  "portion": "4 oz",        "calories": 230, "protein": 2,  "carbs": 8,  "fat": 22},
    {"item_name": "Queso",            "category": "extras",  "portion": "4 oz",        "calories": 120, "protein": 6,  "carbs": 8,  "fat": 8},
    {"item_name": "Lettuce",          "category": "extras",  "portion": "1 oz",        "calories": 5,   "protein": 0,  "carbs": 1,  "fat": 0},
]

# ── Step definitions ──────────────────────────────────────────────────────────
# Each step is a tuple: (step_id, kind, allow_none)
#   step_id    — key used in selections dict and STEP_TITLES
#   kind       — "single" | "multi" | "toggle" | "qesa_veggies" | "summary"
#   allow_none — only relevant for "single" steps; adds a "None" option

ALL_STEPS = [
    ("base",           "single",       False),
    ("rice",           "single",       True),
    ("beans",          "single",       True),
    ("protein",        "single",       True),
    ("double_protein", "toggle",       False),
    ("veggies",        "multi",        False),
    ("salsa",          "multi",        False),
    ("dairy",          "multi",        False),
    ("extras",         "multi",        False),
    ("summary",        "summary",      False),
]

# Quesadillas skip rice, beans, salsa, dairy, extras, double protein.
# Cheese is always included. Only protein (optional) and fajita veggies (yes/no).
QUESADILLA_STEPS = [
    ("base",           "single",       False),
    ("protein",        "single",       True),
    ("qesa_veggies",   "qesa_veggies", False),
    ("summary",        "summary",      False),
]

STEP_TITLES = {
    "base":           "Choose your base",
    "rice":           "Choose your rice",
    "beans":          "Choose your beans",
    "protein":        "Choose your protein",
    "double_protein": "Double protein?",
    "veggies":        "Choose your veggies",
    "salsa":          "Choose your salsa",
    "dairy":          "Choose your dairy",
    "extras":         "Choose your extras",
    "qesa_veggies":   "Add fajita veggies?",
    "summary":        "Your order summary",
}


# ── Helper — build category index ─────────────────────────────────────────────
def build_category_index(data):
    """Return dict mapping category name -> list of item dicts."""
    index = {}
    for item in data:
        index.setdefault(item["category"], []).append(item)
    return index


# ── Selection state ───────────────────────────────────────────────────────────
def fresh_selections():
    """Return a blank selections dict."""
    return {
        "base":          None,   # str item name or None
        "rice":          None,
        "beans":         None,
        "protein":       None,
        "double_protein": False, # bool
        "veggies":       [],     # list of str item names
        "salsa":         [],
        "dairy":         [],
        "extras":        [],
        "qesa_veggies":  False,  # bool — fajita veggies inside quesadilla
    }


# ── Step routing ──────────────────────────────────────────────────────────────
def is_quesadilla(selections):
    """Return True if the user picked a Quesadilla base."""
    return selections.get("base") == "Quesadilla"


def active_steps(selections):
    """Return the correct step list based on current base selection."""
    return QUESADILLA_STEPS if is_quesadilla(selections) else ALL_STEPS


# ── Nutrition calculation ─────────────────────────────────────────────────────
def build_order_lines(selections, item_lookup):
    """
    Return a list of (label, category_tag, item_dict) tuples representing
    every item in the current order, and a totals dict.

    The totals dict has keys: calories, protein, carbs, fat.
    """
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    order_lines = []

    def _add(item, mult=1):
        for k in totals:
            totals[k] += item[k] * mult

    if is_quesadilla(selections):
        # Quesadilla shell (calories already baked into the base item)
        base_item = item_lookup["Quesadilla"]
        order_lines.append(("Quesadilla", "base", base_item))
        _add(base_item)

        # Cheese is always included in a quesadilla
        cheese = item_lookup["Cheese"]
        order_lines.append(("Cheese (included)", "dairy", cheese))
        _add(cheese)

        # Optional protein
        if selections["protein"]:
            it = item_lookup[selections["protein"]]
            order_lines.append((selections["protein"], "protein", it))
            _add(it)

        # Optional fajita veggies
        if selections["qesa_veggies"]:
            veg = item_lookup["Fajita Veggies"]
            order_lines.append(("Fajita Veggies", "veggies", veg))
            _add(veg)

    else:
        # Standard bowl / burrito / taco build
        for cat in ("base", "rice", "beans"):
            name = selections[cat]
            if name:
                it = item_lookup[name]
                order_lines.append((name, cat, it))
                _add(it)

        if selections["protein"]:
            it = item_lookup[selections["protein"]]
            mult = 2 if selections["double_protein"] else 1
            label = selections["protein"] + (" (×2)" if mult == 2 else "")
            order_lines.append((label, "protein", it))
            _add(it, mult)

        for cat in ("veggies", "salsa", "dairy", "extras"):
            for name in selections[cat]:
                it = item_lookup[name]
                order_lines.append((name, cat, it))
                _add(it)

    return order_lines, totals