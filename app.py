from datetime import datetime
import customtkinter as ctk
from tkinter import (colorchooser,Menu,
                    messagebox,
                    filedialog,
                    END,
                    re,
                    ttk,
                    IntVar,
                    Scrollbar,
                    VERTICAL,
                    HORIZONTAL,
                    RIGHT,
                    Y,X,BOTTOM,NO,YES,W)
from matplotlib.figure import Figure    
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import sqlite3
import os
import seaborn as sns
import matplotlib.ticker as mticker
import time
import pandas as pd
import gc

# Funciones para crear objetos
def crear_etiqueta(tipo,texto):
    if tipo == "tabla1":
        return ctk.CTkLabel(ventana_datos,
                            text=texto,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color=color_etiquetas,
                            bg_color=color_ventanas)
    elif tipo == "tabla2":
        return ctk.CTkLabel(ventana_filtrar,
                            text=texto,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color=color_etiquetas,
                            bg_color=color_ventanas)
    elif tipo == "tabla_usuarios":
        return ctk.CTkLabel(ventana_usuarios,
                            text=texto,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color=color_etiquetas,
                            bg_color=color_ventanas)
def crear_entrada(tipo):
    if tipo == "tabla1":
        return ctk.CTkEntry(ventana_datos,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color="#b3e5fc",
                            bg_color=color_ventanas,
                            border_color="#b3e5fc")
    elif tipo == "tabla2":
        return ctk.CTkEntry(ventana_filtrar,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color="#b3e5fc",
                            bg_color=color_ventanas,
                            border_color="#b3e5fc")
    elif tipo == "tabla_usuarios":
        return ctk.CTkEntry(ventana_usuarios,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color="#b3e5fc",
                            bg_color=color_ventanas,
                            border_color=color_ventanas)
    elif tipo == "ventana_login":
        return ctk.CTkEntry(ventana_login,
                            text_font=("helvetica",10),
                            text_color="black",
                            fg_color="#b3e5fc",
                            bg_color="#b3e5fc",
                            border_color="#b3e5fc")
def crear_boton(main,texto,fuente_texto,color_texto,plano_color,fondo_color,comando):
    return ctk.CTkButton(main,
                        text=texto,
                        text_font=fuente_texto,
                        text_color=color_texto,
                        fg_color=plano_color,
                        bg_color=fondo_color,
                        command=comando)

#------------------------------------------------------------------------------------------------
#          Programa Principal - ( Se ejecuta si el usuario y contraseña es correcto )           |   
#------------------------------------------------------------------------------------------------

def ventana_principal():
    global ventana
    global ventana_grafico
    global fig
    global canvas
    global grafico_seleccionado
    global diccionario_compartido
    global ventana_calculadora
    global ventana_documentos
    global color_ventanas
    global color_botones
    global color_tablas_distinto
    global color_tablas_igual
    global color_tablas_seleccion
    global color_titulos
    global color_etiquetas
    global color_entradas
    
    color_ventanas = "#0080c0"
    color_botones = "#00acc1"
    color_etiquetas = "#64b5f6"
    color_tablas_distinto = "#90caf9"
    color_tablas_igual = "#42a5f5"
    color_tablas_seleccion = "#0d47a1"
    color_titulos = "#64b5f6"
    color_entradas = "#b3e5fc"
    
    ventana=ctk.CTk()
    w = 1589 # width for the Tk root
    h = 1080 # height for the Tk root
    ws = ventana.winfo_screenwidth() # width of the screen
    hs = ventana.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    ventana.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    ventana.resizable(width=False, height=False)
    
    ventana.configure(background="#212121")

    # Definir parametros de graficos
    
    ventana_grafico = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_grafico.place(x=800,y=576,height=400,width=770)
    fig = Figure(figsize = (8, 5), dpi = 90)
    canvas = FigureCanvasTkAgg(fig,master = ventana_grafico)
    grafico_seleccionado = "ventas"
    diccionario_compartido = {} 
    sns.set(rc={'axes.facecolor':color_entradas})

    # Ventana de calculadora
    ventana_calculadora = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_calculadora.place(x=20,y=675,height=301,width=245)
    
    # Ventana de documentos usados

    ventana_documentos = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_documentos.place(x=275,y=675,height=301,width=515)
def crear_estilo():
    global estilo
    estilo = ttk.Style()
    # Temas : ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    estilo.theme_use("default")
    estilo.configure("Treeview",
                    background = color_ventanas,
                    foreground = color_ventanas,
                    rowheight  = 25,
                    fieldbackground = color_ventanas)


    estilo.map("Treeview",background=[("selected","#347083")])
def crear_lista_ventana():
    global tabla_ventana
    global tabla1
    global tabla_ventana_marco

    tabla_ventana_marco = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    tabla_ventana_marco.place(x=20,y=20,height=330,width=770)

    tabla_ventana = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    tabla_ventana.place(x=30,y=30,height=300,width=749) 

    # Scroll barra
    scroll_vertical_tabla = Scrollbar(tabla_ventana,orient=VERTICAL)
    scroll_vertical_tabla.pack(side = RIGHT, fill = Y)

    scroll_horizontal_tabla = Scrollbar(tabla_ventana,
                                        orient=HORIZONTAL)
    
    scroll_horizontal_tabla.pack(side = BOTTOM, fill = X)

    tabla1 = ttk.Treeview(   tabla_ventana,
                            yscrollcommand=scroll_vertical_tabla.set,
                            xscrollcommand=scroll_horizontal_tabla.set, 
                            selectmode="extended")

    scroll_horizontal_tabla.config(command=tabla1.xview)
    scroll_vertical_tabla.config(command=tabla1.yview)
    
    tabla1.pack()

    tabla1["columns"] = ("oID",
                        "Nombre",
                        "Apellido",
                        "Ciudad",
                        "Provincia",
                        "Codigo Postal",
                        "Direccion",
                        "Telefono",
                        "Correo",
                        "Descripcion",
                        "Producto Favorito",
                        "Ventas",
                        "Saldo",
                        "Inicio Actividad",
                        "Ultima Venta",)
    
    tabla1.column("#0", width=-1, stretch=NO)
    tabla1.column("oID",anchor="center", width=30)
    tabla1.column("Nombre",anchor="center", width=140)
    tabla1.column("Apellido",anchor="center", width=140)
    tabla1.column("Ciudad",anchor="center", width=140)
    tabla1.column("Provincia",anchor="center", width=140)
    tabla1.column("Codigo Postal",anchor="center", width=140)
    tabla1.column("Direccion",anchor="center", width=140)
    tabla1.column("Telefono",anchor="center", width=140)
    tabla1.column("Correo",anchor="center", width=140)
    tabla1.column("Descripcion",anchor="center", width=140)
    tabla1.column("Producto Favorito",anchor="center", width=140)
    tabla1.column("Ventas",anchor="center", width=140)
    tabla1.column("Saldo",anchor="center", width=140)
    tabla1.column("Inicio Actividad",anchor="center", width=140)
    tabla1.column("Ultima Venta",anchor="center", width=140)

    tabla1.heading("#0",text="", anchor=W)
    tabla1.heading("oID",text= "oID",anchor="center")
    tabla1.heading("Nombre",text="Nombre", anchor="center")
    tabla1.heading("Apellido",text="Apellido", anchor="center")
    tabla1.heading("Ciudad",text= "Ciudad",anchor="center")
    tabla1.heading("Provincia",text= "Provincia",anchor="center")
    tabla1.heading("Codigo Postal",text= "Codigo Postal",anchor="center")
    tabla1.heading("Direccion",text= "Direccion",anchor="center")
    tabla1.heading("Telefono",text= "Telefono",anchor="center")
    tabla1.heading("Correo",text= "Correo",anchor="center")
    tabla1.heading("Descripcion",text= "Descripcion",anchor="center")
    tabla1.heading("Producto Favorito",text= "Producto Favorito",anchor="center")
    tabla1.heading("Ventas",text= "Ventas",anchor="center")
    tabla1.heading("Saldo",text= "Saldo",anchor="center")
    tabla1.heading("Inicio Actividad",text= "Inicio Actividad",anchor="center")
    tabla1.heading("Ultima Venta",text= "Ultima Venta",anchor="center")
    
    # Crear filas con colores distintos diferenciando cada campo

    tabla1.tag_configure("oddrow", background="#e0f7fa")
    tabla1.tag_configure("evenrow", background="#80deea")
def agregar_entrada_registros():
    global ventana_datos,titulo_ingreso_datos,nombre_etiqueta,apellido_etiqueta,ciudad_etiqueta,provincia_etiqueta,codigo_postal_etiqueta,direccion_etiqueta,telefono_etiqueta,correo_etiqueta,descripcion_etiqueta,producto_etiqueta,ventas_etiqueta,saldo_etiqueta,inicio_etiqueta,ultima_etiqueta,nombre_entrada,apellido_entrada,ciudad_entrada,provincia_entrada,codigo_postal_entrada,direccion_entrada,telefono_entrada,correo_entrada,descripcion_entrada,producto_entrada,ventas_entrada,saldo_entrada,inicio_entrada,ultima_entrada,id_entrada,id_etiqueta
    global lista_entradas,lista_etiquetas
    ventana_datos = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_datos.place(x=20,y=358,height=200,width=770)
    
    #-------------Texto-----------
    titulo_ingreso_datos = ctk.CTkLabel(ventana_datos,text="AGREGAR NUEVOS REGISTROS",text_font=("helvetica",9),
                                        text_color="black",fg_color="#64b5f6")

    titulo_ingreso_datos.place(x=140,y=10,height=20,width=500)

    # --------------------- ENTRADA DE DATOS -----------------------
    # Etiquetas
    nombre_etiqueta = crear_etiqueta("tabla1","Nombre") 
    apellido_etiqueta = crear_etiqueta("tabla1","Apellido") 
    ciudad_etiqueta = crear_etiqueta("tabla1","Ciudad") 
    provincia_etiqueta = crear_etiqueta("tabla1","Provincia") 
    codigo_postal_etiqueta = crear_etiqueta("tabla1","Codigo Postal") 
    direccion_etiqueta = crear_etiqueta("tabla1","Direccion") 
    telefono_etiqueta = crear_etiqueta("tabla1","Telefono") 
    correo_etiqueta = crear_etiqueta("tabla1","Correo") 
    descripcion_etiqueta = crear_etiqueta("tabla1","Descripcion") 
    producto_etiqueta = crear_etiqueta("tabla1","Producto") 
    ventas_etiqueta = crear_etiqueta("tabla1","Ventas") 
    saldo_etiqueta = crear_etiqueta("tabla1","Saldo") 
    inicio_etiqueta = crear_etiqueta("tabla1","Inicio") 
    ultima_etiqueta = crear_etiqueta("tabla1","Ultima") 
    id_etiqueta = crear_etiqueta("tabla1","ID") 
    # Entradas
    nombre_entrada  = crear_entrada("tabla1")
    apellido_entrada  = crear_entrada("tabla1")
    ciudad_entrada  = crear_entrada("tabla1")
    provincia_entrada  = crear_entrada("tabla1")
    codigo_postal_entrada  = crear_entrada("tabla1")
    direccion_entrada  = crear_entrada("tabla1")
    telefono_entrada  = crear_entrada("tabla1")
    correo_entrada  = crear_entrada("tabla1")
    descripcion_entrada  = crear_entrada("tabla1")
    producto_entrada  = crear_entrada("tabla1")
    ventas_entrada  = crear_entrada("tabla1")
    saldo_entrada  = crear_entrada("tabla1")
    inicio_entrada  = crear_entrada("tabla1")
    ultima_entrada  = crear_entrada("tabla1")
    id_entrada  = crear_entrada("tabla1")
    
    # -------------------- Ubicar cada objeto en la ventana de agregar datos ----------------------
    
    lista_entradas = [ nombre_entrada,apellido_entrada,ciudad_entrada,provincia_entrada,
                    codigo_postal_entrada,direccion_entrada,telefono_entrada,correo_entrada,
                    descripcion_entrada,producto_entrada,ventas_entrada,saldo_entrada,
                    inicio_entrada,ultima_entrada,id_entrada]
    
    lista_etiquetas = [ nombre_etiqueta,apellido_etiqueta,ciudad_etiqueta,provincia_etiqueta,
                        codigo_postal_etiqueta,direccion_etiqueta,telefono_etiqueta,correo_etiqueta,
                        descripcion_etiqueta,producto_etiqueta,ventas_etiqueta,saldo_etiqueta,
                        inicio_etiqueta,ultima_etiqueta,id_etiqueta]
    
    # cada 5 a + 240
    # cada 5 b + 240
    # cada 1 c +  30    45 , 75 , 105 , 135 , 165 despues de 5 reset

    a,b,c,contador = 30,140,45,1
    
    for x in lista_etiquetas:
        x.place(x=a,y=c,height=20,width=100)
        if contador == 5:
            a +=240
            c = 45
            contador = 1
        else:
            contador +=1
            c += 30
    
    a,b,c,contador = 30,140,45,1
    
    for x in lista_entradas:
        x.place(x=b,y=c,height=20,width=120)
        if contador == 5:
            b +=240
            c = 45
            contador = 1
        else:
            contador += 1
            c += 30
def agregar_botones_datos():
    global ventana_botones_datos
    global boton_actualizar
    global boton_agregar
    global boton_remover_seleccionado
    global boton_remover_varios
    global boton_mover_arriba
    global boton_mover_abajo
    global boton_remover_varios
    global boton_borrar_entradas
    global valor
    global lista_botones_tabla1
    
    #---------Ventana------------
    
    ventana_botones_datos = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_botones_datos.place(x=20,y=565,height=100,width=770)
    
    #---------- Crear Botones -----------

    boton_agregar = crear_boton(ventana_botones_datos,"Agregar Registro",("helvetica",10),"black",color_botones,color_ventanas,agregar_registro)
    boton_actualizar = crear_boton(ventana_botones_datos,"Actualizar Registro",("helvetica",10),"black",color_botones,color_ventanas,actualizar_registro)
    boton_remover_seleccionado = crear_boton(ventana_botones_datos,"Quitar Registro",("helvetica",10),"black",color_botones,color_ventanas,remover_registro_seleccionado)
    boton_remover_varios = crear_boton(ventana_botones_datos,"Quitar Varios",("helvetica",10),"black",color_botones,color_ventanas,remover_varios_registro)
    boton_mover_arriba = crear_boton(ventana_botones_datos,"Mover Arriba",("helvetica",10),"black",color_botones,color_ventanas,mover_arriba_registro)
    boton_mover_abajo = crear_boton(ventana_botones_datos,"Mover Abajo",("helvetica",10),"black",color_botones,color_ventanas,mover_abajo_registro)
    boton_borrar_entradas = crear_boton(ventana_botones_datos,"Borrar Entradas",("helvetica",10),"black",color_botones,color_ventanas,borrar_entradas)
    
    #------------ Crear Lista de Botones --------

    lista_botones_tabla1 = [boton_agregar,
                            boton_actualizar,
                            boton_remover_seleccionado,
                            boton_remover_varios,
                            boton_mover_arriba,
                            boton_mover_abajo,
                            boton_borrar_entradas]
    
    #---------- Ubicar en la grilla -----------
    
    boton_agregar.place(x=115,y=20,height=25,width=130)
    boton_actualizar.place(x=115,y=50,height=25,width=130)
    boton_remover_seleccionado.place(x=255,y=20,height=25,width=130)
    boton_remover_varios.place(x=255,y=50,height=25,width=130)
    boton_mover_arriba.place(x=395,y=20,height=25,width=130)
    boton_mover_abajo.place(x=395,y=50,height=25,width=130)
    boton_borrar_entradas.place(x=535,y=35,height=25,width=130)

    valor = 0

    # --------- Seleccionar Registro Bind -----------

    tabla1.bind("<ButtonRelease-1>",seleccionar_registro)

#------------------------------------------------------------------------------------------------
#                       Analisis - ( Filtro de busqueda y Botones )                             |   
#------------------------------------------------------------------------------------------------

def crear_tabla_2():

    global ventana_tabla2
    global tabla2
    global tabla2_ventana_marco
    
    tabla2_ventana_marco = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    tabla2_ventana_marco.place(x=799,y=20,height=330,width=770)

    ventana_tabla2 = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_tabla2.place(x=809,y=30,height=300,width=749)

    # Scroll barra
    scroll_vertical_tabla2 = Scrollbar(ventana_tabla2,orient=VERTICAL)
    scroll_vertical_tabla2.pack(side = RIGHT, fill = Y)

    scroll_horizontal_tabla2 = Scrollbar(ventana_tabla2,orient=HORIZONTAL)
    scroll_horizontal_tabla2.pack(side = BOTTOM, fill = X)

    tabla2 = ttk.Treeview(   ventana_tabla2,
                            yscrollcommand=scroll_vertical_tabla2.set,
                            xscrollcommand=scroll_horizontal_tabla2.set, 
                            selectmode="extended")

    scroll_horizontal_tabla2.config(command=tabla2.xview)
    scroll_vertical_tabla2.config(command=tabla2.yview)
    
    tabla2.pack()

    tabla2["columns"] = ("oID",
                        "Nombre",
                        "Apellido",
                        "Ciudad",
                        "Provincia",
                        "Codigo Postal",
                        "Direccion",
                        "Telefono",
                        "Correo",
                        "Descripcion",
                        "Producto Favorito",
                        "Ventas",
                        "Saldo",
                        "Inicio Actividad",
                        "Ultima Venta",)
    
    tabla2.column("#0", width=-1, stretch=NO)
    tabla2.column("oID",anchor="center", width=30)
    tabla2.column("Nombre",anchor="center", width=140)
    tabla2.column("Apellido",anchor="center", width=140)
    tabla2.column("Ciudad",anchor="center", width=140)
    tabla2.column("Provincia",anchor="center", width=140)
    tabla2.column("Codigo Postal",anchor="center", width=140)
    tabla2.column("Direccion",anchor="center", width=140)
    tabla2.column("Telefono",anchor="center", width=140)
    tabla2.column("Correo",anchor="center", width=140)
    tabla2.column("Descripcion",anchor="center", width=140)
    tabla2.column("Producto Favorito",anchor="center", width=140)
    tabla2.column("Ventas",anchor="center", width=140)
    tabla2.column("Saldo",anchor="center", width=140)
    tabla2.column("Inicio Actividad",anchor="center", width=140)
    tabla2.column("Ultima Venta",anchor="center", width=140)

    tabla2.heading("#0",text="", anchor=W)
    tabla2.heading("oID",text= "oID",anchor="center")
    tabla2.heading("Nombre",text="Nombre", anchor="center")
    tabla2.heading("Apellido",text="Apellido", anchor="center")
    tabla2.heading("Ciudad",text= "Ciudad",anchor="center")
    tabla2.heading("Provincia",text= "Provincia",anchor="center")
    tabla2.heading("Codigo Postal",text= "Codigo Postal",anchor="center")
    tabla2.heading("Direccion",text= "Direccion",anchor="center")
    tabla2.heading("Telefono",text= "Telefono",anchor="center")
    tabla2.heading("Correo",text= "Correo",anchor="center")
    tabla2.heading("Descripcion",text= "Descripcion",anchor="center")
    tabla2.heading("Producto Favorito",text= "Producto Favorito",anchor="center")
    tabla2.heading("Ventas",text= "Ventas",anchor="center")
    tabla2.heading("Saldo",text= "Saldo",anchor="center")
    tabla2.heading("Inicio Actividad",text= "Inicio Actividad",anchor="center")
    tabla2.heading("Ultima Venta",text= "Ultima Venta",anchor="center")
    
    # Crear filas con colores distintos diferenciando cada campo

    tabla2.tag_configure("oddrow", background="#e0f7fa")
    tabla2.tag_configure("evenrow", background="#80deea")
def agregar_herramientas_tabla2():
    global ventana_filtrar
    global Buscar,Resetear
    global ventana_botones_graficos
    global boton_grafico_provincia
    global boton_grafico_ventas
    global boton_grafico_ciudad
    global boton_grafico_producto
    #--------------------------------
    global campo_filtrar_etiqueta1
    global columna_filtrar_etiqueta1
    global columna_filtrar_entrada1
    global campo_filtrar_entrada1
    #--------------------------------
    global columna_filtrar_entrada2
    global campo_filtrar_entrada2
    global campo_filtrar_etiqueta2
    global columna_filtrar_etiqueta2
    #--------------------------------
    global columna_filtrar_entrada3
    global campo_filtrar_entrada3
    global campo_filtrar_etiqueta3
    global columna_filtrar_etiqueta3
    
    ventana_filtrar = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_filtrar.place(x=799,y=358,height=100,width=770)

    ventana_botones_graficos = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_botones_graficos.place(x=799,y=467,height=100,width=770)

    #-------------------------------------------------------------------------------
    campo_filtrar_etiqueta1 = crear_etiqueta("tabla2","Campo n°1")
    columna_filtrar_etiqueta1 = crear_etiqueta("tabla2","Columna n°1")
    campo_filtrar_etiqueta2 =crear_etiqueta("tabla2","Campo n°2")
    columna_filtrar_etiqueta2 = crear_etiqueta("tabla2","Columna n°2")
    campo_filtrar_etiqueta3 = crear_etiqueta("tabla2","Campo n°3")
    columna_filtrar_etiqueta3 = crear_etiqueta("tabla2","Columna n°3")
    
    campo_filtrar_entrada1 = crear_entrada("tabla2")
    columna_filtrar_entrada1 = crear_entrada("tabla2")
    campo_filtrar_entrada2 = crear_entrada("tabla2")
    columna_filtrar_entrada2 = crear_entrada("tabla2")
    campo_filtrar_entrada3 = crear_entrada("tabla2")
    columna_filtrar_entrada3 = crear_entrada("tabla2")
    
    espaciado = 10
    
    campo_filtrar_etiqueta1.place(      x=110   ,y=25,height=20,width=87)     
    columna_filtrar_etiqueta1.place(    x=110   ,y=55,height=20,width=87)
    campo_filtrar_etiqueta2.place(      x=315   ,y=25,height=20,width=87)            
    columna_filtrar_etiqueta2.place(    x=315   ,y=55,height=20,width=87)
    campo_filtrar_etiqueta3.place(      x=520   ,y=25,height=20,width=87)
    columna_filtrar_etiqueta3.place(    x=520   ,y=55,height=20,width=87)
    #---------------------------------------------------------------
    campo_filtrar_entrada1.place(   x = 110 + 85 + espaciado   ,y=25,height=20,width=100)
    columna_filtrar_entrada1.place( x = 110 + 85 + espaciado   ,y=55,height=20,width=100)
    campo_filtrar_entrada2.place(   x = 315 + 85 + espaciado   ,y=25,height=20,width=100)
    columna_filtrar_entrada2.place( x = 315 + 85 + espaciado   ,y=55,height=20,width=100)
    campo_filtrar_entrada3.place(   x = 520 + 85 + espaciado   ,y=25,height=20,width=100)
    columna_filtrar_entrada3.place( x = 520 + 85 + espaciado   ,y=55,height=20,width=100)

    Buscar                  = crear_boton(ventana_filtrar,"Buscar",("helvetica",10),"black",color_botones,color_ventanas,busqueda_filtrada)
    Resetear                = crear_boton(ventana_filtrar,"Resetear",("helvetica",10),"black",color_botones,color_ventanas,resetear)
    boton_grafico_ventas    = crear_boton(ventana_botones_graficos,"Ventas/ID",("helvetica",10),"black",color_botones,color_ventanas,grafico_ventas)
    boton_grafico_ciudad    = crear_boton(ventana_botones_graficos,"Ventas/Ciudad",("helvetica",10),"black",color_botones,color_ventanas,grafico_ciudad)
    boton_grafico_provincia = crear_boton(ventana_botones_graficos,"Ventas/Provincia",("helvetica",10),"black",color_botones,color_ventanas,grafico_provincia)
    boton_grafico_producto  = crear_boton(ventana_botones_graficos,"Producto Favorito",("helvetica",10),"black",color_botones,color_ventanas,grafico_producto_favorito)
    
    Buscar.place(x=20,y=20,height=28,width=70)
    Resetear.place(x=20,y=50,height=28,width=70)
    boton_grafico_ventas.place(x=40,y=20,height=28,width=120)
    boton_grafico_ciudad.place(x=40,y=55,height=28,width=120)
    boton_grafico_provincia.place(x=180,y=20,height=28,width=120)
    boton_grafico_producto.place(x=180,y=55,height=28,width=120)
def busqueda_filtrada():
    global registros
    # Limpiar datos de la tabla ( TREEVIEW )
    
    tabla2.delete(*tabla2.get_children())

    # Datos para filtrar

    columna_filtrada1 = str(columna_filtrar_entrada1.get())
    campo_filtrado1 = str(campo_filtrar_entrada1.get())

    columna_filtrada2 = str(columna_filtrar_entrada2.get())
    campo_filtrado2 = str(campo_filtrar_entrada2.get())
    
    columna_filtrada3 = str(columna_filtrar_entrada3.get())
    campo_filtrado3 = str(campo_filtrar_entrada3.get())
    #------------------- Filtrado por 1 campo y 1 columna -------------------------
    if  (len(columna_filtrada1) > 2 and len(campo_filtrado1) > 2 and
        len(columna_filtrada2) == 0 and len(campo_filtrado2) == 0 and
        len(columna_filtrada3) == 0 and len(campo_filtrado3) == 0 ):
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()   
            c.execute("SELECT rowid,* FROM clientes WHERE "+columna_filtrada1+" like ?", (campo_filtrado1,))
            registros = c.fetchall()
            
            # Funcion para agregar a la tabla del programa
            agregar_datos_a_treeview("tabla2")
            conexion.commit()
            conexion.close()
    
    # ------------------- Filtrado por 2 campo y 2 columna -------------------------
    if  (len(columna_filtrada1) > 2 and len(campo_filtrado1) > 2 and 
        len(columna_filtrada2) > 2 and len(campo_filtrado2) > 2 and
        len(columna_filtrada3) == 0 and len(campo_filtrado3) == 0):
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()
            c.execute("SELECT rowid,* FROM clientes WHERE "+columna_filtrada1+" like ? AND "+columna_filtrada2+" like ?",(campo_filtrado1,campo_filtrado2))
            registros = c.fetchall()
            
            
            # Funcion para agregar a la tabla del programa
            agregar_datos_a_treeview("tabla2")
            conexion.commit()
            conexion.close()

    if  (len(columna_filtrada1) > 2 and len(campo_filtrado1) > 2 and 
        len(columna_filtrada2) > 2 and len(campo_filtrado2) > 2 and
        len(columna_filtrada3) > 2 and len(campo_filtrado3) > 2):
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()
            c.execute("SELECT rowid,* FROM clientes WHERE "+columna_filtrada1+" like ? AND "+columna_filtrada2+" like ? AND "+columna_filtrada3+" like ?",(campo_filtrado1,campo_filtrado2,campo_filtrado3))
            registros = c.fetchall()
            
            
            # Funcion para agregar a la tabla del programa
            agregar_datos_a_treeview("tabla2")
            conexion.commit()
            conexion.close()
def resetear():

    # Limpiar datos de la tabla n°2 
    
    tabla2.delete(*tabla2.get_children())

    # Limpiar casillas entradas

    columna_filtrar_entrada1.delete(0,END)
    campo_filtrar_entrada1.delete(0,END)

    columna_filtrar_entrada2.delete(0,END)
    campo_filtrar_entrada2.delete(0,END)

    columna_filtrar_entrada3.delete(0,END)
    campo_filtrar_entrada3.delete(0,END)

#------------------------------------------------------------------------------------------------
#                       Base de datos - ( Crear, agregar datos a las tablas )                   |   
#------------------------------------------------------------------------------------------------

def crear_base_de_datos(crear_tabla_clientes,crear_tabla_archivos,crear_tabla_usuarios):
    
    # Tabla clientes
    if crear_tabla_clientes == True:
        datos_test = [  ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"],
                        ["Franco","Micheletti","Rosario","Santa Fe","2000","Alvear 384","4367870","franco_urquiza@hotmail.com","Alumno","Barras Metalicas",10532,43234.00,"26/03/2019","24/04/2022"]]
        
        conexion = sqlite3.connect("tabla_crm.db")
        c = conexion.cursor()
        c.execute("""CREATE TABLE if not exists clientes (
            nombre text,
            apellido text,
            ciudad text,
            provincia text,
            codigo_postal text,
            direccion text,
            telefono text,
            correo text,
            descripcion text,
            producto_favorito text,
            ventas integer,
            saldo real,
            inicio_actividad text,
            ultima_venta text)""")
        for registro in datos_test:
            c.execute("INSERT INTO clientes VALUES ( :nombre, :apellido, :ciudad, :provincia, :codigo_postal, :direccion, :telefono, :correo,:descripcion, :producto_favorito, :ventas, :saldo, :inicio_actividad, :ultima_venta)",
            
                    { 
                    "nombre":registro[0],
                    "apellido":registro[1],
                    "ciudad":registro[2],
                    "provincia":registro[3],
                    "codigo_postal":registro[4],
                    "direccion":registro[5],
                    "telefono":registro[6],
                    "correo":registro[7],
                    "descripcion":registro[8],
                    "producto_favorito":registro[9],
                    "ventas":registro[10],
                    "saldo":registro[11],
                    "inicio_actividad":registro[12],
                    "ultima_venta":registro[13]          })
        conexion.commit()
        conexion.close()

    # Tabla archivos_almacenados
    if crear_tabla_archivos == True:
        datos_archivos = [  ["","","","","","",""] ]
        
        conexion = sqlite3.connect("tabla_crm.db")
        c = conexion.cursor()
        c.execute("""CREATE TABLE if not exists archivos (
            ruta_archivo1 text,
            ruta_archivo2 text,
            ruta_archivo3 text,
            ruta_archivo4 text,
            ruta_archivo5 text,
            ruta_archivo6 text,
            ruta_archivo7 text )""")
        
        for registro_ in datos_archivos:
            c.execute("INSERT INTO archivos VALUES ( :ruta_archivo1,:ruta_archivo2,:ruta_archivo3,:ruta_archivo4,:ruta_archivo5,:ruta_archivo6,:ruta_archivo7 )",
            
                    { "ruta_archivo1":registro_[0],
                    "ruta_archivo2":registro_[1],
                    "ruta_archivo3":registro_[2],
                    "ruta_archivo4":registro_[3],
                    "ruta_archivo5":registro_[4],
                    "ruta_archivo6":registro_[5],
                    "ruta_archivo7":registro_[6]   } )        
    
        conexion.commit()
        conexion.close()

    # Tabla usuarios del programa
    if crear_tabla_usuarios == True:
        
        # Borrar la tabla anterior
        conexion = sqlite3.connect("tabla_crm.db")
        c = conexion.cursor()
        c.execute("""DROP TABLE usuarios""")
        conexion.commit()
        conexion.close()

        # Crear la tabla con el usuario admin
        datos_usuarios = [  ["franco","123456","si","si","si","si"] ]
        conexion = sqlite3.connect("tabla_crm.db")
        c = conexion.cursor()
        c.execute("""CREATE TABLE if not exists usuarios (
            nombre text,
            contraseña text,
            permiso_agregar text,
            permiso_actualizar text,
            permiso_borrar text,
            permiso_admin_usuarios )""")

        for registro_usuario in datos_usuarios:
            c.execute("""INSERT INTO usuarios VALUES ( :nombre,
                                                        :contraseña,
                                                        :permiso_agregar,
                                                        :permiso_actualizar,
                                                        :permiso_borrar,
                                                        :permiso_admin_usuarios )""",
            
                    { "nombre":registro_usuario[0],
                    "contraseña":registro_usuario[1],
                    "permiso_agregar":registro_usuario[2],
                    "permiso_actualizar":registro_usuario[3],
                    "permiso_borrar":registro_usuario[4],
                    "permiso_admin_usuarios":registro_usuario[5] } )        
    
        conexion.commit()
        conexion.close()
def agregar_datos_a_treeview(tabla):
    
    if tabla == "tabla1":

        contador = 0
        for registro in registros:
            if contador % 2 == 0:
                tabla1.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=(registro[0],
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                        registro[10],
                        registro[11],
                        registro[12],
                        registro[13],
                        registro[14]),
                        tags="evenrow")
            else: 
                tabla1.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=(registro[0],
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                        registro[10],
                        registro[11],
                        registro[12],
                        registro[13],
                        registro[14]),
                        tags="oddrow")
            contador +=1
    elif tabla == "tabla2":
        contador = 0
        for registro in registros:
            if contador % 2 == 0:
                tabla2.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=(registro[0],
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                        registro[10],
                        registro[11],
                        registro[12],
                        registro[13],
                        registro[14]),
                        tags="evenrow")
            else: 
                tabla2.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=(registro[0],
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                        registro[10],
                        registro[11],
                        registro[12],
                        registro[13],
                        registro[14]),
                        tags="oddrow")
            contador +=1
    elif tabla == "tabla_usuarios":
        contador = 0
        for registro in registros:
            if contador % 2 == 0:
                tabla_usuarios.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=( registro[0],
                         registro[1],
                         registro[3],
                         registro[4],
                         registro[5],
                         registro[6] ),
                        tags="evenrow")
            else: 
                tabla_usuarios.insert(parent="", 
                index="end", 
                id=contador, 
                text="", 
                values=( registro[0],
                         registro[1],
                         registro[3],
                         registro[4],
                         registro[5],
                         registro[6] ),
                        tags="oddrow")
            contador +=1
def mover_datos_base_a_programa():
    global registros
    conexion = sqlite3.connect("tabla_crm.db")

    c = conexion.cursor()   

    c.execute("SELECT rowid,* FROM clientes")
    
    registros = c.fetchall()

    agregar_datos_a_treeview("tabla1")

    conexion.commit()

    conexion.close()
def mover_datos_base_a_usuarios():

    global registros
    conexion = sqlite3.connect("tabla_crm.db")

    c = conexion.cursor()   

    c.execute("SELECT rowid,* FROM usuarios")
    
    registros = c.fetchall()

    agregar_datos_a_treeview("tabla_usuarios")

    conexion.commit()

    conexion.close()

#------------------------------------------------------------------------------------------------
#                       Graficos - ( Generar graficos , depende de los datos )                  |   
#------------------------------------------------------------------------------------------------

def grafico_ventas():
    global grafico_seleccionado
    grafico_seleccionado = grafico_seleccionado
    global ax,canvas,fig,id,ventas,ventana_grafico
    canvas.flush_events()
    diccionario_compartido = {}
    gc.collect()
    ventana_grafico.destroy()
    ventana_grafico = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_grafico.place(x=800,y=576,height=400,width=770)
    for id in tabla1.get_children():
        diccionario_compartido[id] = tabla1.item(id,"values")[11]

    fig = Figure(figsize = (9, 5), dpi = 80)
    id = [(int(x)+1) for x in diccionario_compartido.keys() ]
    ventas = [int(tabla1.item(x,"values")[11]) for x in diccionario_compartido.keys() ]
    
    ax = fig.subplots()
    
    sns.barplot(x=id,y=ventas,ax=ax,ci=None)
    ax.set(ylabel='VENTAS')
    ax.set(xlabel='ID')
    ax.tick_params(axis='x', rotation=0)
    fig.patch.set_facecolor(color_ventanas)
    # Acomodar eje X cuando hay mas de 30 registros
    if len(id) > 30:
        Locator = mticker.MultipleLocator(round(len(id)/10))
        ax.xaxis.set_major_locator(Locator)
    
    # Creating the Tkinter canvas containing the Matplotlib figure   
    canvas = FigureCanvasTkAgg(fig,master = ventana_grafico)
    # Placing the canvas on the Tkinter window  
    canvas.get_tk_widget().grid(column=0,row=0)
    
    grafico_seleccionado = "ventas"
def grafico_ciudad():
    global grafico_seleccionado
    grafico_seleccionado = grafico_seleccionado
    global ax,canvas,fig,ciudades,ventas,ventana_grafico
    canvas.flush_events()
    diccionario_compartido = {}
    gc.collect()
    ventana_grafico.destroy()
    ventana_grafico = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_grafico.place(x=800,y=576,height=400,width=770)
    for id in tabla1.get_children():
        if tabla1.item(id,"values")[3] in diccionario_compartido.keys():
            diccionario_compartido[tabla1.item(id,"values")[3]] =  int(diccionario_compartido.get(tabla1.item(id,"values")[3]) + int(tabla1.item(id,"values")[11]))
        else:    
            diccionario_compartido[tabla1.item(id,"values")[3]] = int(tabla1.item(id,"values")[11])
    
    
    fig = Figure(figsize = (11, 5.6), dpi = 70)
    
    ciudades = [x for x in diccionario_compartido.keys() ]
    ventas = [diccionario_compartido.get(x) for x in diccionario_compartido.keys() ]


    ax = fig.subplots()
    sns.barplot(x=ciudades,y=ventas,ax=ax,ci=None)
    ax.set(ylabel='VENTAS')
    ax.tick_params(axis='x', rotation=20)
    fig.patch.set_facecolor(color_ventanas)
    # Creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = ventana_grafico)  
    # Placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column=0,row=0)
    grafico_seleccionado = "ciudad"
def grafico_provincia():
    global grafico_seleccionado
    grafico_seleccionado = grafico_seleccionado
    global ax,canvas,fig,provincias,ventas,ventana_grafico
    canvas.flush_events()
    diccionario_compartido = {}
    gc.collect()
    ventana_grafico.destroy()
    ventana_grafico = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_grafico.place(x=800,y=576,height=400,width=770)
    for id in tabla1.get_children():
        if tabla1.item(id,"values")[4] in diccionario_compartido.keys():
            diccionario_compartido[tabla1.item(id,"values")[4]] =  int(diccionario_compartido.get(tabla1.item(id,"values")[4]) + int(tabla1.item(id,"values")[11]))
        else:    
            diccionario_compartido[tabla1.item(id,"values")[4]] = int(tabla1.item(id,"values")[11])
    
    fig = Figure(figsize = (11, 5.6), dpi = 70)
    
    provincias = [x for x in diccionario_compartido.keys() ]
    ventas = [diccionario_compartido.get(x) for x in diccionario_compartido.keys() ]
    
    ax = fig.subplots()
    sns.barplot(x=provincias,y=ventas,ax=ax,ci=None)
    ax.set(ylabel='VENTAS')
    ax.tick_params(axis='x', rotation=30)
    fig.patch.set_facecolor(color_ventanas)
    # Creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = ventana_grafico)  
    # Placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column=0,row=0)
    grafico_seleccionado = "provincia"
def grafico_producto_favorito():
    global grafico_seleccionado
    grafico_seleccionado = grafico_seleccionado
    global ax,canvas,fig,productos,contador,ventana_grafico
    diccionario_compartido = {}
    canvas.flush_events()
    gc.collect()
    ventana_grafico.destroy()
    ventana_grafico = ctk.CTkFrame(ventana,fg_color=color_ventanas)
    ventana_grafico.place(x=800,y=576,height=400,width=770)
    for id in tabla1.get_children():
        if tabla1.item(id,"values")[10] in diccionario_compartido.keys():
            diccionario_compartido[tabla1.item(id,"values")[10]] = diccionario_compartido.get(tabla1.item(id,"values")[10]) + 1
        else:
            diccionario_compartido[tabla1.item(id,"values")[10]] = 1
        

    fig = Figure(figsize = (11, 5.6), dpi = 70)
    
    productos,contador = [],[]

    for x in diccionario_compartido.keys():
        productos.append(x)
        contador.append(diccionario_compartido.get(x))
    
    ax = fig.subplots()
    sns.barplot(x=productos,y=contador,ax=ax,ci=None)
    ax.tick_params(axis='x', rotation=15)
    fig.patch.set_facecolor(color_ventanas)
    # Creating the Tkinter canvas containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig,master = ventana_grafico)  
    # Placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column=0,row=0)
    grafico_seleccionado = "producto"

#------------------------------------------------------------------------------------------------
#                      Herramientas Administrativas ( Calculadora y Documentos )                |   
#------------------------------------------------------------------------------------------------
# Calculadora
class calculadora:
    def __init__(self,ventana,ventana_calculadora):
        global largo_boton
        global ancho_boton
        global boton1,boton2,boton3,boton4,boton5,boton6,boton6,boton7,boton8,boton9,boton10,boton11,boton12,boton13,boton14,boton15,boton16,boton17
        global pantalla_calc,titulo_calc,botones_calc

        largo_boton = 36
        ancho_boton = 51
        boton1_x = 20
        boton1_y = 90
        self.ventana = ventana
        self.ventana_calculadora = ventana_calculadora
        
        self.pantalla = ctk.CTkEntry(self.ventana_calculadora,state="disabled",disabledbackground=color_entradas,fg_color=color_entradas,bg_color=color_ventanas,text_font=("helvetica",10),border_color=color_entradas)
        self.pantalla.place(x=boton1_x,y=boton1_y-27,height=27,width=204)
        self.titulo_calculadora = ctk.CTkLabel(self.ventana_calculadora,
                                               text="CALCULADORA",
                                               text_font=("helvetica",10),
                                               text_color="black",
                                               fg_color=color_botones,
                                               bg_color=color_botones)
        self.titulo_calculadora.place(x=boton1_x,y=boton1_y-50,height=27,width=204)
        pantalla_calc = self.pantalla

        titulo_calc = self.titulo_calculadora
        self.operacion=""


        #-----------------------------ESTILO BOTON-------------------------------
        
        estilo.configure("TButton", font =('calibri', 11, 'bold'))
        

        boton1 = self.crearBoton(7)
        boton2 = self.crearBoton(8)
        boton3 = self.crearBoton(9)
        boton4 = self.crearBoton(u"\u232B",escribir=False)
        boton5 = self.crearBoton(4)
        boton6 = self.crearBoton(5)
        boton7 = self.crearBoton(6)
        boton8 = self.crearBoton("-")
        boton9 = self.crearBoton(1)
        boton10 = self.crearBoton(2)
        boton11 = self.crearBoton(3)
        boton12 = self.crearBoton("+")
        boton13 = self.crearBoton(",")
        boton14 = self.crearBoton(0)
        boton15 = self.crearBoton(u"\u00F7")
        boton16 = self.crearBoton("*")
        boton17 = self.crearBoton("=",escribir=False)

        botones_calc = [boton1,boton2,boton3,boton4,boton5,boton6,boton6,boton7,boton8,boton9,boton10,boton11,boton12,boton13,boton14,boton15,boton16,boton17]
        
        boton1.place(x=boton1_x,y=boton1_y,height=largo_boton,width=ancho_boton)
        boton2.place(x=boton1_x+ancho_boton,y=boton1_y,height=largo_boton,width=ancho_boton)
        boton3.place(x=boton1_x+ancho_boton*2,y=boton1_y,height=largo_boton,width=ancho_boton)
        boton4.place(x=boton1_x+ancho_boton*3,y=boton1_y,height=largo_boton,width=ancho_boton)

        boton5.place(x=boton1_x,y=boton1_y+largo_boton,height=largo_boton,width=ancho_boton)
        boton6.place(x=boton1_x+ancho_boton,y=boton1_y+largo_boton,height=largo_boton,width=ancho_boton)
        boton7.place(x=boton1_x+ancho_boton*2,y=boton1_y+largo_boton,height=largo_boton,width=ancho_boton)
        boton8.place(x=boton1_x+ancho_boton*3,y=boton1_y+largo_boton,height=largo_boton,width=ancho_boton)

        boton9.place(x=boton1_x,y=boton1_y+largo_boton*2,height=largo_boton,width=ancho_boton)
        boton10.place(x=boton1_x+ancho_boton,y=boton1_y+largo_boton*2,height=largo_boton,width=ancho_boton)
        boton11.place(x=boton1_x+ancho_boton*2,y=boton1_y+largo_boton*2,height=largo_boton,width=ancho_boton)
        boton12.place(x=boton1_x+ancho_boton*3,y=boton1_y+largo_boton*2,height=largo_boton,width=ancho_boton)

        boton13.place(x=boton1_x,y=boton1_y+largo_boton*3,height=largo_boton,width=ancho_boton)
        boton14.place(x=boton1_x+ancho_boton,y=boton1_y+largo_boton*3,height=largo_boton,width=ancho_boton)
        boton15.place(x=boton1_x+ancho_boton*2,y=boton1_y+largo_boton*3,height=largo_boton,width=ancho_boton)
        boton16.place(x=boton1_x+ancho_boton*3,y=boton1_y+largo_boton*3,height=largo_boton,width=ancho_boton)
        boton17.place(x=boton1_x+ancho_boton,y=boton1_y+largo_boton*4,height=largo_boton,width=102)
    
    def crearBoton(self,valor,escribir=True):
        return ctk.CTkButton(ventana_calculadora,
                            text=valor,
                            text_font=("Calibri",12),
                            text_color="black",
                            highlightbackground="black",
                            fg_color=color_botones,bg_color=color_botones,
                            command=lambda:self.click(valor,escribir))
                
    def click(self,texto,escribir):
        if not escribir:

            if texto == "=" and self.operacion != "":
                self.operacion = re.sub(u"\u00F7","/",self.operacion)
                resultado = str(eval(self.operacion))
                self.operacion=""
                self.limpiar_pantalla()
                self.mostrar_en_pantalla(resultado)

            elif texto ==u"\u232B":
                self.operacion=""
                self.limpiar_pantalla()
        
        else:

            self.operacion +=str(texto)
            self.mostrar_en_pantalla(texto)
        
        return

    def limpiar_pantalla(self):
        self.pantalla.configure(state="normal")
        self.pantalla.delete("0",END)       
        self.pantalla.configure(state="disabled")
        return

    def mostrar_en_pantalla(self,valor):
        self.pantalla.configure(state="normal")
        self.pantalla.insert(END,valor)
        self.pantalla.configure(state="disabled")

        return

# Administrador de archivos
def administrador_archivos():
    global boton_abrir_archivo,boton_abrir_todos,boton_guardar_archivo

    global archivo1_entrada
    global archivo2_entrada
    global archivo3_entrada
    global archivo4_entrada
    global archivo5_entrada
    global archivo6_entrada
    global archivo7_entrada
    global seleccion
    global archivo1_radioboton,archivo2_radioboton,archivo3_radioboton,archivo4_radioboton,archivo5_radioboton,archivo6_radioboton,archivo7_radioboton
    seleccion = IntVar()
    seleccion.set(1)
    entrada_y = 85
    y_agregar = 30
    entrada_y+y_agregar*1
    boton_guardar_archivo = crear_boton(ventana_documentos,"Recordar Archivo",("helvetica",10),"black",color_botones,color_ventanas,almacenar_archivo)
    boton_guardar_archivo.place(x=58,y=40,height=25,width=120)
    
    boton_abrir_archivo = crear_boton(ventana_documentos,"Abrir Archivo",("helvetica",10),"black",color_botones,color_ventanas,abrir_archivo)
    boton_abrir_archivo.place(x=203,y=40,height=25,width=120)

    boton_abrir_todos = crear_boton(ventana_documentos,"Abrir Todos",("helvetica",10),"black",color_botones,color_ventanas,abrir_todos)
    boton_abrir_todos.place(x=348,y=40,height=25,width=120)

    archivo1_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo1_entrada.place(x=40,y=entrada_y,height=25,width=450)

    archivo2_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo2_entrada.place(x=40,y=entrada_y+y_agregar*1,height=25,width=450)

    archivo3_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo3_entrada.place(x=40,y=entrada_y+y_agregar*2,height=25,width=450)

    archivo4_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo4_entrada.place(x=40,y=entrada_y+y_agregar*3,height=25,width=450)

    archivo5_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo5_entrada.place(x=40,y=entrada_y+y_agregar*4,height=25,width=450)

    archivo6_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo6_entrada.place(x=40,y=entrada_y+y_agregar*5,height=25,width=450)

    archivo7_entrada = ctk.CTkEntry(ventana_documentos,state="disable",disabledbackground="#b3e5fc",fg_color="#b3e5fc",bg_color=color_ventanas,border_color="#b3e5fc",text_font=("helvetica",10),text_color="black" )
    archivo7_entrada.place(x=40,y=entrada_y+y_agregar*6,height=25,width=450)


    archivo1_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=1,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo1_radioboton.place(x=15,y=entrada_y+1,width=22)

    archivo2_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=2,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo2_radioboton.place(x=15,y=entrada_y+y_agregar*1+1,width=22)

    archivo3_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=3,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo3_radioboton.place(x=15,y=entrada_y+y_agregar*2+1,width=22)

    archivo4_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=4,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo4_radioboton.place(x=15,y=entrada_y+y_agregar*3+1,width=22)

    archivo5_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=5,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo5_radioboton.place(x=15,y=entrada_y+y_agregar*4+1,width=22)

    archivo6_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=6,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo6_radioboton.place(x=15,y=entrada_y+y_agregar*5+1,width=22)

    archivo7_radioboton = ctk.CTkRadioButton(ventana_documentos,variable=seleccion,value=7,text="",fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas)
    archivo7_radioboton.place(x=15,y=entrada_y+y_agregar*6+1,width=22)

    
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM archivos")
    
    registro_archivos = c.fetchall()

    lista_archivos_abrir = [ registro for registro in registro_archivos ]
    
    archivo1_entrada.configure(state="normal")
    archivo1_entrada.delete(0,END)
    archivo1_entrada.insert(0,lista_archivos_abrir[0][1])
    archivo1_entrada.configure(state="disabled")
    #----
    archivo2_entrada.configure(state="normal")
    archivo2_entrada.delete(0,END)
    archivo2_entrada.insert(0,lista_archivos_abrir[0][2])
    archivo2_entrada.configure(state="disabled")
    #----
    archivo3_entrada.configure(state="normal")
    archivo3_entrada.delete(0,END)
    archivo3_entrada.insert(0,lista_archivos_abrir[0][3])
    archivo3_entrada.configure(state="disabled")
    #----
    archivo4_entrada.configure(state="normal")
    archivo4_entrada.delete(0,END)
    archivo4_entrada.insert(0,lista_archivos_abrir[0][4])
    archivo4_entrada.configure(state="disabled")
    #----
    archivo5_entrada.configure(state="normal")
    archivo5_entrada.delete(0,END)
    archivo5_entrada.insert(0,lista_archivos_abrir[0][5])
    archivo5_entrada.configure(state="disabled")
    #----
    archivo6_entrada.configure(state="normal")
    archivo6_entrada.delete(0,END)
    archivo6_entrada.insert(0,lista_archivos_abrir[0][6])
    archivo6_entrada.configure(state="disabled")
    #----
    archivo7_entrada.configure(state="normal")
    archivo7_entrada.delete(0,END)
    archivo7_entrada.insert(0,lista_archivos_abrir[0][7])
    archivo7_entrada.configure(state="disabled")

    
    conexion.commit()
    conexion.close()
def almacenar_archivo():

    ruta_archivo = filedialog.askopenfilename()
    
    if seleccion.get() == 1:
        archivo1_entrada.configure(state="normal")
        archivo1_entrada.delete(0,END)
        archivo1_entrada.insert(0,ruta_archivo)
        archivo1_entrada.configure(state="disabled")
    elif seleccion.get() == 2:
        archivo2_entrada.configure(state="normal")
        archivo2_entrada.delete(0,END)
        archivo2_entrada.insert(0,ruta_archivo)
        archivo2_entrada.configure(state="disabled")
    elif seleccion.get() == 3:
        archivo3_entrada.configure(state="normal")
        archivo3_entrada.delete(0,END)
        archivo3_entrada.insert(0,ruta_archivo)
        archivo3_entrada.configure(state="disabled")
    elif seleccion.get() == 4:
        archivo4_entrada.configure(state="normal")
        archivo4_entrada.delete(0,END)
        archivo4_entrada.insert(0,ruta_archivo)
        archivo4_entrada.configure(state="disabled")
    elif seleccion.get() == 5:
        archivo5_entrada.configure(state="normal")
        archivo5_entrada.delete(0,END)
        archivo5_entrada.insert(0,ruta_archivo)
        archivo5_entrada.configure(state="disabled")
    elif seleccion.get() == 6:
        archivo6_entrada.configure(state="normal")
        archivo6_entrada.delete(0,END)
        archivo6_entrada.insert(0,ruta_archivo)
        archivo6_entrada.configure(state="disabled")
    elif seleccion.get() == 7:
        archivo7_entrada.configure(state="normal")
        archivo7_entrada.delete(0,END)
        archivo7_entrada.insert(0,ruta_archivo)
        archivo7_entrada.configure(state="disabled")

    conexion = sqlite3.connect("tabla_crm.db")

    c = conexion.cursor()   

    c.execute("""UPDATE archivos SET 

            ruta_archivo1 = :ruta_archivo1,
            ruta_archivo2 = :ruta_archivo2,
            ruta_archivo3 = :ruta_archivo3,
            ruta_archivo4 = :ruta_archivo4,
            ruta_archivo5 = :ruta_archivo5,
            ruta_archivo6 = :ruta_archivo6,
            ruta_archivo7 = :ruta_archivo7 """,
                    
            {   
                "ruta_archivo1":archivo1_entrada.get(),
                "ruta_archivo2":archivo2_entrada.get(),
                "ruta_archivo3":archivo3_entrada.get(),
                "ruta_archivo4":archivo4_entrada.get(),
                "ruta_archivo5":archivo5_entrada.get(),
                "ruta_archivo6":archivo6_entrada.get(),
                "ruta_archivo7":archivo7_entrada.get()    })

    
    conexion.commit()

    conexion.close()
def abrir_todos():
    time.sleep(5)
    os.popen('"%s"' % archivo1_entrada.get())
    time.sleep(5)
    os.popen('"%s"' % archivo2_entrada.get())
    time.sleep(5)
    os.popen('"%s"' % archivo3_entrada.get())
def abrir_archivo():

    if seleccion.get() == 1:
        if len((archivo1_entrada.get())) == 0:
            pass
        else:
            os.popen('"%s"' % archivo1_entrada.get())
    elif seleccion.get() == 2:
        if len((archivo2_entrada.get())) == 0:
            pass
        else:
            os.popen('"%s"' % archivo2_entrada.get())
    elif seleccion.get() == 3:
        if len((archivo3_entrada.get())) == 0:
            pass
        else:
            os.popen('"%s"' % archivo3_entrada.get())

#------------------------------------------------------------------------------------------------
#                       Menu - ( Crea el menu y agrega herramientas )                           |   
#------------------------------------------------------------------------------------------------

# Crear menu
def menu_app():
    
    # --- Barra principal ---
    mi_menu = Menu(ventana)
    ventana.config(menu=mi_menu)

    # ------------------------ ARCHIVO --------------------------------
    menu_archivo = Menu(mi_menu,tearoff=0)
    mi_menu.add_cascade(label="Archivo",menu = menu_archivo )

    # ------------------------ Exportar -------------------------------
    menu_exportar = Menu(mi_menu,tearoff=0)
    menu_archivo.add_cascade(label="Exportar a ",menu = menu_exportar )
    # csv
    menu_exportar.add_command(label="Formato CSV",command=exportar_a_csv)
    # excel
    menu_exportar.add_command(label="Formato EXCEL",command=exportar_a_excel)
    
    #-------------------- Cerrar Programa------------------------------
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir",command=ventana.quit)
    
    # ------------------------ OPCIONES -------------------------------
    menu_opciones = Menu(mi_menu,tearoff=0)
    mi_menu.add_cascade(label="Opciones",menu = menu_opciones )

    # Cambiar Colores Tabla 
    menu_cambiar_color = Menu(mi_menu,tearoff=0)
    menu_opciones.add_cascade(label="Colores",menu = menu_cambiar_color )

    menu_cambiar_color.add_command(label="Cambiar a Tema 1",command=color_tema1)
    menu_cambiar_color.add_command(label="Cambiar a Tema 2",command=color_tema2)

    # ------------------------ ADMINISTRACION -------------------------
    
    menu_administracion = Menu(mi_menu,tearoff=0)
    mi_menu.add_cascade(label="Administracion",menu = menu_administracion )

    menu_administracion.add_command(label="Usuarios",command=admin_usuarios)

# Cambio de colores
def color_tema1():
    global color_ventanas
    global color_botones
    global color_tablas_distinto
    global color_tablas_igual
    global color_tablas_seleccion
    global color_titulos
    global color_etiquetas
    
    color_ventanas = "#0080c0"
    color_botones = "#00acc1"
    color_etiquetas = "#64b5f6"
    color_tablas_distinto = "#90caf9"
    color_tablas_igual = "#42a5f5"
    color_tablas_seleccion = "#0d47a1"
    color_titulos = "#64b5f6"
    
    cambiar_color_todos()
def color_tema2():
    global color_ventanas
    global color_botones
    global color_tablas_distinto
    global color_tablas_igual
    global color_tablas_seleccion
    global color_etiquetas
    global color_titulos

    color_ventanas = "#ba68c8"
    color_botones = "#8e24aa"
    color_etiquetas = "#ce93d8"
    color_tablas_distinto = "#e1bee7"
    color_tablas_igual = "#f3e5f5"
    color_tablas_seleccion = "#ab47bc"
    color_titulos = "#ba68c8"

    cambiar_color_todos()
    
def cambiar_color_todos():
    
    # VENTANAS 
    ventana_datos.configure(fg_color=color_ventanas)
    ventana_calculadora.configure(fg_color=color_ventanas)
    ventana_documentos.configure(fg_color=color_ventanas)
    ventana_datos.configure(fg_color=color_ventanas)
    ventana_filtrar.configure(fg_color=color_ventanas)
    ventana_grafico.configure(fg_color=color_ventanas)
    ventana_tabla2.configure(fg_color=color_ventanas)
    ventana_botones_graficos.configure(fg_color=color_ventanas)
    ventana_botones_datos.configure(fg_color=color_ventanas)
    tabla_ventana.configure(fg_color=color_ventanas)
    tabla_ventana_marco.configure(fg_color=color_ventanas)
    tabla2_ventana_marco.configure(fg_color=color_ventanas)
    
    # TABLAS
    tabla1.tag_configure("oddrow", background = color_tablas_distinto)        # 200
    tabla1.tag_configure("evenrow", background = color_tablas_igual)          # 400
    tabla2.tag_configure("oddrow", background = color_tablas_distinto)        # 200
    tabla2.tag_configure("evenrow", background = color_tablas_igual)          # 400
    estilo.map("Treeview",background=[("selected",color_tablas_seleccion)])   # 900
    estilo.configure("Treeview",background = color_ventanas,foreground = "black",rowheight  = 25,fieldbackground = color_ventanas)
    
    # BOTONES
    archivo1_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo2_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo3_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo4_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo5_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo6_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    archivo7_radioboton.configure(fg_color=color_botones,border_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    for boton in botones_calc:
        boton.configure(fg_color=color_botones,bg_color=color_botones,hover_color=color_etiquetas)
    for boton in lista_botones_tabla1:
        boton.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    Buscar.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    Resetear.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_grafico_ventas.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_grafico_provincia.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_grafico_ciudad.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_grafico_producto.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_abrir_archivo.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_guardar_archivo.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    boton_abrir_todos.configure(fg_color=color_botones,bg_color=color_ventanas,hover_color=color_etiquetas)
    
    # ETIQUETAS
    titulo_calc.configure(fg_color=color_botones,bg_color=color_botones)
    titulo_ingreso_datos.configure(fg_color=color_titulos,bg_color=color_ventanas)
    for etiqueta in lista_etiquetas:
        etiqueta.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    campo_filtrar_etiqueta1.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    campo_filtrar_etiqueta2.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    campo_filtrar_etiqueta3.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    columna_filtrar_etiqueta1.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    columna_filtrar_etiqueta2.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    columna_filtrar_etiqueta3.configure(fg_color=color_etiquetas,bg_color=color_ventanas)
    
    # GRAFICOS
    if grafico_seleccionado == "ventas":
        grafico_ventas()
    elif grafico_seleccionado == "ciudad":
        grafico_ciudad()
    elif grafico_seleccionado == "provincia":
        grafico_provincia()
    elif grafico_seleccionado == "producto":
        grafico_producto_favorito()

# Exportacion
def exportar_a_excel():
    exportar = 1
    global registros
    diccionario_data = {}
    conexion = sqlite3.connect("tabla_crm.db")

    c = conexion.cursor()   

    c.execute("SELECT rowid,* FROM clientes")
    
    registros = c.fetchall()
    

    lista_nombre = [registro[1] for registro in registros]
    lista_apellido = [registro[2] for registro in registros]
    lista_ciudad = [registro[3] for registro in registros]
    lista_provincia = [registro[4] for registro in registros]
    lista_codigo_postal = [registro[5] for registro in registros]
    lista_direccion = [registro[6] for registro in registros]
    lista_telefono = [registro[7] for registro in registros]
    lista_correo = [registro[8] for registro in registros]
    lista_descripcion = [registro[9] for registro in registros]
    lista_producto = [registro[10] for registro in registros]
    lista_ventas = [registro[11] for registro in registros]
    lista_saldo = [registro[12] for registro in registros]
    lista_inicio = [registro[13] for registro in registros]
    lista_ultima = [registro[14] for registro in registros]
    #-------------------------------------------------------------
    diccionario_data["Nombre"] = lista_nombre
    diccionario_data["Apellido"] = lista_apellido
    diccionario_data["Ciudad"] = lista_ciudad
    diccionario_data["Provincia"] = lista_provincia
    diccionario_data["Codigo_Postal"] = lista_codigo_postal
    diccionario_data["Direccion"] = lista_direccion
    diccionario_data["Telefono"] = lista_telefono
    diccionario_data["Correo"] = lista_correo
    diccionario_data["Descripcion"] = lista_descripcion
    diccionario_data["Producto"] = lista_producto
    diccionario_data["Ventas"] = lista_ventas
    diccionario_data["Saldo"] = lista_saldo
    diccionario_data["Inicio"] = lista_inicio
    diccionario_data["Ultima"] = lista_ultima


    conexion.commit()
    conexion.close()

    data = pd.DataFrame(data=diccionario_data)
    fecha = int(datetime.timestamp(datetime.today()))
    nombre_doc = "proyecto_data_excel"+str(fecha)+".xlsx"
    data.to_excel("proyecto_data_excel"+str(fecha)+".xlsx")

    if exportar == 1:
        messagebox.showinfo("Exportacion a EXCEL","Datos exportados a "+nombre_doc)
def exportar_a_csv():
    exportar = 1
    global registros
    diccionario_data = {}
    conexion = sqlite3.connect("tabla_crm.db")

    c = conexion.cursor()   

    c.execute("SELECT rowid,* FROM clientes")
    
    registros = c.fetchall()
    

    lista_nombre = [registro[1] for registro in registros]
    lista_apellido = [registro[2] for registro in registros]
    lista_ciudad = [registro[3] for registro in registros]
    lista_provincia = [registro[4] for registro in registros]
    lista_codigo_postal = [registro[5] for registro in registros]
    lista_direccion = [registro[6] for registro in registros]
    lista_telefono = [registro[7] for registro in registros]
    lista_correo = [registro[8] for registro in registros]
    lista_descripcion = [registro[9] for registro in registros]
    lista_producto = [registro[10] for registro in registros]
    lista_ventas = [registro[11] for registro in registros]
    lista_saldo =  [registro[12] for registro in registros]
    lista_inicio = [registro[13] for registro in registros]
    lista_ultima = [registro[14] for registro in registros]
    #-------------------------------------------------------------
    diccionario_data["Nombre"] = lista_nombre
    diccionario_data["Apellido"] = lista_apellido
    diccionario_data["Ciudad"] = lista_ciudad
    diccionario_data["Provincia"] = lista_provincia
    diccionario_data["Codigo_Postal"] = lista_codigo_postal
    diccionario_data["Direccion"] = lista_direccion
    diccionario_data["Telefono"] = lista_telefono
    diccionario_data["Correo"] = lista_correo
    diccionario_data["Descripcion"] = lista_descripcion
    diccionario_data["Producto"] = lista_producto
    diccionario_data["Ventas"] = lista_ventas
    diccionario_data["Saldo"] = lista_saldo
    diccionario_data["Inicio"] = lista_inicio
    diccionario_data["Ultima"] = lista_ultima
    
    conexion.commit()
    conexion.close()

    data = pd.DataFrame(data=diccionario_data)
    fecha = int(datetime.timestamp(datetime.today()))
    nombre_doc = "proyecto_data_csv"+str(fecha)+".csv"
    data.to_csv("proyecto_data_csv"+str(fecha)+".csv")

    if exportar == 1:
        messagebox.showinfo("Exportacion a CSV","Datos exportados a "+nombre_doc)

# Administracion
def admin_usuarios():
    global tabla_usuarios
    global ventana_usuarios
    ventana_usuarios = ctk.CTkToplevel(ventana,fg_color=color_ventanas)
    ventana_usuarios.title("Administrar Usuarios")
    w = 600 # width for the Tk root
    h = 400 # height for the Tk root
    ws = ventana_usuarios.winfo_screenwidth() # width of the screen
    hs = ventana_usuarios.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    ventana_usuarios.geometry('%dx%d+%d+%d' % (w, h, x, y))

    marco_ventana_tabla = ctk.CTkFrame(ventana_usuarios,fg_color=color_ventanas)
    marco_ventana_tabla.place(x=20,y=20,height=200,width=560)
    
    # Barras de scroll y creacion de tabla
    scroll_vertical_tabla = Scrollbar(marco_ventana_tabla,orient=VERTICAL)
    scroll_vertical_tabla.pack(side = RIGHT, fill = Y)
    scroll_horizontal_tabla = Scrollbar(marco_ventana_tabla,orient=HORIZONTAL)
    scroll_horizontal_tabla.pack(side = BOTTOM, fill = X)
    
    tabla_usuarios = ttk.Treeview(   marco_ventana_tabla,
                            yscrollcommand=scroll_vertical_tabla.set,
                            xscrollcommand=scroll_horizontal_tabla.set, 
                            selectmode="extended")
    
    scroll_horizontal_tabla.config(command=tabla_usuarios.xview)
    scroll_vertical_tabla.config(command=tabla_usuarios.yview)
    
    tabla_usuarios.pack()

    # Contruir columnas y textos
    tabla_usuarios["columns"] = ("oID",
                                 "Usuario",
                                 "Permiso_agregar",
                                 "Permiso_actualizar",
                                 "Permiso_borrar",
                                 "Permiso_admin_usuarios")

    tabla_usuarios.column("#0", width=-1, stretch=NO)
    tabla_usuarios.column("oID",anchor="center", width=30)
    tabla_usuarios.column("Usuario",anchor="center", width=140)
    tabla_usuarios.column("Permiso_agregar",anchor="center", width=140)
    tabla_usuarios.column("Permiso_actualizar",anchor="center", width=140)
    tabla_usuarios.column("Permiso_borrar",anchor="center", width=140)
    tabla_usuarios.column("Permiso_admin_usuarios",anchor="center", width=140)
    
    tabla_usuarios.heading("#0",text="", anchor=W)
    tabla_usuarios.heading("oID",text= "oID",anchor="center")
    tabla_usuarios.heading("Usuario",text="Usuario", anchor="center")
    tabla_usuarios.heading("Permiso_agregar",text="Permiso Agregar", anchor="center")
    tabla_usuarios.heading("Permiso_actualizar",text="Permiso Actualizar", anchor="center")
    tabla_usuarios.heading("Permiso_borrar",text="Permiso Borrar", anchor="center")
    tabla_usuarios.heading("Permiso_admin_usuarios",text="Permiso Administrar", anchor="center")
    
    # Crear filas con colores distintos diferenciando cada campo

    tabla_usuarios.tag_configure("oddrow", background = color_tablas_distinto)    # 50
    tabla_usuarios.tag_configure("evenrow", background = color_tablas_igual)      # 100
    estilo.map("Treeview",background=[("selected",color_tablas_seleccion)])       # 200
    
    # Agregar entradas de usuarios
    agregar_entradas_administrar_usuarios()
    # Agregar botones para funciones de administracion
    agregar_botones_administrar_usuarios()
    
    # Limpiar datos de la tabla ( TREEVIEW )
    tabla_usuarios.delete(*tabla_usuarios.get_children())
    # Mover datos de la base de datos hacia la tabla de usuarios
    mover_datos_base_a_usuarios()
def agregar_entradas_administrar_usuarios():
    global ID_usuario_entrada
    global nombre_usuario_entrada
    global permiso_agregar_entrada
    global permiso_actualizar_entrada
    global permiso_borrar_entrada
    global permiso_admin_entrada
    global administracion_entradas_lista
    
    ID_usuario_etiqueta = crear_etiqueta("tabla_usuarios","ID")
    nombre_usuario_etiqueta = crear_etiqueta("tabla_usuarios","Nombre")
    permiso_agregar_etiqueta = crear_etiqueta("tabla_usuarios","Agregar")
    permiso_actualizar_etiqueta = crear_etiqueta("tabla_usuarios","Actualizar")
    permiso_borrar_etiqueta = crear_etiqueta("tabla_usuarios","Borrar")
    permiso_admin_etiqueta = crear_etiqueta("tabla_usuarios","Admin")
    #--------------------------------------------------------------------------------------------------------------------
    ID_usuario_entrada          = crear_entrada("tabla_usuarios")
    nombre_usuario_entrada      = crear_entrada("tabla_usuarios")
    permiso_agregar_entrada     = crear_entrada("tabla_usuarios")
    permiso_actualizar_entrada  = crear_entrada("tabla_usuarios")
    permiso_borrar_entrada      = crear_entrada("tabla_usuarios")
    permiso_admin_entrada       = crear_entrada("tabla_usuarios")
    #-----------------------------------------------------------------------------------------------------------------
    detalle_login = ctk.CTkLabel(ventana_usuarios,
                                text='Logueado como: ',
                                text_font=("helvetica",10),
                                text_color="black",
                                fg_color="#e8eaf6",
                                bg_color=color_ventanas)
    
    nombre_del_usuario_logeado =  ctk.CTkLabel(ventana_usuarios,
                                               text=str(usuario_logeado),
                                               text_font=("helvetica",10),
                                               text_color="#f50057",
                                               fg_color="#e8eaf6",
                                               bg_color=color_ventanas)
    #-----------------------------------------------------------------------
    administracion_entradas_lista = [ID_usuario_entrada,
                                     nombre_usuario_entrada,
                                     permiso_agregar_entrada,
                                     permiso_actualizar_entrada,
                                     permiso_borrar_entrada,
                                     permiso_admin_entrada]
    #-----------------------------------------------------------------------
    ID_usuario_entrada.place(x=130,y=230,height=20,width=100)
    nombre_usuario_entrada.place(x=130,y=255,height=20,width=100)
    permiso_agregar_entrada.place(x=130,y=280,height=20,width=100)
    permiso_actualizar_entrada.place(x=130,y=305,height=20,width=100)
    permiso_borrar_entrada.place(x=130,y=330,height=20,width=100)
    permiso_admin_entrada.place(x=130,y=355,height=20,width=100)
    #-----------------------------------------------------------------------
    ID_usuario_etiqueta.place(x=20,y=230,height=20,width=100)
    nombre_usuario_etiqueta.place(x=20,y=255,height=20,width=100)
    permiso_agregar_etiqueta.place(x=20,y=280,height=20,width=100)
    permiso_actualizar_etiqueta.place(x=20,y=305,height=20,width=100)
    permiso_borrar_etiqueta.place(x=20,y=330,height=20,width=100)
    permiso_admin_etiqueta.place(x=20,y=355,height=20,width=100)
    #-----------------------------------------------------------------------
    detalle_login.place(x=320,y=230,height=20,width=130)
    nombre_del_usuario_logeado.place(x=470,y=230,height=20,width=75)
def agregar_botones_administrar_usuarios():
    #-----------------------------------------------------------------------
    boton_agregar_usuario = crear_boton(ventana_usuarios,"Agregar Usuario",("helvetica",10),"black",color_botones,color_ventanas,agregar_usuario)
    boton_actualizar_usuario = crear_boton(ventana_usuarios,"Actualizar Usuario",("helvetica",10),"black",color_botones,color_ventanas,actualizar_usuario)
    boton_quitar_usuario_seleccionado = crear_boton(ventana_usuarios,"Quitar Usuario",("helvetica",10),"black",color_botones,color_ventanas,quitar_usuario_seleccionado)
    #-----------------------------------------------------------------------
    boton_agregar_usuario.place(x=370,y=260,height=20,width=130)
    boton_actualizar_usuario.place(x=370,y=285,height=20,width=130)
    boton_quitar_usuario_seleccionado.place(x=370,y=310,height=20,width=130)

     # --------- Seleccionar Registro Bind -----------

    tabla_usuarios.bind("<ButtonRelease-1>",seleccion_usuario_en_administracion)
def agregar_usuario():
    # Comprobar si el usuario tiene permiso para remover registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    
    # Si el usuario logueado tiene permiso de administracion de usuarios continuar
    for registro in registros:
        if registro[6] == "si":
            
            # Comprobar si el usuario ya existe
            
            usuario_no_usado = True

            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()   
            c.execute("SELECT rowid,* FROM usuarios")
            registros = c.fetchall()

            for registro in registros:
                if registro[1] == nombre_usuario_entrada.get():
                    messagebox.showinfo("Atencion","El usuario ya existe, elija otro",parent=ventana_usuarios)
                    conexion.commit()
                    conexion.close()
                    usuario_no_usado = False
                    break   
            
            # Agregar el nuevo usuario a la base de datos si el nombre de usuario no esta en uso
            
            if usuario_no_usado == True:
                
                conexion = sqlite3.connect("tabla_crm.db")
                c = conexion.cursor()   
                c.execute("""INSERT INTO usuarios VALUES (
                                        :nombre,
                                        :contraseña,
                                        :permiso_agregar,
                                        :permiso_actualizar,
                                        :permiso_borrar,
                                        :permiso_admin_usuarios )""",
                                        {
                                            "nombre":nombre_usuario_entrada.get(),
                                            "contraseña":"",
                                            "permiso_agregar":permiso_agregar_entrada.get(),
                                            "permiso_actualizar":permiso_actualizar_entrada.get(),
                                            "permiso_borrar":permiso_borrar_entrada.get(),
                                            "permiso_admin_usuarios":permiso_admin_entrada.get() })

                conexion.commit()
                conexion.close()

                # Borrar datos de casillas de entrada
                for entrada in administracion_entradas_lista:
                    entrada.delete(0,END)
                # Limpiar datos de la tabla ( TREEVIEW )
                tabla_usuarios.delete(*tabla_usuarios.get_children())
                # Actualizar datos de la tabla haciendo una petision a la base de datos
                mover_datos_base_a_usuarios()
                
                messagebox.showinfo("Exito","El usuario fue creado correctamente!",parent=ventana_usuarios)
        else:
            messagebox.showerror("Error","Usted no tiene permisos para modificar los usuarios",parent=ventana_usuarios)
def actualizar_usuario():
    
    # Comprobar si el usuario tiene permiso para remover registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    
    # Si el usuario logueado tiene permiso de administracion de usuarios continuar
    for registro in registros:
        if registro[6] == "si":
            
            # Comprobar si el usuario ya existe
            
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()   
            c.execute("SELECT rowid,* FROM usuarios")
            registros = c.fetchall()
            
            usuario_no_usado = True
            
            for registro in registros:
                if registro[1] == nombre_usuario_entrada.get():
                    messagebox.showinfo("Atencion","El usuario ya existe o es el mismo que el anterior",parent=ventana_usuarios)
                    conexion.commit()
                    conexion.close()
                    usuario_no_usado = False
                    break   
            
            # Actualizar el usuario en la base de datos si el nuevo nombre no existe o no es el mismo de antes.
            
            if usuario_no_usado == True:
                conexion = sqlite3.connect("tabla_crm.db")
                c = conexion.cursor()   
                c.execute("""UPDATE usuarios SET 

                        nombre = :nombre,
                        contraseña = :contraseña,
                        permiso_agregar = :permiso_agregar,
                        permiso_actualizar = :permiso_actualizar,
                        permiso_borrar = :permiso_borrar,
                        permiso_admin_usuarios = :permiso_admin_usuarios
                                
                        WHERE oid == :oid""",
                        {   
                            "nombre":nombre_usuario_entrada.get(),
                            "contraseña":"",
                            "permiso_agregar":permiso_agregar_entrada.get(),
                            "permiso_actualizar":permiso_actualizar_entrada.get(),
                            "permiso_borrar":permiso_borrar_entrada.get(),
                            "permiso_admin_usuarios":permiso_admin_entrada.get(),
                            "oid":ID_usuario_entrada.get()      })
                conexion.commit()
                conexion.close()
                
                # Borrar datos de casillas de entrada
                for entrada in administracion_entradas_lista:
                    entrada.delete(0,END)
                # Limpiar datos de la tabla ( TREEVIEW )
                tabla_usuarios.delete(*tabla_usuarios.get_children())
                # Actualizar datos de la tabla haciendo una petision a la base de datos
                mover_datos_base_a_usuarios()
                
                messagebox.showinfo("Exito","El usuario fue actualizado correctamente!",parent=ventana_usuarios)
        else:
            messagebox.showerror("Error","Usted no tiene permisos para modificar los usuarios",parent=ventana_usuarios)
def quitar_usuario_seleccionado():
    # Comprobar si el usuario tiene permiso para remover registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    
    # Si el usuario logueado tiene permiso de administracion de usuarios continuar
    for registro in registros:
        if registro[6] == "si":
    
            # ---------------- Remover usuario de la tabla ( Treeview ) ---------------

            fila_seleccionada_remover = tabla_usuarios.selection()[0]
            tabla_usuarios.delete(fila_seleccionada_remover)

            # ---------------- Remover usuario de la base de datos ---------------
            
            conexion = sqlite3.connect("tabla_crm.db")

            c = conexion.cursor()   
                    
            c.execute("DELETE from usuarios WHERE oid=" + ID_usuario_entrada.get() )
                                    
            conexion.commit()
            conexion.close()

            # ------- Mensaje de aviso de eliminacion ---------- 

            messagebox.showinfo("Removido","El usuario fue removido!",parent=ventana_usuarios)
        else:
            messagebox.showerror("Error","Usted no tiene permisos para modificar los usuarios",parent=ventana_usuarios)    
def seleccion_usuario_en_administracion(e):
    valor = 0

    datos_entrada_lista = [ ID_usuario_entrada,
                            nombre_usuario_entrada,
                            permiso_agregar_entrada,
                            permiso_actualizar_entrada,
                            permiso_borrar_entrada,
                            permiso_admin_entrada]

    # Almacenar los datos del registro seleccionado
    
    seleccionado = tabla_usuarios.focus()
    valores = tabla_usuarios.item(seleccionado,"values")
    
    # Borrar datos anteriores en los cuadrados de entradas
    # Agregar datos del registro en los cuadrados de entradas
    
    for entrada in datos_entrada_lista:
        entrada.delete(0,END)
        entrada.insert(0, valores[valor])

        if valor == 5:
            break
        else:
            valor +=1

#--------------------------------------------------------------------------------------------
#                                   Ingreso con usuario y contraseña                        |
#--------------------------------------------------------------------------------------------

def ingresar_al_programa():
    # Chequeo usuario y contraseña con base de datos
    global registros
    global usuario_logeado
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios")
    registros = c.fetchall()

    for registro in registros:
        if registro[1] == usuario_entrada.get():
            if len(registro[2]) > 0:
                if contraseña_entrada.get() == registro[2]:
                    
                    # Guardar nombre de usuario
                    usuario_logeado = usuario_entrada.get()
                    ventana_login_root.destroy()
                    ventana_login_root.quit()
                    contraseña_correcta = True
                    

                    # Primera parte
                    ventana_principal()
                    crear_lista_ventana()
                    agregar_entrada_registros()
                    agregar_botones_datos()
                    # Segunda parte
                    crear_tabla_2()
                    agregar_herramientas_tabla2()
                    # Estilo tablas
                    crear_estilo()
                    # Base de datos
                    # Crear Base de datos - ( Agregar valores falsos si no quiere crear las tablas nuevas )
                    crear_base_de_datos(crear_tabla_clientes=False,crear_tabla_archivos=False,crear_tabla_usuarios=False)
                    # Mover datos a programa
                    mover_datos_base_a_programa()
                    # Crear Menus
                    menu_app()
                    tabla1.tag_configure("oddrow", background = "#90caf9")       # 200
                    tabla1.tag_configure("evenrow", background = "#42a5f5")      # 400
                    tabla2.tag_configure("oddrow", background = "#90caf9")       # 200
                    tabla2.tag_configure("evenrow", background = "#42a5f5")      # 400
                    estilo.map("Treeview",background=[("selected","#0d47a1")])   # 900
                    # Herramientas administrativas
                    administrador_archivos()
                    calculadora_objeto = calculadora(ventana,ventana_calculadora)
                    ventana.mainloop()
                    conexion.commit()
                    conexion.close()
                    break
            else:
                print("La contraseña no se encontraba en la base de datos y se le asigno la que escribio en el login")
                # La contraseña no se encontraba en la base de datos y se le asigno la que escribio en el login
                # ----------------MODIFICAR LA BASE DE DATOS ---------------
                conexion = sqlite3.connect("tabla_crm.db")
                c = conexion.cursor()   
                c.execute("""UPDATE usuarios SET 

                        contraseña = :contraseña
                
                        WHERE nombre = :nombre""",
                        { "contraseña":contraseña_entrada.get(),
                          "nombre":usuario_entrada.get()         })

                # Guardar nombre de usuario
                usuario_logeado = usuario_entrada.get()
                ventana_login_root.destroy()
                ventana_login_root.quit()
                contraseña_correcta = True
            
                # Primera parte
                ventana_principal()
                crear_lista_ventana()
                agregar_entrada_registros()
                agregar_botones_datos()
                # Segunda parte
                crear_tabla_2()
                agregar_herramientas_tabla2()
                # Estilo tablas
                crear_estilo()
                # Base de datos
                # Crear Base de datos - ( Agregar valores falsos si no quiere crear las tablas nuevas )
                crear_base_de_datos(crear_tabla_clientes=False,crear_tabla_archivos=False,crear_tabla_usuarios=False)
                # Mover datos a programa
                mover_datos_base_a_programa()
                # Crear Menus
                menu_app()
                # Herramientas administrativas
                administrador_archivos()

                calculadora_objeto = calculadora(ventana,ventana_calculadora)
                ventana.mainloop()
                conexion.commit()
                conexion.close()   
                break   
        else:
            contraseña_correcta = False
    else:
        contraseña_correcta = False   
    
    
    if contraseña_correcta == False:
    
        usuario_entrada.delete(0,END)
        usuario_entrada.insert(0,"Usuario")
        usuario_entrada.configure(text_color="gray")

        contraseña_entrada.delete(0,END)
        contraseña_entrada.insert(0,"Contraseña")
        contraseña_entrada.configure(text_color="gray")

        messagebox.showinfo("Eror","Usuario o contraseña incorrecto")
def crear_ventana_login():
    global logeo
    global ventana_login
    global boton_login
    global usuario_entrada
    global contraseña_entrada
    global ventana_login_root
    global color_ventanas
    global color_botones
    
    color_ventanas = "#0080c0"
    color_botones = "#00acc1"
    
    ventana_login_root = ctk.CTk() # create a Tk root window
    w = 900 # width for the Tk root
    h = 700 # height for the Tk root
    ws = ventana_login_root.winfo_screenwidth() # width of the screen
    hs = ventana_login_root.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    ventana_login_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    ventana_login_root.configure(background="#212121")

    ventana_login = ctk.CTkFrame(ventana_login_root,fg_color=color_ventanas)
    ventana_login.place(x=300,y=250,height=200,width=300)
    ventana_login.configure(background="#212121")
    logeo = ""
    
    boton_login = crear_boton(ventana_login,"LOGIN",("helvetica",10),"black",color_botones,color_ventanas,ingresar_al_programa)
    boton_login.place(x=110,y=130,height=25,width=80)
    
    usuario_entrada = crear_entrada("ventana_login")
    usuario_entrada.place(x=85,y=50,height=25,width=130)
    usuario_entrada.insert(0,"Usuario")
    usuario_entrada.configure(text_color="gray")
    
    contraseña_entrada = crear_entrada("ventana_login")
    contraseña_entrada.place(x=85,y=80,height=25,width=130)
    contraseña_entrada.insert(0,"Contraseña")
    contraseña_entrada.configure(text_color="gray")

    usuario_entrada.bind("<ButtonRelease-1>",limpiar_usuario_entrada_login)
    contraseña_entrada.bind("<ButtonRelease-1>",limpiar_contraseña_entrada_login)

    usuario_entrada.bind(("<Tab>"),usar_tab_en_usuario)
    contraseña_entrada.bind(("<Tab>"),usar_tab_en_contraseña)
def limpiar_usuario_entrada_login(e):
    
    if len(contraseña_entrada.get()) == 0:
        contraseña_entrada.insert(0,"Contraseña")
        contraseña_entrada.configure(text_color="gray",show="")
    if usuario_entrada.get() =="Usuario":
        usuario_entrada.delete(0,END)
        usuario_entrada.configure(text_color="black")
def limpiar_contraseña_entrada_login(e):
    
    if len(usuario_entrada.get()) == 0:
        usuario_entrada.insert(0,"Usuario")
        usuario_entrada.configure(text_color="gray")

    if contraseña_entrada.get() == "Contraseña":
        contraseña_entrada.delete(0,END)
        contraseña_entrada.configure(text_color="black",show="*")
def usar_tab_en_usuario(e):
    if len(usuario_entrada.get()) == 0:
        usuario_entrada.delete(0,END)
        usuario_entrada.insert(0,"Usuario")
        usuario_entrada.configure(text_color="gray")
    else:
        contraseña_entrada.delete(0,END)
        contraseña_entrada.configure(text_color="black",show="*")
def usar_tab_en_contraseña(e):
    if len(contraseña_entrada.get()) == 0:
        contraseña_entrada.delete(0,END)
        contraseña_entrada.insert(0,"Usuario")
        contraseña_entrada.configure(text_color="gray")
    else:
        usuario_entrada.delete(0,END)
        usuario_entrada.configure(text_color="black",show="")

#------------------------------------------------------------------------------------------------
#                       Funciones Tabla - ( Modificacion de registros )                         |   
#------------------------------------------------------------------------------------------------

def actualizar_registro():
    # Comprobar si el usuario tiene permiso para agregar registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    # Si el usuario logueado tiene permiso para actualizar entonces continuar
    for registro in registros:
        if registro[4] == "si":

        
            # MOSTRAR DATOS ACTUALIZADOS

            fila_seleccionada = tabla1.focus()
            valores = [entrada.get() for entrada in lista_entradas]
            tabla1.item(fila_seleccionada, text="", values=valores )

            # Modificar la base de datos
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()   
            c.execute("""UPDATE clientes SET 

                    nombre = :nombre,
                    apellido = :apellido,
                    ciudad = :ciudad,
                    provincia = :provincia,
                    codigo_postal = :codigo_postal,
                    direccion = :direccion,
                    telefono = :telefono,
                    correo = :correo,
                    descripcion = :descripcion,
                    producto_favorito = :producto_favorito,
                    ventas = :ventas,
                    saldo = :saldo,
                    inicio_actividad = :inicio_actividad,
                    ultima_venta = :ultima_venta            
                    
                    WHERE oid == :oid""",
                    {   
                        "nombre":nombre_entrada.get(),
                        "apellido":apellido_entrada.get(),
                        "ciudad":ciudad_entrada.get(),
                        "provincia":provincia_entrada.get(),
                        "codigo_postal":codigo_postal_entrada.get(),
                        "direccion":direccion_entrada.get(),
                        "telefono":telefono_entrada.get(),
                        "correo":correo_entrada.get(),
                        "descripcion":descripcion_entrada.get(),
                        "producto_favorito":producto_entrada.get(),
                        "ventas":ventas_entrada.get(),
                        "saldo":saldo_entrada.get(),
                        "inicio_actividad":inicio_entrada.get(),
                        "ultima_venta":ultima_entrada.get(),
                        "oid":id_entrada.get()      })
            conexion.commit()
            conexion.close()
            
            # Borrar datos de casillas de entrada
            borrar_entradas()
            
            # Limpiar datos de la tabla ( TREEVIEW )
            tabla1.delete(*tabla1.get_children())
            
            # Actualizar datos de la tabla haciendo una petision a la base de datos
            mover_datos_base_a_programa()
        else:
            messagebox.showinfo("Error","Usted no tiene permiso para actualizar registros")
def agregar_registro():
    
    # Comprobar si el usuario tiene permiso para agregar registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    # Si el usuario logueado tiene permiso para agregar entonces continuar
    for registro in registros:
        if registro[3] == "si":
            # Agregar el nuevo registro a la base de datos
            conexion = sqlite3.connect("tabla_crm.db")
            c = conexion.cursor()   
            c.execute("""INSERT INTO clientes VALUES (
                                    :nombre, 
                                    :apellido,
                                    :ciudad, 
                                    :provincia, 
                                    :codigo_postal, 
                                    :direccion, 
                                    :telefono, 
                                    :correo, 
                                    :descripcion,
                                    :producto_favorito,
                                    :ventas,
                                    :saldo,
                                    :inicio_actividad,
                                    :ultima_venta)""",
                                    {
                                        "nombre":nombre_entrada.get(),
                                        "apellido":apellido_entrada.get(),
                                        "ciudad":ciudad_entrada.get(),
                                        "provincia":provincia_entrada.get(),
                                        "codigo_postal":codigo_postal_entrada.get(),
                                        "direccion":direccion_entrada.get(),
                                        "telefono":telefono_entrada.get(),
                                        "correo":correo_entrada.get(),
                                        "descripcion":descripcion_entrada.get(),
                                        "producto_favorito":producto_entrada.get(),
                                        "ventas":ventas_entrada.get(),
                                        "saldo":saldo_entrada.get(),
                                        "inicio_actividad":inicio_entrada.get(),
                                        "ultima_venta":ultima_entrada.get()  })                 
            conexion.commit()
            conexion.close()

            # Borrar datos de casillas de entrada
            borrar_entradas()
            # Limpiar datos de la tabla ( TREEVIEW )
            tabla1.delete(*tabla1.get_children())
            # Actualizar datos de la tabla haciendo una petision a la base de datos
            mover_datos_base_a_programa()
        else:
            messagebox.showinfo("Error","Usted no tiene permiso para agregar registros")
def remover_registro_seleccionado():
    # Comprobar si el usuario tiene permiso para remover registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    # Si el usuario logueado tiene permiso para remove registros entonces continuar
    for registro in registros:
        if registro[5] == "si":
            # ---------------- Remover registro de la tabla ( Treeview ) ---------------

            fila_seleccionada_remover = tabla1.selection()[0]
            tabla1.delete(fila_seleccionada_remover)

            # ---------------- Remover registro de la base de datos ---------------
            
            conexion = sqlite3.connect("tabla_crm.db")

            c = conexion.cursor()   
                    
            c.execute("DELETE from clientes WHERE oid=" + id_entrada.get() )
                                    
            conexion.commit()
            conexion.close()

            # ------- Mensaje de aviso de eliminacion ---------- 

            messagebox.showinfo("Eliminado","El registro fue eliminado!")
        else:
            messagebox.showinfo("Error","Usted no tiene permiso para remover registros")
def remover_varios_registro():
    # Comprobar si el usuario tiene permiso para remover registros
    conexion = sqlite3.connect("tabla_crm.db")
    c = conexion.cursor()   
    c.execute("SELECT rowid,* FROM usuarios WHERE nombre=?",(usuario_logeado,))
    registros = c.fetchall()
    conexion.commit()
    conexion.close()
    # Si el usuario logueado tiene permiso para remove registros entonces continuar
    for registro in registros:
        if registro[5] == "si":
            # ------- Mensaje de confirmacion de eliminacion ---------- 

            respuesta = messagebox.askyesno("ALERTA!,","¿ Eliminar los registros seleccionados ?")

            # ------ Seguro que quieres eliminar varios registros ? ------
            if respuesta == 1:
                
                # ------ Crear lista de IDs para luego eliminar de la base de datos ------
                
                filas_seleccionadas_remover = tabla1.selection()
                lista_IDs = [ tabla1.item(x,"values")[0] for x in filas_seleccionadas_remover ]
                
                # ------ Quitar de la tabla ------
                
                for fila in filas_seleccionadas_remover:
                    tabla1.delete(fila)
                
                # ------ Quitar de la base de datos ------

                conexion = sqlite3.connect("tabla_crm.db")
                c = conexion.cursor()   
                c.executemany("DELETE from clientes WHERE oid = ?", [ (a,) for a in lista_IDs ]  )
                conexion.commit()
                conexion.close()
        else:
            messagebox.showinfo("Error","Usted no tiene permiso para remover registros")
def mover_arriba_registro():

    filas = tabla1.selection()

    for fila in filas:
        tabla1.move(fila, tabla1.parent(fila), tabla1.index(fila)-1)
def mover_abajo_registro():
    
    filas = tabla1.selection()

    for fila in reversed(filas):
        tabla1.move(fila, tabla1.parent(fila), tabla1.index(fila)+1)
def seleccionar_registro(e):

    valor = 0

    datos_entrada_lista = [ id_entrada,nombre_entrada,apellido_entrada,
                            ciudad_entrada,provincia_entrada,codigo_postal_entrada,
                            direccion_entrada,telefono_entrada,correo_entrada,
                            descripcion_entrada,producto_entrada,ventas_entrada,
                            saldo_entrada,inicio_entrada,ultima_entrada]

    # Almacenar los datos del registro seleccionado
    
    seleccionado = tabla1.focus()
    valores = tabla1.item(seleccionado,"values")
    
    # Borrar datos anteriores en los cuadrados de entradas
    # Agregar datos del registro en los cuadrados de entradas
    
    for entrada in datos_entrada_lista:
        entrada.delete(0,END)
        entrada.insert(0, valores[valor])

        if valor == 14:
            break
        else:
            valor +=1
def borrar_entradas():
    for entrada in lista_entradas:
        entrada.delete(0,END)

crear_ventana_login()
ventana_login_root.mainloop()
