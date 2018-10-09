# Bibliotecas
import numpy as np

m0 = {'N': True, 'S': True, 'E': True, 'O': True, 'NE': True, 'NO': True, 'SE': True, 'SO': True}
[lin, col, inicio, alvo, ch, cv, cd, movimento, obstaculo] = [3, 3, 1, 9, 1, 1, 12, m0, [2, 3]]
# Configurações
LINHAS = lin       # Número de Linhas
COLUNAS = col      # Número de Colunas
INICIO = inicio    # Posição Inicial
ALVO = alvo        # Posição Alvo
CH = ch            # Custo Horizontal
CV = cv            # Custo Vertical
# Custo Diagonal (Vários tipos)
dcustos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,  11: CV+CH, 12: (CH**2+CV**2)**(1/2)}
CD = dcustos.get(cd, 12)
MOVIMENTACAO = movimento  # {'N':True,'S':True,'E':True,'O':True,'NE':True,'NO':True,'SE':True, 'SO':True}
OBSTACULOS = obstaculo
CUSTO = 0                # Custo total
ABERTO = []              # Conjunto de Posições Abertas
FECHADO = []             # Conjunto de Posições Fechadas

# Inicialização das variáveis dadas as configurações
mapaLabirinto = np.arange(1, LINHAS * COLUNAS + 1, 1).reshape(LINHAS, COLUNAS)  # Labirinto com cada posição numerada
mapaCusto = np.zeros(LINHAS*COLUNAS).reshape(LINHAS, COLUNAS)            # Labirinto com o custo de cada posição
mapaCustoG = np.zeros(LINHAS*COLUNAS).reshape(LINHAS, COLUNAS)            # Labirinto com o custo de cada posição
mapaCustoH = np.zeros(LINHAS*COLUNAS).reshape(LINHAS, COLUNAS)            # Labirinto com o custo de cada posição
mapaCaminho = [[None for a in range(LINHAS)] for b in range(COLUNAS)]    # Labirinto com o caminho para cada posição
# mapaCaminhosAlt = [[[] for a in range(LINHAS)] for b in range(COLUNAS)]    # Labirinto com o caminho para cada posição
alvoIndex = np.argwhere(mapaLabirinto == ALVO)          # Index da posição alvo


# Funções
def atualizar_config(ln, cl, ini, al, cho, cve, cdi, mov, obst):
    """ Atualiza as configurações do algoritmo A*"""
    global LINHAS, COLUNAS, INICIO, ALVO, CH, CV, CD, MOVIMENTACAO, OBSTACULOS
    global dcustos
    LINHAS = ln   # Número de Linhas
    COLUNAS = cl  # Número de Colunas
    INICIO = ini  # Posição Inicial
    ALVO = al     # Posição Alvo
    CH = cho      # Custo Horizontal
    CV = cve      # Custo Vertical
    dcustos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: cve + cho,
               12: (cho ** 2 + cve ** 2) ** (1 / 2)}
    CD = dcustos.get(cdi, 12)  # Custo Diagonal (Vários tipos)
    # {'N': True, 'S': True, 'E': True, 'W': True, 'NE': True, 'NW': True, 'SE': True, 'SW': True}
    MOVIMENTACAO = mov
    OBSTACULOS = obst   # Lista com os obstáculos


def dist_manhattan(x_inicial, y_inicial, x_alvo, y_alvo):
    """ Distância Manhattan entre as células """
    custo = abs(x_inicial - x_alvo) + abs(y_inicial - y_alvo)
    return custo


def dist_pitagoras(x_inicial, y_inicial, x_alvo, y_alvo):
    """ Distância pitagórica entre as células """
    custo = ((x_inicial - x_alvo)**2 + (y_inicial - y_alvo)**2)**(1/2)
    return custo


def melhor_caminho(pos):
    caminho = [pos]
    pos_index = np.argwhere(mapaLabirinto == pos)
    x_0 = pos_index[0][0]
    y_0 = pos_index[0][1]
    anterior = mapaCaminho[x_0][y_0]
    while anterior != INICIO:
        caminho.append(anterior)
        n_index = np.argwhere(mapaLabirinto == anterior)
        x_n = n_index[0][0]
        y_n = n_index[0][1]
        anterior = mapaCaminho[x_n][y_n]
    caminho.append(INICIO)
    return list(reversed(caminho))


def custo_posicao(pos):
    pos_index = np.argwhere(mapaLabirinto == pos)
    x = pos_index[0][0]
    y = pos_index[0][1]
    return mapaCusto[x][y]


def custo_movimentacao(caminho=list([]), pos_i=1, pos_f=1):
    """ Retorna o custo da movimentação entre duas posições ou um caminho."""
    custo = 0
    # Caso o argumento sejam duas posições
    pos_i_index = np.argwhere(mapaLabirinto == pos_i)
    pos_f_index = np.argwhere(mapaLabirinto == pos_f)
    x_i = pos_i_index[0][0]
    y_i = pos_i_index[0][1]
    x_f = pos_f_index[0][0]
    y_f = pos_f_index[0][1]
    if x_f != x_i and y_f != y_i:
        custo = CD
    elif x_f != x_i:
        custo = CH
    elif y_f != y_i:
        custo = CV
    # Caso o argumento seja uma lista
    if len(caminho) >= 1:
        custo = 0
        for index in range(len(caminho)-1):
            custo += custo_movimentacao([], caminho[index], caminho[index + 1])
    return custo


def conexao_celula(cel_index):
    """ Retorna uma lista com as possiveis conexoes da celula, dada em index da matrix. """
    x = cel_index[0][0]
    y = cel_index[0][1]
    conexao = []
    # Possíveis Movimentos
    if x > 0 and MOVIMENTACAO['E']:
        conexao.append(mapaLabirinto[x - 1][y])
    if x < LINHAS - 1 and MOVIMENTACAO['O']:
        conexao.append(mapaLabirinto[x + 1][y])
    if y > 0 and MOVIMENTACAO['N']:
        conexao.append(mapaLabirinto[x][y - 1])
    if y < COLUNAS - 1 and MOVIMENTACAO['S']:
        conexao.append(mapaLabirinto[x][y + 1])
    if x > 0 and y > 0 and MOVIMENTACAO['NO']:
        conexao.append(mapaLabirinto[x - 1][y - 1])
    if x < LINHAS - 1 and y < COLUNAS - 1 and MOVIMENTACAO['SE']:
        conexao.append(mapaLabirinto[x + 1][y + 1])
    if y > 0 and x < LINHAS - 1 and MOVIMENTACAO['SO']:
        conexao.append(mapaLabirinto[x + 1][y - 1])
    if x > 0 and y < COLUNAS - 1 and MOVIMENTACAO['NE']:
        conexao.append(mapaLabirinto[x - 1][y + 1])
    # Ignorando celulas obstaculo como caminho possivel
    set_conexao = set(conexao)
    set_obstaculos = set(OBSTACULOS)
    conexao = list(set_conexao - set_obstaculos)
    return conexao  # lista com as celulas que se conectam com cel_index


def run_a_estrela():
    global LINHAS, COLUNAS, INICIO, ALVO, CH, CV, CD, MOVIMENTACAO, OBSTACULOS, ABERTO, FECHADO
    global mapaLabirinto, mapaCaminho, mapaCusto, mapaCustoG, mapaCustoH, alvoIndex

    # Inicialização das variáveis dadas as configurações

    ABERTO = [INICIO]  # Conjunto de Posições Abertas
    FECHADO = []  # Conjunto de Posições Fechadas
    CAMINHO = []  # Caminho Encontrado

    mapaLabirinto = np.arange(1, LINHAS * COLUNAS + 1, 1).reshape(LINHAS,
                                                                  COLUNAS)   # Labirinto com cada posição numerada
    mapaCusto = np.zeros(LINHAS * COLUNAS).reshape(LINHAS, COLUNAS)          # Labirinto com o custo de cada posição
    mapaCustoG = np.zeros(LINHAS * COLUNAS).reshape(LINHAS, COLUNAS)  # Labirinto com o custo de cada posição
    mapaCustoH = np.zeros(LINHAS * COLUNAS).reshape(LINHAS, COLUNAS)  # Labirinto com o custo de cada posição
    mapaHeuristica = np.zeros(LINHAS * COLUNAS).reshape(LINHAS, COLUNAS)  # Labirinto com as heurísticas
    mapaCaminho = [[None for a in range(COLUNAS)] for b in range(LINHAS)]    # Labirinto com o caminho para cada posição
    # mapaCaminhosAlt = [[[] for a in range(COLUNAS)] for b in range(LINHAS)]  # Labirinto com o caminhos alternativos
    alvoIndex = np.argwhere(mapaLabirinto == ALVO)                           # Index da posição alvo

    while True:
        if len(ABERTO) == 0:
            print("O algoritmo não encontrou nenhum caminho!")
            return None, None, None, None, None, None, None, None
        else:
            custoInicial = [0 for a in range(len(ABERTO))]
            # Procurar menor f'
            abertoIndex = 0
            for i in ABERTO:
                tempIndex = np.argwhere(mapaLabirinto == i)
                heuristica = dist_pitagoras(tempIndex[0][0], tempIndex[0][1], alvoIndex[0][0], alvoIndex[0][1])
                custoInicial[abertoIndex] = mapaCusto[tempIndex[0][0]][tempIndex[0][1]] + heuristica
                abertoIndex += 1
                mapaHeuristica[tempIndex[0][0]][tempIndex[0][1]] = heuristica
            # print(custoInicial)
            # Index de menor função custo
            nCusto = min(custoInicial)
            nIndex = np.argwhere(mapaLabirinto == ABERTO[custoInicial.index(nCusto)])
            nPosicao = mapaLabirinto[nIndex[0][0]][nIndex[0][1]]
            ABERTO.remove(nPosicao)
            FECHADO.append(nPosicao)
            # Verifica se está na posição alvo
            if nPosicao == mapaLabirinto[alvoIndex[0][0]][alvoIndex[0][1]]:
                print("Chegamos ao local alvo!")
                CAMINHO = melhor_caminho(nPosicao)
                print(CAMINHO)
                #CUSTO = custo_movimentacao(CAMINHO)
                #print(CUSTO)
                print(mapaCaminho)
                print(mapaCusto)
                print(mapaCustoH)
                return CAMINHO, ABERTO, FECHADO, mapaCusto, mapaCustoH, mapaHeuristica, mapaCaminho
            # Sucessores
            nSucessores = conexao_celula(nIndex)
            for m in range(len(nSucessores)):
                mPosicao = nSucessores[m]
                mIndex = np.argwhere(mapaLabirinto == mPosicao)
                if mPosicao not in ABERTO and nSucessores[m] not in FECHADO:
                    ABERTO.append(mPosicao)
                    # Dá valores a função custo dos nós abertos
                    mapaCustoG[mIndex[0][0]][mIndex[0][1]] = custo_posicao(nPosicao)
                    mapaCustoH[mIndex[0][0]][mIndex[0][1]] = custo_movimentacao([], nPosicao, mPosicao)
                    # mapaCusto[mIndex[0][0]][mIndex[0][1]] = (custo_posicao(nPosicao) + custo_movimentacao([],
                    #                                                                                       nPosicao,
                    #                                                                                       mPosicao))
                    mapaCusto[mIndex[0][0]][mIndex[0][1]] = mapaCustoG[mIndex[0][0]][mIndex[0][1]] + \
                                                            mapaCustoH[mIndex[0][0]][mIndex[0][1]]
                    # Dá valores ao mapa caminho
                    mapaCaminho[mIndex[0][0]][mIndex[0][1]] = nPosicao
                # Caso a posição já tenha sido encontrada
                elif mPosicao in ABERTO:
                    custoVelho = custo_posicao(mPosicao)
                    custoAtual = custo_posicao(nPosicao) + custo_movimentacao([], nPosicao, mPosicao)
                    if custoAtual < custoVelho:
                        mapaCustoG[mIndex[0][0]][mIndex[0][1]] = custo_posicao(nPosicao)
                        mapaCustoH[mIndex[0][0]][mIndex[0][1]] = custo_movimentacao([], nPosicao, mPosicao)
                        mapaCusto[mIndex[0][0]][mIndex[0][1]] = custoAtual
                        mapaCaminho[mIndex[0][0]][mIndex[0][1]] = nPosicao
                elif mPosicao in FECHADO:
                    custoVelho = custo_posicao(mPosicao)
                    custoAtual = custo_posicao(nPosicao) + custo_movimentacao([], nPosicao, mPosicao)
                    if custoAtual < custoVelho:
                        mapaCustoG[mIndex[0][0]][mIndex[0][1]] = custo_posicao(nPosicao)
                        mapaCustoH[mIndex[0][0]][mIndex[0][1]] = custo_movimentacao([], nPosicao, mPosicao)
                        mapaCusto[mIndex[0][0]][mIndex[0][1]] = custoAtual
                        mapaCaminho[mIndex[0][0]][mIndex[0][1]] = nPosicao

