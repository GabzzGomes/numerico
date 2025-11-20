import numpy as np

def regra_trapezio(profundidades, espacamento):
    """
    Calcula a área usando a Regra do Trapézio (Repetida)
    A = (h/2) * [y0 + 2*(y1 + y2 + ... + yn-1) + yn]
    """
    n = len(profundidades)
    area = (espacamento / 2) * (
        profundidades[0] + 
        2 * sum(profundidades[1:-1]) + 
        profundidades[-1]
    )
    return area

def regra_simpson_1_3(profundidades, espacamento, mostrar_aviso: bool = True):
    """
    Calcula a área usando a Regra de Simpson 1/3 (Repetida)
    A = (h/3) * [y0 + 4*(y1+y3+y5+...) + 2*(y2+y4+y6+...) + yn]
    Requer número ímpar de pontos (número par de intervalos)
    """
    n = len(profundidades)
    
    if n % 2 == 0:
        if mostrar_aviso:
            print("AVISO: Regra de Simpson 1/3 requer número ímpar de pontos.")
            print("Aplicando Simpson 1/3 até o penúltimo ponto e Trapézio no último intervalo.\n")
        
        soma_impares = sum(profundidades[i] for i in range(1, n-2, 2))
        soma_pares = sum(profundidades[i] for i in range(2, n-2, 2))
        area_simpson = (espacamento / 3) * (
            profundidades[0] + 
            4 * soma_impares + 
            2 * soma_pares + 
            profundidades[n-2]
        )
        
        area_trapezio = espacamento * (profundidades[n-2] + profundidades[n-1]) / 2
        
        return area_simpson + area_trapezio
    else:
        soma_impares = sum(profundidades[i] for i in range(1, n-1, 2))
        soma_pares = sum(profundidades[i] for i in range(2, n-1, 2))
        
        area = (espacamento / 3) * (
            profundidades[0] + 
            4 * soma_impares + 
            2 * soma_pares + 
            profundidades[-1]
        )
        return area

def imprimir_resultados(profundidades, distancias, espacamento, area_trapezio, area_simpson):
    """Imprime os resultados formatados"""
    print("\n" + "="*70)
    print("DADOS DE ENTRADA")
    print("="*70)
    print(f"{'Ponto':<8} {'Distância (m)':<18} {'Profundidade (m)':<20}")
    print("-"*70)
    for i, (dist, prof) in enumerate(zip(distancias, profundidades)):
        print(f"{i:<8} {dist:<18.2f} {prof:<20.2f}")
    
    print(f"\nEspaçamento entre pontos: {espacamento:.2f} m")
    print(f"Número de pontos: {len(profundidades)}")
    print(f"Número de intervalos: {len(profundidades)-1}")
    
    print("\n" + "="*70)
    print("RESULTADOS")
    print("="*70)
    print(f"Área pela Regra do Trapézio:        {area_trapezio:.4f} m²")
    print(f"Área pela Regra de Simpson 1/3:     {area_simpson:.4f} m²")
    print(f"Diferença entre os métodos:         {abs(area_trapezio - area_simpson):.4f} m²")
    print(f"Diferença percentual:               {abs(area_trapezio - area_simpson)/area_simpson*100:.2f}%")
    print("="*70)

def main():
    print("="*70)
    print("CÁLCULO DE ÁREA DA SEÇÃO RETA DE RIOS E LAGOS")
    print("Métodos: Regra do Trapézio e Regra de Simpson 1/3 (Repetida)")
    print("="*70)
    
    print("\nEscolha uma opção:")
    print("1 - Usar dados do exemplo da figura")
    print("2 - Inserir dados manualmente")
    
    opcao = input("\nOpção: ").strip()
    
    if opcao == "1":
        distancias_acum = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        profundidades = np.array([0, 1.8, 2.0, 4.0, 4.0, 6.0, 4.0, 3.6, 3.4, 2.8, 0])
        
        espacamento = 2.0
        
    else:
        n_pontos = int(input("\nQuantidade de pontos medidos: "))
        
        print("\nOs pontos estão igualmente espaçados?")
        print("1 - Sim")
        print("2 - Não")
        espacamento_igual = input("Opção: ").strip()
        
        if espacamento_igual == "1":
            espacamento = float(input("Espaçamento entre pontos (m): "))
            distancias_acum = np.array([i * espacamento for i in range(n_pontos)])
        else:
            print("\nInsira as distâncias a partir da margem esquerda:")
            distancias_acum = []
            for i in range(n_pontos):
                dist = float(input(f"Distância do ponto {i} (m): "))
                distancias_acum.append(dist)
            distancias_acum = np.array(distancias_acum)
            
            diferencas = np.diff(distancias_acum)
            if np.allclose(diferencas, diferencas[0], rtol=0.01):
                espacamento = diferencas[0]
            else:
                print("\nERRO: Os métodos requerem pontos igualmente espaçados!")
                return
        
        print("\nInsira as profundidades:")
        profundidades = []
        for i in range(n_pontos):
            prof = float(input(f"Profundidade no ponto {i} (m): "))
            profundidades.append(prof)
        profundidades = np.array(profundidades)
    
    area_trapezio = regra_trapezio(profundidades, espacamento)
    area_simpson = regra_simpson_1_3(profundidades, espacamento)
    
    imprimir_resultados(profundidades, distancias_acum, espacamento, 
                       area_trapezio, area_simpson)

if __name__ == "__main__":
    main()
    
    print("\n\nDeseja fazer outro cálculo? (s/n): ", end="")
    resposta = input().strip().lower()
    if resposta == 's':
        print("\n")
        main()