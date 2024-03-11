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
