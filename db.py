'''Database class to manage the database

Author: Alejandro Sanchez Rodriguez
Description: This class is used to manage the database. It contains methods to 
    create the tables, insert, read, edit and delete data.
Date: 2023-06-30
'''

import sqlite3
import numpy as np


class Database:
    '''Constructor'''
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
    
    '''Destructor'''
    def __del__(self):
        self.conn.close()

    '''Execute a query passed as a parameter'''
    def query(self, query):
        self.cur.execute(query)
        self.conn.commit()


    ############################################################################
    '''Create a table called usuarios with the following fields: id, nombre, usuario'''
    def create_table_usuarios(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS usuarios \
                        (id INTEGER PRIMARY KEY, nombre TEXT, usuario TEXT)")
        self.conn.commit()
    
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
    def create_table_registros(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS registros \
                        (id INTEGER PRIMARY KEY, fechaEntrada DATETIME, operador TEXT, identificador TEXT, importe REAL,\
                        estado TEXT, x TEXT, num_llamadas INTEGER, fechaResolucion DATETIME, operadorResolucion TEXT, \
                        observaciones TEXT)")
        self.conn.commit()

    '''Create a table called logs with the following fields: id, fecha, usuario, accion'''
    def create_table_logs(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS logs \
                        (id INTEGER PRIMARY KEY, fecha DATETIME, usuario TEXT, accion TEXT)")
        self.conn.commit()


    ############################################################################
    '''Insert a new user'''
    def insert_usuario(self, nombre, usuario):
        self.cur.execute("INSERT INTO usuarios VALUES (NULL, ?, ?)", (nombre, usuario))
        self.conn.commit()
    
    '''Read all users'''
    def get_all_usuarios(self):
        self.cur.execute("SELECT * FROM usuarios")
        rows = self.cur.fetchall()
        return rows
    
    '''Edit a user'''
    def edit_usuario(self, id, nombre, usuario):
        self.cur.execute("UPDATE usuarios SET nombre = ?, usuario = ? WHERE id = ?", (nombre, usuario, id))
        self.conn.commit()

    '''Delete a user'''
    def delete_usuario(self, id):
        self.cur.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        self.conn.commit()


    ############################################################################
    '''Read all registers'''
    def get_all_registros(self):
        self.cur.execute("SELECT * FROM registros")
        rows = self.cur.fetchall()
        return rows
    
    '''Read a single register'''
    def get_registro(self, id):
        self.cur.execute("SELECT * FROM registros WHERE id = ?", (id,))
        rows = self.cur.fetchall()
        return rows

    '''Read a single register by a given parameter'''
    def get_registro_by(self, parameter, value):
        self.cur.execute("SELECT * FROM registros WHERE ? = ?", (parameter, value))
        rows = self.cur.fetchall()
        return rows
    
    '''Read all registers within a fecha_entrada range'''
    def get_all_registros_fecha_entrada(self, rango):
        self.cur.execute("SELECT * FROM registros WHERE fechaEntrada BETWEEN ? AND ?",
                        (rango[0], rango[1]))
        rows = self.cur.fetchall()
        return rows
    
    '''Insert a new register, passing the values as an array'''
    def insert_registro(self, values=[]):
        list = np.array(values).tolist()
        self.cur.execute(
            "INSERT INTO registros VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (list))
        self.conn.commit()

    '''Insert multiple new registers'''
    def insert_multiples_registros(self, values=[]):
        list = np.array(values).tolist()
        self.cur.executemany(
            "INSERT INTO registros VALUES (NULL, ?)",
            (list))
        self.conn.commit()
    
    '''Edit a register'''
    def edit_registro(self, values=[]):
        list = np.array(values).tolist()
        self.cur.execute(
            "UPDATE registros SET fechaEntrada = ? \
                WHERE id = ?",
            (list))
        self.conn.commit()

    '''Delete a register'''
    def delete_registro(self, id):
        self.cur.execute("DELETE FROM registros WHERE id = ?", (id,))
        self.conn.commit()


    ############################################################################