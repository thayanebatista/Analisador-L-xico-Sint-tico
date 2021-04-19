
# -*- coding: UTF-8 -*-
import os
import string

# --- token1 do tipo simples para simbolos
#       token100 - +
#       token101 - -
#       token102 - *
#       token103 - /
#       token104 - =
#       token105 - >
#       token106 - <
#       token107 - (
#       token108 - )
#       token109 - ,
#       token110 - .
#       token111 - ;
#       token112 - :
#       token113 -

# --- token2 do tipo duplo para simbolos
#       token200 - <>
#       token201 - >=
#       token202 - <=
#       token203 - :=

# --- token3 tipo de numero

#       token300 - inteiro
#       token301 - real

# --- token4 do tipo palavras reservadas
#       token400 - program
#       token401 - if
#       token402 - else
#       token403 - integer
#       token404 - var
#       token405 - then
#       token406 - while
#       token407 - do
#       token408 - begin
#       token409 - end
#       token410 - procedure
#       token411 - real
#       token412 - write
#       token413 - read


# --- token5 para identificadores
#       tokens 500_
class Lexico():

    # inicializando atributos da classe
    def __init__(self, entrada):
        self.input = entrada
        self.output = "resultado_lexico.txt"

    # definindo o arquivo lido para string
    def arq(self):
        self.input = string

    def arqentrada(self):
        return self.input

    def arqsaida(self):
        return self.output

    # definindo se é um simbolo unico, simples
    def simbolounico(self, entrada):
        # operadores de adição e subtração
        # operadores de divisao e multiplicação
        # operadores relacionais simples
        unico = "+-*/=><(),.;:"
        if entrada in unico:
            return True
        return False

    def qualunico(self, entrada):
        unico = "+-*/=><(),.;:"
        posicao = unico.find(entrada)  # find retorna a posição do caracter caso exista no arquivo
        if posicao <= 9:
            return "token10" + str(posicao)
        else:
            return "token1" + str(posicao)

    # definindo se é um simbolo duplo, mais de 1 caracter
    def simboloduplo(self, entrada):
        # operadores relacionais duplos
        # delimitadores
        duplo = "<>,>=,<=,:=".split(',')
        if entrada in duplo:
            return True
        return False

    def qualduplo(self, entrada):
        duplo = "<>,>=,<=,:=".split(',')
        posicao = 0
        for x in duplo:
            if x == entrada:
                break
            posicao += 1
        return "token20" + str(posicao)

    def palavra_reservada(self, entrada):
        # listagem das palavras reservadas da linguagem
        reservadas = "program,if,else,integer,var,then,while,do,begin,end,procedure,real,write,read".split(',')
        if entrada in reservadas:
            return True
        return False

    def qualreservada(self, entrada):
        reservadas = "program,if,else,integer,var,then,while,do,begin,end,procedure,real,write,read".split(',')
        posicao = 0
        for x in reservadas:
            if x == entrada:
                break
            posicao += 1
        if posicao <= 9:
            return "token40" + str(posicao)
        else:
            return "token4" + str(posicao)

    def letra(self, entrada):
        # desta vez utilizando a lib string para nos dizer as letras
        letras = string.ascii_letters
        if entrada in letras:
            return True
        return False

    def numeros(self, entrada):
        # lista de numeros
        number = '0123456789'
        if entrada in number:
            return True
        return False

    def lexanalise(self):

        # abrindo o arquivo que ira para o analisador sintatico
        saida = open(self.output, 'w')

        # verificando se o arquivo esta presente
        if not os.path.exists(self.input):
            saida.write("Nao existe input!")
            return

        # abrindo o arquivo de entrada com lalgol
        lalgol = open(self.input, 'r')

        # lendo a linha do arquivo com a linguagem lalgol
        linhaLALGOL = lalgol.readline()

        # numero da linha
        linha = 1

        while linhaLALGOL:  # enquanto ainda estiver lendo a linha do arquivo txt
            i = 0
            tam = len(linhaLALGOL)  # tamanho da linha

            while i < tam:  # enquanto menor que o tamanho da linha sendo lida
                ch_atual = linhaLALGOL[i]
                prox_ch = None
                # verificando se o prox caracter existe
                if i + 1 < tam:
                    prox_ch = linhaLALGOL[i + 1]

                # ****iniciando verificações de linguagem

                # --- verificando simbolo duplo
                # prox_ch != None
                if prox_ch != None and self.simboloduplo(ch_atual + prox_ch):
                    saida.write(self.qualduplo(ch_atual + prox_ch) + '_' +
                                ch_atual + prox_ch + '=>' + str(linha) + '\n')
                    i += 1

                # --- reconhecendo comentarios - tipo de comentario '*/'
                elif ch_atual == '/' and prox_ch == '*':
                    com = True
                    linhaatual = linha
                    while com and not (ch_atual == '*' and prox_ch == '/'):
                        if i + 2 < tam:
                            i += 1
                            ch_atual = linhaLALGOL[i]
                            prox_ch = linhaLALGOL[i + 1]
                        else:  # lendo a proxima linha
                            linhaLALGOL = lalgol.readline()
                            tam = len(linhaLALGOL)
                            linha += 1
                            i = -1
                            if not linhaLALGOL:
                                saida.write(
                                    "Erro Lexico - comentario aberto e nao fechado - linha: %d\n" % linhaatual)
                                com = False
                    i += 1  # nao considera o endoffile
                # --- lendo tipo de comentario entre '{}'
                elif ch_atual == '{':
                    com = True  # comentario
                    linhaatual = linha
                    while com and not ch_atual == '}':
                        if i + 1 < tam:
                            i += 1
                            ch_atual = linhaLALGOL[i]
                        else:
                            linhaLALGOL = lalgol.readline()
                            tam = len(linhaLALGOL)
                            linha += 1
                            i = -1
                            if not linhaLALGOL:
                                saida.write(
                                    "Erro Lexico - comentario aberto e nao fechado - linha: %d\n" % linhaatual)
                                # %d - escrever como string a variavel linhaatua
                                com = False

                # --- verificando simbolo unico
                elif self.simbolounico(ch_atual):
                    saida.write(self.qualunico(ch_atual) + '_' + ch_atual + '=>' +
                                str(linha) + '\n')

                # --- verificando se é numero
                elif self.numeros(ch_atual):
                    temp = ch_atual
                    i += 1
                    j = 0  # usando para verificar numeros com casa decimal
                    ch_atual = linhaLALGOL[i]
                    while self.numeros(ch_atual) and (i + 1 < tam):
                        temp += ch_atual
                        i += 1
                        ch_atual = linhaLALGOL[i]

                    if ch_atual == '.':
                        if i + 1 < tam:
                            temp += ch_atual
                            i += 1
                            ch_atual = linhaLALGOL[i]
                            while self.numeros(ch_atual) and i + 1 < tam:
                                j += 1
                                temp += ch_atual
                                i += 1
                                ch_atual = linhaLALGOL[i]
                            if ch_atual == '.':
                                j = 0
                                while i + 1 < tam:
                                    i += 1
                                    ch_atual = linhaLALGOL[i]
                                    if self.numeros(ch_atual) or ch_atual == ' ':
                                        i -= 1  # verificando a malformação de numeros
                                        break
                        else:
                            saida.write("Erro Lexico - mal formação de numero - linha: %d\n" % linha)
                        if j > 0:
                            saida.write('token301_' + temp + '=>' + str(linha) + '\n')
                        else:
                            saida.write("Erro Lexico - mal formação de numero - linha: %d\n" % linha)
                    else:
                        saida.write('token300_' + temp + '=>' + str(linha) + '\n')

                    if not self.numeros(ch_atual):
                        i -= 1

                # --- verificando palavra reservada ou identificador
                elif self.letra(ch_atual):
                    temp = ch_atual
                    i += 1
                    erro = False

                    while i < tam:
                        prox_ch = None
                        ch_atual = linhaLALGOL[i]
                        if i + 1 < tam:
                            prox_ch = linhaLALGOL[i + 1]
                        if (self.letra(ch_atual) or self.numeros(ch_atual) or ch_atual == '_'):
                            temp += ch_atual
                        elif (ch_atual == ',' or ch_atual == ';'
                              or ch_atual == ' ' or ch_atual == '\t'
                              or ch_atual == '\r' or ch_atual == '/'):
                            i -= 1
                            break
                        elif (prox_ch != None
                              and self.simboloduplo(ch_atual + prox_ch)
                              or self.simbolounico(ch_atual)):
                            i -= 1
                            break
                        elif ch_atual != '\n':
                            saida.write("Erro Lexico: Identificador invalido {" + ch_atual + "} - linha: %d\n" % linha)
                            erro = True  # reconheceu o erro
                            break
                        i += 1  # seguindo com as verificações
                    if erro:
                        while i + 1 < tam:
                            i += 1
                            ch_atual = linhaLALGOL[i]
                            if (self.simbolounico(ch_atual) or ch_atual == ' '
                                    or ch_atual == '\t' or ch_atual == '\r'
                                    or ch_atual == '/'):
                                i -= 1
                                break
                    else:
                        if self.palavra_reservada(temp):
                            saida.write(
                                self.qualreservada(temp) + '_' + temp + '=>' +
                                str(linha) + '\n')
                        else:
                            saida.write("token500_" + temp + '=>' + str(linha) + '\n')
                # --- reconhecendo tipo de caracter invalido
                elif (ch_atual != '\n' and ch_atual == ' '
                      and ch_atual == '\t' and ch_atual == '\r'
                      ):
                    saida.write("Erro Lexico: Caracter {" + ch_atual + "} invalido - linha: %d\n" % linha)
                # --- reconhecendo algum caracter que nao existe na linguagem
                elif (self.letra(ch_atual) == False
                      and self.numeros(ch_atual) == False
                      and self.palavra_reservada(ch_atual) == False
                      and ch_atual != '\n' and ch_atual != ' '
                      and ch_atual != '\t' and ch_atual != '\r'):
                    saida.write(
                        "Erro Lexico: Caracter {" + ch_atual + "} nao reconhecido na linguagem - linha: %d\n" % linha)
                i += 1

            linhaLALGOL = lalgol.readline()
            linha += 1
        # --- fim
        #saida.write('$')
        lalgol.close()
        saida.close()