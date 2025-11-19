import numpy as np

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
    
    print("Resultado: ")
    print(gauss_sidel(matriz,row,col))


if __name__ == "__main__":
    main()