import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

# cur = connection.cursor()
#
# cur.execute("INSERT INTO answers (id, will_be) VALUES (?, ?)",
#             ('Test', 0)
#             )

connection.commit()
connection.close()
