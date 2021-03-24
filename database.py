import sqlite3


# Creates a table
def create_table():
    conn = sqlite3.connect("college.db")
    c = conn.cursor()
    c. execute("CREATE TABLE student (student_id INTEGER, first_name TEXT, last_name TEXT, attendance TEXT)")
    c.close()
    conn.close()


# converts a file to binary format for storage in the database
def to_binary(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


# inserts blob into the table
def insert(id, first_name, last_name):
    try:
        conn = sqlite3.connect("college.db")
        c = conn.cursor()
        data_tuple = (id, first_name, last_name, 'A')
        c.execute("INSERT INTO student (student_id, first_name, last_name, attendance) VALUES (?, ?, ?, ?)", data_tuple)
        conn.commit()
        print('Student data inserted successfully!!!')
        c.close()
    except sqlite3.Error as error:
        print(error)
        print("Failed to enter the data into the table")
    finally:
        if conn:
            conn.close()
            print("Connection Closed!!!!")


# converts binary format to readable format for storage
def write_to_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


# reads the blob data
def read_data(id):
    try:
        conn = sqlite3.connect('college.db')
        c = conn.cursor()
        sql_fetch_blob_query = """SELECT * FROM student WHERE student_id = ?"""
        c.execute(sql_fetch_blob_query, (id,))
        record = c.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1]+' '+row[2], "Attendance = ", row[3])

        c.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")


def mark_attendance(id):
    try:
        conn = sqlite3.connect('college.db')
        c = conn.cursor()

        c.execute("UPDATE student SET attendance = ? WHERE student_id = (?)", ('P', id))
        print('Marked the student present!!')
        c.close()
        conn.commit()
    except sqlite3.Error as error:
        print("Failed to update attendance!!", error)
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection is closed!!")


def mark_absent():
    try:
        conn = sqlite3.connect('college.db')
        c = conn.cursor()

        c.execute("UPDATE student SET attendance = 'A' ")
        print("Marked all student absent!!")
        conn.commit()
    except sqlite3.Error as error:
        print("failed to update attendance!!", error)
    finally:
        if conn:
            conn.close()
            print("Sqlite3 connection is closed")


def show_all():
    try:
        conn = sqlite3.connect('college.db')
        c = conn.cursor()
        c. execute('SELECT * FROM student')
        record = c.fetchall()
        for row in record:
            print("Id = ", row[0], " Name = ", row[1] + row[2], " Attendance = ", row[3])
        c.close()
    except sqlite3.Error as error:
        print("Failed to fetch the details!! ", error)
    finally:
        if conn:
            conn.close()
            print("Sqlite connection is closed!!")

show_all()