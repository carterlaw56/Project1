# gui.py
# ─────────────────────────────────────────────────────────────────────────────
# Tkinter GUI for the Chipotle Nutrition Calculator.
# All data, step definitions, and nutrition logic live in logic.py.
# Run this file directly to launch the app.
# ─────────────────────────────────────────────────────────────────────────────

import tkinter as tk

from logic_chipotle import (
    MENU_DATA,
    STEP_TITLES,
    build_category_index,
    fresh_selections,
    active_steps,
    is_quesadilla,
    build_order_lines,
)

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

COLOR_CALORIES = ACCENT
COLOR_PROTEIN  = "#185FA5"
COLOR_CARBS    = "#3B6D11"
COLOR_FAT      = "#854F0B"


class ChipotleApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chipotle Nutrition Calculator")
        self.root.geometry("600x580")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.categories  = build_category_index(MENU_DATA)
        self.item_lookup = {it["item_name"]: it for it in MENU_DATA}

        # Persistent tk variables — created once, reused every redraw
        self._single_var   = tk.StringVar()
        self._double_var   = tk.BooleanVar()
        self._qesa_veg_var = tk.BooleanVar()
        self._multi_vars   = {}    # name -> BooleanVar, rebuilt each multi step
        self._single_step  = None  # which category _single_var belongs to

        self.selections   = fresh_selections()
        self.current_step = 0

        self._build_skeleton()
        self._show_step()

    # ── Static skeleton ───────────────────────────────────────────────────────

    def _build_skeleton(self):
        # Header
        hdr = tk.Frame(self.root, bg=ACCENT, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Chipotle Nutrition Calculator",
                 font=("Helvetica", 17, "bold"),
                 bg=ACCENT, fg="white").pack()
        tk.Label(hdr, text="Build your meal · track your macros",
                 font=("Helvetica", 10), bg=ACCENT, fg="#FAECE7").pack(pady=(2, 0))

        # Progress bar
        self.prog_canvas = tk.Canvas(self.root, height=5, bg=BORDER,
                                     highlightthickness=0, bd=0)
        self.prog_canvas.pack(fill="x")
        self.prog_fill = self.prog_canvas.create_rectangle(
            0, 0, 0, 5, fill=ACCENT, outline="")

        # Step label
        self.step_lbl = tk.Label(self.root, text="",
                                  font=("Helvetica", 11),
                                  bg=BG, fg=TEXT_SEC, pady=7)
        self.step_lbl.pack()

        # Scrollable content area
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

        # Nav bar
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

    # ── Step rendering ────────────────────────────────────────────────────────

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _show_step(self):
        self._clear()

        steps = active_steps(self.selections)
        step_id, kind, allow_none = steps[self.current_step]
        total = len(steps)

        # Progress bar
        self.prog_canvas.update_idletasks()
        pw = self.prog_canvas.winfo_width()
        pct = self.current_step / (total - 1)
        self.prog_canvas.coords(self.prog_fill, 0, 0, int(pw * pct), 5)

        self.step_lbl.config(
            text=f"Step {self.current_step + 1} of {total}"
                 f"  ·  {STEP_TITLES[step_id]}")

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

    # ── Widget helpers ────────────────────────────────────────────────────────

    def _make_card(self, parent, title=None):
        """White bordered card. Returns the inner card frame."""
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
        """Recursively apply bg to a widget and all its children."""
        try:
            container.configure(bg=bg)
        except tk.TclError:
            pass
        for child in container.winfo_children():
            self._recolor_widgets(child, bg)

    def _make_option_row(self, card, label, sublabel, is_selected, make_control):
        """
        Build one selectable row inside a card and return (row, accent).

        make_control(inner_frame) -> widget
            Called with the already-created inner frame so the control widget
            is parented correctly from the start — no reparenting needed.
        """
        bg = SEL_BG if is_selected else CARD_BG

        row = tk.Frame(card, bg=bg, cursor="hand2")
        row.pack(fill="x")

        accent = tk.Frame(row, bg=ACCENT if is_selected else CARD_BG, width=4)
        accent.pack(side="left", fill="y")

        inner = tk.Frame(row, bg=bg, padx=10, pady=9)
        inner.pack(side="left", fill="x", expand=True)

        # Control widget (Radiobutton or Checkbutton) created HERE with inner
        # as its parent — this is the key fix vs the previous version.
        ctrl = make_control(inner)
        ctrl.pack(side="left", padx=(0, 6))

        tk.Label(inner, text=label, font=("Helvetica", 11),
                 bg=bg, fg=TEXT_PRI, anchor="w").pack(side="left")

        if sublabel:
            tk.Label(inner, text=sublabel, font=("Helvetica", 10),
                     bg=bg, fg=TEXT_SEC).pack(side="right", padx=6)

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

        return row, accent, inner

    # ── Single-choice (radio) ─────────────────────────────────────────────────

    def _render_single(self, step_id, allow_none):
        self._single_step = step_id
        items = self.categories.get(step_id, [])

        saved = self.selections[step_id]
        init_val = (saved if saved is not None
                    else ("__none__" if allow_none
                          else (items[0]["item_name"] if items else "")))
        self._single_var.set(init_val)

        card     = self._make_card(self.content)
        row_meta = {}  # val -> (row_frame, accent_frame)

        def _select(val):
            self._single_var.set(val)
            for v, (rf, ab) in row_meta.items():
                sel = (v == val)
                self._recolor_widgets(rf, SEL_BG if sel else CARD_BG)
                ab.configure(bg=ACCENT if sel else CARD_BG)

        def _add_row(val, label, sublabel):
            sel = (val == init_val)

            def make_ctrl(inner):
                return tk.Radiobutton(
                    inner,                          # ← correct parent
                    variable=self._single_var,
                    value=val,
                    bg=SEL_BG if sel else CARD_BG,
                    activebackground=SEL_BG if sel else CARD_BG,
                    highlightthickness=0,
                    command=lambda v=val: _select(v))

            rf, ab, inner = self._make_option_row(
                card, label, sublabel, sel, make_ctrl)

            row_meta[val] = (rf, ab)

            # Clicking the whole row also selects
            for w in (rf, inner, ab):
                w.bind("<Button-1>", lambda e, v=val: _select(v))

        if allow_none:
            _add_row("__none__", "None", "")
        for it in items:
            sub = (f"{it['calories']} cal  ·  {it['portion']}"
                   if it["calories"] > 0 else it["portion"])
            _add_row(it["item_name"], it["item_name"], sub)

    # ── Double-protein toggle ─────────────────────────────────────────────────

    def _render_toggle(self):
        self._double_var.set(self.selections["double_protein"])

        card  = self._make_card(self.content, title="Double protein?")
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

    # ── Multi-choice (checkboxes) ─────────────────────────────────────────────

    def _render_multi(self, step_id):
        self._multi_vars = {}
        items = self.categories.get(step_id, [])
        card  = self._make_card(self.content)

        if not items:
            tk.Label(card, text="No items available.",
                     font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_SEC, pady=12).pack()
            return

        row_meta = {}  # name -> (row_frame, accent_frame)

        def _recolor_all():
            for nm, (rf, ab) in row_meta.items():
                sel = self._multi_vars[nm].get()
                self._recolor_widgets(rf, SEL_BG if sel else CARD_BG)
                ab.configure(bg=ACCENT if sel else CARD_BG)

        def _toggle(name):
            var = self._multi_vars[name]
            if var.get():
                if name not in self.selections[step_id]:
                    self.selections[step_id].append(name)
            else:
                self.selections[step_id] = [
                    n for n in self.selections[step_id] if n != name]
            _recolor_all()

        for it in items:
            name    = it["item_name"]
            checked = name in self.selections[step_id]
            var     = tk.BooleanVar(value=checked)
            self._multi_vars[name] = var

            sub = (f"{it['calories']} cal  ·  {it['portion']}"
                   if it["calories"] > 0 else it["portion"])

            def make_ctrl(inner, n=name, v=var):
                return tk.Checkbutton(
                    inner,                          # ← correct parent
                    variable=v,
                    bg=SEL_BG if v.get() else CARD_BG,
                    activebackground=SEL_BG if v.get() else CARD_BG,
                    selectcolor=CARD_BG,
                    highlightthickness=0,
                    cursor="hand2",
                    command=lambda nm=n: _toggle(nm))

            rf, ab, inner_f = self._make_option_row(
                card, name, sub, checked, make_ctrl)

            row_meta[name] = (rf, ab)

            # Row click toggles the checkbox
            for w in (rf, inner_f, ab):
                w.bind("<Button-1>", lambda e, n=name, v=var: (
                    v.set(not v.get()), _toggle(n)))

    # ── Quesadilla fajita-veggies yes/no ─────────────────────────────────────

    def _render_qesa_veggies(self):
        self._qesa_veg_var.set(self.selections["qesa_veggies"])

        card = self._make_card(self.content, title="Add fajita veggies?")

        note_f = tk.Frame(card, bg=CARD_BG, padx=14, pady=6)
        note_f.pack(fill="x")
        tk.Label(note_f,
                 text="Your quesadilla already includes cheese. "
                      "Would you like fajita veggies added inside?",
                 font=("Helvetica", 10), bg=CARD_BG, fg=TEXT_SEC,
                 wraplength=480, justify="left").pack(anchor="w")

        row_meta = {}  # val -> (row_frame, accent_frame)

        def _pick(val):
            self._qesa_veg_var.set(val)
            for v, (rf, ab) in row_meta.items():
                sel = (v == val)
                self._recolor_widgets(rf, SEL_BG if sel else CARD_BG)
                ab.configure(bg=ACCENT if sel else CARD_BG)

        def _add_row(val, label, sublabel):
            sel = (val == self._qesa_veg_var.get())

            def make_ctrl(inner, v=val):
                return tk.Radiobutton(
                    inner,                          # ← correct parent
                    variable=self._qesa_veg_var,
                    value=v,
                    bg=SEL_BG if sel else CARD_BG,
                    activebackground=SEL_BG if sel else CARD_BG,
                    highlightthickness=0,
                    command=lambda vv=v: _pick(vv))

            rf, ab, inner_f = self._make_option_row(
                card, label, sublabel, sel, make_ctrl)

            row_meta[val] = (rf, ab)

            for w in (rf, inner_f, ab):
                w.bind("<Button-1>", lambda e, v=val: _pick(v))

        _add_row(False, "No thanks", "")
        _add_row(True,  "Yes, add fajita veggies", "20 cal  ·  3 oz")

    # ── Summary ───────────────────────────────────────────────────────────────

    def _render_summary(self):
        order_lines, totals = build_order_lines(self.selections, self.item_lookup)

        # Macro cards
        macro_row = tk.Frame(self.content, bg=BG, padx=16, pady=10)
        macro_row.pack(fill="x")
        macros = [
            ("Calories", str(totals["calories"]), COLOR_CALORIES),
            ("Protein",  f"{totals['protein']}g", COLOR_PROTEIN),
            ("Carbs",    f"{totals['carbs']}g",   COLOR_CARBS),
            ("Fat",      f"{totals['fat']}g",     COLOR_FAT),
        ]
        for i, (lbl, val, color) in enumerate(macros):
            cell = tk.Frame(macro_row, bg=color, padx=6, pady=8)
            cell.grid(row=0, column=i, padx=4, sticky="nsew")
            macro_row.columnconfigure(i, weight=1)
            tk.Label(cell, text=val, font=("Helvetica", 18, "bold"),
                     bg=color, fg="white").pack()
            tk.Label(cell, text=lbl, font=("Helvetica", 9),
                     bg=color, fg="white").pack()

        # Order list
        card = self._make_card(self.content, title="Your order")

        if not order_lines:
            tk.Label(card, text="No items selected.",
                     font=("Helvetica", 11),
                     bg=CARD_BG, fg=TEXT_SEC, pady=12).pack()
        else:
            for label, cat_tag, item in order_lines:
                row = tk.Frame(card, bg=CARD_BG, padx=14, pady=7)
                row.pack(fill="x")
                tk.Label(row, text=label, font=("Helvetica", 11),
                         bg=CARD_BG, fg=TEXT_PRI, anchor="w").pack(side="left")
                tk.Label(row, text=f"{item['calories']} cal",
                         font=("Helvetica", 10),
                         bg=CARD_BG, fg=TEXT_SEC).pack(side="right")
                tk.Label(row, text=cat_tag, font=("Helvetica", 9),
                         bg=BG, fg=TEXT_SEC,
                         padx=6, pady=1).pack(side="right", padx=6)
                tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

    # ── Navigation ────────────────────────────────────────────────────────────

    def _save_step(self):
        """Write the current step's UI state back into self.selections."""
        steps = active_steps(self.selections)
        _, kind, _ = steps[self.current_step]

        if kind == "single":
            val = self._single_var.get()
            self.selections[self._single_step] = (
                None if val == "__none__" else val)
        elif kind == "toggle":
            self.selections["double_protein"] = self._double_var.get()
        elif kind == "qesa_veggies":
            self.selections["qesa_veggies"] = self._qesa_veg_var.get()
        # "multi" is saved live on each checkbox click

    def _go_next(self):
        self._save_step()
        steps = active_steps(self.selections)
        if steps[self.current_step][0] == "base" and not self.selections["base"]:
            self._popup("Please choose a base before continuing.")
            return
        if self.current_step < len(steps) - 1:
            self.current_step += 1
            self._show_step()

    def _go_back(self):
        self._save_step()
        if self.current_step > 0:
            self.current_step -= 1
            self._show_step()

    def _update_nav(self):
        steps = active_steps(self.selections)
        last  = len(steps) - 1
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
        self.selections   = fresh_selections()
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
        x = (self.root.winfo_x()
             + (self.root.winfo_width()  - pop.winfo_width())  // 2)
        y = (self.root.winfo_y()
             + (self.root.winfo_height() - pop.winfo_height()) // 2)
        pop.geometry(f"+{x}+{y}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    ChipotleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()