#Мухаметшин Дамир


import sqlite3


def counter(name):
    con = sqlite3.connect('count.db')
    cur = con.cursor()
    cur.execute("""UPDATE motion
    SET cou =cou+1
    WHERE id = ?""", (name,))
    con.commit()
