import sqlite3
import time

database = 'games.sqlite'

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, board TEXT, lastmove REAL, turn TEXT)''')
conn.commit()
conn.close()


def new_game(board):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT MAX(id) FROM games''')
    try:
        id = c.fetchone()[0] + 1
    except TypeError:
        id = 0
    lastmove = time.time()
    data = (id, board, lastmove, 'r')
    c.execute('''REPLACE INTO games VALUES(?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()
    print("Created new game with id {}".format(id))
    return id


def update_game(id, board):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    lastmove = time.time()
    data = (board, lastmove, id)
    c.execute('''UPDATE games SET board = ?, lastmove = ? WHERE id = ?''', data)
    conn.commit()
    conn.close()
    print("Game {} updated".format(id))


def get_board(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT board FROM games WHERE id = ?''', (id,))
    return c.fetchone()[0]
