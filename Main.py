from Lexico import Lexico
from Sintatico import Sintatico
entrada = "entrada.txt"
print("entrada.txt\n")
lex = Lexico(entrada)
lex.lexanalise()
print("analise lexica feita\n")
sint = Sintatico()
sint.programa()
sint.output.close()
print("analise sintatica pronta!\n")
