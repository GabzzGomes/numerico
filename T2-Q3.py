import numpy as np

def apresentar_menu():
    print("="*60)
    print(" MÉTODO DE GAUSS-SEIDEL – OPÇÕES")
    print("="*60)
    print("1 - Resolver automaticamente a questão do circuito (A, B, C)")
    print("2 - Inserir matriz manualmente")
    print("="*60)
    escolha = input("Escolha uma opção: ").strip()
    return escolha


def apresentar_questao():
    print("\n=== QUESTÃO DO CIRCUITO ===\n")
    print("Sistema linear das malhas (Lei de Kirchhoff):\n")
    print("11.5·i1  -2.5·i2          -4·i4        =  12")
    print("-2.5·i1   7·i2            -3·i5        = -16")
    print("                  8·i3                 =  14")
    print("-4·i1               9·i4  -3·i5        = -12")
    print("        -3·i2      -3·i4     6·i5      =  30")

    print("\nMatriz estendida usada:")
    print("[ 11.5  -2.5   0   -4    0   |  12 ]")
    print("[ -2.5   7     0    0   -3   | -16 ]")
    print("[   0    0     8    0    0   |  14 ]")
    print("[  -4    0     0    9   -3   | -12 ]")
    print("[   0   -3     0   -3    6   |  30 ]\n")


def matriz_questao():
    return np.array([
        [11.5, -2.5, 0,   -4,   0,  12],
        [-2.5,  7,   0,    0,  -3, -16],
        [0,     0,   8,    0,   0,  14],
        [-4,    0,   0,    9,  -3, -12],
        [0,    -3,   0,   -3,   6,  30]
    ], dtype=float)


def gauss_sidel(matriz,row,col):
    pr = float(input(print("Defina a precisão desejada para a operação: ")))

    diff = np.zeros(col-1)
    k = np.zeros(col-1)
    k1 = np.zeros(col-1)

    diffR = 0

    for i in range(row):
        k[i] =  ( matriz[i][col-1] / matriz[i][i] )
    while True:
        for i in range(row):
            res = 0
            for j in range(col-1):
                if(i != j):
                    res += matriz[i][j]*k[j]
            k1[i] = ( matriz[i][col-1] - res ) / matriz[i][i]
            diff[i] = abs( k1[i] - k[i] )
        k = k1.copy()
        diffR = diff.max() / np.abs(k1).max()
        if(diffR <= pr):
            break;
    return k




def gauss(matriz,rows,col):
    for j in range(rows):
        for i in range(j+1,rows):
            line = matriz[i]
            matriz[i] = line - ( (matriz[i][j] / matriz[j][j]) * matriz[j] )
    result = np.zeros(rows)

    print("Matriz escalonada:")
    print(matriz)

    for z in range(rows-1,-1,-1):
        res = 0
        k = z+1
        while(k <= rows-1):
            res += matriz[z][k]*result[k]
            k += 1
        x = ((matriz[z][-1] - res) / matriz[z][z])
        result[z] = x

    return result

def main():
    escolha = apresentar_menu()

    if escolha == "1":
        apresentar_questao()
        matriz = matriz_questao()
        row, col = matriz.shape

        print("Calculando correntes do circuito...\n")
        resultado = gauss_sidel(matriz, row, col)

        print("=== RESULTADOS ===")
        for i, val in enumerate(resultado):
            print(f"i{i+1} = {val:.6f} A")
        print("==================")

    else:
        row = int(input("Insira quantidade de linhas da matriz estendida: "))
        col = int(input("Insira quantidade de colunas da matriz estendida: "))

        matriz = np.zeros((row, col), dtype=float)

        print("\nDigite os valores da matriz:")
        for i in range(row):
            for j in range(col):
                matriz[i, j] = float(input(f"Valor linha {i+1}, coluna {j+1}: "))

        print("\nResultado:")
        resultado = gauss_sidel(matriz, row, col)
        print(resultado)


if __name__ == "__main__":
    main()