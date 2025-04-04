import sqlite3
import bcrypt

def create_connection():
    try:
        conn = sqlite3.connect('database.db3')
        return conn
    except sqlite3.Error as e:
        print(f"{e}")
    return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               name TEXT,
               email TEXT UNIQUE,
               passwrd TEXT
            )
        ''')

        conn.commit()

    except sqlite3.Error as e:
        print(f"{e}")

def register_users(name, email, passwrd):
    conn = create_connection()
    cursor = conn.cursor()

    passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO users (name, email, passwrd) 
            VALUES (?, ?, ?)
        """, (name, email, passwrd))

        conn.commit()

        return True
    
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

def user_signin(email, passwrd):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT passwrd FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            passwrd_hash = user[0]
            if bcrypt.checkpw(passwrd.encode('utf-8'), passwrd_hash):
                print("Sign-in successful.")
                return True
            else:
                return False
        else:
            return False
            
    except sqlite3.Error as e:
        print(f"{e}")
        return False
    
    finally:
        conn.close()

def user_details(email):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email FROM users WHERE email = ?
        """, (email,))
        
        user = cursor.fetchone()
        
        if user:
            user_details = {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }
            return user_details
        else:
            return None

    except sqlite3.Error as e:
        print(f"{e}")
        return None
    
    finally:
        conn.close()


