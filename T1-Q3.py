import numpy as np
from typing import List, Tuple

def imprimir_matriz(matriz: np.ndarray, nome: str = "Matriz"):
    print(f"\n{nome}:")
    print("-" * 80)
    linhas, colunas = matriz.shape
    for i in range(linhas):
        linha_str = "| "
        for j in range(colunas):
            valor = matriz[i, j]
            if abs(valor) < 1e-10:
                valor = 0.0
            linha_str += f"{valor:10.4f} "
        linha_str += "|"
        print(linha_str)
    print("-" * 80)

def eliminacao_gaussiana(A: np.ndarray, b: np.ndarray, mostrar_passos: bool = True) -> np.ndarray:
    """
    Resolve um sistema linear Ax = b usando eliminação gaussiana com pivoteamento parcial.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vetor de termos independentes (n x 1)
        mostrar_passos: Se True, mostra os passos intermediários
    
    Returns:
        Vetor solução x
    """
    n = len(b)
    Ab = np.column_stack([A.astype(float), b.astype(float)])
    
    if mostrar_passos:
        print("\n" + "="*80)
        print("MÉTODO DE ELIMINAÇÃO GAUSSIANA")
        print("="*80)
        imprimir_matriz(Ab, "Matriz Aumentada Inicial [A|b]")
    
    for k in range(n-1):
        max_idx = k
        for i in range(k+1, n):
            if abs(Ab[i, k]) > abs(Ab[max_idx, k]):
                max_idx = i
        
        if max_idx != k:
            Ab[[k, max_idx]] = Ab[[max_idx, k]]
            if mostrar_passos:
                print(f"\nTroca de linhas {k+1} ↔ {max_idx+1} (pivoteamento)")
                imprimir_matriz(Ab, f"Após pivoteamento na etapa {k+1}")
        
        for i in range(k+1, n):
            if Ab[k, k] != 0:
                fator = Ab[i, k] / Ab[k, k]
                Ab[i, k:] = Ab[i, k:] - fator * Ab[k, k:]
                
                if mostrar_passos:
                    print(f"\nEliminando elemento ({i+1},{k+1}): L{i+1} = L{i+1} - ({fator:.4f}) * L{k+1}")
        
        if mostrar_passos and k < n-2:
            imprimir_matriz(Ab, f"Matriz após eliminação na coluna {k+1}")
    
    if mostrar_passos:
        imprimir_matriz(Ab, "Matriz Triangular Superior Final")
    
    x = np.zeros(n)
    
    if mostrar_passos:
        print("\n" + "="*80)
        print("SUBSTITUIÇÃO RETROATIVA")
        print("="*80)
    
    for i in range(n-1, -1, -1):
        soma = 0
        for j in range(i+1, n):
            soma += Ab[i, j] * x[j]
        
        if Ab[i, i] == 0:
            raise ValueError(f"Sistema impossível ou indeterminado: pivô zero na linha {i+1}")
        
        x[i] = (Ab[i, n] - soma) / Ab[i, i]
        
        if mostrar_passos:
            print(f"\nx[{i+1}] = ({Ab[i, n]:.4f} - {soma:.4f}) / {Ab[i, i]:.4f} = {x[i]:.4f}")
    
    return x

def criar_sistema_mineracao(necessidades: List[float], composicao: List[List[float]]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Cria o sistema de equações lineares para o problema de mineração.
    
    Args:
        necessidades: [areia, cascalho_fino, cascalho_grosso] em m³
        composicao: [[%areia_mina1, %cfino_mina1, %cgrosso_mina1], ...]
    
    Returns:
        Tupla (A, b) onde A é a matriz de coeficientes e b o vetor de necessidades
    """
    A = np.array(composicao) / 100.0
    A = A.T
    b = np.array(necessidades)
    
    return A, b

def verificar_solucao(A: np.ndarray, b: np.ndarray, x: np.ndarray) -> None:
    """Verifica se a solução encontrada está correta."""
    resultado = A @ x
    print("\n" + "="*80)
    print("VERIFICAÇÃO DA SOLUÇÃO")
    print("="*80)
    print("\nQuantidades obtidas vs. necessárias:")
    materiais = ["Areia", "Cascalho Fino", "Cascalho Grosso"]
    
    for i, material in enumerate(materiais):
        print(f"{material:20s}: {resultado[i]:10.4f} m³ (necessário: {b[i]:10.4f} m³)")
        erro = abs(resultado[i] - b[i])
        print(f"{'':20s}  Erro: {erro:.6f} m³")

def main():
    print("="*80)
    print("SISTEMA DE RESOLUÇÃO DE PROBLEMAS DE MINERAÇÃO")
    print("Método: Eliminação Gaussiana")
    print("="*80)
    
    print("\n--- PROBLEMA ORIGINAL ---")
    necessidades_original = [4800, 5800, 5700]
    composicao_original = [
        [55, 30, 15],
        [25, 45, 30],
        [25, 20, 55]
    ]
    
    print("\nNecessidades do engenheiro:")
    print(f"  Areia:           {necessidades_original[0]:8.2f} m³")
    print(f"  Cascalho Fino:   {necessidades_original[1]:8.2f} m³")
    print(f"  Cascalho Grosso: {necessidades_original[2]:8.2f} m³")
    
    print("\nComposição das minas:")
    print("       Areia  C.Fino  C.Grosso")
    for i, comp in enumerate(composicao_original):
        print(f"Mina {i+1}:  {comp[0]:3d}%    {comp[1]:3d}%      {comp[2]:3d}%")
    
    A, b = criar_sistema_mineracao(necessidades_original, composicao_original)
    
    print("\n\nSISTEMA DE EQUAÇÕES LINEARES:")
    print("-" * 80)
    print("Seja x1, x2, x3 as quantidades a minerar de cada mina (em m³):")
    print()
    for i, material in enumerate(["Areia", "Cascalho Fino", "Cascalho Grosso"]):
        eq = f"{A[i,0]:.2f}·x1 + {A[i,1]:.2f}·x2 + {A[i,2]:.2f}·x3 = {b[i]:.2f}"
        print(f"{material:15s}: {eq}")
    
    try:
        solucao = eliminacao_gaussiana(A, b, mostrar_passos=True)
        
        print("\n" + "="*80)
        print("SOLUÇÃO FINAL")
        print("="*80)
        print("\nQuantidades a minerar de cada mina:")
        for i, quantidade in enumerate(solucao):
            print(f"  Mina {i+1}: {quantidade:10.4f} m³")
        
        verificar_solucao(A, b, solucao)
        
    except Exception as e:
        print(f"\nErro ao resolver o sistema: {e}")
    
    print("\n" + "="*80)
    print("RESOLVER NOVO PROBLEMA")
    print("="*80)
    
    resposta = input("\nDeseja resolver um novo problema? (s/n): ").strip().lower()
    
    if resposta == 's':
        print("\n--- ENTRADA DE NOVOS DADOS ---")
        
        print("\nDigite as necessidades (em m³):")
        areia = float(input("  Areia: "))
        cfino = float(input("  Cascalho Fino: "))
        cgrosso = float(input("  Cascalho Grosso: "))
        necessidades_nova = [areia, cfino, cgrosso]
        
        print("\nDigite a composição de cada mina (em %):")
        composicao_nova = []
        for i in range(3):
            print(f"\nMina {i+1}:")
            areia_p = float(input("  % Areia: "))
            cfino_p = float(input("  % Cascalho Fino: "))
            cgrosso_p = float(input("  % Cascalho Grosso: "))
            composicao_nova.append([areia_p, cfino_p, cgrosso_p])
        
        A_nova, b_nova = criar_sistema_mineracao(necessidades_nova, composicao_nova)
        
        print("\n\nNOVO SISTEMA DE EQUAÇÕES:")
        print("-" * 80)
        for i, material in enumerate(["Areia", "Cascalho Fino", "Cascalho Grosso"]):
            eq = f"{A_nova[i,0]:.2f}·x1 + {A_nova[i,1]:.2f}·x2 + {A_nova[i,2]:.2f}·x3 = {b_nova[i]:.2f}"
            print(f"{material:15s}: {eq}")
        
        try:
            solucao_nova = eliminacao_gaussiana(A_nova, b_nova, mostrar_passos=True)
            
            print("\n" + "="*80)
            print("SOLUÇÃO FINAL - NOVO PROBLEMA")
            print("="*80)
            print("\nQuantidades a minerar de cada mina:")
            for i, quantidade in enumerate(solucao_nova):
                print(f"  Mina {i+1}: {quantidade:10.4f} m³")
            
            verificar_solucao(A_nova, b_nova, solucao_nova)
            
        except Exception as e:
            print(f"\nErro ao resolver o sistema: {e}")

if __name__ == "__main__":
    main()