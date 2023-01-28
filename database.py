import sqlite3

conn = sqlite3.connect("db.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        language TEXT,
                        dot TEXT,
                        dash TEXT,
                        mode TEXT);''')
conn.commit()
conn.close()


class SQLiter:

    def __init__(self, database) -> object:
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

    def add_to_db(self, user_id, language='English', dot='•', dash='–', mode='Morse'):
        """Добавление пользователя в БД"""
        self.c.execute("INSERT INTO users(user_id, language, dot, dash, mode) VALUES(?,?,?,?,?)", (user_id,
                                                                                                   language,
                                                                                                   dot,
                                                                                                   dash,
                                                                                                   mode))
        self.conn.commit()

    def update_language(self, user_id, language):
        """Обновление языка в БД"""
        self.c.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
        self.conn.commit()

    def update_dot(self, user_id, dot):
        """Обновление точки в БД"""
        self.c.execute("UPDATE users SET dot = ? WHERE user_id = ?", (dot, user_id))
        self.conn.commit()

    def update_dash(self, user_id, dash):
        """Обновление тире в БД"""
        self.c.execute("UPDATE users SET dash = ? WHERE user_id = ?", (dash, user_id))
        self.conn.commit()

    def update_mode(self, user_id, mode):
        """Обновление режима работы в БД"""
        self.c.execute("UPDATE users SET mode = ? WHERE user_id = ?", (mode, user_id))
        self.conn.commit()

    def reset_all_default(self, user_id, language='English', dot='•', dash='–', mode='Morse'):
        """Сбросить все по умолчанию"""
        self.c.execute("UPDATE users SET language=?, dot=?, dash=?, mode=? WHERE user_id=?", (language,
                                                                                              dot,
                                                                                              dash,
                                                                                              mode,
                                                                                              user_id))
        self.conn.commit()

    def select_all_for_user(self, user_id):
        """Вывод данных из БД"""
        return self.c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def exists_user(self, user_id):
        """Проверка существования пользователя в БД"""
        return bool(self.c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone())
