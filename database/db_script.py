import sqlite3
import random
import sys

first_name_list = ["Antônio", "Carlos", "Francisco", "João", "José", "Luís", "Luiz", "Pedro", "Mateus", "Miguel",
                   "Alberto", "Roberto", "Ana", "Alice", "Maria", "Fátima", "Francisca", "Cora", "Mariana"]
last_name_list = ["Almeida", "Souza", "Bernardes", "Neves", "Oliveira", "Silva", "Souza", "Lira", "Costa", "Moura",
                  "Rodrigues", "Gomes", "Gonçalves", "Martins"]
localization_list = ["Sorriso - MT", "São Miguel Arcanjo - SP", "Marialva - PR", "Jatobá - PI", "Ivinhema - MS",
                     "Maués - AM", "Atibaia - SP", "Igarapé-Mirim - PA", "Piedade - SP", "Ituporanga - SC",
                     "São Joaquim - SC", "Reserva - PR", "São Desidério - BA", "Uberaba - MG"]
pesticide_list = ["2,4-D", "Metomil", "Clorpirifós", "Diazinona", "Acefato", "Atrazina", "Diuron", "Glifosato",
                  "Melationa", "Mancozebe"]  # 10/30/40

# Class 1: 2,4-D; Metomil;
# Class 2: Clorpirifós; Diazinona
# Class 3 & 4: Acefato, Atrazina, Diuron, Glifosato, Malationa, Mancozebe

conn = sqlite3.connect('pesticides.db')
cursor = conn.cursor()

# cursor.execute("DROP TABLE farmers")
cursor.execute("""CREATE TABLE farmers (
            id integer PRIMARY KEY,
            firstname text,
            lastname text,
            localization text,
            pesticide text,
            category text
 )""")
conn.commit()



#cursor.execute("DELETE FROM farmers")
#conn.commit()


def populate():
    for i in range(121):
        if i < 20:
            cursor.execute("INSERT INTO farmers VALUES (?, ?, ?, ?, ?, ?)", (i+1, random.choice(first_name_list),
                                                                       random.choice(last_name_list),
                                                                       random.choice(localization_list),
                                                                       pesticide_list[random.randint(0, 1)],
                                                                        "1"))
            conn.commit()
        elif 20 < i < 61:
            cursor.execute("INSERT INTO farmers VALUES (?, ?, ?, ?, ?, ?)", (i+1, random.choice(first_name_list),
                                                                       random.choice(last_name_list),
                                                                       random.choice(localization_list),
                                                                       pesticide_list[random.randint(2, 3)],
                                                                       "2"))
            conn.commit()
        elif i >= 61:
            cursor.execute("INSERT INTO farmers VALUES (?, ?, ?, ?, ?, ?)", (i+1, random.choice(first_name_list),
                                                                       random.choice(last_name_list),
                                                                       random.choice(localization_list),
                                                                       pesticide_list[random.randint(4, 9)],
                                                                       "3"))
            conn.commit()


populate()

cursor.execute("SELECT * FROM farmers")
#sys.stdout = open("test.txt", "w")
#print(cursor.fetchall())
#sys.stdout.close()
print(cursor.fetchall())
conn.commit()
conn.close()

# def populate():
#    for i in 99:
#        if i < 9:

#        cursor.execute("INSERT INTO farmers VALUES (?, ?, ?)", (random.choice(first_name_list),
#                       random.choice(last_name_list), random.choice(localization_list)))
