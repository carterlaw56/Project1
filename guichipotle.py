import tkinter as tk

# ── Embedded menu data ────────────────────────────────────────────────────────
MENU_DATA = [
    {"item_name": "Bowl",             "category": "base",    "portion": "1 bowl",      "calories": 0,   "protein": 0,  "carbs": 0,  "fat": 0},
    {"item_name": "Burrito Tortilla", "category": "base",    "portion": "1 tortilla",  "calories": 320, "protein": 8,  "carbs": 50, "fat": 9},
    {"item_name": "Tacos (3 Soft)",   "category": "base",    "portion": "3 tortillas", "calories": 210, "protein": 6,  "carbs": 33, "fat": 6},
    {"item_name": "Tacos (3 Crispy)","category": "base",    "portion": "3 shells",    "calories": 195, "protein": 3,  "carbs": 27, "fat": 9},
    {"item_name": "Quesadilla",       "category": "base",    "portion": "1 whole",     "calories": 500, "protein": 18, "carbs": 49, "fat": 25},
    {"item_name": "White Rice",       "category": "rice",    "portion": "4 oz",        "calories": 210, "protein": 4,  "carbs": 40, "fat": 4},
    {"item_name": "Brown Rice",       "category": "rice",    "portion": "4 oz",        "calories": 210, "protein": 4,  "carbs": 36, "fat": 6},
    {"item_name": "Black Beans",      "category": "beans",   "portion": "4 oz",        "calories": 130, "protein": 8,  "carbs": 22, "fat": 1},
    {"item_name": "Pinto Beans",      "category": "beans",   "portion": "4 oz",        "calories": 130, "protein": 8,  "carbs": 21, "fat": 1},
    {"item_name": "Chicken",          "category": "protein", "portion": "4 oz",        "calories": 180, "protein": 32, "carbs": 0,  "fat": 7},
    {"item_name": "Steak",            "category": "protein", "portion": "4 oz",        "calories": 150, "protein": 21, "carbs": 1,  "fat": 6},
    {"item_name": "Barbacoa",         "category": "protein", "portion": "4 oz",        "calories": 170, "protein": 24, "carbs": 2,  "fat": 7},
    {"item_name": "Carnitas",         "category": "protein", "portion": "4 oz",        "calories": 210, "protein": 23, "carbs": 0,  "fat": 12},
    {"item_name": "Sofritas",         "category": "protein", "portion": "4 oz",        "calories": 150, "protein": 8,  "carbs": 9,  "fat": 10},
    {"item_name": "Fajita Veggies",   "category": "veggies", "portion": "3 oz",        "calories": 20,  "protein": 1,  "carbs": 4,  "fat": 0},
    {"item_name": "Tomato Salsa",     "category": "salsa",   "portion": "2 oz",        "calories": 25,  "protein": 0,  "carbs": 4,  "fat": 0},
    {"item_name": "Corn Salsa",       "category": "salsa",   "portion": "2 oz",        "calories": 80,  "protein": 3,  "carbs": 16, "fat": 1},
    {"item_name": "Green Salsa",      "category": "salsa",   "portion": "2 oz",        "calories": 15,  "protein": 0,  "carbs": 3,  "fat": 0},
    {"item_name": "Red Salsa",        "category": "salsa",   "portion": "2 oz",        "calories": 30,  "protein": 0,  "carbs": 4,  "fat": 1},
    {"item_name": "Cheese",           "category": "dairy",   "portion": "1 oz",        "calories": 110, "protein": 6,  "carbs": 1,  "fat": 9},
    {"item_name": "Sour Cream",       "category": "dairy",   "portion": "2 oz",        "calories": 120, "protein": 2,  "carbs": 2,  "fat": 10},
    {"item_name": "Guacamole",        "category": "extras",  "portion": "4 oz",        "calories": 230, "protein": 2,  "carbs": 8,  "fat": 22},
    {"item_name": "Queso",            "category": "extras",  "portion": "4 oz",        "calories": 120, "protein": 6,  "carbs": 8,  "fat": 8},
    {"item_name": "Lettuce",          "category": "extras",  "portion": "1 oz",        "calories": 5,   "protein": 0,  "carbs": 1,  "fat": 0},
]

# ── Theme ─────────────────────────────────────────────────────────────────────
BG            = "#F5F0EB"
CARD_BG       = "#FFFFFF"
ACCENT        = "#D85A30"
ACCENT_DARK   = "#993C1D"
TEXT_PRI      = "#1C1916"
TEXT_SEC      = "#6B635C"
SEL_BG        = "#FAECE7"
BORDER        = "#E0D9D2"
BTN_DANGER    = "#A32D2D"
BTN_DANGER_BG = "#FCEBEB"


def group_by_category(data):
    cats = {}
    for item in data:
        cats.setdefault(item["category"], []).append(item)
    return cats


class ChipotleApp:
    # All possible steps
    ALL_STEPS = [
        ("base",           "single",  False),
        ("rice",           "single",  True),
        ("beans",          "single",  True),
        ("protein",        "single",  True),
        ("double_protein", "toggle",  False),
        ("veggies",        "multi",   False),
        ("salsa",          "multi",   False),
        ("dairy",          "multi",   False),
        ("extras",         "multi",   False),
        ("summary",        "summary", False),
    ]
    # Quesadilla-only steps: base → protein → fajita veggies → summary
    QUESADILLA_STEPS = [
        ("base",           "single",       False),
        ("protein",        "single",       True),   # allow None (no protein)
        ("qesa_veggies",   "qesa_veggies", False),  # yes/no fajita veggies
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

    def _is_quesadilla(self):
        return self.selections.get("base") == "Quesadilla"

    def _active_steps(self):
        return self.QUESADILLA_STEPS if self._is_quesadilla() else self.ALL_STEPS

    def __init__(self, root):
        self.root = root
        self.root.title("Chipotle Nutrition Calculator")
        self.root.geometry("600x580")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.categories  = group_by_category(MENU_DATA)
        self.item_lookup = {it["item_name"]: it for it in MENU_DATA}

        # tk vars — created once, reused across steps
        self._single_var = tk.StringVar()
        self._double_var   = tk.BooleanVar()
        self._qesa_veg_var = tk.BooleanVar()   # fajita veggies for quesadilla
        self._multi_vars = {}           # name -> BooleanVar, rebuilt each multi step
        self._single_step = None        # which category _single_var belongs to

        self._fresh_selections()
        self.current_step = 0
        self._build_skeleton()
        self._show_step()

    # ── state ─────────────────────────────────────────────────────────────────
    def _fresh_selections(self):
        self.selections = {
            "base": None, "rice": None, "beans": None,
            "protein": None, "double_protein": False,
            "veggies": [], "salsa": [], "dairy": [], "extras": [],
            "qesa_veggies": False,   # fajita veggies added to quesadilla
        }

    # ── static skeleton (built once) ──────────────────────────────────────────
    def _build_skeleton(self):
        hdr = tk.Frame(self.root, bg=ACCENT, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Chipotle Nutrition Calculator",
                 font=("Helvetica", 17, "bold"),
                 bg=ACCENT, fg="white").pack()
        tk.Label(hdr, text="Build your meal · track your macros",
                 font=("Helvetica", 10), bg=ACCENT, fg="#FAECE7").pack(pady=(2, 0))

        self.prog_canvas = tk.Canvas(self.root, height=5, bg=BORDER,
                                     highlightthickness=0, bd=0)
        self.prog_canvas.pack(fill="x")
        self.prog_fill = self.prog_canvas.create_rectangle(
            0, 0, 0, 5, fill=ACCENT, outline="")

        self.step_lbl = tk.Label(self.root, text="",
                                  font=("Helvetica", 11),
                                  bg=BG, fg=TEXT_SEC, pady=7)
        self.step_lbl.pack()

        self.scroll_canvas = tk.Canvas(self.root, bg=BG,
                                        highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(self.root, orient="vertical",
                            command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.scroll_canvas.pack(fill="both", expand=True)

        self.content = tk.Frame(self.scroll_canvas, bg=BG)
        self._cwin = self.scroll_canvas.create_window(
            (0, 0), window=self.content, anchor="nw")

        self.content.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.itemconfig(
                self._cwin, width=e.width))
        self.scroll_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.scroll_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"))

        nav = tk.Frame(self.root, bg=BG, pady=9)
        nav.pack(fill="x", padx=18)
        nav.columnconfigure(1, weight=1)

        self.reset_btn = tk.Button(
            nav, text="Reset", font=("Helvetica", 11), width=8,
            bg=BTN_DANGER_BG, fg=BTN_DANGER,
            activebackground="#F7C1C1", activeforeground=BTN_DANGER,
            relief="flat", bd=0, cursor="hand2",
            command=self._reset_all)
        self.reset_btn.grid(row=0, column=0)

        right = tk.Frame(nav, bg=BG)
        right.grid(row=0, column=2, sticky="e")

        self.back_btn = tk.Button(
            right, text="← Back", font=("Helvetica", 11), width=9,
            bg=CARD_BG, fg=TEXT_PRI, activebackground=BORDER,
            relief="flat", bd=0, cursor="hand2",
            command=self._go_back)
        self.back_btn.pack(side="left", padx=(0, 6))

        self.next_btn = tk.Button(
            right, text="Next →", font=("Helvetica", 11, "bold"), width=11,
            bg=ACCENT, fg="white", activebackground=ACCENT_DARK,
            relief="flat", bd=0, cursor="hand2",
            command=self._go_next)
        self.next_btn.pack(side="left")

    # ── clear content area ────────────────────────────────────────────────────
    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── master show step ──────────────────────────────────────────────────────
    def _show_step(self):
        self._clear()
        steps = self._active_steps()
        step_id, kind, allow_none = steps[self.current_step]
        total = len(steps)

        self.prog_canvas.update_idletasks()
        pw = self.prog_canvas.winfo_width()
        pct = self.current_step / (total - 1)
        self.prog_canvas.coords(self.prog_fill, 0, 0, int(pw * pct), 5)

        self.step_lbl.config(
            text=f"Step {self.current_step + 1} of {total}"
                 f"  ·  {self.STEP_TITLES[step_id]}")

        if kind == "single":
            self._render_single(step_id, allow_none)
        elif kind == "toggle":
            self._render_toggle()
        elif kind == "multi":
            self._render_multi(step_id)
        elif kind == "qesa_veggies":
            self._render_qesa_veggies()
        elif kind == "summary":
            self._render_summary()

        self._update_nav()
        self.scroll_canvas.yview_moveto(0)

    # ── helpers ───────────────────────────────────────────────────────────────
    def _make_card(self, parent, title=None):
        outer = tk.Frame(parent, bg=BG, padx=16, pady=8)
        outer.pack(fill="x")
        card = tk.Frame(outer, bg=CARD_BG,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=BORDER)
        card.pack(fill="x")
        if title:
            tk.Label(card, text=title, font=("Helvetica", 12, "bold"),
                     bg=CARD_BG, fg=TEXT_PRI, anchor="w",
                     padx=14, pady=10).pack(fill="x")
            tk.Frame(card, bg=BORDER, height=1).pack(fill="x")
        return card

    def _recolor_widgets(self, container, bg):
        """Recursively set bg on all widgets inside container."""
        try:
            container.configure(bg=bg)
        except tk.TclError:
            pass
        for child in container.winfo_children():
            self._recolor_widgets(child, bg)

    # ── single-choice step ────────────────────────────────────────────────────
    def _render_single(self, step_id, allow_none):
        self._single_step = step_id
        items = self.categories.get(step_id, [])

        # restore saved selection
        saved = self.selections[step_id]
        if saved is None:
            init_val = "__none__" if allow_none else (
                items[0]["item_name"] if items else "")
        else:
            init_val = saved

        # set the shared var WITHOUT triggering old traces
        self._single_var.set(init_val)

        card = self._make_card(self.content)

        # row_meta: value -> {"row": frame, "accent": frame}
        row_meta = {}

        def _select(val):
            self._single_var.set(val)
            for v, meta in row_meta.items():
                sel = (v == val)
                bg = SEL_BG if sel else CARD_BG
                ab = ACCENT if sel else CARD_BG
                self._recolor_widgets(meta["row"], bg)
                meta["accent"].configure(bg=ab)

        def _add_row(val, label, sublabel):
            sel = (val == init_val)
            bg = SEL_BG if sel else CARD_BG

            row = tk.Frame(card, bg=bg, cursor="hand2")
            row.pack(fill="x")

            accent = tk.Frame(row, bg=ACCENT if sel else CARD_BG, width=4)
            accent.pack(side="left", fill="y")

            inner = tk.Frame(row, bg=bg, padx=10, pady=9)
            inner.pack(side="left", fill="x", expand=True)

            # Radiobutton — no command= so it never triggers a re-render
            rb = tk.Radiobutton(inner, variable=self._single_var, value=val,
                                 bg=bg, activebackground=bg,
                                 highlightthickness=0,
                                 command=lambda v=val: _select(v))
            rb.pack(side="left", padx=(0, 6))

            tk.Label(inner, text=label, font=("Helvetica", 11),
                     bg=bg, fg=TEXT_PRI, anchor="w").pack(side="left")

            if sublabel:
                tk.Label(inner, text=sublabel, font=("Helvetica", 10),
                         bg=bg, fg=TEXT_SEC).pack(side="right", padx=6)

            tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

            row_meta[val] = {"row": row, "accent": accent}

            for w in [row, inner, accent]:
                w.bind("<Button-1>", lambda e, v=val: _select(v))

        if allow_none:
            _add_row("__none__", "None", "")

        for it in items:
            sub = (f"{it['calories']} cal  ·  {it['portion']}"
                   if it["calories"] > 0 else it["portion"])
            _add_row(it["item_name"], it["item_name"], sub)

    # ── double-protein toggle ─────────────────────────────────────────────────
    def _render_toggle(self):
        self._double_var.set(self.selections["double_protein"])

        card = self._make_card(self.content, title="Double protein?")

        inner = tk.Frame(card, bg=CARD_BG, padx=14, pady=14)
        inner.pack(fill="x")
        tk.Checkbutton(inner,
                        text="Yes — double my protein",
                        variable=self._double_var,
                        font=("Helvetica", 12),
                        bg=CARD_BG, fg=TEXT_PRI,
                        activebackground=CARD_BG,
                        selectcolor=CARD_BG,
                        cursor="hand2").pack(anchor="w")

        note = ("Doubles calories, protein, carbs and fat for your protein choice."
                if self.selections["protein"]
                else "No protein selected — this option has no effect.")
        tk.Label(card, text=note, font=("Helvetica", 10),
                 bg=CARD_BG, fg=TEXT_SEC, padx=14, pady=6,
                 wraplength=480, justify="left").pack(anchor="w")

    # ── multi-choice step ─────────────────────────────────────────────────────
    def _render_multi(self, step_id):
        self._multi_vars = {}
        items = self.categories.get(step_id, [])

        card = self._make_card(self.content)

        if not items:
            tk.Label(card, text="No items available.",
                     font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_SEC, pady=12).pack()
            return

        row_meta = {}  # name -> {"row": frame, "accent": frame}

        def _recolor_all():
            for nm, meta in row_meta.items():
                sel = self._multi_vars[nm].get()
                bg = SEL_BG if sel else CARD_BG
                self._recolor_widgets(meta["row"], bg)
                meta["accent"].configure(bg=ACCENT if sel else CARD_BG)

        def _toggle_item(name):
            var = self._multi_vars[name]
            # update selections list
            if var.get():
                if name not in self.selections[step_id]:
                    self.selections[step_id].append(name)
            else:
                self.selections[step_id] = [
                    n for n in self.selections[step_id] if n != name]
            _recolor_all()

        def _row_click(name):
            self._multi_vars[name].set(not self._multi_vars[name].get())
            _toggle_item(name)

        for it in items:
            name = it["item_name"]
            checked = name in self.selections[step_id]
            var = tk.BooleanVar(value=checked)
            self._multi_vars[name] = var

            bg = SEL_BG if checked else CARD_BG

            row = tk.Frame(card, bg=bg, cursor="hand2")
            row.pack(fill="x")

            accent = tk.Frame(row, bg=ACCENT if checked else CARD_BG, width=4)
            accent.pack(side="left", fill="y")

            inner = tk.Frame(row, bg=bg, padx=10, pady=9)
            inner.pack(side="left", fill="x", expand=True)

            cb = tk.Checkbutton(inner, variable=var,
                                 bg=bg, activebackground=bg,
                                 selectcolor=CARD_BG,
                                 highlightthickness=0,
                                 cursor="hand2",
                                 command=lambda n=name: _toggle_item(n))
            cb.pack(side="left", padx=(0, 6))

            tk.Label(inner, text=name, font=("Helvetica", 11),
                     bg=bg, fg=TEXT_PRI, anchor="w").pack(side="left")

            sub = (f"{it['calories']} cal  ·  {it['portion']}"
                   if it["calories"] > 0 else it["portion"])
            tk.Label(inner, text=sub, font=("Helvetica", 10),
                     bg=bg, fg=TEXT_SEC).pack(side="right", padx=6)

            tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

            row_meta[name] = {"row": row, "accent": accent}

            for w in [row, inner, accent]:
                w.bind("<Button-1>", lambda e, n=name: _row_click(n))

    # ── quesadilla fajita-veggies yes/no ─────────────────────────────────────
    def _render_qesa_veggies(self):
        self._qesa_veg_var.set(self.selections["qesa_veggies"])

        card = self._make_card(self.content, title="Add fajita veggies?")

        note = tk.Frame(card, bg=CARD_BG, padx=14, pady=6)
        note.pack(fill="x")
        tk.Label(note,
                 text="Your quesadilla already includes cheese. "
                      "Would you like fajita veggies added inside?",
                 font=("Helvetica", 10), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=480, justify="left").pack(anchor="w")

        row_meta = {}

        def _pick(val):
            self._qesa_veg_var.set(val)
            for v, meta in row_meta.items():
                sel = (v == val)
                bg = SEL_BG if sel else CARD_BG
                self._recolor_widgets(meta["row"], bg)
                meta["accent"].configure(bg=ACCENT if sel else CARD_BG)

        def _add_row(val, label, sublabel):
            sel = (val == self._qesa_veg_var.get())
            bg = SEL_BG if sel else CARD_BG
            row = tk.Frame(card, bg=bg, cursor="hand2")
            row.pack(fill="x")
            accent = tk.Frame(row, bg=ACCENT if sel else CARD_BG, width=4)
            accent.pack(side="left", fill="y")
            inner = tk.Frame(row, bg=bg, padx=10, pady=9)
            inner.pack(side="left", fill="x", expand=True)
            rb = tk.Radiobutton(inner, variable=self._qesa_veg_var, value=val,
                                 bg=bg, activebackground=bg,
                                 highlightthickness=0,
                                 command=lambda v=val: _pick(v))
            rb.pack(side="left", padx=(0, 6))
            tk.Label(inner, text=label, font=("Helvetica", 11),
                     bg=bg, fg=TEXT_PRI, anchor="w").pack(side="left")
            if sublabel:
                tk.Label(inner, text=sublabel, font=("Helvetica", 10),
                         bg=bg, fg=TEXT_SEC).pack(side="right", padx=6)
            tk.Frame(card, bg=BORDER, height=1).pack(fill="x")
            row_meta[val] = {"row": row, "accent": accent}
            for w in [row, inner, accent]:
                w.bind("<Button-1>", lambda e, v=val: _pick(v))

        _add_row(False, "No thanks", "")
        _add_row(True,  "Yes, add fajita veggies", "20 cal  ·  3 oz")

    # ── summary step ──────────────────────────────────────────────────────────
    def _render_summary(self):
        totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

        def add(item, mult=1):
            for k in totals:
                totals[k] += item[k] * mult

        order_lines = []

        if self._is_quesadilla():
            # Base (Quesadilla shell + built-in cheese)
            base_it = self.item_lookup["Quesadilla"]
            order_lines.append(("Quesadilla", "base", base_it))
            add(base_it)

            # Cheese is always included — show it as a fixed line
            cheese_it = self.item_lookup["Cheese"]
            order_lines.append(("Cheese (included)", "dairy", cheese_it))
            add(cheese_it)

            # Protein (optional)
            pname = self.selections["protein"]
            if pname:
                it = self.item_lookup[pname]
                order_lines.append((pname, "protein", it))
                add(it)

            # Fajita veggies (optional)
            if self.selections["qesa_veggies"]:
                veg_it = self.item_lookup["Fajita Veggies"]
                order_lines.append(("Fajita Veggies", "veggies", veg_it))
                add(veg_it)

        else:
            for cat in ["base", "rice", "beans"]:
                name = self.selections[cat]
                if name:
                    it = self.item_lookup[name]
                    order_lines.append((name, cat, it))
                    add(it)

            pname = self.selections["protein"]
            if pname:
                it = self.item_lookup[pname]
                mult = 2 if self.selections["double_protein"] else 1
                label = pname + (" (×2)" if mult == 2 else "")
                order_lines.append((label, "protein", it))
                add(it, mult)

            for cat in ["veggies", "salsa", "dairy", "extras"]:
                for name in self.selections[cat]:
                    it = self.item_lookup[name]
                    order_lines.append((name, cat, it))
                    add(it)

        # macro cards
        macro_row = tk.Frame(self.content, bg=BG, padx=16, pady=10)
        macro_row.pack(fill="x")
        macros = [
            ("Calories", str(totals["calories"]), ACCENT),
            ("Protein",  f"{totals['protein']}g", "#185FA5"),
            ("Carbs",    f"{totals['carbs']}g",   "#3B6D11"),
            ("Fat",      f"{totals['fat']}g",      "#854F0B"),
        ]
        for i, (lbl, val, color) in enumerate(macros):
            cell = tk.Frame(macro_row, bg=color, padx=6, pady=8)
            cell.grid(row=0, column=i, padx=4, sticky="nsew")
            macro_row.columnconfigure(i, weight=1)
            tk.Label(cell, text=val, font=("Helvetica", 18, "bold"),
                     bg=color, fg="white").pack()
            tk.Label(cell, text=lbl, font=("Helvetica", 9),
                     bg=color, fg="white").pack()

        # order list
        card = self._make_card(self.content, title="Your order")

        if not order_lines:
            tk.Label(card, text="No items selected.",
                     font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_SEC, pady=12).pack()
        else:
            for label, cat, it in order_lines:
                row = tk.Frame(card, bg=CARD_BG, padx=14, pady=7)
                row.pack(fill="x")
                tk.Label(row, text=label, font=("Helvetica", 11),
                         bg=CARD_BG, fg=TEXT_PRI, anchor="w").pack(side="left")
                tk.Label(row, text=f"{it['calories']} cal",
                         font=("Helvetica", 10),
                         bg=CARD_BG, fg=TEXT_SEC).pack(side="right")
                tk.Label(row, text=cat, font=("Helvetica", 9),
                         bg=BG, fg=TEXT_SEC,
                         padx=6, pady=1).pack(side="right", padx=6)
                tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

    # ── save + navigate ───────────────────────────────────────────────────────
    def _save_step(self):
        steps = self._active_steps()
        _, kind, _ = steps[self.current_step]
        if kind == "single":
            val = self._single_var.get()
            self.selections[self._single_step] = (
                None if val == "__none__" else val)
        elif kind == "toggle":
            self.selections["double_protein"] = self._double_var.get()
        elif kind == "qesa_veggies":
            self.selections["qesa_veggies"] = self._qesa_veg_var.get()
        # multi is saved live on each checkbox click

    def _go_next(self):
        self._save_step()
        steps = self._active_steps()
        if steps[self.current_step][0] == "base":
            if not self.selections["base"]:
                self._popup("Please choose a base before continuing.")
                return
        # If user just picked base, clamp step index in case flow length changed
        if self.current_step < len(steps) - 1:
            self.current_step += 1
            # Re-evaluate active steps after potential base change
            self._show_step()

    def _go_back(self):
        self._save_step()
        if self.current_step > 0:
            self.current_step -= 1
            self._show_step()

    def _update_nav(self):
        steps = self._active_steps()
        last = len(steps) - 1
        self.back_btn.config(
            state="disabled" if self.current_step == 0 else "normal")

        if self.current_step == last:
            self.next_btn.config(text="Done", state="normal",
                                  command=self._reset_all)
        elif self.current_step == last - 1:
            self.next_btn.config(text="Summary →", state="normal",
                                  command=self._go_next)
        else:
            self.next_btn.config(text="Next →", state="normal",
                                  command=self._go_next)

    def _reset_all(self):
        self._fresh_selections()
        self.current_step = 0
        self._qesa_veg_var.set(False)
        self._show_step()

    def _popup(self, msg):
        pop = tk.Toplevel(self.root)
        pop.title("")
        pop.resizable(False, False)
        pop.configure(bg=CARD_BG)
        pop.grab_set()
        tk.Label(pop, text=msg, font=("Helvetica", 11),
                 bg=CARD_BG, fg=TEXT_PRI,
                 padx=24, pady=16, wraplength=300).pack()
        tk.Button(pop, text="OK", font=("Helvetica", 11, "bold"),
                  bg=ACCENT, fg="white", activebackground=ACCENT_DARK,
                  relief="flat", bd=0, padx=20, pady=6,
                  command=pop.destroy).pack(pady=(0, 14))
        pop.update_idletasks()
        x = (self.root.winfo_x() +
             (self.root.winfo_width()  - pop.winfo_width())  // 2)
        y = (self.root.winfo_y() +
             (self.root.winfo_height() - pop.winfo_height()) // 2)
        pop.geometry(f"+{x}+{y}")


def main():
    root = tk.Tk()
    ChipotleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()