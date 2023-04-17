import sqlite3
from Model.User import User
import hashlib

class UserController:
    def __init__(self):
        self.conn = sqlite3.connect('Database/Migrations/diary.db')
        self.create_user_table()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS travellers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        name TEXT NOT NULL,
                        password TEXT NOT NULL
                                            )''')
        self.conn.commit()

    def register_user(self, username:str, name:str, password:str, con_password:str):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM travellers WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is not None:
            print('deu nao')
            return False, 'Nome de usuário já existente!'

        # Create a new user and add it to the database
        if len(username) < 3:
            return False, 'Nome de usuário deve ter mais de 3 caracteres'
        if len(name) < 3:
            return False, 'Nome deve ter mais de 3 caracteres'
        if not name.isalpha():
            return False, 'O nome não deve conter caracteres especiais ou números'
        if len(password) < 3:
            return False, 'Senha deve ter mais de 3 caracteres'
        if con_password != password:
            return False, 'A senha e confirmação da senha não são iguais!'

        password = self.md5_hash_password(password)

        cursor.execute('INSERT INTO travellers (username, name, password) VALUES (?, ?, ?)',
                       (username, name, password))
        self.conn.commit()
        print('Criado')
        return True, 'Viajante criado com sucesso!'

    def login(self, username: str, password: str):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM travellers WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is None:
            return False, 'Usuário não registrado!'

        stored_user = self.get_user_by_username(username)

        #better to be safe than sorry
        if stored_user is None:
            return False, 'Usuário não encontrado'

        if stored_user.password == self.md5_hash_password(password):
            return True, f'Entrou como {username}'
        else:
            return False, 'Senha incorreta!'

    def get_user_by_username(self, username: str):
        # Retrieve a user by username
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM travellers WHERE username=?', (username,))
        result = cursor.fetchone()
        if result is None:
            return None
        return User(result[1], result[2], result[3])

    def md5_hash_password(self, password: str):
        hashed_password = hashlib.md5(password.encode())
        hashed_password = hashed_password.hexdigest()

        return hashed_password

