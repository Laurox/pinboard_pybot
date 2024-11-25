from sqlite3 import connect

DATABASE_PATH = "./data/db/database.sqlite3"
BUILD_PATH = "./data/db/build.sql"

con = connect(DATABASE_PATH, check_same_thread=False)
cur = con.cursor()

def build() -> None:
    print("Building database...")
    with open(BUILD_PATH, "r", encoding="utf-8") as build_file:
        cur.executescript(build_file.read())

def execute(command, *values):
    cur.execute(command, tuple(values))
    con.commit()

def fetchone(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()