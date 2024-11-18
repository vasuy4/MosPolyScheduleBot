import sqlite3
from faker import Faker

with sqlite3.connect("database.sqlite") as conn:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id > 3")
    conn.commit()

    cursor.execute("SELECT * FROM students;")
    print(cursor.fetchall())

    fake = Faker()
    for i in range(52):
        full_name = fake.name().split()
        cursor.execute(
            "INSERT INTO students (name, surname) VALUES ('{}', '{}')".format(
                full_name[0], full_name[1]
            )
        )
        conn.commit()

    cursor.execute("SELECT * FROM students;")
    print(cursor.fetchall())
