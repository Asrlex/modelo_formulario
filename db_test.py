import db

DB_FILE = "template.db"

# Create database instance
database = db.Database(DB_FILE)
database.create_table_usuarios()
database.create_table_registros()

u = "s"
while u == "s":
    u = input("\nNuevo usuario? (s/n): ")
    if u == "s":
        nombre = input("Nombre: ")
        usuario = input("Usuario: ")
        database.insert_usuario(nombre, usuario)

# Close database connection
del database