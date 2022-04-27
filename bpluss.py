import math
import pandas as pd 

# Criar um nó 
class No:
    #construct
    def __init__(self, ordem):
        self.ordem = ordem
        self.valores = []
        self.chaves = []
        self.proxChave = None
        self.pai = None
        self.ver_folha = False

    # Inserir em uma folha 
    def inserir_na_folha(self, folha, valor, chave):
        if (self.valores):
            valFolha1 = self.valores
            for i in range(len(valFolha1)):
                if (valor == valFolha1[i]):
                    self.chave[i].append(chave)
                    break
                elif (valor < valFolha1[i]):
                    self.valores = self.valores[:i] + [valor] + self.valores[i:]
                    self.chaves = self.chaves[:i] + [[chave]] + self.chaves[i:]
                    break
                elif (i + 1 == len(valFolha1)):
                    self.valores.append(valor)
                    self.chaves.append([chave])
                    break
        else:
            self.valores = [valor]
            self.chaves = [[chave]]

# B+ tree
class arvoreBMais:
    #construct
    def __init__(self, ordem):
        self.raiz = No(ordem)
        self.raiz.ver_folha = True
    
    #operação de procurar um nó
    def procurar(self, valor):
        no_atual = self.raiz
        while(no_atual.ver_folha == False):
            valFolha2 = no_atual.valores
            for i in range(len(valFolha2)):
                if (valor == valFolha2[i]):
                    no_atual = no_atual.chaves[i + 1]
                    break
                elif (valor < valFolha2[i]):
                    no_atual = no_atual.chaves[i]
                    break
                elif (i + 1 == len(no_atual.valores)):
                    no_atual = no_atual.chaves[i + 1]
                    break
        return no_atual

    #operação de inserir um nó
    def inserir(self, valor, chave):
        valor = str(valor)
        no_velho = self.procurar(valor)
        no_velho.inserir_na_folha(no_velho, valor, chave)
        if (len(no_velho.valores) == no_velho.ordem):
            no1 = No(no_velho.ordem)
            no1.ver_folha = True
            no1.pai = no_velho.pai
            meio = int(math.ceil(no_velho.ordem/2)) -1
            no1.valores = no_velho.valores[meio + 1:]
            no1.chaves = no_velho.chaves[meio + 1:]
            no1.proxChave = no_velho.proxChave
            no_velho.valores = no_velho.valores[:meio + 1]
            no_velho.chaves = no_velho.chaves[:meio + 1]
            no_velho.proxChave = no1
            self.inserir_no_pai(no_velho, no1.valores[0], no1)

    #operação para achar um nó
    def achar(self, valor, chave):
        j = self.procurar(valor)
        for i, item in enumerate(j.valores):
            if item == valor:
                if chave in j.chaves[i]:
                    return True
                else:
                    return False
            return False

    #operação para inserir um nó no pai 
    def inserir_no_pai(self, n, valor, ndash):
        if (self.raiz == n):
            raizNo = No(n.ordem)
            raizNo.valores = [valor]
            raizNo.chaves = [n , ndash]
            self.raiz = raizNo
            n.pai = raizNo
            ndash.pai = raizNo
            return

        paiNo = n.pai
        valFolha3 = paiNo.chaves
        for i in range(len(valFolha3)):
            if (valFolha3[i] == n):
                paiNo.valores = paiNo.valores[:i]+ \
                    [valor] + paiNo.valores[i:]
                paiNo.chaves = paiNo.chaves[:i + 1] + [ndash] + paiNo.chaves[i + 1:]
                if (len(paiNo.chaves) > paiNo.ordem):
                    paiDash = No(paiNo.ordem)
                    paiDash.pai = paiNo.pai
                    meio = int(math.ceil(paiNo.ordem/2))-1
                    paiDash.valores = paiNo.valores[meio+1:]
                    paiDash.chaves = paiNo.chaves[meio + 1:]
                    valor_ = paiNo.valores[meio]
                    if (meio == 0):
                        paiNo.valores = paiNo.valores[:meio+1]
                    else:
                        paiNo.valores = paiNo.valores[:meio]
                    paiNo.chaves = paiNo.chaves[:meio +1]
                    for j in paiNo.chaves:
                        j.pai = paiNo
                    for j in paiDash.chaves:
                        j.pai = paiDash
                    self.inserir_no_pai(paiNo, valor_, paiDash)

    #operação para deletar um nó
    def deletar(self, valor, chave):
        no_ = self.procurar(valor)

        valFolha = 0
        for i, item in enumerate(no_.valores):
            if item == valor:
                valFolha = 1

                if chave in no_.chaves[i]:
                    if len(no_.chaves[i]) > 1:
                        no_.chaves[i].pop(no_.chaves[i].index(chave))
                    elif no_ == self.raiz:
                        no_.valores.pop(i)
                        no_.chaves.pop(i)
                    else:
                        no_.chaves[i].pop(no_.chaves[i].index(chave))
                        del no_.chaves[i]
                        no_.valores.pop(no_.valores.index(valor))
                        self.deletarEntrada(no_, valor, chave)
                else:
                    print("Não há valor na chave dada")
                    return
        if valFolha == 0:
            print("Valor não está na chave")
            return

    #operação para deletar uma entrada
    def deletarEntrada(self, no_, valor, chave):
        if not no_.ver_folha:
            for i, item in enumerate(no_.chaves):
                if item == chave:
                    no_.chaves.pop(i)
                    break
            for i, item in enumerate(no_.valores):
                if item == valor:
                    no_.valores.pop(i)
                    break
        if self.raiz == no_ and len(no_.chaves) == 1:
            self.raiz = no_.chaves[0]
            no_.chaves[0].parent = None
            del no_
            return
        elif (len(no_.cahves) < int(math.ceil(no_.ordem/2)) and no_.ver_folha == False) or (no_.valores < int(math.ceil((no_.ordem -1) / 2)) and no_.ver_folha == True):
            predecessor = 0
            paiNo = no_.pai
            antNo = -1
            proxNo = -1
            antChave = -1
            proxChave = -1
            for i, item in enumerate(paiNo.chaves):
                if item == no_:
                    if i > 0:
                        antNo = paiNo.chaves[i - 1]
                        antChave = paiNo.valores[i -1]
                    if i < len(paiNo.chaves) - 1:
                        proxNo = paiNo.chaves[i + 1]
                        proxChave = paiNo.valores[i]
            if antNo == -1:
                ndash = proxNo
                valor_ = proxChave
            elif proxNo == -1:
                predecessor = 1
                ndash = antNo
                valor_ = antChave
            else:
                if len(no_.valores) + len(proxNo.valores) < no_.ordem:
                    ndash = antNo
                    valor_ = antChave
                else: 
                    predecessor = 1
                    ndash = antNo
                    valor_ = antChave
            if len(no_.valores) + len(ndash.valores) < no_.ordem:
                if predecessor == 0:
                    no_, ndash = ndash, no_
                ndash.chaves += no_.chaves
                if not no_.ver_folha:
                    ndash.valores.append(valor_)
                else:
                    ndash.proxChave = no_.proxChave
                ndash.valores += no_.valores

                if not ndash.ver_folha:
                    for j in ndash.chaves:
                        j.pai = ndash
                self.deletarEntrada(no_.pai, valor_, no_)
                del no_
            else:
                if predecessor == 1:
                    if not no_.ver_folha:
                        ndashpm = ndash.chaves.pop(-1)
                        ndashkm_1 = ndash.valores.pop(-1)
                        no_.chaves = [ndashpm] + no_.chaves
                        no_.valores = [valor_] + no_.valores
                        paiNo = no_.pai
                        for i, item in enumerate(paiNo.valores):
                            if item == valor_:
                                p.valores[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.chaves.pop(-1)
                        ndashkm = ndash.valores.pop(-1)
                        no_.chaves = [ndashpm] + no_.chaves
                        no_.valores = [ndashkm] + no_.valores
                        paiNo = no_.pai
                        for i, item in enumerate(p.valores):
                            if item == valor_:
                                paiNo.valores[i] = ndashkm
                                break
                else:
                    if not no_.ver_folha:
                        ndashp0 = ndash.chaves.pop(0)
                        ndashk0 = ndash.valores.pop(0)
                        no_.chaves = no_.chaves + [ndashp0]
                        no_.valores = no_.valores + [valor_]
                        paiNo = no_.pai
                        for i, item in enumerate(paiNo.valores):
                            if item == valor_:
                                paiNo.valores[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.chaves.pop(0)
                        ndashk0 = ndash.valores.pop(0)
                        no_.chaves = no_.chaves + [ndashp0]
                        no_.valores = no_.valores + [ndashk0]
                        paiNo = no_.pai
                        for i, item in enumerate(paiNo.valores):
                            if item == valor_:
                                paiNo.valores[i] = ndash.valores[0]
                                break
                if not ndash.ver_folha:
                    for j in ndash.chaves:
                        j.pai = ndash
                if not no_.ver_folha:
                    for j in no_.chaves:
                        j.pai = no_
                if not paiNo.ver_folha:
                    for j in paiNo.chaves:
                        j.pai = paiNo       

# mostrar árvore b+
def printarArvore(tree):
    prim = [tree.raiz]
    level = [0]
    folha = None
    flag = 0
    lev_folha = 0
    no1 = No(str(level[0]) + str(tree.raiz.valores))
    while (len(prim) != 0):
        x = prim.pop(0)
        lev = level.pop(0)
        if (x.ver_folha == False):
            for i, item in enumerate(x.chaves):
                print(item.valores)
        else:
            for i, item in enumerate(x.chaves):
                print(item.valores)
                if (flag == 0):
                    lev_folha = lev
                    folha = x
                    flag = 1

marcar_tam = 3
arvorebmais = arvoreBMais(marcar_tam)
arvorebmais.inserir('5', '33')
arvorebmais.inserir('15', '21')
arvorebmais.inserir('25', '31')
arvorebmais.inserir('35', '41')
arvorebmais.inserir('45', '10')
printarArvore(arvorebmais)

if(arvorebmais.achar('5', '34')):
    print("Encontrado")
else:
    print("Não Encontrado")