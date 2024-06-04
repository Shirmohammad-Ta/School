


import sqlite3
from sqlite3 import Error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np



def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('school_management.db')
        return conn
    except Error as e:
        print(e)
    return conn



def create_tables(conn):
    try:
        sql_create_students_table = """CREATE TABLE IF NOT EXISTS students (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            age INTEGER,
                                            gender TEXT,
                                            grade TEXT
                                        );"""
        sql_create_scores_table = """CREATE TABLE IF NOT EXISTS scores (
                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          student_id INTEGER NOT NULL,
                                          subject TEXT NOT NULL,
                                          score INTEGER,
                                          FOREIGN KEY (student_id) REFERENCES students (id)
                                      );"""
        conn.execute(sql_create_students_table)
        conn.execute(sql_create_scores_table)
    except Error as e:
        print(e)



def add_student(conn, student):
    sql = '''INSERT INTO students(name, age, gender, grade)
             VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid



def add_score(conn, score):
    sql = '''INSERT INTO scores(student_id, subject, score)
             VALUES(?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, score)
    conn.commit()
    return cur.lastrowid



def list_students(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    for row in rows:
        print(row)



def list_scores(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM scores")
    rows = cur.fetchall()
    for row in rows:
        print(row)


# پیش‌بینی نمرات آینده
def predict_scores(conn, student_id):
    cur = conn.cursor()
    cur.execute("SELECT subject, score FROM scores WHERE student_id=?", (student_id,))
    rows = cur.fetchall()
    if not rows:
        print("No scores found for the given student ID.")
        return


    df = pd.DataFrame(rows, columns=['subject', 'score'])
    df['subject'] = df['subject'].astype('category').cat.codes


    X = df[['subject']]
    y = df['score']

    # تقسیم داده‌ها به آموزش و آزمایش
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ایجاد و آموزش مدل
    model = LinearRegression()
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)


    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # نمایش نمرات واقعی و پیش‌بینی شده
    plt.scatter(X_test, y_test, color='blue', label='Actual Scores')
    plt.scatter(X_test, y_pred, color='red', label='Predicted Scores')
    plt.xlabel('Subject')
    plt.ylabel('Score')
    plt.title('Actual vs Predicted Scores')
    plt.legend()
    plt.show()



def main():
    conn = create_connection()
    if conn is not None:
        create_tables(conn)
    else:
        print("Error! Cannot create the database connection.")
        return

    while True:
        print("\nSchool Management System with AI")
        print("1. Add Student")
        print("2. List Students")
        print("3. Add Score")
        print("4. List Scores")
        print("5. Predict Scores")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter student's name: ")
            age = int(input("Enter student's age: "))
            gender = input("Enter student's gender: ")
            grade = input("Enter student's grade: ")
            student = (name, age, gender, grade)
            add_student(conn, student)
            print("Student added successfully.")
        elif choice == '2':
            list_students(conn)
        elif choice == '3':
            student_id = int(input("Enter student ID: "))
            subject = input("Enter subject: ")
            score = int(input("Enter score: "))
            score_record = (student_id, subject, score)
            add_score(conn, score_record)
            print("Score added successfully.")
        elif choice == '4':
            list_scores(conn)
        elif choice == '5':
            student_id = int(input("Enter student ID: "))
            predict_scores(conn, student_id)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    if conn:
        conn.close()


if __name__ == '__main__':
    main()
