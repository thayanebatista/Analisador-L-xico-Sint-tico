import os


# mudança no reconhecimento

# gramatica
# inclusao do comando repeat until
# comentarios entre chaves
# Identificadores e números são itens léxicos da forma:
# - ident: seqüência de letras e dígitos, começando por letra
# - número inteiro: seqüência de dígitos (0 a 9)
# - número real: pelo menos um dígito seguido de um ponto decimal
#                e de uma seqüência de um ou mais dígitos]


class Sintatico():

    def __init__(self):
        self.input = "resultado_lexico.txt"
        self.output = "resultado_sintatico.txt"
        self.output = open("resultado_sintatico.txt", 'w')
        # verificando se o arquivo de saida do lexico existe
        if not os.path.exists(self.input):
            print("Arquivo de entrada não existe!\nRode o Analisador Lexico primeiro!\nThanks")
            self.output.write("Arquivo de entrada não existe!\nRode o Analisador Lexico primeiro!\nThanks")
            return

        # abrindo o arquivo que veio do lexico
        self.arquivo = open("resultado_lexico.txt", 'r')
        self.tokens = self.arquivo.readlines()
        self.arquivo.close()
        # para contar linha
        self.i = 0
        #self.j = 0
        self.linhaatual = ""
        self.tipoatual = ""
        self.simbolos = {}
        #self.quad = {}
        self.temp = 1

    def proxtoken(self):
        self.i += 1
        self.linhaatual = self.tokens[self.i][self.tokens[self.i].find('=>') + 2: -1]

    def qualtoken(self):
        return self.tokens[self.i][:self.tokens[self.i].find('=>')]

    def tipotoken(self):
        return self.tokens[self.i][self.tokens[self.i].find('_') + 1:self.tokens[self.i].find('=>')]

    # <programa> ::= program ident <corpo>
    def programa(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "tok400_program" in self.tokens[self.i]:
            self.proxtoken()
            if "token500" in self.tokens[self.i]:
                self.proxtoken()
                self.corpo()
                if "token110_." not in self.tokens[self.i]:
                    print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado '.' - linha: " +
                          self.linhaatual + "\n")
                    self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado '.' - linha: "
                                      + self.linhaatual + "\n")
                else:
                    self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: "
                      + self.linhaatual + "\n")
                self.output.write(
                    "Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: "
                    + self.linhaatual + "\n")
        else:
            print(
                "Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'program' - linha: " +
                self.linhaatual + "\n")
            self.output.write(
                "Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'program' - linha: " +
                self.linhaatual + "\n")

    # <corpo> ::= <dc> begin <comandos> end
    def corpo(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.dc()
        if "token408_begin" in self.tokens[self.i]:
            self.proxtoken()
            self.comandos()
            if "token409_end" in self.tokens[self.i]:
                self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                                  self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'begin' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'begin' - linha: " +
                              self.linhaatual + "\n")

    # <dc> ::= <dc_v> <dc_p>
    def dc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "token404_var" in self.tokens[self.i]:
            self.dc_v()

        if "token410_procedure" in self.tokens[self.i]:
            self.dc_p()

    # <dc_v> ::= var <variaveis> : <tipo_var> ; <dc_v> | λ
    def dc_v(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "token404_var" in self.tokens[self.i]:
            self.proxtoken()
            self.variaveis()
            if "token112_:" in self.tokens[self.i]:
                self.proxtoken()
                self.tipo_var()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':' - linha: " +
                                  self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'var' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'var' - linha: " +
                              self.linhaatual + "\n")

    # <tipo_var> ::= real | integer
    def tipo_var(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "token411_real" in self.tokens[self.i]:
            self.proxtoken()
        elif "token403_integer" in self.tokens[self.i]:
            self.proxtoken()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'real ou integer' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'real ou integer' - linha: "
                              + self.linhaatual + "\n")

    # <variaveis> ::= ident <mais_var>
    def variaveis(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token500" in self.tokens[self.i]:
            self.proxtoken()
            self.mais_var()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                              self.linhaatual + "\n")

    # <mais_var> ::= , <variaveis> | λ
    def mais_var(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token109_," in self.tokens[self.i]:
            self.proxtoken()
            self.variaveis()
        elif "token500" in self.tokens[self.i]:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ',' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ',' - linha: " +
                              self.linhaatual + "\n")

    # <dc_p> ::= procedure ident <parametros> ; <corpo_p> <dc_p> | λ
    def dc_p(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token410_procedure" in self.tokens[self.i]:
            self.proxtoken()
            if "token500" in self.tokens[self.i]:
                self.proxtoken()
                self.parametros()

                if "token111_;" in self.tokens[self.i]:
                    self.proxtoken()
                    self.corpo_p()
                    self.dc_p()
                else:
                    print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                          self.linhaatual + "\n")
                    self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                                      self.linhaatual + "\n")
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                      self.linhaatual + "\n")
                self.output.write(
                    "Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                    self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'procedure' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'procedure' - linha: " +
                              self.linhaatual + "\n")

    # <parametros> ::= ( <lista_par> ) | λ
    def parametros(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token07_(" in self.tokens[self.i]:
            self.proxtoken()
            self.lista_par()
            if "token08_)" in self.tokens[self.i]:
                self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                                  self.linhaatual + "\n")

    # <lista_par> ::= <variaveis> : <tipo_var> <mais_par>
    def lista_par(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.variaveis()
        if "token112_:" in self.tokens[self.i]:
            self.tipo_var()
            self.mais_par()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':' - linha: " +
                              self.linhaatual + "\n")

    # <mais_par> ::= ; <lista_par> | λ
    def mais_par(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token111_;" in self.tokens[self.i]:
            self.proxtoken()
            self.lista_par()

    # <corpo_p> ::= <dc_loc> begin <comandos> end ;
    def corpo_p(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.dc_loc()
        if "token408_begin" in self.tokens[self.i]:
            self.proxtoken()
            self.comandos()
            if "token409_end" in self.tokens[self.i]:
                self.proxtoken()
                if "token409_end" in self.tokens[self.i]:
                    self.proxtoken()
                else:
                    print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                          self.linhaatual + "\n")
                    self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                                      self.linhaatual + "\n")
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                    self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                    self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'begin' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'begin' - linha: " +
                              self.linhaatual + "\n")

    # <dc_loc> ::= <dc_v>
    def dc_loc(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token404_var" in self.tokens[self.i]:
            self.dc_v()

    # <lista_arg> ::= ( <argumentos> ) | λ
    def lista_arg(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token107_(" in self.tokens[self.i]:
            self.proxtoken()
            self.arguemntos()
            if "token108_)" in self.tokens[self.i]:
                self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                                  self.linhaatual + "\n")

    # <argumentos> ::= ident <mais_ident>
    def arguemntos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token500" in self.tokens[self.i]:
            self.proxtoken()
            self.mais_ident()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'identificador' - linha: " +
                              self.linhaatual + "\n")

    # <mais_ident> ::= ; <argumentos> | λ
    def mais_ident(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token111_;" in self.tokens[self.i]:
            self.proxtoken()
            self.arguemntos()

    # <pfalsa> ::= else <cmd> | λ
    def pfalsa(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token402_else" in self.tokens[self.i]:
            self.proxtoken()
            self.cmd()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'else' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'else' - linha: " +
                              self.linhaatual + "\n")

    # <comandos> ::= <cmd> ; <comandos> | λ
    def comandos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        self.cmd()
        if "token111_;" in self.tokens[self.i]:
            self.proxtoken()
            self.comandos()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ';' - linha: " +
                              self.linhaatual + "\n")

    # <cmd> ::= read ( <variaveis> ) |
    #           write ( <variaveis> ) |
    #           while <condicao> do <cmd> |
    #           if <condicao> then <cmd> <pfalsa> |
    #           ident := <expressao> |
    #           ident <lista_arg> |
    #           begin <comandos> end
    def cmd(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1

        if "token413_read" in self.tokens[self.i]:
            self.proxtoken()
            if "token107_(" in self.tokens[self.i]:
                self.proxtoken()
                self.variaveis()
                if "token108_)" in self.tokens[self.i]:
                    self.proxtoken()
                else:
                    print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                          self.linhaatual + "\n")
                    self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                                      self.linhaatual + "\n")
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado '(' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado '(' - linha: " +
                                  self.linhaatual + "\n")
        elif "token412_write" in self.tokens[self.i]:
            self.proxtoken()
            if "token107_(" in self.tokens[self.i]:
                self.proxtoken()
                self.variaveis()
                if "token108_)" in self.tokens[self.i]:
                    self.proxtoken()
                else:
                    print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                          self.linhaatual + "\n")
                    self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ')' - linha: " +
                                      self.linhaatual + "\n")
        elif "token406_while" in self.tokens[self.i]:
            self.proxtoken()
            self.condicao()
            if "token407_do" in self.tokens[self.i]:
                self.proxtoken()
                self.cmd()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'do' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'do' - linha: " +
                                  self.linhaatual + "\n")
        elif "token401_if" in self.tokens[self.i]:
            self.proxtoken()
            self.condicao()
            if "token405_then" in self.tokens[self.i]:
                self.proxtoken()
                self.cmd()
                self.pfalsa()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'then' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'then' - linha: " +
                                  self.linhaatual + "\n")
        elif "token500" in self.tokens[self.i]:
            self.proxtoken()
            if "token203_:=" in self.tokens[self.i]:
                self.expressao()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':=' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado ':=' - linha: " +
                                  self.linhaatual + "\n")
        elif "token500" in self.tokens[self.i]:
            self.lista_arg()
        elif "token408_begin" in self.tokens[self.i]:
            self.comandos()
            if "token409_end" in self.tokens[self.i]:
                self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                      self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() + "} esperado 'end' - linha: " +
                                  self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() +
                  "} esperado 'read' ou 'write' ou 'while' ou 'if' ou 'identificador' - linha: " +
                  self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                              "} esperado 'read' ou 'write' ou 'while' ou 'if' ou 'identificador' - linha: " +
                              self.linhaatual + "\n")

    # <condicao> ::= <expressao> <relacao> <expressao>
    def condicao(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.expressao()
        self.relacao()
        self.expressao()

    # <relacao> ::= = | <> | >= | <= | > | <
    def relacao(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token104_=" in self.tokens[self.i]:
            self.proxtoken()
        elif "token200_<>" in self.tokens[self.i]:
            self.proxtoken()
        elif "token201_>=" in self.tokens[self.i]:
            self.proxtoken()
        elif "token202_<=" in self.tokens[self.i]:
            self.proxtoken()
        elif "token105_>" in self.tokens[self.i]:
            self.proxtoken()
        elif "token106_<" in self.tokens[self.i]:
            self.proxtoken()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() +
                  "} esperado '= | <> | >= | <= | > | <' - linha: " + self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                              "} esperado '= | <> | >= | <= | > | <' - linha: " + self.linhaatual + "\n")

    # <expressao> ::= <termo> <outros_termos>
    def expressao(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.termo()
        self.outros_termos()

    # <op_un> ::= + | - | λ
    def op_un(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token100_+" in self.tokens[self.i]:
            self.proxtoken()
        elif "token101_-" in self.tokens[self.i]:
            self.proxtoken()

    # <outros_termos> ::= <op_ad> <termo> <outros_termos> | λ
    def outros_termos(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if ("token100" or "token101") in self.tokens[self.i]:
            self.op_ad()
            self.termo()
            self.outros_termos()

    # <op_ad> ::= + | -
    def op_ad(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token100_+" in self.tokens[self.i]:
            self.proxtoken()
        elif "token101_-" in self.tokens[self.i]:
            self.proxtoken()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() +
                  "} esperado operador '+' ou '-' - linha: " + self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                              "} esperado operador '+' ou '-' - linha: " + self.linhaatual + "\n")

    # <termo> ::= <op_un> <fator> <mais_fatores>
    def termo(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        self.op_un()
        self.fator()
        self.mais_fatores()

    # <mais_fatores> ::= <op_mul> <fator> <mais_fatores> | λ
    def mais_fatores(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if ("token102" or "token103") in self.tokens[self.i]:
            self.op_mul()
            self.fator()
            self.mais_fatores()

    # <op_mul> ::= * | /
    def op_mul(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token102_*" in self.tokens[self.i]:
            self.proxtoken()
        elif "token103_/" in self.tokens[self.i]:
            self.proxtoken()
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() +
                  "} esperado operador '*' ou '/' - linha: " + self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                              "} esperado operador '*' ou '/' - linha: " + self.linhaatual + "\n")

    # <fator> ::= ident | numero_int | numero_real | ( <expressao> )
    def fator(self):
        if "Erro Lexico" in self.tokens[self.i]:
            self.i += 1
        if "token500" in self.tokens[self.i]:
            self.proxtoken()
        elif "token300" in self.tokens[self.i]:
            self.proxtoken()
        elif "token301" in self.tokens[self.i]:
            self.proxtoken()
        elif "token107_(" in self.tokens[self.i]:
            self.proxtoken()
            self.expressao()
            if "token108_)" in self.tokens[self.i]:
                self.proxtoken()
            else:
                print("Erro sintatico - Erro em {" + self.tipotoken() +
                      "} esperado ')' - linha: " + self.linhaatual + "\n")
                self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                                  "} esperado ')' - linha: " + self.linhaatual + "\n")
        else:
            print("Erro sintatico - Erro em {" + self.tipotoken() +
                  "} esperado 'ident | numero_int | numero_real' - linha: " + self.linhaatual + "\n")
            self.output.write("Erro sintatico - Erro em {" + self.tipotoken() +
                              "} esperado 'ident | numero_int | numero_real' - linha: " + self.linhaatual + "\n")
