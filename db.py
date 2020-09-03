import sqlite3
import time

database = 'games.sqlite'

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, board TEXT, lastmove REAL, turn TEXT, red_sid TEXT, yellow_sid TEXT)''')
conn.commit()
conn.close()


def new_game(board, sid):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT MAX(id) FROM games''')
    try:
        id = c.fetchone()[0] + 1
    except TypeError:
        id = 0
    lastmove = time.time()
    data = (id, board, lastmove, 'r', sid, None)
    c.execute('''REPLACE INTO games VALUES(?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()
    print("Created new game with id {}".format(id))
    return id


def join_game(id, sid):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''UPDATE games SET yellow_sid = ? WHERE id = ?''', (sid, id))
    conn.commit()


def update_game(id, board):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    lastmove = time.time()
    data = (board, lastmove, id)
    c.execute('''UPDATE games SET board = ?, lastmove = ? WHERE id = ?''', data)
    conn.commit()
    conn.close()
    print("Game {} updated".format(id))


def get_color_by_sid(id, sid):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT * FROM games WHERE id = ? AND red_sid = ?''', (id, sid))
    if len(c.fetchall()) == 0:
        return 'y'
    else:
        return 'r'


def get_sid_by_color(id, color):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if color == 'r':
        c.execute('''SELECT red_sid FROM games WHERE id = ?''', (id,))
    else:
        c.execute('''SELECT yellow_sid FROM games WHERE id = ?''', (id,))
    return c.fetchone()[0]


def get_board(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT board FROM games WHERE id = ?''', (id,))
    return c.fetchone()[0]

def delete_game(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''DELETE FROM games WHERE id = ?''', (id,))
    conn.commit()
