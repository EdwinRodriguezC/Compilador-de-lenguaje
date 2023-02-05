ERR = -1
ACP = 999
idx = 0
entrada = ''
noErr = True
arche = ''
archs = ''
nRen=1
nCol=0
pc = 1
cEq = 1
ambito = ''

codigo = []
tabSim = []

class oPrgm:
    def __init__(self, nomb, clas, tipo, dim1, dim2):
        self.nomb = nomb
        self.clas = clas
        self.tipo = tipo
        self.dim1 = dim1
        self.dim2 = dim2

def buscarObjeto(iden): 
    for x in tabSim: 
        if x.nom == iden:
            return x
    return None

def genOprgm(nomb, clas, tipo, dim1, dim2):
    global oPrgm, tamSim
    v = oPrgm(nomb, clas, tipo, dim1, dim2)
    tabSim.append(v)


class code:
    def __init__(self, nemo, dir1, dir2):
        self.nemo = nemo
        self.dir1 = dir1
        self.dir2 = dir2

def genCod(nemo, dir1, dir2):
    global code, codigo, pc
    x = code(nemo, dir1, dir2)
    codigo.append(x)
    pc += 1

matran=[
    #0      1       2   3    4    5    6    7   8   9   10  11  12
    #letra  digito  _   .    -    Del  OpA  =   !   <,> DeU "   /
    [5,     2,      5,  ERR, 1,   12,  11,  8,  9,  6,  0,  13, 15], #0
    [ACP,   2,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #1 OpA -
    [ACP,   2,      ACP,3,   ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #2
    [ERR,   4,      ERR,ERR, ERR, ERR, ERR, ERR,ERR,ERR,ERR,ACP], #3
    [ACP,   4,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #4
    [5,     5,      5,  ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #5
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 7,  ACP,ACP,ACP,ACP], #6
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #7
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 10, ACP,ACP,ACP,ACP], #8
    [ERR,   ERR,    ERR,ERR, ERR, ERR, ERR, 10, ERR,ERR, ERR,ERR], #9
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #10
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #11  OpA
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #12  Del
    [13,    13,     13, 13,  13,  13,  13,  13, 13, 13, 13, 14 ], #13  Del
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #14  Del
]
palRes = ['if', 'else', 'lee', 'imprime', 'imprimenl', 'verdadero', 
          'falso', 'entero', 'logico', 'decimal', 'palabra',
          'desde', 'mientras', 'si', 'sino', 'haz', 
          'hasta', 'que', 'y', 'o', 'no', 'nulo', 'regresa']

def esReservada(lex):
    global palRes
    for x in palRes:
        if x == lex: return True
    
    return False

def error(c, des):
    global ERR, noErr
    cl = nCol - 1
    rn = nRen
    if cl < 1: 
        cl = 1
        rn = nRen - 1
    print('['+str(rn)+', '+str(cl)+ ']', c, des)
    noErr = False
    return ERR

def colCar( x ):
    if (ord(x) >= 65 and ord(x) <= 90) or \
       (ord(x) >= 97 and ord(x) <= 122): return 0 
    if (ord(x) >= 48 and ord(x) <= 57): return 1
    if x == '_': return 2
    if x == '.': return 3
    if x == '-': return 4
    if x == '{' or x == '}' or x == '(' or x == ')' or \
       x == '[' or x == ']' or x == ';' or x == ',' or \
       x == ':': return 5  #delimitador
    if x == '+' or x == '*' or x == '/' or \
       x == '^' or x == '%': return 6
    if x == '=': return 7
    if x == '!': return 8
    if x == '<' or x == '>': return 9
    if x == ' ' or x == '\t' or x == '\n': return 10
    if x == '"': return 11
    else: return error(x, 'Simbolo Ilegal NO válido en Lenguaje')

def scanner():
    global entrada, ERR, idx, matran, nCol, nRen
    estado = 0
    lexema = ''
    token = ''
    estAnt = 0
    while estado != ERR and idx < len(entrada):
        c = entrada[idx]
        idx += 1
        nCol = nCol + 1
        if c == '\n': 
           nRen = nRen + 1
           nCol = 1
        col = colCar( c )
        if col >=0 and col <=11:
            estAnt = estado
            if estado != ERR and estado != ACP:
                estado = matran[estado][col]
            if estado != ERR and estado != ACP and \
                col != 10 or estado == 13:
                lexema += str(c)
            elif estado == ACP:
                if col != 10: idx -= 1
                break
        else: estado = ERR
    if estado != ACP and estado != ERR: estAnt = estado
    #Verifica Token
    if estAnt == 2: token='Ent'
    elif estAnt == 3 or estAnt == 9: error(lexema, 'Error Léxico')
    elif estAnt == 4: token = 'Dec'
    elif estAnt == 5:
        token = 'Ide'
        if esReservada(lexema): token = 'Res'
        if lexema == 'y' or lexema == 'o' or \
           lexema == 'no': token = 'OpL'
        elif lexema == 'verdadero' or lexema == 'falso': token='CtL' 
    elif estAnt == 6 or estAnt == 7 or estAnt == 10: token='OpR'
    elif estAnt == 8: token = 'OpS'
    elif estAnt == 1 or estAnt == 11: token = 'OpA'
    elif estAnt == 12: token = 'Del'
    elif estAnt == 14: token = 'Cad'

    return token, lexema

def encvarsfuncs():
    global tok, lex, ambito, pc, nVar, tPo
    if lex != 'nulo' and lex != 'entero' and \
       lex != 'decimal' and lex != 'logico'and \
       lex != 'palabra':
       error('Error de Sintaxis', 'Se esperaba tipo y llegó '+ lex)
    if lex == 'nulo': tPo = 'I'
    elif lex == 'entero': tPo='E'
    elif lex == 'decimal': tPo='D'
    elif lex == 'palabra': tPo='P'
    elif lex == 'logico': tPo='L'
    tok, lex = scanner()
    if tok == 'Ide': 
        ambito = lex
        nVar = lex
        if lex == 'principal':
            genOprgm('_P', 'I', 'I', str(pc), '0')
        else:
            genOprgm(lex, 'F', tPo, str(pc), '0')
    if tok != 'Ide':
            error('Error de Sintaxis', 'Se esperaba <Ide>, y llegó '+ lex)    
    tok, lex = scanner()

def tipo(): 
    global tok, lex, pc, ambito, tpo
    if lex != 'entero' and lex != 'palabra' and \
       lex != 'decimal' and lex != 'nulo' and lex != 'logico':
       error('Error de Sintaxis', 'se esperaba <tipo> y llegó '+lex) 
    if lex == 'entero': tpo = 'E'
    elif lex == 'decimal': tpo = 'D'
    elif lex == 'palabra': tpo = 'P'
    elif lex == 'logico': tpo = 'L'

    tok, lex = scanner()

def dparams(): 
    global tok, lex, ambito, pc, tpo
    tipo()
    if tok != 'Ide': error('Error de Sintáxis', 'se esperaba Ide y llegó '+tok)
    else: 
        ide = lex + '&' + ambito
        genOprgm(ide,'R', tpo, '0', '0')
        genCod('STO', '0', ide)
    tok, lex = scanner()
    if lex == ',': 
        tok, lex = scanner()
        dparams()

    
def udim(): pass

def cte(): 
    global ambito, pc, tok, lex
    if tok == 'Ent' or tok == 'Dec' or tok == 'Cad' or \
       tok == 'Ctl': 
       genCod('LIT', lex, '0')
    else:
        error('Error de Sintaxis', 'se esperaba cte lógica, entera, decimal o cadena y llegó ' + lex)

def uparams():
    global tok, lex, pc, ambito
    expr()
    if lex == ',': 
        tok, lex = scanner()
        uparams()

def termino():
    global pc, tok, lex, ambito
    if lex == '(':
        expr()
        if lex != ')':
           error('Erorr de Sintaxis', 'se esperaba ) y llegó '+lex)
        tok, lex = scanner()
    elif tok == 'Ide':
        ide = lex
        tok, lex = scanner()
        if lex == '[': udim()
        if lex == '(': 
            etq = '_E'+ str(cEq)
            cEq += 1
            genCod('LOD', etq, '0')
            uparams()
            tok, lex = scanner()
            if lex != ')': 
                error('Error de Sintáxis se esperaba ) y llegó '+lex)
            genCod('CAL', ide, '0')
            genOprgm(etq, 'I', 'I', str(pc), '0')
        else: ide=ide+'&'+ambito
        genCod('LOD', ide, '0')
    else: 
        cte()
        tok, lex = scanner()

def signo(): 
    global tok, lex
    if lex == '-':
        tok, lex = scanner()
    termino()

def expo(): 
    global tok, lex, tFe 
    opr = '^'
    while opr == '^':
        signo()
        opr = lex
        if opr == '^':
            tok, lex = scanner()

def multi(): 
    global tok, lex
    opr = '*'
    while opr == '*' or opr == '/':
        expo()
        opr = lex
        if opr == '*' or opr == '/':
            tok, lex = scanner()

def expr():
    global tok, lex
    opr = '+'
    while opr == '+' or opr == '-':
        multi()
        opr = lex
        if opr == '+' or opr == '-':
            tok, lex = scanner()


def asigna(): 
    global tok, lex, nVar, ambito
    nObj = nVar+ambito
    o = buscarObjeto(nVar)
    if o == None: 
        o = buscarObjeto(nObj)
    if o == None:
        error('Error de Semántica', 'la variable '+nVar+' no ha sido declarada')
    tok, lex = scanner()
    if lex == '[': udim()
    if lex != '=': 
        error('Error de Sintaxis', 'Se esperaba = y llegó ' + lex)
    tok, lex = scanner()
    expr()
  
def si(): 
    global tok, lex, nVar, ndim, tFe
    tok, lex = scanner()
    if lex != '(': 
        error("Error de Sintaxis", 'se esperaba ( y llegó ' + lex )
    tok, lex = scanner()
    expr()
    if tPo == 'E': tpd = 'Entero'
    if tPo == 'C': tpd = 'Cadena'
    if tPo == 'D': tpd = 'Decimal'
    if tPo == 'L': tpd = 'Logico'
    if tPo == 'E': tpr = 'Entero'
    if tPo == 'C': tpr = 'Cadena'
    if tPo == 'D': tpr = 'Decimal'
    if tPo == 'L': tpr = 'Logico'
    if tPo != tFe:
        error("Error de Sintaxis", 'se esperaba ) y llegó ' + lex )

def lFunc():
    global tok, lex, pc, ambito, nFunc, cEq
    etq = '_E' + str(cEq)
    cEq += 1
    genCod('LOD', etq, '0')
    uparams()
    if lex != ')':
        error('Error de Sintaxis', 'se esperaba ) y llegó '+lex)
    genCod('CAL', nFunc, '0')
    genOprgm(etq, 'I', 'I', str(pc), '0')


def imprime():
    global tok, lex, ambito
    tok, lex = scanner()
    if lex != '(':
        error('Error de sintáxis', 'se esperaba ( y llegó '+ lex)
    tok, lex = scanner()
    sep = ','
    while sep == ',':
        expr()
        if lex == ',':
            genCod('OPR', '0', '20')
            sep = lex
            tok, lex = scanner()
        else: sep = lex

    if lex != ')':
        error('Error de Sintáxis', 'se esperaba ) y llegó '+lex)
    else: 
        genCod('OPR', '0', '20')

def imprimenl():
    global tok, lex, ambito
    tok, lex = scanner()
    if lex != '(':
        error('Error de sintáxis', 'se esperaba ( y llegó '+ lex)
    tok, lex = scanner()
    sep = ','
    while sep == ',':
        expr()
        if lex == ',':
            genCod('OPR', '0', '20')
            sep = lex
            tok, lex = scanner()
        else: sep = lex

    if lex != ')':
        error('Error de Sintáxis', 'se esperaba ) y llegó '+lex)
    else: 
        genCod('OPR', '0', '21')

def lee():
    global lex, tok
    tok, lex = scanner()
    if lex != '(':
        error('Error de Sintáxis', 'se esperaba ( y llegó '+lex)
    tok, lex = scanner()
    if tok != 'Ide': 
        error('Error de Sintáxis', 'se esperaba <ide> y llegó '+ tok)
    ide = lex+'&'+ambito
    genOprgm(ide, 'V', 'P', '0', '0')
    genCod('OPR', ide, '19')
    tok, lex = scanner()
    if lex != ')':
        error('Error de Sintáxis', 'se esperaba ) y llegó '+lex)

def comando(): 
    global tok, lex, pc, ambito, nFunc, nVar
    if tok == 'Ide': 
        nFunc = lex
        nVar = lex
        #antAmb = ambito
        #ambito = lex
        tok, lex = scanner()
        if lex == '(':
            tok, lex = scanner()
            lFunc()
        else: asigna()
    if lex == 'si': si()
    if lex == 'imprime': imprime()
    if lex == 'imprimenl': imprimenl()
    if lex == 'lee': lee()


def estatutos(): 
    global tok, lex, ambito, pc
    while lex != '}':
        if lex != ';': 
            comando()
            tok, lex = scanner()
        if lex != ';': 
            error('Error de Sintaxis', 'Se esperaba <;> y llegó '+ lex)
        tok, lex = scanner()

def dfunc():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    if lex != ')': dparams()
    tok, lex = scanner()
    if lex != '{':
        error('Error Sintáxis', 'Se esperaba "{", y llegó '+lex)
    tok, lex = scanner()
    if lex != '}': estatutos()
    if lex == '}':
        if ambito == 'principal': genCod('OPR', '0', '0')
        elif ambito != '': genCod('OPR', '0', '1')
    else: 
        error('Error de Sintáxis', 'Se espera "}" en función y llegó ' +lex)

def dimens():
    global tok, lex, ambito, nVar, tPo
    conD = 1
    conV = 1
    while lex == '[':
        tok, lex = scanner()
        if conD == 1: dim1 = lex
        elif conD == 2: 
            dim2 = lex
            genOprgm(nVar, 'V', )
        cte()
        tok, lex = scanner
        if lex != '[': error('Error de Sintáxis', 'se esperaba ] y llego ' +lex)
        tok, lex = scanner()

def gCtes():
    global tok, lex
    tok, lex = scanner()
    if lex == '{':
        deli = ','
        while deli == ',':
            tok, lex = scanner()
            cte()
            tok, lex = scanner()
            deli = lex
        if lex != '}': error('Error de Sintáxis', 'se esperaba <}> y llego ' +lex)
    else: cte()


def dvars(): 
    global tok, lex, ambito, nVar, tPo, dim1, dim2
    dim1 = '0'
    dim2 = '0'
    if lex == '[': dimens()
    elif lex == '=': 
        gCtes()
    elif lex == ',': 
        tok, lex = scanner()
        return
    elif lex == ',':
        genOprgm(nVar, 'V', tPo, dim1, dim2)
        tok, lex == scanner()
        if tok != 'Ide': error('Error de Sintáxis', 'se esperaba <Ide> y llego '+tok)
        nVar = lex
        dvars()
    else: 
        error('Error de sintaxis', 'se esperaba <[, =, , ó ; y encontro '+lex)
def prgm():
    global tok, lex, idx, ambito, pc
    tok, lex = scanner()
    while (lex == 'nulo' or lex == 'entero' or \
          lex == 'decimal' or lex == 'logico'or \
          lex == 'palabra') and \
          idx < len(entrada):
            encvarsfuncs()
            if lex == '(':
                dfunc()
            else: 
                ambito = ''
                dvars()
            tok, lex = scanner()
            if tok != 'Ide': error('Error de sitanxis', 'se esperaba <Ide> y llego '+tok)

        
          
def parser():
    global noErr, arche, codigo, pc, tabSim, archs
    prgm()
    if noErr:
        print('El archivo['+arche+'] Compiló SIN errores')
        #Impresion de Tambim y Codigo PL0
        aSal=''    
        for x in tabSim:
           aSal += x.nomb+',' + x.clas+',' + x.tipo+',' + x.dim1+',' + x.dim2+',#,\n'
        aSal += '@\n'
        cCod = 1
        for x in codigo:
           aSal += str(cCod) + ' ' + x.nemo + ' '+ x.dir1 +', ' + x.dir2 + '\n'
           if cCod == pc: break
           cCod += 1

        print(aSal)
        with open(archs, 'w') as salida:
            salida.write(aSal)
            salida.close()

if __name__ == '__main__':
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    archivo = open(arche, 'r')
    entrada = ''
    archs = arche[0:len(arche)-3]
    archs += 'eje'

    for linea in archivo:
        entrada += linea

    parser()
