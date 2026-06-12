import csv
import sqlite3
import os
from pathlib import Path
from datetime import datetime

current_dir = Path(__file__).parent.absolute()
os.chdir(current_dir)

def loginAdmin(usuario:dict):#Em progresso, falta implementar sistema de resposta de mensagens
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    while True:
        print("\n-----Menu de Administrador-----\n" \
            "Selecione uma opção:\n" \
            "1 - Exibir dados\n" \
            "2 - Deletar instância\n" \
            "3 - Ressetar dados\n" \
            "4 - Apagar mensagens")
        
        try:
            op = int(input("0 - Sair:"))
        except:
            continue
        match op:
            case 1:
                while True:
                    print("\nSelecione um tipo de registro a ser exibido:\n" \
                    "1 - Usuarios\n" \
                    "2 - Transações\n" \
                    "3 - Cocos\n" \
                    "4 - Créditos de carbono")
                    try:
                        op = int(input("0 - Voltar:"))
                    except:
                        print("Opção invalida!")
                        continue
                    match op:
                        case 0:
                            break
                        case 1:
                            showUsuario()
                            continue
                        case 2:
                            showTransacao()
                            continue
                        case 3:
                            showCoco()
                            continue
                        case 4:
                            showCreditoDeCarbono()
                            continue
                        case 0:
                            break
                        case _:
                            print("Opção invalida!")
                            continue
            case 2:
                while True:
                    print("\nSelecione uma tabela do banco de dados:\n" \
                        "1 - Usuario\n" \
                        "2 - Transação\n" \
                        "3 - Coco\n" \
                        "4 - Crédito de carbono\n" \
                        "0 - Voltar")
                    try:
                        op = int(input("Selecione uma opção:"))
                    except:
                        print("Opção inválida!")
                        continue
                    match op:
                        case 1:
                            while True:
                                try:
                                    registro = input("\nDigite 0 para voltar!\n" \
                                        "Informe a id do registro que deseja apagar:")
                                except:
                                    print("Opção inválida!")
                                    continue
                                if validaIdUsuario(registro) == True:
                                    break
                                else:
                                    print("Id informada não pertence a nenhum usuario.\n")
                                    continue
                            usuario = getUsuario(registro)
                            deleteUsuario(usuario["email"],usuario["senha"])
                            print("Usuário deletado com sucesso.\n")
                            del usuario
                            del registro
                            continue
                        case 2:#Transacao, Em desenvolvimento
                            while True:
                                try:
                                    registro = input("\nDigite 0 para voltar!\n" \
                                        "Informe a id do registro que deseja apagar:")
                                except:
                                    print("Opção inválida!")
                                    continue
                                if validaIdTransacao(registro) == True:
                                    break
                                else:
                                    print("Id informada não pertence a nenhuma transação.\n")
                                    continue
                            deleteTransacao(registro)
                            print("Transação deletada com sucesso.\n")
                            del registro
                            continue
                        case 3:
                            while True:
                                try:
                                    registro = input("\nDigite 0 para voltar!\n" \
                                        "Informe a id do registro que deseja apagar:")
                                except:
                                    print("Opção inválida!")
                                    continue
                                if validaIdCoco(registro) == True:
                                    break
                                else:
                                    print("Id informada não pertence a nenhuma transação.\n")
                                    continue
                            deleteCoco(registro)
                            print("Transação deletada com sucesso.\n")
                            del registro
                            continue
                        case  4:
                            while True:
                                try:
                                    registro = input("\nDigite 0 para voltar!\n" \
                                        "Informe a id do registro que deseja apagar:")
                                except:
                                    print("Opção inválida!")
                                    continue
                                if validaIdCreditoDeCarbono(registro) == True:
                                    break
                                else:
                                    print("Id informada não pertence a nenhuma transação.\n")
                                    continue
                            deleteCreditoDeCarbono(registro)
                            print("Transação deletada com sucesso.\n")
                            del registro
                            continue
                        case 0:
                            break
                        case _:
                            print("Numero inválido!")
                            continue
            case 3:
                resetUsuario()
                resetTransacao()
                resetCoco()
                resetCreditoDeCarbono()
                print("\nTodas as tabelas foram resetadas com sucesso!")
                continue
            case 4:#Criar tabela de mensagens, e desenvolver um método de interação!
                resetMensagens()
                pass
            case 0:
                break
            case _:
                print("Opção invalida!")
                continue
            

    cursor.close()
    db.close()

def validaIdUsuario(id:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id,)
    cursor.execute("SELECT id FROM usuario WHERE id= ?",id)
    validador = cursor.fetchone()
    cursor.close()
    db.close()
    if validador == None:
        return False
    else:
        return True
    
def validaIdTransacao(id_transacao:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id_transacao,)
    cursor.execute("SELECT id_transacao FROM transacao WHERE id_transacao= ?",id)
    validador = cursor.fetchone()
    cursor.close()
    db.close()
    if validador == None:
        return False
    else:
        return True

def validaIdCoco(id_produto:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id_produto,)
    cursor.execute("SELECT id_produto FROM coco WHERE id_produto= ?",id)
    validador = cursor.fetchone()
    cursor.close()
    db.close()
    if validador == None:
        return False
    else:
        return True

def validaIdCreditoDeCarbono(id_produto:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id_produto,)
    cursor.execute("SELECT id_produto FROM credito_de_carbono WHERE id_produto= ?",id)
    validador = cursor.fetchone()
    cursor.close()
    db.close()
    if validador == None:
        return False
    else:
        return True

def resetCreditoDeCarbono():
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        credito = csv.reader(open('credito_de_carbono.csv','r',newline=''))
        next(credito)
        db.execute('DELETE FROM credito_de_carbono')
        #db.execute("""CREATE TABLE credito_de_carbono(id_produto INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,tonelada_de_carbono INTEGER,preco REAL,data TEXT, FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")
        db.commit()
        cursor.executemany("INSERT INTO credito_de_carbono VALUES(?,?,?,?,?)", credito)
        db.commit()
    except sqlite3.OperationalError:
        db.execute("""CREATE TABLE credito_de_carbono(id_produto INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,tonelada_de_carbono INTEGER,preco REAL,data TEXT, FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")
        db.commit()
        cursor.executemany("INSERT INTO credito_de_carbono VALUES(?,?,?,?,?)", credito)
        db.commit()
    finally:
        cursor.close()
        db.close()

def resetCoco():
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        coco = csv.reader(open('coco.csv','r',newline=''))
        next(coco)
        cursor.execute('DELETE FROM coco')
        db.commit()
        cursor.executemany("INSERT INTO coco VALUES(?,?,?,?)", coco)
        db.commit()
    except sqlite3.OperationalError:
        db.execute("""CREATE TABLE coco(id_produto INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,peso_kg REAL,data TEXT, FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")
        db.commit
        cursor.executemany("INSERT INTO coco VALUES(?,?,?,?)", coco)
        db.commit()
    finally:
        cursor.close()
        db.close()

def resetMensagens():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    db.execute("DELETE FROM mensagem")
    db.commit()
    cursor.close()
    db.close()

def resetUsuario():
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        usuario = csv.reader(open('empresas_ficticias.csv',newline=''))
        next(usuario)
        cursor.execute("DELETE FROM usuario")
        db.commit()
        cursor.executemany("INSERT INTO usuario VALUES(?,?,?,?,?,?,?,?)",usuario)
        db.commit()
    except sqlite3.OperationalError:
        db.execute('''CREATE TABLE usuario(id INTEGER NOT NULL PRIMARY KEY,cnpj TEXT,email TEXT,telefone TEXT,cep TEXT,endereço TEXT,tipo_de_usuário TEXT,senha TEXT) ''')
        db.commit()
        cursor.executemany("INSERT INTO usuario VALUES(?,?,?,?,?,?,?,?)",usuario)
        db.commit()
    finally:
        cursor.close()
        db.close()

def resetTransacao():
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        transacoes_ficticias = csv.reader(open('transacoes_ficticias.csv',newline=''))
        next(transacoes_ficticias)
        cursor.execute('DELETE FROM transacao')
        #db.execute("""CREATE TABLE transacao(id_transacao INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,id_comprador TEXT,tipo TEXT,valor TEXT,data TEXT,FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")
        db.commit()
        cursor.executemany("INSERT INTO transacao VALUES(?,?,?,?,?,?)", transacoes_ficticias)
        db.commit()
    except sqlite3.OperationalError:
        db.execute("""CREATE TABLE transacao(id_transacao INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,id_comprador INTEGER NOT NULL,tipo TEXT,valor TEXT,data TEXT,FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")
        db.commit()
        cursor.executemany("INSERT INTO transacao VALUES(?,?,?,?,?,?)", transacoes_ficticias)
        db.commit()
    finally:
        cursor.close()
        db.close()    

def getTables():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    print(cursor.fetchall())
    cursor.close()
    db.close()

def showCoco():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM coco''')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    db.close()

def showUsuario():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM usuario''')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    db.close()

def showTransacao():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM transacao''')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    db.close()

def showCreditoDeCarbono(): #Exibe todas as ofertas de crédito de carbono
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM credito_de_carbono''')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    db.close()

def addUsuario(email, senha):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    #acha uma id de usuario que ainda não foi utilizada
    cursor.execute("SELECT * FROM usuario")
    newId = len(cursor.fetchall()) 
    while True:
        query = 'SELECT email FROM usuario WHERE id=' + str(newId)
        cursor.execute(query)
        if cursor.fetchone() == None:
            break
        else:
            newId += 1
    input = "INSERT INTO usuario (id,email,senha) VALUES(?,?,?)"
    usuario = (newId,email,senha)
    db.execute(input,usuario)
    db.commit()
    cursor.close()
    db.close()

def addTransacao(id_vendedor,id_comprador,tipo,valor,data):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    

    cursor.execute("SELECT * FROM transacao")
    newId = len(cursor.fetchall()) 
    while True:
        query = 'SELECT id_transacao FROM transacao WHERE id_transacao=' + str(newId)
        cursor.execute(query)
        if cursor.fetchone() == None:
            break
        else:
            newId += 1

    query = "INSERT INTO transacao VALUES(?,?,?,?,?,?)"
    transacao = (newId,id_vendedor,id_comprador,tipo,valor,data)
    db.execute(query,transacao)
    db.commit()

    cursor.close()
    db.close()

def addCoco(id_vendedor,peso_kg,data):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    #cria uma id que ainda não está em uso
    cursor.execute("SELECT * FROM coco")
    newId = len(cursor.fetchall()) 
    while True:
        query = 'SELECT id_produto FROM coco WHERE id_produto=' + str(newId)
        cursor.execute(query)
        if cursor.fetchone() == None:
            break
        else:
            newId += 1

    coco = (newId,id_vendedor,peso_kg,data)
    query = "INSERT INTO coco VALUES (?,?,?,?)"
    db.execute(query,coco)
    db.commit()
    cursor.close()
    db.close()

def addCreditoDeCarbono(id_vendedor:int,tonelada_de_carbono:int,preço:float,data:str):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    #cria uma id que ainda não está em uso
    cursor.execute("SELECT * FROM credito_de_carbono")
    newId = len(cursor.fetchall()) 
    while True:
        query = 'SELECT id_produto FROM credito_de_carbono WHERE id_produto=' + str(newId)
        cursor.execute(query)
        if cursor.fetchone() == None:
            break
        else:
            newId += 1

    coco = (newId,id_vendedor,tonelada_de_carbono,preço,data)
    query = "INSERT INTO credito_de_carbono VALUES (?,?,?,?,?)"
    db.execute(query,coco)
    db.commit()
    cursor.close()
    db.close()

def deleteUsuario(email,senha):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    query = "DELETE FROM usuario WHERE email=? AND senha=?"
    usuario = (email,senha)
    db.execute(query,usuario)
    db.commit()
    cursor.close()
    db.close()

def deleteTransacao(id_transacao):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    #Cria uma tupla com a id_transacao e uma query, para combinar os 2 no execute
    transacao = (id_transacao,)
    query = "DELETE FROM transacao WHERE id_transacao=?"
    db.execute(query,transacao)
    db.commit()
    cursor.close()
    db.close()

def deleteCoco(id_produto):
    db = sqlite3.connect('database.db')
    produto = (id_produto,)
    query = "DELETE FROM coco WHERE id_produto=?"
    db.execute(query,produto)
    db.commit()
    db.close

def deleteCreditoDeCarbono(id_produto):
    db = sqlite3.connect("database.db")
    query = "DELETE FROM credito_de_carbono WHERE id_produto=?"
    produto = (id_produto,)
    db.execute(query,produto)
    db.commit()
    db.close

def updateUsuario(usuario:dict):
    db = sqlite3.connect('database.db')
    db.execute("UPDATE usuario SET cnpj= :cnpj,email = :email, telefone= :telefone,cep= :cep,endereço= :endereço,tipo_de_usuário= :tipo_de_usuário,senha= :senha WHERE id= :id",usuario)
    db.commit()
    db.close()

def getCoco(id:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id,)
    cursor.execute("SELECT * FROM coco WHERE id_produto=?",id)
    t = cursor.fetchone()
    if t == None:
        return {}
    coco = {"id_produto": t[0],
            "id_vendedor": t[1],
            "peso_kg": t[2],
            "data": t[3]}
    cursor.close()
    db.close()
    return coco

def getCreditoDeCarbono(id_produto):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id_produto = (id_produto,)
    cursor.execute("SELECT * FROM credito_de_carbono WHERE id_produto=?",id_produto)
    info = cursor.fetchone()
    if info == None:
        return {}
    creditoDeCarbono = {"id_produto": info[0],
        "id_vendedor": info[1],
        "tonelada_de_carbono":info[2],
        "preco":info[3],
        "data":info[4]}
    return creditoDeCarbono

def getUsuario(id:int):
    '''Retorna um dicionario com as informações do usuario'''
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id = (id,)
    cursor.execute("SELECT * FROM usuario WHERE id=?",id)
    t = cursor.fetchone()
    if t == None:
        return None
    usuario = {"id":t[0],
               "cnpj":t[1],
               "email":t[2],
               "telefone":t[3],
               "cep":t[4],
               "endereço":t[5],
               "tipo_de_usuário":t[6],
               "senha":t[7]}
    cursor.close()
    db.close()
    return usuario

def getLogin(email:str,senha:str):
    '''Retorna um dicionário com os dados do usuario com base no email e senha'''
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    login = (email,senha)
    cursor.execute("SELECT * FROM usuario WHERE email=? AND senha=?",login)
    t = cursor.fetchone()
    if t == None:
        return None
    usuario = {"id":t[0],
               "cnpj":t[1],
               "email":t[2],
               "telefone":t[3],
               "cep":t[4],
               "endereço":t[5],
               "tipo_de_usuário":t[6],
               "senha":t[7]}
    cursor.close()
    db.close()
    return usuario

def exibirChat(id_chat):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    id_chat = (id_chat,)
    cursor.execute("Select * FROM mensagem WHERE id_chat = ? ORDER BY data LIMIT 10",id_chat)
    for row in cursor.fetchall():
        usuario = getUsuario(row[2])
        print(usuario["email"],": ",row[4])
    cursor.close()
    db.close()

def getMensagensDefault(): #Mensagens que aparecem no menu de suporte!
    mensagens = ["1 - Entre em contato com a equipe CocoCarbon!",
                "2 - Deseja marcar uma coleta/entrega de materiais?",
                "3 - Tem alguma dúvida sobre o app? Fale com nossa assistênte virtual!",
                "4 - Quer fazer uma solicitação? Envie uma mensagem para nossa equipe de suporte!\n"
                "5 - Busca atendimento direto com nosso operador? Temos uma equipe disponível para assistência"]
    return mensagens

def menuNovasMensagens(usuario:dict): #Exibe um menu com mensagens prontas para serem mandadas para a equipe de suporte.
    mensagens = getMensagensDefault()
    print("Selecione uma das mensagens a seguir:")
    for row in mensagens:
        print(row)
    while True:
        try:
            op = int(input("Digite 0 para voltar.\n" \
                "Selecione uma opção:"))
        except:
            print("Selecione uma opção válida.")
            continue
        match op:
            case 1:
                mensagem = {'id_usuario':usuario["id"],'id_sender':usuario["id"],'id_chat':None,'mensagem':"Olá! Pode me ajudar?"}
                addMensagem(mensagem)
                del mensagem
                break
            case 2:
                mensagem = {'id_usuario':usuario["id"],'id_sender':usuario["id"],'id_chat':None,'mensagem':"Poderia me ajuda em marcar uma coleta/entrega de materiais?"}
                addMensagem(mensagem)
                del mensagem
                break
            case 3:
                mensagem = {'id_usuario':usuario["id"],'id_sender':usuario["id"],'id_chat':None,'mensagem': "Olá, poderia me tirar uma dúvida?"}
                addMensagem(mensagem)
                del mensagem
                break
            case 4:
                mensagem = {'id_usuario':usuario["id"],'id_sender':usuario["id"],'id_chat':None,'mensagem':"Gostaria de fazer uma solicitação!"}
                addMensagem(mensagem)
                del mensagem
                break
            case 5:
                mensagem = {'id_usuario':usuario["id"],'id_sender':usuario["id"],'id_chat':None,'mensagem':"Olá, pode me ajudar?"}
                addMensagem(mensagem)
                del mensagem
                break
            case 0:
                break
            case _:
                print("Selecione uma opção válida.")
                continue

def showMensagem():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM mensagem''')
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    db.close()

def addMensagem(mensagem:dict):
    """ Esse dicionário precisa conter as chaves: 'id_usuario','id_sender','id_chat','mensagem','status' """
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    mensagem["data"] = str(datetime.now())

    #Acha uma id que não está em utilização
    cursor.execute("SELECT id FROM mensagem")
    newId = len(cursor.fetchall()) 
    while True:
        query = 'SELECT id FROM mensagem WHERE id=' + str(newId)
        cursor.execute(query)
        if cursor.fetchone() == None:
            break
        else:
            newId += 1
    if newId == 0:
        newId = 1

    #Acha uma id_chat que não está em utilização
    if mensagem["id_chat"] == None:
        cursor.execute("SELECT id_chat FROM mensagem ORDER BY id_chat DESC LIMIT 1") #pega o maior numero ultilizado como id_chat
        newIdChat = cursor.fetchone()
        if newIdChat == None:
            newIdChat = 1
        else:
            newIdChat = newIdChat[0] #Tira o numero da Id_chat do formato tupla para o formato de numero inteiro
        while True:
            query = 'SELECT id_chat FROM mensagem WHERE id_chat=' + str(newIdChat)
            cursor.execute(query)
            if cursor.fetchone() == None:
                break
            else:
                newIdChat += 1
        mensagem["id_chat"] = newIdChat
        mensagem["status"] = "aberto"

    mensagem["id"] = newId
    db.execute("INSERT INTO mensagem (id,id_usuario,id_sender,id_chat,mensagem,data,status) VALUES ( :id , :id_usuario , :id_sender , :id_chat , :mensagem , :data, :status)",mensagem)
    db.commit()

    cursor.close()
    db.close()

def validaIdChat(id_chat:int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    id_chat = (id_chat,)
    cursor.execute("SELECT id_chat FROM mensagem WHERE id_chat= ?",id_chat)
    validador = cursor.fetchone()
    cursor.close()
    db.close()
    if validador == None:
        return False
    else:
        return True

def menuChatsAbertos(usuario:dict):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT id_chat FROM mensagem WHERE status='aberto' AND id_usuario= :id",usuario)
    id_chat = cursor.fetchall()
    if id_chat == []:
        print("Não existe nenhum chat aberto!")
        cursor.close()
        db.close()
        return
    print("Selecione o chat que deseja exibir:")
    for row in id_chat:
        idTupla = (row[0],)
        cursor.execute("SELECT mensagem,id_chat FROM mensagem WHERE id_chat=? ORDER BY data LIMIT 1",idTupla)
        mensagem = cursor.fetchone()
        print("Chat ",mensagem[1],"- ",usuario["email"], ":" ,mensagem[0])
    while True:
        try:
            idChat = int(input("Selecione um dos chats para exibir: "))
        except:
            print("Opção Inválida!")
            continue
        if validaIdChat(idChat) == True:
            break
        else:
            print("Opção inválida!")
            continue
    exibirChat(idChat)
    print("Deseja adicionar uma nova mensagem ao chat?\n" \
        "1 - Sim\n" \
        "2 - Não")
    while True:
        op = input("Selecione uma opção:")
        match op:
            case "1":
                msg = input("Digite a nova mensagem a ser adicionada:")
                mensagem = {"id_usuario":usuario["id"],"id_sender":usuario["id"],"status":"aberto","id_chat":idChat,"mensagem":msg}
                addMensagem(mensagem)
                cursor.close()
                db.close()
                return
            case "2":
                cursor.close()
                db.close()
                return
            case "_":
                print("Opção invalida!")
                continue

def login(): #Tela inicial, pede login e senha. Caso seja o primeiro login, o usuario precisa preencher os dados necessários.
    while True: 
        print("-----Bem vindo ao app da CocoCabon-----\n" \
            "Selecione uma opção para avancar:\n" \
            "1 - Login\n" \
            "2 - Cadastro\n" \
            "3 - Sair")
        try: #Caso o input contenha um caracter que não seja um numero, ele pede um input válido.
            opcao = int(input("Selecione uma opção:"))
        except:
            print("Não podem ser usados caracteres especiais!")
            continue
        match opcao:
            case 1:
                while True:
                    email = input("Digite seu email:")
                    senha = input("Digite sua senha:")
                    usuario = {"email":email,"senha":senha}
                    usuario = getLogin(email,senha)
                    if usuario == None:
                        print("O email ou senha informados são inválidos")
                        continue
                    else:
                        print("Login efetuado!")
                        break
                if None in usuario.values(): #Caso algum dado do usuario não esteja cadastrado, os dados serão solicitados
                    print("Detectamos que você precisa atualizar seus dados.")
                    if usuario["cnpj"] == None:
                        cnpj = input("Informe o cnpj da empresa:")
                        usuario["cnpj"] = cnpj
                        del cnpj
                    if usuario["telefone"] == None:
                        telefone = input("Informe o telefone da empresa para contato:")
                        usuario["telefone"] = telefone
                        del telefone
                    if usuario["cep"] == None:
                        cep = input("Informe o CEP da empresa:")
                        usuario["cep"] = cep
                        del cep
                    if usuario["endereço"] == None:
                        endereço = input('Informe o endereço da sua empresa:\n' \
                        'No formato "Rua, Numero"')
                        usuario["endereço"] = endereço
                        del endereço
                    if usuario["tipo_de_usuário"] == None:
                        while True:
                            print("Selecione um tipo de usuario:\n" \
                            "1 - Vendedor de Coco\n" \
                            "2 - Produtor de energia apartir de Biomassa\n" \
                            "3 - Empresa compradora de crédito de carbono")
                            try:
                                op = int(input())
                            except:
                                print("Um dos caracteres informados é invalido.")
                                continue
                            if op == 1:
                                usuario["tipo_de_usuário"] = "vendedor_de_biomassa"
                            elif op == 2:
                                usuario["tipo_de_usuário"] = "produtor_de_energia"
                            elif op == 3:
                                usuario["tipo_de_usuário"] = "comprador_de_credito"
                            else:
                                print("Selecione uma opção válida.")
                                continue
                            break
                    updateUsuario(usuario)
                if usuario["tipo_de_usuário"] == "admin":
                    loginAdmin(usuario)
                else:
                    menuPrincipal(usuario)
                break
            case 2: 
                email = input("Digite seu email de login:")
                senha = input("Digite sua senha de login:")
                addUsuario(email,senha)
                print("Novo usuario registrado com sucesso!")
                continue
            case 3:
                break
            case _:
                print("Opção invalida!")
                continue

def menuPrincipal(usuario:dict): 
    print(f"Bem vindo {usuario["email"]}.")
    match usuario["tipo_de_usuário"]: # Seleciona a ação de acordo com o tipo de usuário
        case "vendedor_de_biomassa": #Ações a serem executadas caso o usuario seja um Produtor de Biomassa
            while True:
                print("-----------------------Menu---------------------------\n" \
                    "1 - Registrar uma oferta de coco\n" \
                    "2 - Acessar histórico de ofertas\n" \
                    "3 - Acessar histórico de transações\n" \
                    "4 - Fale conosco, abra um novo chat!\n" \
                    "5 - Acompanhe chats abertos\n" \
                    "0 - Sair")
                try:  #Caso o input contenha um caracter que não seja um numero, ele pede um input válido.
                    op = int(input("Selecione uma opção:"))
                except:
                    print("Opção inválida!")
                    continue
                match op:
                    case 1: #Usuario registra uma oferta de coco
                        peso = float(input("Quantos kilos de coco deseja ofertar:"))
                        data = str(datetime.now().date())
                        addCoco(usuario["id"],peso,data)
                        print("Oferta registrada com sucesso!")
                        continue
                    case 2: #Usuario acessa todas as suas ofertas abertas
                        db = sqlite3.connect("database.db")
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM coco WHERE id_vendedor= :id",usuario)
                        for row in cursor.fetchall():
                            print(row)
                        cursor.close()
                        db.close()
                        continue
                    case 3: #Acessa histórico de transações do usuário
                        db = sqlite3.connect("database.db")
                        cursor = db.cursor()
                        cursor.execute("SELECT * FROM transacao WHERE id_vendedor= :id",usuario)
                        for row in cursor.fetchall():
                            vendedor = getUsuario(row[1])
                            comprador = getUsuario(row[2])
                            print("id: ",row[0],",vendedor: ",vendedor["email"],", comprador: ", comprador["email"],", tipo:",row[3],", Valor:",row[4],", data:",row[4])
                        cursor.close()
                        db.close()
                        continue
                    case 4:
                        menuNovasMensagens(usuario)
                        continue
                    case 5:
                        menuChatsAbertos(usuario)
                        continue
                    case 0:
                        break
                    case _:
                        print("Opção inválida!")
                        continue

        case "produtor_de_energia": #Ações a serem executadas caso o usuário seja um Produtor de Biomassa
            while True:
                print("-----------------------Menu---------------------------\n" \
                    "1 - Acessar ofertas de coco\n" \
                    "2 - Comprar coco\n" \
                    "3 - Acessar histórico de transações\n" \
                    "4 - Fale conosco, abra um novo chat!\n" \
                    "5 - Acompanhe chats abertos\n" \
                    "0 - Sair")
                try: #Caso o input contenha um caracter que não seja um numero, ele pede um input válido.
                    op = int(input("Selecione uma opção:"))
                except:
                    print("Opção invalida!")
                    continue
                match op:
                    case 1:
                        showCoco()
                        continue
                    case 2: #Compra uma oferta de casca de coco para produção de biomassa
                        while True:
                            print("Digite 0 para voltar.")
                            try:
                                id = int(input("Informe o id da oferta que você deseja comprar:"))
                            except:
                                print("Caracter inválido.")
                                continue
                            if id == 0:
                                break
                            coco = getCoco(id)
                            if coco == {}:
                                print("Id informada não pertence a nenhuma oferta existente.")
                                continue
                            else:
                                deleteCoco(coco["id_produto"])
                                data = str(datetime.now())
                                addTransacao(coco["id_vendedor"],usuario["id"],"venda_de_biomassa",coco["peso_kg"],data)
                                del coco
                                print("Transação efetuada com sucesso!")
                                break
                        continue
                    case 3:
                        db = sqlite3.connect("database.db")
                        cursor = db.cursor()
                        id_vendedor = (usuario["id"],)
                        cursor.execute("SELECT * FROM transacao WHERE id_comprador=?",id_vendedor)
                        del id_vendedor
                        for row in cursor.fetchall():
                            vendedor = getUsuario(row[1])
                            comprador = getUsuario(row[2])
                            print("id: ",row[0],",vendedor: ",vendedor["email"],", comprador: ", comprador["email"],", tipo:",row[3],", Valor:",row[4],", data:",row[4])
                        del vendedor,comprador
                        cursor.close()
                        db.close()
                    case 4:
                        menuNovasMensagens(usuario)
                        continue
                    case 5:
                        menuChatsAbertos(usuario)
                        continue
                    case 0:
                        break
                    case _:
                        print("Opção inválida!")
        case "comprador_de_credito": #Ações a serem executadas caso o usuário seja uma Empresa parceira
            while True:
                print("-----------------------Menu---------------------------\n" \
                    "1 - Acessar ofertas de crédito de carbono disponivel\n" \
                    "2 - Comprar contrato de crédito de carbono\n"\
                    "3 - Acessar histórico de transações\n"  \
                    "4 - Fale conosco, abra um novo chat!\n" \
                    "5 - Acompanhe chats abertos\n" \
                    "0 - Sair")
                try: #Caso o input contenha um caracter que não seja um numero, ele pede um input válido.
                    op = int(input("Selecione uma opção:"))
                except:
                    print("Caracter inválido presente!")
                    continue
                match op:
                    case 1:
                        showCreditoDeCarbono()
                        continue
                    case 2:
                        while True:
                            print("Digite 0 para voltar.")
                            try:
                                id = int(input("Digite a id da oferta que deseja comprar:"))
                            except:
                                print("Um dos caracteres informados é inválido!")
                                continue
                            if id == 0:
                                break
                            if validaIdCreditoDeCarbono(id) == False:
                                print("A id informada não pertence a nenhuma transação existente.")
                                continue
                            credito = getCreditoDeCarbono(id)
                            if credito == {}:
                                print("A id informada não pertence a nenhum produto.")
                            deleteCreditoDeCarbono(credito["id_produto"])
                            data = str(datetime.now().date())
                            addTransacao(credito["id_vendedor"],usuario["id"],"credito_de_carbono",credito["preco"]*credito["tonelada_de_carbono"],data)
                            print("Transação efetuada com sucesso!")
                            break
                        continue
                    case 3:
                        db = sqlite3.connect("database.db")
                        cursor = db.cursor()
                        id = (usuario["id"],usuario["id"])
                        cursor.execute("SELECT * FROM transacao WHERE id_comprador=? OR id_vendedor=?",id)
                        del id
                        for row in cursor.fetchall():
                            vendedor = getUsuario(row[1])
                            comprador = getUsuario(row[2])
                            print("id: ",row[0],",vendedor: ",vendedor["email"],", comprador: ", comprador["email"],", tipo:",row[3],", Valor:",row[4],", data:",row[4])
                        continue
                    case 4:
                        menuNovasMensagens(usuario)
                        continue
                    case 5:
                        menuChatsAbertos(usuario)
                        continue
                    case 0:
                        break
                    case _:
                        print("Opção inválida!")
                        continue

    return
#db.execute("""CREATE TABLE transacao(id_transacao INTEGER NOT NULL PRIMARY KEY,id_vendedor INTEGER NOT NULL,id_comprador TEXT,tipo TEXT,valor TEXT,data TEXT,FOREIGN KEY(id_vendedor) REFERENCES usuario(id))""")





login()


#cursor.execute("SELECT * FROM transacao")
#for row in cursor.fetchall():
#    print(f'{type(row[0])}, {type(row[1])}, {type(row[2])}')



