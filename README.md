# Framework para formularios

## Descripción ![Python](imgs/python.png)

Este framework es una herramienta que permite la creación de formularios de manera sencilla y rápida con la librería **Tkinter** de Python.
Hay parametrizados una serie de campos e inputs predefinidos que permiten replicar elementos comunes en los formularios.

## Instalación

Tan solo se debe clonar el repositorio y expandir sobre el esqueleto inicial.

```bash
git clone <url del repositorio>
# Opcional: renombrar el directorio
cd <nombre del repositorio>
rm -rf .git
git init
git commit -m "Initial commit"
# Opcional: crear nuevo repositorio en GitHub
git branch -M main
git remote add origin <url del repositorio>
git push -u origin main
```

## Uso

### Main

El fichero principal es `main.py` y se debe ejecutar con Python 3.8 o superior.
Importa las librerías externas tkinter para el GUI, PIL para las imágenes y configparse para la lectura del fichero de configuración.
Documentación completa en [Python](./docs/main.html).

<details>
  <summary>Detalles</summary>
  
#### Configuración

El fichero de configuración `config.ini` contiene los parámetros de configuración del formulario, como la db a usar, cabeceras, o parámetros de estilo.

```ini
[DB]
DB_FILENAME = template.db

[STYLES]
THEME = light
FONT = Arial 12
```

Se lee el fichero de configuración para poder inicializar.

```python
config = configparser.ConfigParser()
config.read('config.ini')
```

Se crea o importa la base de datos con el nombre indicado en el fichero de configuración.

```python
DB_FILE = config["DB"]["DB_FILENAME"]
DB_FILE = os.path.join(os.path.dirname(__file__), DB_FILE)
database = db.Database(DB_FILE)
```

#### GUI

Se inicializa la ventana principal y se le asigna un título., se definen estilos y se añaden estos estilos a ciertos componentes.

```python
ventana_principal = tk.Tk()
ventana_principal.title("Nombre del servicio")
ventana_principal.resizable(False, False)
ventana_principal.iconbitmap("imgs/favicon.ico")
ventana_principal.configure(background="#FFFFFF")

STYLE_THEME = config["STYLES"]["THEME"]
style = ttk.Style(ventana_principal)
style.configure("TFrame", background="#FFFFFF")
style.configure("TLabel", font=("Gotham", 12), padding=(15, 5, 5, 5), 
    foreground="#00558C", background="#FFFFFF")
style.configure("TButton", font=("Gotham", 12), padding=(5, 5, 5, 5),
    width=16, cursor="hand2", justify=tk.CENTER, background="#FFFFFF")
style.configure("TEntry", font=("Gotham Light", 12), width=22)
```

Después de inicializar la ventana principal, se añaden los componentes del formulario. Se estructura en un `Frame` principal y otros secundarios para cada sección, separados por `Separator`.

Se inicializan las variables principales asociadas a los campos de entrada de datos.

```python
fecha_entrada = tk.StringVar()
identificador = tk.StringVar()
importe = tk.DoubleVar()
campo = tk.StringVar()
num_llamadas = tk.StringVar()
fecha_resolucion = tk.StringVar()
operador_resolucion = tk.StringVar()
observaciones = tk.StringVar()
```

#### Métodos

Se definen métodos con funciones genéricas y útiles para la gestión de eventos.

```python
def buscar_id()
def submit()
def clear()
def toggle_use_incidencias(new_state)
def estado_seleccionado(event)
def verificar_numerico(char)
def exportar_aux()
def exportar(selector, fechas="", window=None)
def verificar_cabeceras(headers)
def verificar_datos(datos)
def importar()
def help()
def about()
```

</details>

### DB

El fichero `db.py` contiene la clase `Database` que permite la conexión y gestión de la base de datos. Se utiliza SQLite3 para la gestión de la base de datos.
Se definen métodos para la creación de la base de datos, la inserción de datos, la consulta de datos y la exportación de datos.
Además de los métodos genéricos, se definen métodos específicos para la gestión de la base de datos de la aplicación.

<details>
  <summary>Detalles</summary>

#### Inicialización DB

Se inicializa la base de datos con el nombre del fichero de la base de datos.

```python
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
```

#### Métodos DB

Se definen métodos para la gestión de registros genéricos, usuarios y logs.

```python
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
```

</details>

### Excel

El fichero `excel.py` contiene la clase `Excel` que permite la gestión de la exportación de datos a ficheros Excel. Usa la librería `openpyxl` para la gestión de ficheros Excel.

<details>
  <summary>Detalles</summary>

#### Inicialización Excel

Se inicializa la clase con los parámetros base vacíos.

```python
def __init__(self):
    """ Constructor """
    self.archivo = ''
    self.libro = ''
    self.hoja = ''
    self.celdas = []
    self.datos = []
    self.columnas = []
    self.filas = []
```

#### Métodos Excel

Se definen métodos para la gestión de la exportación de datos a ficheros Excel, como crear un nuevo archivo, cargar uno existente, gestión de hojas, y formateo de celdas.

```python
def crear_archivo(self, nombre):
    """ Crea un archivo excel """
    self.libro = Workbook()
    self.archivo = nombre
    self.hoja = self.libro.active
    self.hoja.title = 'Registros'
    self.celdas = list(self.hoja)
    self.datos = list(self.hoja.values)
    self.columnas = list(self.hoja.columns)
    self.filas = list(self.hoja.rows)

def crear_hoja(self, nombre):
    """ Crea una hoja en el archivo """
    self.hoja = self.libro.create_sheet(nombre)
    self.celdas = list(self.hoja)
    self.datos = list(self.hoja.values)
    self.columnas = list(self.hoja.columns)
    self.filas = list(self.hoja.rows)

def rellenar_hoja(self, registros):
    """ Rellena la hoja con los registros """
    for registro in registros:
        self.hoja.append(registro)
    self.actualizar_hoja()
```

Se definen métodos para los estilos de las cabeceras y las celdas normales.

```python
def formato_hoja(self):
    """ Formatea la hoja """
    for fila in self.filas[1:]:
        for celda in fila:
            celda.alignment = Alignment(horizontal='center', vertical='center')
            celda.border = Border(
                left = Side(style='thin'), 
                right = Side(style='thin'), 
                top = Side(style='thin'), 
                bottom = Side(style='thin'))
            celda.font = Font(name='Gotham Light', size=10)
    for columna in self.columnas:
        self.hoja.column_dimensions[columna[0].column_letter].width = 20

def formato_cabecera(self):
    """ Formatea la cabecera """
    for celda in self.celdas[0]:
        celda.alignment = Alignment(horizontal='center', vertical='center')
        celda.border = Border(
            left=Side(style='thick'), 
            right=Side(style='thick'), 
            top=Side(style='thick'), 
            bottom=Side(style='thick'))
        celda.font = Font(name='Gotham Bold', size=12)
```

</details>
