from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import List, Sequence

from solvers import Q1Result, Q2Result, Q3Result, solve_q1, solve_q2, solve_q3

DEFAULT_Q1_NECESSIDADES = [4800, 5800, 5700]
DEFAULT_Q1_COMPOSICAO = [
    [55, 30, 15],
    [25, 45, 30],
    [25, 20, 55],
]
DEFAULT_Q2_X = "0.25, 0.75, 1.25, 1.5, 2.0"
DEFAULT_Q2_Y = "-0.45, -0.60, 0.70, 1.88, 6.0"
DEFAULT_Q2_GRAU = "4"
DEFAULT_Q2_X_ALVO = "1.1"
DEFAULT_Q3_DIST = "0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20"
DEFAULT_Q3_PROF = "0, 1.8, 2.0, 4.0, 4.0, 6.0, 4.0, 3.6, 3.4, 2.8, 0"
DEFAULT_Q3_ESPACAMENTO = "2.0"

BG_COLOR = "#f7f9fc"
CARD_COLOR = "#ffffff"
PRIMARY_COLOR = "#2563eb"
ACCENT_COLOR = "#0ea5e9"
TEXT_COLOR = "#0f172a"
MONO_BG = "#0f172a"
MONO_FG = "#f8fafc"


class UnifiedApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self._configure_styles(master)
        self.pack(fill="both", expand=True)

        header = ttk.Frame(self, style="Header.TFrame", padding=(20, 18))
        header.pack(fill="x")
        ttk.Label(
            header,
            text="Laboratório de Métodos Numéricos",
            style="Header.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="Resolva as três questões em um único painel organizado",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(self, style="Card.TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_q1_tab(notebook)
        self._build_q2_tab(notebook)
        self._build_q3_tab(notebook)

    # ---------- Questão 1 ----------
    def _build_q1_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=10, style="Content.TFrame")
        notebook.add(frame, text="Questão 1 - Mineração")

        needs_frame = ttk.LabelFrame(frame, text="Necessidades (m³)", style="Card.TLabelframe", padding=10)
        needs_frame.pack(fill="x", pady=5)
        materiais = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
        self.q1_need_entries: List[ttk.Entry] = []
        for idx, (label, default) in enumerate(zip(materiais, DEFAULT_Q1_NECESSIDADES)):
            ttk.Label(needs_frame, text=label).grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            entry = ttk.Entry(needs_frame, width=15)
            entry.insert(0, str(default))
            entry.grid(row=idx, column=1, padx=5, pady=2)
            self.q1_need_entries.append(entry)

        comp_frame = ttk.LabelFrame(frame, text="Composição das Minas (%)", style="Card.TLabelframe", padding=10)
        comp_frame.pack(fill="x", pady=5)
        headers = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
        for col, header in enumerate([""] + headers):
            label_font = ("Segoe UI", 9, "bold") if header else ("Segoe UI", 9)
            ttk.Label(comp_frame, text=header or "Mina", font=label_font).grid(row=0, column=col, padx=5, pady=2)
        self.q1_comp_entries: List[List[ttk.Entry]] = []
        for row_idx in range(3):
            ttk.Label(comp_frame, text=f"Mina {row_idx + 1}").grid(row=row_idx + 1, column=0, padx=5, pady=2)
            row_entries: List[ttk.Entry] = []
            for col_idx in range(3):
                entry = ttk.Entry(comp_frame, width=10)
                entry.insert(0, str(DEFAULT_Q1_COMPOSICAO[row_idx][col_idx]))
                entry.grid(row=row_idx + 1, column=col_idx + 1, padx=5, pady=2)
                row_entries.append(entry)
            self.q1_comp_entries.append(row_entries)

        ttk.Button(frame, text="Calcular minerações", style="Accent.TButton", command=self._run_q1).pack(pady=8)
        self.q1_output = self._build_output_box(frame)

    def _run_q1(self) -> None:
        try:
            necessidades = [float(entry.get()) for entry in self.q1_need_entries]
            composicao = [[float(cell.get()) for cell in row] for row in self.q1_comp_entries]
            result = solve_q1(necessidades, composicao)
            texto = self._format_q1_result(result)
            self._write_output(self.q1_output, texto)
        except Exception as exc:
            messagebox.showerror("Erro na Questão 1", str(exc))

    # ---------- Questão 2 ----------
    def _build_q2_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=10, style="Content.TFrame")
        notebook.add(frame, text="Questão 2 - Interpolação")

        points_frame = ttk.LabelFrame(frame, text="Pontos (separe por vírgula, espaço ou nova linha)", style="Card.TLabelframe", padding=10)
        points_frame.pack(fill="x", pady=5)

        ttk.Label(points_frame, text="x:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.q2_x_entry = ttk.Entry(points_frame)
        self.q2_x_entry.insert(0, DEFAULT_Q2_X)
        self.q2_x_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(points_frame, text="y:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.q2_y_entry = ttk.Entry(points_frame)
        self.q2_y_entry.insert(0, DEFAULT_Q2_Y)
        self.q2_y_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        points_frame.columnconfigure(1, weight=1)

        params_frame = ttk.Frame(frame, style="Content.TFrame")
        params_frame.pack(fill="x", pady=5)
        ttk.Label(params_frame, text="x alvo:").grid(row=0, column=0, padx=5, pady=2)
        self.q2_x_alvo_entry = ttk.Entry(params_frame, width=10)
        self.q2_x_alvo_entry.insert(0, DEFAULT_Q2_X_ALVO)
        self.q2_x_alvo_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(params_frame, text="Grau do polinômio:").grid(row=0, column=2, padx=5, pady=2)
        self.q2_grau_entry = ttk.Entry(params_frame, width=10)
        self.q2_grau_entry.insert(0, DEFAULT_Q2_GRAU)
        self.q2_grau_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(frame, text="Interpolar", style="Accent.TButton", command=self._run_q2).pack(pady=8)
        self.q2_output = self._build_output_box(frame)

    def _run_q2(self) -> None:
        try:
            x_pontos = self._parse_float_sequence(self.q2_x_entry.get())
            y_pontos = self._parse_float_sequence(self.q2_y_entry.get())
            x_alvo = float(self.q2_x_alvo_entry.get())
            grau = int(float(self.q2_grau_entry.get()))
            result = solve_q2(x_pontos, y_pontos, x_alvo, grau)
            texto = self._format_q2_result(result, grau, x_alvo)
            self._write_output(self.q2_output, texto)
        except Exception as exc:
            messagebox.showerror("Erro na Questão 2", str(exc))

    # ---------- Questão 3 ----------
    def _build_q3_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=10, style="Content.TFrame")
        notebook.add(frame, text="Questão 3 - Área (Trapézio/Simpson)")

        inputs_frame = ttk.LabelFrame(frame, text="Dados de entrada", style="Card.TLabelframe", padding=10)
        inputs_frame.pack(fill="x", pady=5)

        ttk.Label(inputs_frame, text="Distâncias acumuladas (m):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.q3_dist_entry = ttk.Entry(inputs_frame)
        self.q3_dist_entry.insert(0, DEFAULT_Q3_DIST)
        self.q3_dist_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(inputs_frame, text="Profundidades (m):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.q3_prof_entry = ttk.Entry(inputs_frame)
        self.q3_prof_entry.insert(0, DEFAULT_Q3_PROF)
        self.q3_prof_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(inputs_frame, text="Espaçamento (m) [opcional se distâncias informadas]:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.q3_esp_entry = ttk.Entry(inputs_frame, width=10)
        self.q3_esp_entry.insert(0, DEFAULT_Q3_ESPACAMENTO)
        self.q3_esp_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        inputs_frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Calcular áreas", style="Accent.TButton", command=self._run_q3).pack(pady=8)
        self.q3_output = self._build_output_box(frame)

    def _run_q3(self) -> None:
        try:
            profundidades = self._parse_float_sequence(self.q3_prof_entry.get())
            distancias_text = self.q3_dist_entry.get().strip()
            distancias = self._parse_float_sequence(distancias_text) if distancias_text else None
            espacamento_text = self.q3_esp_entry.get().strip()
            espacamento = float(espacamento_text) if espacamento_text else None
            result = solve_q3(profundidades, espacamento=espacamento, distancias=distancias)
            texto = self._format_q3_result(result)
            self._write_output(self.q3_output, texto)
        except Exception as exc:
            messagebox.showerror("Erro na Questão 3", str(exc))

    # ---------- Utilitários ----------
    def _build_output_box(self, parent: ttk.Frame) -> ScrolledText:
        output = ScrolledText(
            parent,
            height=18,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            background=MONO_BG,
            foreground=MONO_FG,
            borderwidth=0,
            padx=10,
            pady=10,
        )
        output.pack(fill="both", expand=True, pady=5)
        return output

    def _write_output(self, widget: ScrolledText, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.configure(state="disabled")

    def _parse_float_sequence(self, text: str) -> List[float]:
        text = text.strip()
        if not text:
            return []
        tokens = re.split(r"[\s,;]+", text)
        values: List[float] = []
        for token in tokens:
            if token:
                values.append(float(token))
        return values

    def _format_q1_result(self, result: Q1Result) -> str:
        linhas = ["=== RESULTADOS - QUESTÃO 1 ===", "Quantidades a minerar por mina (m³):"]
        for idx, valor in enumerate(result.quantidades_minas, start=1):
            linhas.append(f"  Mina {idx}: {valor:10.4f}")
        linhas.append("\nVerificação das necessidades:")
        materiais = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
        for nome, obtido, necessario, erro in zip(materiais, result.obtido, result.necessidades, result.erros):
            linhas.append(
                f"  {nome:<15} -> obtido: {obtido:10.4f} | necessário: {necessario:10.4f} | erro: {erro: .6f}"
            )
        return "\n".join(linhas)

    def _format_q2_result(self, result: Q2Result, grau: int, x_alvo: float) -> str:
        linhas = ["=== RESULTADOS - QUESTÃO 2 ===", f"Pontos selecionados para grau {grau}:"]
        for idx, (x_val, y_val) in enumerate(result.pontos_selecionados):
            linhas.append(f"  P{idx}: ({x_val:.6f}, {y_val:.6f})")
        linhas.extend(
            [
                "",
                f"Valor interpolado por Lagrange em x = {x_alvo}: {result.valor_lagrange:.10f}",
                f"Valor interpolado por Newton   em x = {x_alvo}: {result.valor_newton:.10f}",
                f"Diferença absoluta: {result.diferenca:.12f}",
            ]
        )
        return "\n".join(linhas)

    def _format_q3_result(self, result: Q3Result) -> str:
        linhas = [
            "=== RESULTADOS - QUESTÃO 3 ===",
            f"Espaçamento adotado: {result.espacamento:.4f} m",
            f"Número de pontos: {len(result.profundidades)}",
            "",
            "Distância (m) | Profundidade (m)",
            "--------------+-----------------",
        ]
        for dist, prof in zip(result.distancias, result.profundidades):
            linhas.append(f"{dist:12.4f} | {prof:13.4f}")
        linhas.extend(
            [
                "",
                f"Área - Trapézio : {result.area_trapezio:.4f} m²",
                f"Área - Simpson  : {result.area_simpson:.4f} m²",
                f"Diferença       : {result.diferenca:.4f} m² ({result.diferenca_percentual:.2f}%)",
            ]
        )
        return "\n".join(linhas)

    def _configure_styles(self, master: tk.Misc) -> None:
        master.configure(bg=BG_COLOR)
        style = ttk.Style(master)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Header.TFrame", background=BG_COLOR)
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 18), foreground=TEXT_COLOR, background=BG_COLOR)
        style.configure("Subheader.TLabel", font=("Segoe UI", 11), foreground="#475569", background=BG_COLOR)

        style.configure("Content.TFrame", background=BG_COLOR)
        style.configure(
            "Card.TLabelframe",
            background=CARD_COLOR,
            foreground=TEXT_COLOR,
            borderwidth=1,
            relief="ridge",
        )
        style.configure("Card.TLabelframe.Label", background=CARD_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10, "bold"))

        style.configure(
            "Accent.TButton",
            background=PRIMARY_COLOR,
            foreground="#ffffff",
            padding=(16, 8),
            borderwidth=0,
            focusthickness=3,
            focuscolor=PRIMARY_COLOR,
        )
        style.map(
            "Accent.TButton",
            background=[("active", ACCENT_COLOR)],
            foreground=[("disabled", "#94a3b8")],
        )

        style.configure("Card.TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("Card.TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map(
            "Card.TNotebook.Tab",
            background=[("selected", CARD_COLOR), ("!selected", BG_COLOR)],
            foreground=[("selected", TEXT_COLOR), ("!selected", "#475569")],
        )


def main() -> None:
    root = tk.Tk()
    root.title("Questões Numéricas - Interface Gráfica")
    root.geometry("960x720")
    UnifiedApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
