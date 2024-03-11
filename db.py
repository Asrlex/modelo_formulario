'''Database class to manage the database

Author: Alejandro Sanchez Rodriguez
Description: This class is used to manage the database. It contains methods to 
    create the tables, insert, read, edit and delete data.
Date: 2023-06-30
'''

import sqlite3
import numpy as np


class Database:
    def __init__(self, db):
        '''Constructor'''
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
    
    def __del__(self):
        '''Destructor'''
        self.conn.close()

    def query(self, query):
        '''Execute a query passed as a parameter'''
        self.cur.execute(query)
        self.conn.commit()


    ############################################################################
    def create_table_usuarios(self):
        '''Create a table called usuarios with the following fields: id, nombre, usuario'''
        self.cur.execute("CREATE TABLE IF NOT EXISTS usuarios \
                        (id INTEGER PRIMARY KEY, nombre TEXT, usuario TEXT)")
        self.conn.commit()
    
    def create_table_registros(self):
        '''Create a table called registros that stores every registered task
            The table called registros has following fields:
                id (integer, primary key),
                fechaEntrada (datetime),
                operador (text),
                identificador (text),
                importe (real),
                estado (text),
                x (text),
                num_llamadas (integer),
                fechaResolucion (datetime),
                operadorResolucion (text),
                observaciones (text)
        '''
        self.cur.execute("CREATE TABLE IF NOT EXISTS registros \
                        (id INTEGER PRIMARY KEY, fechaEntrada DATETIME, operador TEXT, identificador TEXT, importe REAL,\
                        estado TEXT, x TEXT, num_llamadas INTEGER, fechaResolucion DATETIME, operadorResolucion TEXT, \
                        observaciones TEXT)")
        self.conn.commit()

    def create_table_logs(self):
        '''Create a table called logs with the following fields: id, fecha, usuario, accion'''
        self.cur.execute("CREATE TABLE IF NOT EXISTS logs \
                        (id INTEGER PRIMARY KEY, fecha DATETIME, usuario TEXT, accion TEXT)")
        self.conn.commit()


    ############################################################################
    def insert_usuario(self, nombre, usuario):
        '''Insert a new user'''
        self.cur.execute("INSERT INTO usuarios VALUES (NULL, ?, ?)", (nombre, usuario))
        self.conn.commit()
    
    def get_all_usuarios(self):
        '''Read all users'''
        self.cur.execute("SELECT * FROM usuarios")
        rows = self.cur.fetchall()
        return rows
    
    def edit_usuario(self, id, nombre, usuario):
        '''Edit a user'''
        self.cur.execute("UPDATE usuarios SET nombre = ?, usuario = ? WHERE id = ?", (nombre, usuario, id))
        self.conn.commit()

    def delete_usuario(self, id):
        '''Delete a user'''
        self.cur.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        self.conn.commit()


    ############################################################################
    def get_all_registros(self):
        '''Read all registers'''
        self.cur.execute("SELECT * FROM registros")
        rows = self.cur.fetchall()
        return rows
    
    def get_registro(self, id):
        '''Read a single register'''
        self.cur.execute("SELECT * FROM registros WHERE id = ?", (id,))
        rows = self.cur.fetchall()
        return rows

    def get_registro_by(self, parameter, value):
        '''Read a single register by a given parameter'''
        self.cur.execute("SELECT * FROM registros WHERE ? = ?", (parameter, value))
        rows = self.cur.fetchall()
        return rows
    
    def get_all_registros_fecha_entrada(self, rango):
        '''Read all registers within a fecha_entrada range'''
        self.cur.execute("SELECT * FROM registros WHERE fechaEntrada BETWEEN ? AND ?",
                        (rango[0], rango[1]))
        rows = self.cur.fetchall()
        return rows
    
    def insert_registro(self, values=[]):
        '''Insert a new register, passing the values as an array'''
        list = np.array(values).tolist()
        self.cur.execute(
            "INSERT INTO registros VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (list))
        self.conn.commit()

    def insert_multiples_registros(self, values=[]):
        '''Insert multiple new registers'''
        list = np.array(values).tolist()
        self.cur.executemany(
            "INSERT INTO registros VALUES (NULL, ?)",
            (list))
        self.conn.commit()
    
    def edit_registro(self, values=[]):
        '''Edit a register'''
        list = np.array(values).tolist()
        self.cur.execute(
            "UPDATE registros SET fechaEntrada = ? \
                WHERE id = ?",
            (list))
        self.conn.commit()

    def delete_registro(self, id):
        '''Delete a register'''
        self.cur.execute("DELETE FROM registros WHERE id = ?", (id,))
        self.conn.commit()


    ############################################################################