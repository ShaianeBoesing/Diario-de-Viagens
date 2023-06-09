import sqlite3

conn = sqlite3.connect('diary.db')

cursor = conn.cursor()

# Inserir dados na tabela travellers
cursor.execute("""
  INSERT INTO travellers (name, username, password)
  VALUES ('Alice', 'alice123', 'password123');
""")

# Inserir dados na tabela trips
cursor.execute("""
  INSERT INTO trips (title, start_date, end_date, status, traveller_id)
  VALUES ('Viagem à Praia', '2023-06-01', '2023-06-10', 'Planejada', 1);
""")

# Inserir dados na tabela members
cursor.execute("""
  INSERT INTO members (name)
  VALUES ('Bob');
""")

# Inserir dados na tabela spots
cursor.execute("""
  INSERT INTO spots (name, start_hour, end_hour, status, value, rating, trip_id, category_id)
  VALUES ('Praia do Rosa', '2023-06-02 10:00:00', '2023-06-02 18:00:00',
  'Encerrado', 100.00, 2, 1, 1);
""")

# Inserir dados na tabela comments
cursor.execute("""
  INSERT INTO comments (description, date, spot_id)
  VALUES ('Lugar incrível!', '2023-06-02 18:30:00', 1);
""")

# Inserir dados na tabela categories
cursor.execute("""
  INSERT INTO categories (name)
  VALUES ('Comida');
""")

# Inserir dados na tabela spot_members
cursor.execute("""
  INSERT INTO spot_members (spot_id, member_id)
  VALUES (1, 1);
""")

cursor.execute("""
  INSERT INTO traveller_members (member_id, traveller_id)
  VALUES (1, 1);
""")

# Salvar as alterações
conn.commit()

print('Dados inseridos com sucesso.')

conn.close()
