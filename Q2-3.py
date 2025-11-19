import numpy as np


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

def jordan():
    pass


def lu():
    pass

def main():
    row = int(input("Insira quantidade de linhas da sua matriz estendida: "))
    col = int(input("Insira quantidade de colunas da sua matriz estendida: "))

    matriz = np.zeros((row, col), dtype=float)

    for i in range(row):
        for j in range(col):
            data = float(input(f"Informe o valor para coluna:{j+1} | linha:{i+1}: "))
            matriz[i, j] = data

    print("Matriz preenchida:")
    print(matriz)

    print("Resolução:")
    print(gauss(matriz,row,col))


if __name__ == "__main__":
    main()