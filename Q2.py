import numpy as np

def interpolacao_lagrange(x_pontos, y_pontos, x_alvo, mostrar_passos: bool = True):
    """Calcula a interpolação usando o método de Lagrange."""
    n = len(x_pontos)
    resultado = 0.0
    
    if mostrar_passos:
        print("\n=== MÉTODO DE LAGRANGE ===")
        print(f"\nCalculando para x = {x_alvo}")
    
    for i in range(n):
        termo = y_pontos[i]
        L_i = 1.0
        
        if mostrar_passos:
            print(f"\nTermo {i+1}: y_{i} = {y_pontos[i]}")
            print(f"L_{i}({x_alvo}) = ", end="")
        
        numeradores = []
        denominadores = []
        
        for j in range(n):
            if i != j:
                numeradores.append(f"({x_alvo} - {x_pontos[j]})")
                denominadores.append(f"({x_pontos[i]} - {x_pontos[j]})")
                L_i *= (x_alvo - x_pontos[j]) / (x_pontos[i] - x_pontos[j])
        
        if mostrar_passos:
            print(" × ".join(numeradores) + " / " + " × ".join(denominadores))
            print(f"L_{i}({x_alvo}) = {L_i:.10f}")
            print(f"Contribuição: {y_pontos[i]} × {L_i:.10f} = {termo * L_i:.10f}")
        
        resultado += termo * L_i
    
    return resultado

def diferencas_divididas(x_pontos, y_pontos, mostrar_passos: bool = True):
    """Calcula a tabela de diferenças divididas para Newton."""
    n = len(x_pontos)
    tabela = np.zeros((n, n))
    tabela[:, 0] = y_pontos
    
    if mostrar_passos:
        print("\n=== TABELA DE DIFERENÇAS DIVIDIDAS ===")
        print(f"{'i':<5} {'x_i':<10} {'f[x_i]':<15}", end="")
        for ordem in range(1, n):
            print(f"f[x_i,...,x_i+{ordem}]".ljust(20), end="")
        print()
    
    for j in range(1, n):
        for i in range(n - j):
            tabela[i, j] = (tabela[i+1, j-1] - tabela[i, j-1]) / (x_pontos[i+j] - x_pontos[i])
    
    if mostrar_passos:
        for i in range(n):
            print(f"{i:<5} {x_pontos[i]:<10.2f} {tabela[i, 0]:<15.10f}", end="")
            for j in range(1, n - i):
                print(f"{tabela[i, j]:<20.10f}", end="")
            print()
    
    return tabela

def interpolacao_newton(x_pontos, y_pontos, x_alvo, mostrar_passos: bool = True):
    """Calcula a interpolação usando o método de Newton."""
    n = len(x_pontos)
    tabela = diferencas_divididas(x_pontos, y_pontos, mostrar_passos=mostrar_passos)
    
    if mostrar_passos:
        print(f"\n=== MÉTODO DE NEWTON ===")
        print(f"\nCalculando para x = {x_alvo}")
        print(f"\nP(x) = f[x_0]", end="")
        for i in range(1, n):
            print(f" + f[x_0,...,x_{i}]", end="")
            for j in range(i):
                print(f"(x - {x_pontos[j]})", end="")
        print()
    
    resultado = tabela[0, 0]
    if mostrar_passos:
        print(f"\nP({x_alvo}) = {tabela[0, 0]:.10f}", end="")
    
    produto_acumulado = 1.0
    for i in range(1, n):
        produto_acumulado *= (x_alvo - x_pontos[i-1])
        termo = tabela[0, i] * produto_acumulado
        if mostrar_passos:
            print(f" + ({tabela[0, i]:.10f})", end="")
            for j in range(i):
                print(f" × ({x_alvo} - {x_pontos[j]})", end="")
            print(f" = ... + {termo:.10f}", end="")
        resultado += termo
    
    if mostrar_passos:
        print()
    return resultado

def escolher_pontos_centralizados(x_pontos, y_pontos, x_alvo, grau):
    """
    Escolhe os pontos mais próximos de x_alvo para interpolação.
    """
    n_pontos = grau + 1
    
    if len(x_pontos) <= n_pontos:
        return x_pontos, y_pontos
    
    # Calcula distâncias
    distancias = [abs(x - x_alvo) for x in x_pontos]
    
    # Ordena índices por distância
    indices_ordenados = sorted(range(len(x_pontos)), key=lambda i: distancias[i])
    
    # Pega os n_pontos mais próximos e ordena por x
    indices_selecionados = sorted(indices_ordenados[:n_pontos])
    
    x_selecionados = [x_pontos[i] for i in indices_selecionados]
    y_selecionados = [y_pontos[i] for i in indices_selecionados]
    
    return x_selecionados, y_selecionados

def main():
    print("=" * 80)
    print("INTERPOLAÇÃO POLINOMIAL - MÉTODOS DE LAGRANGE E NEWTON")
    print("=" * 80)

    print("\nDados do problema:")
    print("Corrente i (A): [0.25, 0.75, 1.25, 1.5, 2.0]")
    print("Voltagem V (V): [-0.45, -0.60, 0.70, 1.88, 6.0]")

    x_dados = [0.25, 0.75, 1.25, 1.5, 2.0]
    y_dados = [-0.45, -0.60, 0.70, 1.88, 6.0]

    print("\n" + "=" * 80)
    opcao = input("\nDeseja usar os dados do exemplo? (s/n): ").strip().lower()

    if opcao != 's':
        print("\nEntre com os dados:")
        n = int(input("Quantidade de pontos: "))
        x_dados = []
        y_dados = []

        for i in range(n):
            x = float(input(f"x[{i}] = "))
            y = float(input(f"y[{i}] = "))
            x_dados.append(x)
            y_dados.append(y)

    print("\nPontos fornecidos:")
    for i in range(len(x_dados)):
        print(f"  ({x_dados[i]}, {y_dados[i]})")

    x_alvo = float(input("\nEntre com o valor de x para interpolação: "))
    grau = int(input("Entre com o grau do polinômio (ex: 4 para quarto grau): "))

    x_sel, y_sel = escolher_pontos_centralizados(x_dados, y_dados, x_alvo, grau)

    print(f"\nPontos selecionados para interpolação de grau {grau}:")
    for i in range(len(x_sel)):
        print(f"  ({x_sel[i]}, {y_sel[i]})")

    resultado_lagrange = interpolacao_lagrange(x_sel, y_sel, x_alvo)
    resultado_newton = interpolacao_newton(x_sel, y_sel, x_alvo)

    print("\n" + "=" * 80)
    print("RESULTADOS FINAIS")
    print("=" * 80)
    print(f"\nValor interpolado (Lagrange): V({x_alvo}) = {resultado_lagrange:.10f}")
    print(f"Valor interpolado (Newton):   V({x_alvo}) = {resultado_newton:.10f}")
    print(f"\nDiferença entre métodos: {abs(resultado_lagrange - resultado_newton):.15f}")

    if abs(resultado_lagrange - resultado_newton) < 0.0000000001:
        print("✓ Os métodos concordam (diferença desprezível)")
    else:
        print("⚠ Atenção: diferença significativa entre os métodos")


if __name__ == "__main__":
    main()