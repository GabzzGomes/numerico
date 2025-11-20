from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import List, Sequence

from solvers import (
    CircuitResult,
    Q1Result,
    Q2Result,
    Q3Result,
    solve_circuit,
    solve_q1,
    solve_q2,
    solve_q3,
)

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
DEFAULT_CIRCUIT_MATRIX = [
    [11.5, -2.5, 0, -4, 0, 12],
    [-2.5, 7, 0, 0, -3, -16],
    [0, 0, 8, 0, 0, 14],
    [-4, 0, 0, 9, -3, -12],
    [0, -3, 0, -3, 6, 30],
]

BG_COLOR = "#2E3440"
CARD_COLOR = "#3B4252"
PRIMARY_COLOR = "#88C0D0"
ACCENT_COLOR = "#81A1C1"
TEXT_COLOR = "#ECEFF4"
MONO_BG = "#242933"
MONO_FG = "#E5E9F0"
INPUT_BG = "#434C5E"


class UnifiedApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self._configure_styles(master)
        self.pack(fill="both", expand=True)

        header = ttk.Frame(self, style="Header.TFrame", padding=(20, 18))
        header.pack(fill="x")
        ttk.Label(
            header,
            text="Métodos Numéricos",
            style="Header.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="Cálculo numérico - 4 Questões em um único painel",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(self, style="Card.TNotebook")
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._build_q1_tab(notebook)
        self._build_circuit_tab(notebook)
        self._build_q2_tab(notebook)
        self._build_q3_tab(notebook)

    def _build_q1_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=15, style="Content.TFrame")
        notebook.add(frame, text="Questão T1 - Mineração")

        needs_frame = ttk.LabelFrame(frame, text="Necessidades (m³)", style="Card.TLabelframe", padding=15)
        needs_frame.pack(fill="x", pady=5)
        materiais = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
        self.q1_need_entries: List[ttk.Entry] = []
        for idx, (label, default) in enumerate(zip(materiais, DEFAULT_Q1_NECESSIDADES)):
            ttk.Label(needs_frame, text=label).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(needs_frame, width=15)
            entry.insert(0, str(default))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.q1_need_entries.append(entry)

        comp_frame = ttk.LabelFrame(frame, text="Composição das Minas (%)", style="Card.TLabelframe", padding=15)
        comp_frame.pack(fill="x", pady=5)
        headers = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
        for col, header in enumerate([""] + headers):
            label_font = ("Segoe UI", 10, "bold") if header else ("Segoe UI", 10)
            ttk.Label(comp_frame, text=header or "Mina", font=label_font).grid(row=0, column=col, padx=10, pady=5)
        self.q1_comp_entries: List[List[ttk.Entry]] = []
        for row_idx in range(3):
            ttk.Label(comp_frame, text=f"Mina {row_idx + 1}").grid(row=row_idx + 1, column=0, padx=10, pady=5)
            row_entries: List[ttk.Entry] = []
            for col_idx in range(3):
                entry = ttk.Entry(comp_frame, width=10)
                entry.insert(0, str(DEFAULT_Q1_COMPOSICAO[row_idx][col_idx]))
                entry.grid(row=row_idx + 1, column=col_idx + 1, padx=10, pady=5)
                row_entries.append(entry)
            self.q1_comp_entries.append(row_entries)

        ttk.Button(frame, text="Calcular minerações", style="Accent.TButton", command=self._run_q1).pack(pady=10)
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

    def _build_circuit_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=20, style="Content.TFrame")
        notebook.add(frame, text="Questão T2 - Circuitos")

        input_frame = ttk.LabelFrame(frame, text="Matriz Estendida [A|b]", style="Card.TLabelframe", padding=20)
        input_frame.pack(fill="both", expand=True, pady=10)

        ttk.Label(input_frame, text="Insira os coeficientes e termos independentes (separados por espaço/tab):").pack(
            anchor="w", pady=(0, 10)
        )

        self.circuit_input = ScrolledText(
            input_frame,
            height=8,
            font=("Consolas", 11),
            background=INPUT_BG,
            foreground=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            borderwidth=0,
            padx=15,
            pady=15
        )
        self.circuit_input.pack(fill="both", expand=True, pady=5)

        default_text = "\n".join([" ".join(map(str, row)) for row in DEFAULT_CIRCUIT_MATRIX])
        self.circuit_input.insert("1.0", default_text)

        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill="x", pady=15)

        ttk.Label(controls_frame, text="Precisão:").pack(side="left", padx=(0, 10))
        self.circuit_precision = ttk.Entry(controls_frame, width=15)
        self.circuit_precision.insert(0, "0.0001")
        self.circuit_precision.pack(side="left")

        ttk.Button(controls_frame, text="Resolver Circuito", style="Accent.TButton", command=self._run_circuit).pack(
            side="right"
        )

        self.circuit_output = self._build_output_box(frame)

    def _run_circuit(self) -> None:
        try:
            text = self.circuit_input.get("1.0", tk.END).strip()
            if not text:
                raise ValueError("Matriz vazia.")

            matrix = []
            for line in text.splitlines():
                if line.strip():
                    matrix.append([float(x) for x in line.replace(",", " ").split()])

            precision = float(self.circuit_precision.get())
            result = solve_circuit(matrix, precision)
            texto = self._format_circuit_result(result)
            self._write_output(self.circuit_output, texto)
        except Exception as exc:
            messagebox.showerror("Erro na Questão T2", str(exc))

    def _format_circuit_result(self, result: CircuitResult) -> str:
        linhas = ["=== RESULTADOS - QUESTÃO T2 (CIRCUITOS) ===", "Correntes calculadas:"]
        for i, val in enumerate(result.correntes):
            linhas.append(f"  i{i+1} = {val:.6f} A")

        linhas.append("\nVerificação (A*x):")
        ax = result.matriz @ result.correntes
        for i, (calc, expected) in enumerate(zip(ax, result.termos_independentes)):
            erro = abs(calc - expected)
            linhas.append(f"  Eq {i+1}: {calc:10.4f} (esperado: {expected:10.4f}) | erro: {erro:.6e}")

        return "\n".join(linhas)

    def _build_q2_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=20, style="Content.TFrame")
        notebook.add(frame, text="Questão T3 - Interpolação")

        points_frame = ttk.LabelFrame(frame, text="Pontos (separe por vírgula, espaço ou nova linha)", style="Card.TLabelframe", padding=20)
        points_frame.pack(fill="x", pady=10)

        ttk.Label(points_frame, text="x:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.q2_x_entry = ttk.Entry(points_frame)
        self.q2_x_entry.insert(0, DEFAULT_Q2_X)
        self.q2_x_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(points_frame, text="y:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.q2_y_entry = ttk.Entry(points_frame)
        self.q2_y_entry.insert(0, DEFAULT_Q2_Y)
        self.q2_y_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        points_frame.columnconfigure(1, weight=1)

        params_frame = ttk.Frame(frame, style="Content.TFrame")
        params_frame.pack(fill="x", pady=15)
        ttk.Label(params_frame, text="x alvo:").grid(row=0, column=0, padx=10, pady=5)
        self.q2_x_alvo_entry = ttk.Entry(params_frame, width=15)
        self.q2_x_alvo_entry.insert(0, DEFAULT_Q2_X_ALVO)
        self.q2_x_alvo_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(params_frame, text="Grau do polinômio:").grid(row=0, column=2, padx=10, pady=5)
        self.q2_grau_entry = ttk.Entry(params_frame, width=15)
        self.q2_grau_entry.insert(0, DEFAULT_Q2_GRAU)
        self.q2_grau_entry.grid(row=0, column=3, padx=10, pady=5)

        ttk.Button(frame, text="Interpolar", style="Accent.TButton", command=self._run_q2).pack(pady=15)
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

    def _build_q3_tab(self, notebook: ttk.Notebook) -> None:
        frame = ttk.Frame(notebook, padding=20, style="Content.TFrame")
        notebook.add(frame, text="Questão T4 - Área (Trapézio/Simpson)")

        inputs_frame = ttk.LabelFrame(frame, text="Dados de entrada", style="Card.TLabelframe", padding=20)
        inputs_frame.pack(fill="x", pady=10)

        ttk.Label(inputs_frame, text="Distâncias acumuladas (m):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.q3_dist_entry = ttk.Entry(inputs_frame)
        self.q3_dist_entry.insert(0, DEFAULT_Q3_DIST)
        self.q3_dist_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(inputs_frame, text="Profundidades (m):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.q3_prof_entry = ttk.Entry(inputs_frame)
        self.q3_prof_entry.insert(0, DEFAULT_Q3_PROF)
        self.q3_prof_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(inputs_frame, text="Espaçamento (m) [opcional se distâncias informadas]:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.q3_esp_entry = ttk.Entry(inputs_frame, width=15)
        self.q3_esp_entry.insert(0, DEFAULT_Q3_ESPACAMENTO)
        self.q3_esp_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        inputs_frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Calcular áreas", style="Accent.TButton", command=self._run_q3).pack(pady=15)
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

    def _build_output_box(self, parent: ttk.Frame) -> ScrolledText:
        output = ScrolledText(
            parent,
            height=18,
            wrap="word",
            state="disabled",
            font=("Consolas", 11),
            background=MONO_BG,
            foreground=MONO_FG,
            borderwidth=0,
            padx=15,
            pady=15,
        )
        output.pack(fill="both", expand=True, pady=10)
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

        style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)

        style.configure("Header.TFrame", background=BG_COLOR)
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground=PRIMARY_COLOR, background=BG_COLOR)
        style.configure("Subheader.TLabel", font=("Segoe UI", 12), foreground=ACCENT_COLOR, background=BG_COLOR)

        style.configure("Content.TFrame", background=BG_COLOR)
        
        style.configure(
            "Card.TLabelframe",
            background=CARD_COLOR,
            foreground=PRIMARY_COLOR,
            borderwidth=0,
            relief="flat",
        )
        style.configure("Card.TLabelframe.Label", background=CARD_COLOR, foreground=PRIMARY_COLOR, font=("Segoe UI", 11, "bold"))

        style.configure(
            "Accent.TButton",
            background=PRIMARY_COLOR,
            foreground="#2E3440",
            padding=(20, 10),
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", ACCENT_COLOR), ("pressed", ACCENT_COLOR)],
            foreground=[("disabled", "#4c566a")],
        )

        style.configure("Card.TNotebook", background=BG_COLOR, borderwidth=0)
        style.configure("Card.TNotebook.Tab", padding=(20, 12), font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map(
            "Card.TNotebook.Tab",
            background=[("selected", CARD_COLOR), ("!selected", BG_COLOR)],
            foreground=[("selected", PRIMARY_COLOR), ("!selected", "#4c566a")],
            focuscolor=[("selected", BG_COLOR), ("!selected", BG_COLOR)],
        )

        style.configure("TEntry", fieldbackground=INPUT_BG, foreground=TEXT_COLOR, insertcolor=TEXT_COLOR, borderwidth=0, padding=5)
        style.map("TEntry", bordercolor=[("focus", PRIMARY_COLOR)], lightcolor=[("focus", PRIMARY_COLOR)], darkcolor=[("focus", PRIMARY_COLOR)])


def main() -> None:
    root = tk.Tk()
    root.title("Questões Numéricas - Interface Gráfica")
    root.geometry("960x720")
    UnifiedApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
