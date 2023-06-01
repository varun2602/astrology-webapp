import sqlite3
conn = sqlite3.connect("astro2.db")
conn.cursor().execute("create table users(id integer primary key autoincrement not null unique, name text not null unique, hash text not null)")

conn.close()