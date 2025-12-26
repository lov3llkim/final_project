import sqlite3
from config import DATABASE, FAQ

class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.create_tables()
        
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS roles (
                         id integer PRIMARY KEY AUTOINCREMENT,
                         name string(30) NOT NULL UNIQUE);''')
            conn.execute('''
                         CREATE TABLE IF NOT EXISTS users(
                         id integer PRIMARY KEY,
                         name string(100) NOT NULL,
                         id_type integer NOT NULL, FOREIGN KEY(id_type) REFERENCES roles(id)
                        );''')
            conn.execute('''
                         CREATE TABLE IF NOT EXISTS faq (
                         id integer PRIMARY KEY AUTOINCREMENT,
                         topic string(100) NOT NULL UNIQUE,
                         question text NOT NULL UNIQUE,
                         answer text NOT NULL UNIQUE
                         );''')
            conn.execute('''
                         INSERT INTO roles (name)
SELECT 'admin' WHERE NOT EXISTS (
    SELECT 1 FROM roles WHERE name = 'admin' 
 ); ''')
            conn.execute('''                       
                         INSERT INTO roles (name)
SELECT 'client' WHERE NOT EXISTS (
    SELECT 1 FROM roles WHERE name = 'client' 
 ); ''')
            conn.execute('''                       
                         INSERT INTO roles (name)
SELECT 'employe' WHERE NOT EXISTS (
    SELECT 1 FROM roles WHERE name = 'employe' 
                                                
);

                         ''') 
            for topic in FAQ:
                question = FAQ[topic]['question']
                answer = FAQ[topic]['answer']
                conn.execute('''                       
                         INSERT INTO faq (topic, question,answer)
SELECT ?,?,? WHERE NOT EXISTS (
    SELECT 1 FROM faq WHERE topic = ? AND question = ? AND answer = ?
                                                
);''', (topic, question, answer, topic, question, answer))
            conn.commit()
            

        

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    
        
    
            
if __name__ == '__main__':
    db = DB_Manager(DATABASE)