'''Main file of the application

Author: Alejandro Sanchez Rodriguez
Date: 2023-06-22

This file contains the main code of the application. It creates the GUI and defines the functions that
are executed when the user interacts with the widgets.
It also works with the SQLite database and the Excel modules.
It's a general purpose form to structure and cleanly define data models. It can be repurposed for
any project that has a well-defined data structure.
'''


# Import libraries
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import db
from excel import Excel
import tk_utils
import configparser
import os
import re


################################################################################
# Create a function that searches for a record in the database from a given ID
def buscar_id():
    # If the entry field is empty, show an error message
    if not identificador.get():
        messagebox.showerror("Error", "El campo ID es obligatorio")
    else:
        # Clear the entry fields and comboboxes
        clear()
        # Search for the record in the database
        record = database.get_registro(identificador.get())
        # If the record exists, fill the entry fields and comboboxes with its values
        if record:
            print(record)
        # If the record doesn't exist, show an error message
        else:
            messagebox.showerror("Error", "No existe ningún registro con ese ID")

# Create a function that submits the form
def submit():
    # If operador is not selected, show an error message
    if not operador.get():
        messagebox.showerror("Error", "El campo operador es obligatorio")
        return

    # If any of the entry fields or comboboxes are empty, show an error message
    if not fecha_entrada.get() or not observaciones.get('1.0', "end-1c") or \
            not identificador.get() or not importe.get() or estados_cb.get() == "--" or \
            (estados_cb.get() == "INCIDENCIA" and \
                (not fecha_resolucion.get() or not operador_resolucion.get() \
                or not num_llamadas.get() or not campo.get())):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    # If the record already exists, ask for confirmation to overwrite it
    if database.get_registro_by("identificador", identificador.get()):
        if not messagebox.askyesno("Confirmar", "Ya existe un registro con ese ID. ¿Desea sobreescribirlo?"):
            return
        
    # If the record doesn't exist, ask for confirmation to create it
    elif not messagebox.askyesno("Confirmar", "¿Desea crear un nuevo registro?"):
        return

    # Create a list with the values of the entry fields and comboboxes
    values = [
        fecha_entrada.get(),
        operador.get(),
        identificador.get(),
        importe.get(),
        estados_cb.get(),
        campo.get(),
        int(num_llamadas.get()) if num_llamadas.get() else 0,
        fecha_resolucion.get(),
        operador_resolucion.get(),
        observaciones.get('1.0', "end-1c"),
    ]

    # Insert the record in the database
    database.insert_registro(values)

    # Clear the entry fields and comboboxes
    clear()

# Create a function that clears the form
def clear():
    # Clear the entry fields and comboboxes
    fecha_entrada.set("")
    identificador.set("")
    importe.set("")
    operador.set("")
    estados_cb.current(0)
    campo.set("")
    fecha_resolucion.set("")
    operador_resolucion.set("")
    observaciones.delete('1.0', "end-1c")
    num_llamadas.set("")

# Create a function that disables or enables every field in the incidencias category
def toggle_use_incidencias(new_state):
    # Disable or enable every field in the incidencias category
    campo_label.configure(state=new_state)
    campo_entry.configure(state=new_state)
    fres_label.configure(state=new_state)
    cal_resolucion.configure(state=new_state)
    opres_label.configure(state=new_state)
    oper_res_cb.configure(state=new_state)
    num_label.configure(state=new_state)
    num_entry.configure(state=new_state)

# Create a Listener for the estado combobox
def estado_seleccionado(event):
    if estados_cb.get() == "INCIDENCIA":
        toggle_use_incidencias("enabled")
    else:
        toggle_use_incidencias("disabled")

# Create a function that validates an entry field and accepts only numbers and dots
def verificar_numerico(char):
    return char.isdigit() or char == "" or char == "."

# Create a function that shows an auxiliary window to choose whether to extract \
# all the registers or only ones within a certain date range
def exportar_aux():
    # Create a new window
    export_window = tk.Toplevel()
    export_window.title("Exportar")
    export_window.resizable(False, False)
    export_window.iconbitmap("imgs/favicon.ico")

    # Create a label to show a message to the user
    label = tk.Label(export_window, text="¿Qué registros desea exportar?", font=("Gotham Bold", 14))
    label.grid(row=0, column=0, columnspan=3, pady=10)

    # Create a button to export all the registers
    button_all = tk.Button(export_window, text="Todos", 
            command= lambda: [exportar(0, None), export_window.destroy()])
    button_all.grid(row=1, column=0, pady=3)

    # Create a frame to group the date selectors
    frame = tk.Frame(export_window)
    frame.grid(row=1, column=1, pady=3)

    # Create two date selectors to choose the date range
    date_from = DateEntry(frame, width=12, background='darkblue', foreground='white', 
                        borderwidth=2, locale="es_ES", date_pattern="dd-MM-yyyy")
    date_from.pack(pady=3)
    date_to = DateEntry(frame, width=12, background='darkblue', foreground='white', 
                        borderwidth=2, locale="es_ES", date_pattern="dd-MM-yyyy")
    date_to.pack(pady=3)

    # Create a button to export only the registers within a certain date range
    button_range = tk.Button(frame, text="Rango de fechas", 
            command= lambda: [exportar(1, f"{date_from.get()} - {date_to.get()}"), export_window.destroy()])
    button_range.pack(pady=3)

    # Create a frame to group the date selector and button
    frame2 = tk.Frame(export_window)
    frame2.grid(row=1, column=2, pady=3)

    # Create a date selector and button to export only the registers from a certain date
    date = DateEntry(frame2, width=12, background='darkblue', foreground='white', 
                        borderwidth=2, locale="es_ES", date_pattern="dd-MM-yyyy")
    date.pack(pady=3)
    button_date = tk.Button(frame2, text="A partir de una fecha",
            command= lambda: [exportar(2, f"{date.get()}"), export_window.destroy()])
    button_date.pack(pady=3)

    # Create a button to close the window
    button_close = tk.Button(export_window, text="Cerrar", command=export_window.destroy)
    button_close.grid(row=2, column=0, columnspan=3, pady=3)

    tk_utils.centrar_ventana(export_window)

# Create a function that extracts the data from the database and creates an Excel file
def exportar(selector, fechas="", window=None):
    # Get the data from the database
    data = None
    nombre = None
    if selector == 1:
        aux = fechas.split(" - ")
        fechas = (aux[0], aux[1])
        data = database.get_all_registros_fecha_entrada(fechas)
        nombre = f"Extracción {aux[0]} - {aux[1]}.xlsx"
    elif selector == 2:
        data = database.get_all_registros_fecha_entrada(fechas)
        nombre = f"Extracción {fechas}.xlsx"
    else:
        data = database.get_all_registros()
        nombre = "Extracción global.xlsx"

    # Create a new Excel file
    excel = Excel()
    excel.crear_archivo(nombre)

    # Add headers to the Excel file
    excel.rellenar_cabeceras(cabeceras)

    # Add the data to the Excel file
    excel.rellenar_hoja(data)

    # Format the Excel file
    excel.formato_hoja()
    excel.formato_cabecera()

    # Save the Excel file
    excel.guardar_archivo_como()

    # Close the Excel file
    excel.cerrar_archivo()

    # Show a message to the user
    messagebox.showinfo("Información", "El archivo se ha exportado correctamente")

# Create a function that verifies the Excel file headers
def verificar_cabeceras(headers):
    # Check if the headers are correct
    if headers != cabeceras[1:]:
        # Show a message to the user
        messagebox.showerror("Error", "El archivo no tiene los campos correctos")
        return False
    return True

# Create a function that verifies the integrity of the data
def verificar_datos(datos):
    date_regex = r"^\d{2}-\d{2}-\d{4}$"
    for registro in datos:
        # Check if fecha entrada has a valid date format
        if not re.match(date_regex, registro[0]):
            messagebox.showerror("Error", "Fecha de entrada incorrecta")
            return False
        # Check if the next 2 fields are empty
        if registro[1] != "" or registro[2] != "":
            messagebox.showerror("Error", "El registro tiene campos vacíos")
            return False
        # Check if importe is a valid number
        try:
            float(registro[3])
        except ValueError:
            messagebox.showerror("Error", "Importe incorrecto")
            return False
        # If estado is INCIDENCIA, check whether the next fields are valid
        if registro[4] == "INCIDENCIA":
            # Check if registro[5][8][9] are empty
            if registro[5] != "" or registro[8] != "" or registro[9] != "":
                messagebox.showerror("Error", "El registro tiene campos vacíos")
                return False
            # Check if registro[6] is a valid integer
            try:
                int(registro[6])
            except ValueError:
                messagebox.showerror("Error", "Número de llamadas incorrecto")
                return False
            # Check if registro[7] is a valid date
            if not re.match(date_regex, registro[7]):
                messagebox.showerror("Error", "Fecha de resolución incorrecta")
                return False
    return True

# Create a function that imports data from an Excel file to the database
def importar():
    # Create a new Excel file
    excel = Excel()
    excel.cargar_archivo()

    # Check format integrity and insert the data in the database
    if not verificar_cabeceras(excel.datos[0]):
        messagebox.showerror("Error", "El archivo no tiene el formato correcto")
        return
    elif not verificar_datos(excel.datos[1:]):
        return
    else:
        # Delete the headers from the data
        del excel.datos[0]

        # Insert the data in the database
        database.insert_multiples_registros(excel.datos)

    # Show a message to the user
    messagebox.showinfo("Información", "El archivo se ha importado correctamente")

# Create a function that displays an overlay with help for the user
def help():
    # Create a new window
    ventana_ayuda = tk.Toplevel(ventana_principal)
    ventana_ayuda.title("Ayuda")
    ventana_ayuda.resizable(False, False)
    ventana_ayuda.iconbitmap("imgs/favicon.ico")
    ventana_ayuda.configure(background="#FFFFFF")

    # Create a frame for the content
    frame = ttk.Frame(ventana_ayuda)
    frame.pack(padx=10, pady=10)

    # Create a label with the help text
    help_text = """
        Este programa permite registrar, buscar, modificar y eliminar registros de 
        **NOMBRE DEL SERVICIO**.\n
        - Para registrar un nuevo registro, rellene todos los campos del formulario y
        pulse el botón "Confirmar. Todos los campos del cuerpo principal son
        obligatorios.\n
        - Para vaciar el formulario, pulse el botón "Limpiar".\n
        - Si el estado del registro es "INCIDENCIA", se habilitarán los campos
        "Campo", "Fecha de resolución", "Operador de resolución" y "Número de
        llamadas", que pasarán a ser obligatorios.\n
        - Para buscar un registro, introduzca su ID en el campo correspondiente y
        pulse el botón "Buscar" (icono de lupa).\n
        - Para modificar un registro, busque el registro y modifique los campos que
        desee. Pulse el botón "Confirmar" para guardar los cambios.\n
        - Para eliminar un registro, busque el registro y pulse el botón "Eliminar".
        Se mostrará una ventana de confirmación.\n\n
        - Para exportar los registros a Excel o cargar un fichero de datos, pulse 
        los botones "Exportar" e "Importar" del menú "Archivo", respectivamente.\n\n
    """

    title_label = ttk.Label(frame, text="Ayuda", font=("Gotham", 18, "bold"))
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="NSEW")

    help_label = ttk.Label(frame, text=help_text)
    help_label.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")

    # Create a button to close the window
    close_button = ttk.Button(frame, text="Cerrar", command=ventana_ayuda.destroy)
    close_button.grid(row=2, column=0, padx=10, pady=10, sticky="NSEW")

    # Center the window
    tk_utils.centrar_ventana(ventana_ayuda)

    # Show the window
    ventana_ayuda.mainloop()

# Mensaje de información
def about():
    messagebox.showinfo("Información", "Aplicación creada por Alejandro Sánchez Rodríguez")


################################################################################
config = configparser.ConfigParser()
config.read('config.ini')

# Create a database instance
DB_FILE = config["DB"]["DB_FILENAME"]
DB_FILE = os.path.join(os.path.dirname(__file__), DB_FILE)
database = db.Database(DB_FILE)

# All needed collections are defined here
usuarios = database.get_all_usuarios()
cabeceras = ["ID", "Fecha entrada", "Operador", "Identificador", 
            "Importe", "Estado", "Campo", "Nº llamadas", "Fecha resolución", 
            "Operador resolución", "Observaciones"]


################################################################################

def main():
    # Create GUI window
    ventana_principal = tk.Tk()
    ventana_principal.title("Nombre del servicio")
    ventana_principal.resizable(False, False)
    ventana_principal.iconbitmap("imgs/favicon.ico")
    ventana_principal.configure(background="#FFFFFF")

    # Add a style
    STYLE_THEME = config["STYLES"]["THEME"]
    style = ttk.Style(ventana_principal)
    style.configure("TFrame", background="#FFFFFF")
    style.configure("TLabel", font=("Gotham", 12), padding=(15, 5, 5, 5), 
        foreground="#00558C", background="#FFFFFF")
    style.configure("TButton", font=("Gotham", 12), padding=(5, 5, 5, 5),
        width=16, cursor="hand2", justify=tk.CENTER, background="#FFFFFF")
    style.configure("TEntry", font=("Gotham Light", 12), width=22)
    # SVF Colour #00558C
    # SVF Colour lighter #376887

    ################################################################################
    # Add a menu
    menu = tk.Menu(ventana_principal)
    ventana_principal.config(menu=menu)
    # Add a file menu with commands to load and extract excel files
    file_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Archivo", menu=file_menu)
    file_menu.add_command(label="Exportar informe", command=exportar_aux)
    file_menu.add_command(label="Importar datos", command=importar)
    file_menu.add_command(label="Salir", command=ventana_principal.quit)
    # Add a help menu
    help_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Ayuda", menu=help_menu)
    help_menu.add_command(label="Ayuda", command=help)
    help_menu.add_command(label="Acerca de...", command=about)


    ################################################################################
    # Add a label
    marco_titulo = ttk.Frame(ventana_principal, style="TFrame")
    logo_img = ImageTk.PhotoImage(Image.open("./imgs/logo.JPG").resize((80, 100)))
    logo_label = ttk.Label(
        marco_titulo,
        image=logo_img,
        background="#FFFFFF",
    )
    logo_label.grid(column=0, row=0, sticky=tk.E)
    titulo = ttk.Label(
        marco_titulo, 
        text="Nombre del servicio",
        font=("Gotham", 30),
        padding=(20, 20),
        justify=tk.CENTER,
        anchor=tk.CENTER,
        width=20
    )
    titulo.grid(column=1, row=0, columnspan=4, sticky=tk.W)
    marco_titulo.grid(column=0, row=0, columnspan=4)


    ################################################################################
    # Create a frame for the comboboxes
    factores_principales = ttk.Frame(ventana_principal, style="TFrame", relief=tk.RAISED, borderwidth=2)
    factores_principales.grid(column=0, row=1, columnspan=4, pady=(10, 10), padx=(10, 10))

    # Add a combobox from which to select the user
    ttk.Label(factores_principales, text="Operador:", font=("Gotham", 14))\
        .grid(column=0, row=0, sticky=tk.E, pady=(5, 15), padx=(15, 0))
    operador = tk.StringVar()
    operador_cb = ttk.Combobox(factores_principales, textvariable=operador, state="readonly",\
                                font=("Gotham", 12), width=25, justify=tk.CENTER)
    operador_cb["values"] = [(f"{u[1]} - {u[2]}") for u in usuarios]
    operador_cb.grid(column=1, row=0, columnspan=2, pady=(5, 15), padx=(15, 15))


    ################################################################################
    # Add a frame for the entry fields
    marco_formulario = ttk.Frame(ventana_principal, style="TFrame")
    marco_formulario.grid(column=0, row=2, columnspan=4, pady=(10, 10), padx=(20))

    # Add entry fields
    fecha_entrada = tk.StringVar()
    identificador = tk.StringVar()
    importe = tk.DoubleVar()
    campo = tk.StringVar()
    num_llamadas = tk.StringVar()
    fecha_resolucion = tk.StringVar()
    operador_resolucion = tk.StringVar()
    observaciones = tk.StringVar()

    # Dynamically advance the row counter to structure the form
    row_form = 0

    ################################################################################
    # Add a separator to define a section
    ttk.Separator(marco_formulario,orient='horizontal')\
        .grid(column=0, row=row_form, columnspan=8, sticky='ew', pady=5)
    row_form += 1

    # Add a date entry field
    ttk.Label(marco_formulario, text="Fecha de\nentrada:")\
        .grid(column=0, row=row_form, sticky=tk.E)
    cal_entrada = DateEntry(marco_formulario, textvariable=fecha_entrada, font=("Gotham Light", 10),
        justify=tk.CENTER, width=20, locale="es_ES", date_pattern="dd-MM-yyyy")
    cal_entrada.grid(column=1, row=row_form)

    # Add a field for the global identifier of the register, and a button to search for it on the database
    ttk.Label(marco_formulario, text="ID:")\
        .grid(column=2, row=row_form, sticky=tk.E)
    marco_id = ttk.Frame(marco_formulario, style="TFrame")
    marco_id.grid(column=3, row=row_form, columnspan=1, sticky=tk.W)

    ttk.Entry(marco_id, textvariable=identificador, font=("Gotham Light", 10), width=19)\
        .grid(column=0, row=0)
    search_img = PhotoImage(file=r".\imgs\search.png")
    ttk.Button(marco_id, image=search_img, command=buscar_id, width=5, padding=(0))\
        .grid(column=1, row=0, sticky=tk.W)

    # Add a number field which validates character entry
    val = marco_formulario.register(verificar_numerico)
    ttk.Label(marco_formulario, text="Importe:")\
        .grid(column=4, row=row_form, sticky=tk.E)
    ttk.Entry(marco_formulario, textvariable=importe, font=("Gotham Light", 10), width=22,
            validate="key", validatecommand=(val, "%S"))\
        .grid(column=5, row=row_form)

    # Add a combobox from a given collection with a bound method that updates multiple widgets
    ttk.Label(marco_formulario, text="Estado:")\
        .grid(column=6, row=row_form, sticky=tk.E)
    estados_cb = ttk.Combobox(marco_formulario, state="readonly",
        font=("Gotham Light", 10), width=20)
    estados_cb['values'] = ["--", "OK", "INCIDENCIA", "KO"]
    estados_cb.current(0)
    estados_cb.grid(column=7, row=row_form)
    estados_cb.bind("<<ComboboxSelected>>", estado_seleccionado)

    row_form += 1

    ################################################################################
    # Add a separator
    ttk.Separator(marco_formulario,orient='horizontal')\
        .grid(column=0, row=row_form, columnspan=8, sticky='ew', pady=5)
    row_form += 1

    # Section with explicitly defined variables for them to be disabled or enabled
    campo_label = ttk.Label(marco_formulario, text="Campo:", state="disabled")
    campo_label.grid(column=0, row=row_form, sticky=tk.E)
    campo_entry = ttk.Entry(marco_formulario, textvariable=campo, font=("Gotham Light", 10),
        width=22, state="disabled")
    campo_entry.grid(column=1, row=row_form)

    num_label = ttk.Label(marco_formulario, text="Nº llamadas:", state="disabled")
    num_label.grid(column=2, row=row_form, sticky=tk.E)
    num_llamadas.set(0)
    num_entry = ttk.Entry(marco_formulario, textvariable=num_llamadas, font=("Gotham Light", 10),
        width=22, state="disabled")
    num_entry.grid(column=3, row=row_form)

    fres_label = ttk.Label(marco_formulario, text="Fecha\nresolución:", state="disabled")
    fres_label.grid(column=4, row=row_form, sticky=tk.E)
    cal_resolucion = DateEntry(marco_formulario, textvariable=fecha_resolucion,
        font=("Gotham Light", 10), state="disabled", 
        justify=tk.CENTER, width=20, locale='es_ES', date_pattern="dd-MM-yyyy")
    cal_resolucion.grid(column=5, row=row_form)

    opres_label = ttk.Label(marco_formulario, text="Operador\nresolución:", state="disabled")
    opres_label.grid(column=6, row=row_form, sticky=tk.E)
    oper_res_cb = ttk.Combobox(marco_formulario, textvariable=operador_resolucion,
        state="disabled", font=("Gotham Light", 10), width=20)
    oper_res_cb['values'] = [u[1] for u in usuarios]
    oper_res_cb.grid(column=7, row=row_form)

    row_form += 1

    ################################################################################
    # Add a separator
    ttk.Separator(marco_formulario,orient='horizontal')\
        .grid(column=0, row=row_form, columnspan=8, sticky='ew', pady=5)
    row_form += 1

    # Add a text field form comments
    ttk.Label(marco_formulario, text="Observaciones:")\
        .grid(column=2, row=row_form, sticky=tk.E)
    observaciones = tk.Text(marco_formulario, font=("Gotham Light", 10), width=50, 
            height=3, background="#F0F0F0", relief="sunken", wrap=tk.WORD)
    observaciones.grid(column=3, row=row_form, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

    row_form += 1

    ################################################################################
    # Add a separator
    ttk.Separator(marco_formulario,orient='horizontal')\
        .grid(column=0, row=row_form, columnspan=8, sticky='ew', pady=5)
    row_form += 1

    # Resize the grid columns and rows
    tk_utils.redimensionar_filas_columnas(marco_formulario)


    ################################################################################
    # Add a button to submit the form and a button to clear the form
    botones = ttk.Frame(ventana_principal, style="TFrame")
    botones.grid(column=0, row=3, columnspan=4, pady=(10, 10), padx=(10, 10))

    confirmar = ttk.Button(botones, text="Confirmar", command=submit)\
        .grid(column=1, row=0, pady=(10, 20), padx=(0, 15))
    limpiar = ttk.Button(botones, text="Limpiar", command=clear)\
        .grid(column=2, row=0, pady=(10, 20), padx=(15, 0))

    clear()


    ################################################################################
    # Center the window in the screen
    tk_utils.centrar_ventana(ventana_principal)

    # Start GUI
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()