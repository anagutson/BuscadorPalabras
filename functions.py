import tkinter as tk
from tkinter import filedialog
import json
from constants import JSON_FILE, TEXT_FILE

def obtener_grupos(ruta_archivo_copia_seguridad):
    data = leer_archivo(ruta_archivo_copia_seguridad)
    if data is None:
        return []
    chat_names = [chat["chat_name"] for chat in data]
    return chat_names


def cargar_archivo(titulo, tipos_archivo, entrada_widget):
    ruta_archivo = filedialog.askopenfilename(title=titulo, filetypes=tipos_archivo)
    if ruta_archivo:
        entrada_widget.delete(0, tk.END)
        entrada_widget.insert(0, ruta_archivo)

def cargar_archivo_palabras(entrada_palabras):
    cargar_archivo("Seleccionar archivo de palabras", TEXT_FILE, entrada_palabras)    

def cargar_archivo_copia_seguridad(entrada_copia_seguridad, grupo_dropdown, radio_button_grupo):
    cargar_archivo("Seleccionar archivo de copia de seguridad de WhatsApp", JSON_FILE, entrada_copia_seguridad)
    chat_names = obtener_grupos(entrada_copia_seguridad.get())
    if chat_names:
        radio_button_grupo.config(state=tk.NORMAL)
        grupo_dropdown['menu'].delete(0, tk.END)  # Limpiar las opciones existentes
        for chat_name in chat_names:
            grupo_dropdown['menu'].add_command(label=chat_name, command=tk._setit(radio_button_grupo, chat_name))
        radio_button_grupo.set(chat_names[0])  # Establecer el primer grupo como seleccionado


def mostrar_error(mensaje, area_resultados):
    area_resultados.delete('1.0', tk.END)
    area_resultados.insert(tk.END, mensaje)

def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        mostrar_error("Error: El archivo '{}' no existe.".format(ruta_archivo))
    except json.JSONDecodeError:
        mostrar_error("Error: El archivo '{}' no está en formato JSON válido.".format(ruta_archivo))
    return None

def leer_palabras(ruta_archivo, area_resultados):
    try:
        with open(ruta_archivo, 'r') as file:
            palabras = file.read().splitlines()
            return palabras
    except FileNotFoundError:
        mostrar_error("Error: El archivo '{}' no existe.".format(ruta_archivo), area_resultados)
    return None
