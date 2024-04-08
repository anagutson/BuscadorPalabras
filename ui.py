import tkinter as tk
from functions import cargar_archivo_copia_seguridad, cargar_archivo_palabras, leer_archivo, leer_palabras, mostrar_error
from constants import TITLE_FONT_SIZE, TEXT_FONT_SIZE

def mostrar_resultado(chat, mensaje, area_resultados):
    area_resultados.insert(tk.END, "--------------- \n")
    area_resultados.insert(tk.END, "Grupo: " + chat["chat_name"] + "\n")
    area_resultados.insert(tk.END, "Remitente: " + mensaje["sender"] + "\n")
    area_resultados.insert(tk.END, "Día y hora: " + mensaje["timestamp"].replace('T', ' ') + "\n")
    area_resultados.insert(tk.END, "Contenido: " + mensaje["content"] + "\n\n")
    
def buscar_mensajes_en_chat(chat, palabras, area_resultados):
    for mensaje in chat["messages"]:
        contenido = mensaje["content"].lower()
        if any(palabra.lower() in contenido for palabra in palabras):
            mostrar_resultado(chat, mensaje, area_resultados)


def limpiar_area_resultados(area_resultados):
    area_resultados.delete('1.0', tk.END)

def buscar_mensajes(entrada_copia_seguridad, entrada_palabras, radio_grupo, area_resultados):
    ruta_archivo_copia_seguridad = entrada_copia_seguridad.get()
    ruta_archivo_palabras = entrada_palabras.get()
    data = leer_archivo(ruta_archivo_copia_seguridad)
    if data is None:
        return

    palabras = leer_palabras(ruta_archivo_palabras, area_resultados)
    if palabras is None:
        return    

    limpiar_area_resultados(area_resultados)

    filtro = radio_grupo.get()
    if filtro == 'Buscar todos':
        for chat in data:
            buscar_mensajes_en_chat(chat, palabras, area_resultados)
    else:
        for chat in data:
            if chat["chat_name"] == filtro:
                buscar_mensajes_en_chat(chat, palabras, area_resultados)

def create_ui():
    ventana = tk.Tk()
    ventana.title("Buscador de Mensajes de WhatsApp")

    etiqueta_archivos = tk.Label(ventana, text="Archivos", anchor="w", font=TITLE_FONT_SIZE)
    etiqueta_archivos.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    etiqueta_palabras = tk.Label(ventana, text="Archivo de palabras", anchor="w", font=TEXT_FONT_SIZE)
    etiqueta_palabras.grid(row=1, column=0, padx=10, pady=5, sticky="w") 

    entrada_palabras = tk.Entry(ventana, font=TEXT_FONT_SIZE)
    entrada_palabras.grid(row=2, column=0, padx=10, pady=5)

    boton_cargar_palabras = tk.Button(ventana, text="Cargar archivo", font=TEXT_FONT_SIZE, command=lambda: cargar_archivo_palabras(entrada_palabras))
    boton_cargar_palabras.grid(row=2, column=1, padx=10, pady=5)

    etiqueta_copia_seguridad = tk.Label(ventana, text="Archivo de copia de seguridad", anchor="w", font=TEXT_FONT_SIZE)
    etiqueta_copia_seguridad.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    entrada_copia_seguridad = tk.Entry(ventana, font=TEXT_FONT_SIZE)
    entrada_copia_seguridad.grid(row=4, column=0, padx=10, pady=5)

    boton_cargar_copia_seguridad = tk.Button(ventana, text="Cargar archivo", font=TEXT_FONT_SIZE, command=lambda: cargar_archivo_copia_seguridad(entrada_copia_seguridad, grupo_dropdown, radio_button_grupo))
    boton_cargar_copia_seguridad.grid(row=4, column=1, padx=10, pady=5)

    etiqueta_filtrar = tk.Label(ventana, text="Filtrar", anchor="w", font=TITLE_FONT_SIZE)
    etiqueta_filtrar.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    radio_grupo_var = tk.StringVar(value="Buscar todos") 
    radio_button_todos = tk.Radiobutton(ventana, text="Buscar todos", variable=radio_grupo_var, value="Buscar todos", font=TEXT_FONT_SIZE)
    radio_button_todos.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    radio_button_grupo = tk.Radiobutton(ventana, text="Filtrar por grupo", variable=radio_grupo_var, value="", font=TEXT_FONT_SIZE)
    radio_button_grupo.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    radio_button_grupo.config(state=tk.DISABLED)

    grupo_var = tk.StringVar()
    grupo_dropdown = tk.OptionMenu(ventana, grupo_var, "")
    grupo_dropdown.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    grupo_dropdown.config(state=tk.DISABLED)

    boton_buscar = tk.Button(ventana, text="Buscar mensajes", command=lambda: buscar_mensajes(entrada_copia_seguridad, entrada_palabras, radio_grupo_var, area_resultados))  # Pasamos la variable del botón de radio
    boton_buscar.grid(row=9, column=0, columnspan=3, padx=10, pady=5)
    
    etiqueta_resultados = tk.Label(ventana, text="Resultados", anchor="w", font=TITLE_FONT_SIZE)
    etiqueta_resultados.grid(row=10, column=0, padx=10, pady=5, sticky="w")

    area_resultados = tk.Text(ventana, width=60, height=10)
    area_resultados.grid(row=11, column=0, columnspan=3, padx=10, pady=5)

    # Ejecutar la ventana
    ventana.mainloop()

create_ui()