import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
from tkinter import messagebox

def abrir_ventana_datos_torsion():
    ventana_principal.withdraw()  # Ocultar la ventana principal
    ventana_datos_torsion = tk.Toplevel(ventana_principal)
    ventana_datos_torsion.title("Datos de Entrada - Torsión")
    ventana_datos_torsion.geometry("600x600")
    ventana_datos_torsion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

    # Etiquetas y campos de entrada para los datos de torsión
    etiqueta_seccion = tk.Label(ventana_datos_torsion, text="Sección de la barra:",  font=("Arial", 10, "bold"))
    etiqueta_seccion.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    opciones_seccion = ["Circular"]
    seleccion_seccion = tk.StringVar(ventana_datos_torsion)
    seleccion_seccion.set(opciones_seccion[0])  # Seleccionar la primera opción por defecto
    menu_seccion = tk.OptionMenu(ventana_datos_torsion, seleccion_seccion, *opciones_seccion)
    menu_seccion.grid(row=0, column=1, padx=15, pady=10)

    etiqueta_diametro = tk.Label(ventana_datos_torsion, text="Diámetro de la barra [mm]:", font=("Arial", 10, "bold"))
    etiqueta_diametro.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    D_entry = tk.Entry(ventana_datos_torsion)
    D_entry.grid(row=1, column=1, padx=10, pady=10)

    etiqueta_longitud = tk.Label(ventana_datos_torsion, text="Longitud de la barra [mm]:", font=("Arial", 10, "bold"))
    etiqueta_longitud.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    L_entry = tk.Entry(ventana_datos_torsion)
    L_entry.grid(row=2, column=1, padx=10, pady=10)

    etiqueta_brazo_giro = tk.Label(ventana_datos_torsion, text="Brazo de giro [mm]:", font=("Arial", 10, "bold"))
    etiqueta_brazo_giro.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    b_entry = tk.Entry(ventana_datos_torsion)
    b_entry.grid(row=3, column=1, padx=10, pady=10)

    etiqueta_brazo_palanca = tk.Label(ventana_datos_torsion, text="Brazo de palanca [mm]:", font=("Arial", 10, "bold"))
    etiqueta_brazo_palanca.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    p_entry = tk.Entry(ventana_datos_torsion)
    p_entry.grid(row=4, column=1, padx=10, pady=10)

    # Etiquetas y campos de entrada para los datos medidos
    etiqueta_pesos = tk.Label(ventana_datos_torsion, text="Peso [N]:", font=("Arial", 10, "bold"))
    etiqueta_pesos.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
    
    pesos = []
    for i in range(6):
        W = tk.Entry(ventana_datos_torsion)
        W.grid(row=5+i+1, column=0, pady=10)
        pesos.append(W)
    
    etiqueta_desplazamientos_medido = tk.Label(ventana_datos_torsion, text="Desplazamiento en Y [mm]:", font=("Arial", 10, "bold"))
    etiqueta_desplazamientos_medido.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
    
    desplazamientos = []
    for i in range(6):
        delta = tk.Entry(ventana_datos_torsion)
        delta.grid(row=5+i+1, column=1, padx=10, pady=10)
        desplazamientos.append(delta)

    def guardar_datos():
    # Definir guardar los datos ingresados por el usuario, abrir la ventana de resultados de torsion y cerrar la ventana actual
        try:
            abrir_ventana_resultados_torsion([W.get() for W in pesos], [delta.get() for delta in desplazamientos], float(D_entry.get()), float(L_entry.get()), float(b_entry.get()), float(p_entry.get()))
            ventana_datos_torsion.destroy()
        except ValueError:
            messagebox.showerror("Error", "Todos los campos deben contener valores numéricos.")
    
    boton_calcular = tk.Button(ventana_datos_torsion, text="Calcular", font=("Arial", 10, "bold"), command=guardar_datos)
    boton_calcular.grid(row=14, column=1, columnspan=2, pady=10, sticky="nsew")

    # Botón para ir a la ventana principal nuevamente
    def cerrar_ventana_datos_torsion():
        ventana_datos_torsion.destroy()  # Cerrar la ventana de datos de torsión
        ventana_principal.deiconify()   # Mostrar la ventana principal nuevamente

    boton_inicio = tk.Button(ventana_datos_torsion, text="Inicio", font=("Arial", 10, "bold"), command=cerrar_ventana_datos_torsion)
    boton_inicio.grid(row=14, column=0, pady=10, sticky="nsew")

def abrir_ventana_resultados_torsion(pesos, desplazamientos, D, L, b, p):
    ventana_resultados_torsion = tk.Toplevel(ventana_principal)
    ventana_resultados_torsion.title("Resultados ensayo torsión")
    ventana_resultados_torsion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

    resultados = []
    for W, dY in zip(pesos, desplazamientos):
        W = float(W)
        dY = float(dY)
        
        # Cálculos utilizando los valores ingresados por el usuario
        phi = math.atan(dY / b)
        T = W * p 
        s = phi * (D/2)
        y = s / L
        tao_max = (16 * T) / (math.pi * (D ** 3))
        J = (math.pi * (D ** 4)) / 32
        G = (T * L) / (J * phi)
        
        resultados.append((f"{W:.2f}", f"{dY:.2f}", f"{phi:.3f}", f"{T:.2f}", f"{s:.5f}", f"{y:.6f}", f"{tao_max:.5f}", f"{G:.5f}"))

    # Crear tabla de resultados
    tabla_torsion = ttk.Treeview(ventana_resultados_torsion)
    tabla_torsion["columns"] = ("Peso", "Desplazamiento", "Phi", "T", "s", "y", "tao_max","G")  # Definir las columnas de la tabla
    tabla_torsion.heading("#0", text="ID")
    tabla_torsion.heading("Peso", text="W [N]")
    tabla_torsion.heading("Desplazamiento", text="dy [mm]")
    tabla_torsion.heading("Phi", text="∅ [rad]")
    tabla_torsion.heading("T", text="T [Nmm]")
    tabla_torsion.heading("s", text="s [mm]")
    tabla_torsion.heading("y", text="γ")
    tabla_torsion.heading("tao_max", text="τ max [MPa]")
    tabla_torsion.heading("G", text="G [MPa]")

    # Ajustar el ancho de las columnas
    tabla_torsion.column("#0", width=50, anchor="center") 
    tabla_torsion.column("Peso", width=50, anchor="center") 
    tabla_torsion.column("Desplazamiento", width=80, anchor="center") 
    tabla_torsion.column("Phi", width=80, anchor="center")  
    tabla_torsion.column("T", width=80, anchor="center")  
    tabla_torsion.column("s", width=80, anchor="center")
    tabla_torsion.column("y", width=80, anchor="center")
    tabla_torsion.column("tao_max", width=110, anchor="center")
    tabla_torsion.column("G", width=100, anchor="center")
    
    # Insertar resultados en la tabla
    for i, resultado in enumerate(resultados):
        tabla_torsion.insert("", "end", text=str(i+1), values=resultado)
    
    tabla_torsion.pack(padx=10, pady=10, fill="both", expand=True)

    # Dividir la tabla del boton
    marco_boton = tk.Frame(ventana_resultados_torsion, width=250, height=30, bg="lightgray")
    marco_boton.pack_propagate(False)
    marco_boton.pack(side="bottom", padx=10, pady=10)
    
    def graficos():
            abrir_ventana_grafica_torsion([W for W in pesos], [delta for delta in desplazamientos], float(D), float(L), float(b), float(p))
            ventana_resultados_torsion.destroy()
        
    boton_graficos = tk.Button(marco_boton, text="Graficar", font=("Arial", 10, "bold"), command=graficos)
    #boton_graficos.grid(row=8, column=1, pady=10, sticky="nsew")
    boton_graficos.pack(expand=False, fill="both")

def abrir_ventana_grafica_torsion(pesos, desplazamientos, D, L, b, p):
    ventana_grafica_torsion = tk.Toplevel(ventana_principal)
    ventana_grafica_torsion.title("Gráfica y tabla de resultados - Torsión")
    ventana_grafica_torsion.geometry("900x550")
    ventana_grafica_torsion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')
    
    valores_G = []
    resultados = []
    for W, dY in zip(pesos, desplazamientos):
        W = float(W)
        dY = float(dY)
        
        # Cálculos utilizando los valores ingresados por el usuario
        phi = math.atan(dY / b)
        T = W * p 
        s = phi * (D/2)
        y = s / L
        tao_max = (16 * T) / (math.pi * (D ** 3))
        J = (math.pi * (D ** 4)) / 32
        G = (T * L) / (J * phi)
        
        valores_G.append(f"{G:.5f}")

        resultados.append((f"{tao_max:.5f}", f"{y:.6f}"))

    # Calcular el promedio de los valores de G
    promedio_G = round(sum(float(valor_G) for valor_G in valores_G) / len(valores_G), 4)
    

    def crear_grafica(frame):
        # Crear figura y ejes para la gráfica
        fig, ax = plt.subplots()
        deformacion_unitaria = [float(resultado[1]) for resultado in resultados]
        esfuerzo_torsor_maximo = [float(resultado[0]) for resultado in resultados]
        fig, ax = plt.subplots(figsize=(6, 4)) #ajustar el tamaño de la grafica
        ax.plot(deformacion_unitaria, esfuerzo_torsor_maximo, marker='o', linestyle='-', color="black")
        ax.set_xlabel('Deformación unitaria x10^6')
        ax.set_ylabel('Esfuerzo torsor máximo (MPa)')
        ax.set_title('Esfuerzo Torsor Máximo vs Deformación Unitaria')
        ax.grid(True)
        
        # Mostrar la gráfica
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafica_torsion)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Función para formatear las etiquetas del eje x
        def format_x_axis(value, tick_number):
            return '{:.0f}'.format(value * 1e6)

        # Aplicar el formato personalizado al eje x
        ax.xaxis.set_major_formatter(FuncFormatter(format_x_axis))
            #canvas.get_tk_widget().pack(side="left", fill="both", padx=10, pady=10, expand=True)
    
    def crear_tabla(frame):
        # Crear tabla de resultados
        tabla = ttk.Treeview(ventana_grafica_torsion)
        tabla["columns"] = ("tao_max", "y")  
        tabla.heading("tao_max", text="τ max [MPa]")
        tabla.heading("y", text="γ")

        # Ajustar el ancho de las columnas
        tabla.column("#0", width=40, anchor="center") 
        tabla.column("tao_max", width=100, anchor="center")
        tabla.column("y", width=100, anchor="center")

        for i, resultado in enumerate(resultados):
            tabla.insert("", "end", text=str(i+1), values=resultado)
        
        tabla.grid(row=0, column=1, padx=10, pady=10)
        #tabla.pack(side="right", fill="both", padx=10, pady=10, expand=True)

    def crear_texto(frame):
    # Crear etiqueta para mostrar el módulo de rigidez
        etiqueta_modulo_rigidez = tk.Label(frame, text=f"El módulo de rigidez es: {promedio_G} MPa", font=("Arial", 10,"bold"), anchor="center", bg="white")
        etiqueta_modulo_rigidez.grid(row=1, column=0, padx=10, pady=10)


    frame_grafica = tk.Frame(ventana_grafica_torsion)
    frame_grafica.grid(row=0, column=0, padx=10, pady=10)
    crear_grafica(frame_grafica)

    # Crear frame para la tabla
    frame_tabla = tk.Frame(ventana_grafica_torsion)
    frame_tabla.grid(row=0, column=1, padx=10, pady=10)
    crear_tabla(frame_tabla)

    # Crear frame para el texto
    frame_texto = tk.Frame(ventana_grafica_torsion, bg="white")
    frame_texto.grid(row=1, column=0, padx=10, pady=10)
    crear_texto(frame_texto)

    def cerrar_ventana_graficos_torsion():
        ventana_grafica_torsion.destroy()  # Cerrar la ventana de datos de torsión
        ventana_principal.deiconify()   # Mostrar la ventana principal nuevamente

    boton_inicio = tk.Button(ventana_grafica_torsion, text="Inicio", font=("Arial", 10, "bold"), command=cerrar_ventana_graficos_torsion)
    boton_inicio.grid(row=2, column=0, pady=10)

def abrir_ventana_datos_flexion():
    ventana_principal.withdraw()  # Ocultar la ventana principal
    ventana_datos_flexion = tk.Toplevel(ventana_principal)
    ventana_datos_flexion.title("Datos de Entrada - Flexión")
    ventana_datos_flexion.geometry("600x600")
    ventana_datos_flexion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

    # Función para mostrar u ocultar los campos de entrada según la selección de la sección
    def mostrar_ocultar_rectangular():
        if seleccion_seccion.get() == "Rectangular":
            etiqueta_base.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            base.grid(row=2, column=1, padx=10, pady=5)
            etiqueta_altura.grid(row=3, column=0, padx=10, pady=5, sticky="w")
            altura.grid(row=3, column=1, padx=10, pady=5)
            # Ocultar los campos de la sección circular
            etiqueta_diametro.grid_remove()
            Diametro.grid_remove()
        else:
            etiqueta_base.grid_remove()
            base.grid_remove()
            etiqueta_altura.grid_remove()
            altura.grid_remove()
            # Mostrar los campos de la sección circular
            etiqueta_diametro.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            Diametro.grid(row=1, column=1, padx=10, pady=5)
            
    # Etiquetas y campos de entrada para los datos de flexión
    etiqueta_seccion = tk.Label(ventana_datos_flexion, text="Sección de la barra:",  font=("Arial", 10, "bold"))
    etiqueta_seccion.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    opciones_seccion = ["Circular", "Rectangular"]
    seleccion_seccion = tk.StringVar(ventana_datos_flexion)
    seleccion_seccion.set(opciones_seccion[0])  # Seleccionar la primera opción por defecto
    seleccion_seccion.trace("w", lambda *args: mostrar_ocultar_rectangular())  # Llamar a la función al cambiar la selección
    menu_seccion = tk.OptionMenu(ventana_datos_flexion, seleccion_seccion, *opciones_seccion)
    menu_seccion.grid(row=0, column=1, padx=10, pady=5)

    # Otros campos de entrada
    etiqueta_diametro = tk.Label(ventana_datos_flexion, text="Diámetro de la sección [mm]:",  font=("Arial", 10, "bold"))
    Diametro = tk.Entry(ventana_datos_flexion)

    etiqueta_base = tk.Label(ventana_datos_flexion, text="Base de la sección [mm]:",  font=("Arial", 10, "bold"))
    base = tk.Entry(ventana_datos_flexion)

    etiqueta_altura = tk.Label(ventana_datos_flexion, text="Altura de la sección [mm]:",  font=("Arial", 10, "bold"))
    altura = tk.Entry(ventana_datos_flexion)

    etiqueta_longitud = tk.Label(ventana_datos_flexion, text="Longitud de la barra [mm]:",  font=("Arial", 10, "bold"))
    longitud = tk.Entry(ventana_datos_flexion)

    etiqueta_seccion_1 = tk.Label(ventana_datos_flexion, text="Sección 1 aplicación de la carga [mm]:",  font=("Arial", 10, "bold"))
    seccion1 = tk.Entry(ventana_datos_flexion)
    etiqueta_deflexion = tk.Label(ventana_datos_flexion, text="Donde se mide la deflexión:",  font=("Arial", 10, "bold"))
    opciones_deflexion = ["Centro de la barra", "En x <= a", "En x > a"]
    seleccion_deflexion = tk.StringVar(ventana_datos_flexion)
    seleccion_deflexion.set(opciones_deflexion[0])  # Seleccionar la primera opción por defecto
    menu_deflexion = tk.OptionMenu(ventana_datos_flexion, seleccion_deflexion, *opciones_deflexion)

    etiqueta_punto_deflexion = tk.Label(ventana_datos_flexion, text="Punto donde se mide la deflexión [mm]:",  font=("Arial", 10, "bold"))
    punto_deflexion = tk.Entry(ventana_datos_flexion)

    etiqueta_longitud.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    longitud.grid(row=5, column=1, padx=10, pady=5)
    etiqueta_seccion_1.grid(row=6, column=0, padx=10, pady=5, sticky="w")
    seccion1.grid(row=6, column=1, padx=10, pady=5)
    etiqueta_deflexion.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    menu_deflexion.grid(row=7, column=1, padx=10, pady=5)
    etiqueta_punto_deflexion.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    punto_deflexion.grid(row=8, column=1, padx=10, pady=5)

    # Etiquetas y campos de entrada para los datos medidos
    etiqueta_pesos = tk.Label(ventana_datos_flexion, text="Peso [N]:", font=("Arial", 10, "bold"))
    etiqueta_pesos.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")
    pesos = []
    for i in range(6):
        peso = tk.Entry(ventana_datos_flexion)
        peso.grid(row=9+i+1, column=0, pady=10)
        pesos.append(peso)
    
    etiqueta_desplazamientos_medido = tk.Label(ventana_datos_flexion, text="Desplazamiento en Y [mm]:", font=("Arial", 10, "bold"))
    etiqueta_desplazamientos_medido.grid(row=9, column=1, padx=10, pady=10, sticky="nsew")
    desplazamientos = []
    for i in range(6):
        delta = tk.Entry(ventana_datos_flexion)
        delta.grid(row=9+i+1, column=1, padx=10, pady=10)
        desplazamientos.append(delta)

    mostrar_ocultar_rectangular()  # Mostrar u ocultar los campos según la selección inicial

    # Botón para cerrar la ventana de datos de flexión y mostrar la ventana principal nuevamente
    def cerrar_ventana_datos_flexion():
        ventana_datos_flexion.destroy()  # Cerrar la ventana de datos de flexión
        ventana_principal.deiconify()   # Mostrar la ventana principal nuevamente

    def guardar_datos():
    # Verificar si todos los campos están completos
        if any(not peso.get() or not dY.get() for peso, dY in zip(pesos, desplazamientos)):
            messagebox.showerror("Error", "Todos los campos deben estar completos.")
            return
        try:
            # Convertir los valores de los campos a flotantes
            pesos_float = [float(peso.get()) for peso in pesos]
            desplazamientos_float = [float(dY.get()) for dY in desplazamientos]
            if Diametro.get():
                Diametro_float = float(Diametro.get())
            else:
                Diametro_float = 0.0
                
            longitud_float = float(longitud.get())

            if base.get():
                base_float = float(base.get())
            else:
                base_float = 0.0
            
            if altura.get():
                altura_float = float(altura.get())
            else:
                altura_float = 0.0
            
            seccion1_float = float(seccion1.get())
            punto_deflexion_float = float(punto_deflexion.get())
            seleccion_deflexion_str = seleccion_deflexion.get()
            seleccion_seccion_str = seleccion_seccion.get()
  
            # Abrir la ventana de resultados de flexión con los datos ingresados
            abrir_ventana_resultados_flexion(pesos_float, desplazamientos_float, Diametro_float, longitud_float, base_float, altura_float, seccion1_float, punto_deflexion_float, seleccion_deflexion_str, seleccion_seccion_str)
            
            # Cerrar la ventana de datos de flexión
            ventana_datos_flexion.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Todos los campos deben contener valores numéricos.")
    
    boton_inicio = tk.Button(ventana_datos_flexion, text="Inicio", font=("Arial", 10, "bold"), command=cerrar_ventana_datos_flexion)
    boton_inicio.grid(row=16, column=0, pady=10, sticky="nsew")

    boton_calcular = tk.Button(ventana_datos_flexion, text="Calcular", font=("Arial", 10, "bold"), command=guardar_datos)
    boton_calcular.grid(row=16, column=1, columnspan=2, pady=10, sticky="nsew")

def abrir_ventana_resultados_flexion(pesos, desplazamientos, Diametro, longitud, base, altura, seccion1, punto_deflexion,seleccion_deflexion,seleccion_seccion):
    ventana_resultados_flexion = tk.Toplevel(ventana_principal)
    ventana_resultados_flexion.title("Resultados de Flexión")
    ventana_resultados_flexion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

    resultados = []
    for peso, dY in zip(pesos, desplazamientos):
        peso = float(peso)
        dY = float(dY)
        
        if seleccion_seccion == "Rectangular":
            B = base
            H = altura

            # Calcular Sección 2 de aplicación de la carga en mm
            b = longitud - seccion1
            c = H / 2
            # Calcular Momento de inercia en mm^4
            I = (B * (H ** 3)) / 12

            # Calcular Momento flector máximo en Nmm
            M_max = seccion1 * (peso * (longitud - seccion1) / longitud)

            # Calcular Esfuerzo flector máximo en MPa
            sigma_max = (M_max * c) / I

            # Calcular Módulo Elástico en MPa
            Pd = seleccion_deflexion
            if Pd == "Centro de la barra":
                E = (peso * b * (3 * longitud ** 2 - 4 * b ** 2)) / (48 * dY * I)

            elif Pd == "En x <= a":
                x = float(punto_deflexion)
                E = ((peso * b * x) * (longitud ** 2 - b ** 2 - x ** 2)) / (6 * longitud * I * dY)

            elif Pd == "En x > a":
                print("Opción aún no disponible")

            else:
                print("Opción de medición de deflexión no válida.")
                return None

            # Calcular Deflexión máxima
            delta_max = (peso * b * (longitud ** 2 - b ** 2) ** (3/2)) / (9 * math.sqrt(3) * longitud * E * I)

            resultados.append([peso, dY, b, M_max, sigma_max, delta_max])

        elif seleccion_seccion == "Circular":
            D = Diametro
            L = longitud

            # Calcular Sección 2 de aplicación de la carga en mm
            b = L - seccion1

            # Calcular Distancia al Eje neutro en mm
            c = D / 2

            # Calcular Momento flector máximo en Nmm
            M_max = seccion1 * (peso * (L - seccion1) / L)

            # Calcular Momento de inercia en mm^4
            I = (math.pi / 32) * (D ** 4)

            # Calcular Esfuerzo flector máximo en MPa
            sigma_max = (M_max * c) / I

            # Calcular Módulo Elástico en MPa
            Pd = seleccion_deflexion
            if Pd == "Centro de la barra":
                E = (peso * b * (3 * L ** 2 - 4 * b ** 2)) / (48 * dY * I)

            elif Pd == "En x <= a":
                x = float(punto_deflexion)
                E = ((peso * b * x) * (L ** 2 - b ** 2 - x ** 2)) / (6 * L * I * dY)

            elif Pd == "En x > a":
                print("Opción aún no disponible")

            else:
                print("Opción de medición de deflexión no válida.")
                return None

            # Calcular Deflexión máxima
            delta_max = (peso * b * (L ** 2 - b ** 2) ** (3/2)) / (9 * math.sqrt(3) * L * E * I)

            resultados.append((f"{peso:.2f}", f"{dY:.2f}", f"{b:.3f}", f"{M_max:.2f}", f"{sigma_max:.5f}", f"{delta_max:.6f}"))
            
        else:
            print("Tipo de sección no reconocido.")
            return None
        
        
    # Crear tabla de resultados
    tabla_flexion = ttk.Treeview(ventana_resultados_flexion)
    tabla_flexion["columns"] = ("Peso", "Deformación", "b","Momento_max", "esf_max", "delta_max")
    tabla_flexion.heading("#0", text="ID")
    tabla_flexion.heading("Peso", text="W [N]")
    tabla_flexion.heading("Deformación", text="δ [mm]")
    tabla_flexion.heading("b", text="b [mm]")
    tabla_flexion.heading("Momento_max", text="M max [Nmm]")
    tabla_flexion.heading("esf_max", text="σ max [MPa]")
    tabla_flexion.heading("delta_max", text="δ max [MPa]")

    # Ajustar el ancho de las columnas
    tabla_flexion.column("#0", width=40)  # Ajustar el ancho de la primera columna
    tabla_flexion.column("Peso", width=60, anchor="center")  # Ajustar el ancho de la segunda columna
    tabla_flexion.column("Deformación", width=100, anchor="center")  # Ajustar el ancho de la segunda columna
    tabla_flexion.column("b", width=100, anchor="center")  # Ajustar el ancho de la tercera columna
    tabla_flexion.column("Momento_max", width=100, anchor="center")  # Ajustar el ancho de la cuarta columna
    tabla_flexion.column("esf_max", width=100, anchor="center")
    tabla_flexion.column("delta_max", width=100, anchor="center")
    
    for i, resultado in enumerate(resultados):
        tabla_flexion.insert("", "end", text=str(i+1), values=resultado)

    tabla_flexion.pack(padx=10, pady=10, fill="both", expand=True)

    # Dividir la tabla del boton
    marco_boton_flexion = tk.Frame(ventana_resultados_flexion, width=250, height=30, bg="lightgray")
    marco_boton_flexion.pack_propagate(False)
    marco_boton_flexion.pack(side="bottom", padx=10, pady=10)

    def graficos_flexion():
            abrir_ventana_grafica_flexion(pesos, desplazamientos, Diametro, longitud, base, altura, seccion1, punto_deflexion, seleccion_deflexion, seleccion_seccion)
            ventana_resultados_flexion.destroy()
    
    boton_graficos = tk.Button(marco_boton_flexion, text="Graficar", font=("Arial", 10, "bold"), command=graficos_flexion)
    #boton_graficos.grid(row=8, column=1, pady=10, sticky="nsew")
    boton_graficos.pack(expand=False, fill="both")

def abrir_ventana_grafica_flexion(pesos, desplazamientos, Diametro, longitud, base, altura, seccion1, punto_deflexion, seleccion_deflexion,seleccion_seccion):
    ventana_grafica_flexion = tk.Toplevel(ventana_principal)
    ventana_grafica_flexion.title("Gráfica y tabla de resultados - Flexion")
    ventana_grafica_flexion.geometry("900x550")
    ventana_grafica_flexion.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

    valores_E = []
    resultados = []
    for pesos, dY in zip(pesos, desplazamientos):
        pesos = float(pesos)
        dY = float(dY)

        if seleccion_seccion == "Rectangular":
            # Calcular Sección 2 de aplicación de la carga en mm
            b = longitud - seccion1
            c = altura / 2
            # Calcular Momento de inercia en mm^4
            I = (base * (altura ** 3)) / 12
            # Calcular Momento flector máximo en Nmm
            M_max = seccion1 * (pesos * (longitud - seccion1) / longitud)
            # Calcular Esfuerzo flector máximo en MPa
            sigma_max = (M_max * c) / I
            # Calcular Módulo Elástico en MPa
            Pd = seleccion_deflexion
            
            if Pd == "Centro de la barra":
                E = (pesos * b * (3 * longitud ** 2 - 4 * b ** 2)) / (48 * dY * I)

            elif Pd == "En x <= a":
                x = float(punto_deflexion)
                E = ((pesos * b * x) * (longitud ** 2 - b ** 2 - x ** 2)) / (6 * longitud * I * dY)

            elif Pd == "En x > a":
                print("Opción aún no disponible")

            else:
                print("Opción de medición de deflexión no válida.")
                return None

            # Calcular Deflexión máxima
            delta_max = (pesos * b * (longitud ** 2 - b ** 2) ** (3/2)) / (9 * math.sqrt(3) * longitud * E * I)

            valores_E.append(E)
            resultados.append([f"{sigma_max:.5f}", f"{delta_max:.6f}",f"{E:.6f}"])

        elif seleccion_seccion == "Circular":
            D = Diametro
            L = longitud
            # Calcular Sección 2 de aplicación de la carga en mm
            b = L - seccion1
            # Calcular Distancia al Eje neutro en mm
            c = D / 2
            # Calcular Momento flector máximo en Nmm
            M_max = seccion1 * (pesos * (L - seccion1) / L)
            # Calcular Momento de inercia en mm^4
            I = (math.pi / 32) * (D ** 4)
            # Calcular Esfuerzo flector máximo en MPa
            sigma_max = (M_max * c) / I

            # Calcular Módulo Elástico en MPa
            Pd = seleccion_deflexion
            if Pd == "Centro de la barra":
                E = (pesos * b * (3 * L ** 2 - 4 * b ** 2)) / (48 * dY * I)

            elif Pd == "En x <= a":
                x = float(punto_deflexion)
                E = ((pesos * b * x) * (L ** 2 - b ** 2 - x ** 2)) / (6 * L * I * dY)

            elif Pd == "En x > a":
                print("Opción aún no disponible")

            else:
                print("Opción de medición de deflexión no válida.")
                return None

            # Calcular Deflexión máxima
            delta_max = (pesos * b * (L ** 2 - b ** 2) ** (3/2)) / (9 * math.sqrt(3) * L * E * I)

            valores_E.append(E)
            resultados.append((f"{sigma_max:.5f}", f"{delta_max:.6f}",f"{E:.6f}" ))
            
        else:
            print("Tipo de sección no reconocido.")
            return None
        
    # Calcular el promedio de los valores de G
    promedio_E = sum(valores_E) / len(valores_E)

    def crear_grafica(frame):
        # Crear figura y ejes para la gráfica
        fig, ax = plt.subplots()
        deformacion_unitaria = [float(resultado[1]) for resultado in resultados]
        esfuerzo_torsor_maximo = [float(resultado[0]) for resultado in resultados]
        fig, ax = plt.subplots(figsize=(6, 4)) #ajustar el tamaño de la grafica
        ax.plot(deformacion_unitaria, esfuerzo_torsor_maximo, marker='o', linestyle='-')
        ax.set_xlabel('Deformación unitaria x10^6')
        ax.set_ylabel('Esfuerzo flector máximo (MPa)')
        ax.set_title('Esfuerzo flector Máximo vs Deformación Unitaria')
        ax.grid(True)
        
        # Mostrar la gráfica
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafica_flexion)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Función para formatear las etiquetas del eje x
        def format_x_axis(value, tick_number):
            return '{:.0f}'.format(value * 1e6)

        # Aplicar el formato personalizado al eje x
        ax.xaxis.set_major_formatter(FuncFormatter(format_x_axis))
            #canvas.get_tk_widget().pack(side="left", fill="both", padx=10, pady=10, expand=True)
    
    def crear_tabla(frame):
        # Crear tabla de resultados
        tabla_grafica_flexion = ttk.Treeview(ventana_grafica_flexion)
        tabla_grafica_flexion["columns"] = ("sigma_max", "y")  
        tabla_grafica_flexion.heading("sigma_max", text="σ máx [MPa]")
        tabla_grafica_flexion.heading("y", text="ε")

        # Ajustar el ancho de las columnas
        tabla_grafica_flexion.column("#0", width=40, anchor="center") 
        tabla_grafica_flexion.column("sigma_max", width=100, anchor="center")
        tabla_grafica_flexion.column("y", width=100, anchor="center")

        for i, resultado in enumerate(resultados):
            tabla_grafica_flexion.insert("", "end", text=str(i+1), values=resultado)
        
        tabla_grafica_flexion.grid(row=0, column=1, padx=10, pady=10)
        #tabla.pack(side="right", fill="both", padx=10, pady=10, expand=True)

    def crear_texto(frame):
    # Crear etiqueta para mostrar el módulo de rigidez
        etiqueta_modulo_rigidez = tk.Label(frame, text=f"El módulo elastico es: {promedio_E} MPa", font=("Arial", 10,"bold"), bg="white")
        etiqueta_modulo_rigidez.grid(row=1, column=0, padx=10, pady=10)


    frame_grafica = tk.Frame(ventana_grafica_flexion)
    frame_grafica.grid(row=0, column=0, padx=10, pady=10)
    crear_grafica(frame_grafica)

    # Crear frame para la tabla
    frame_tabla = tk.Frame(ventana_grafica_flexion)
    frame_tabla.grid(row=0, column=1, padx=10, pady=10)
    crear_tabla(frame_tabla)

    # Crear frame para el texto
    frame_texto = tk.Frame(ventana_grafica_flexion, bg="white")
    frame_texto.grid(row=1, column=0, padx=10, pady=10)
    crear_texto(frame_texto)

    def cerrar_ventana_graficos_flexion():
        ventana_grafica_flexion.destroy()  # Cerrar la ventana de datos de torsión
        ventana_principal.deiconify()   # Mostrar la ventana principal nuevamente

    boton_inicio = tk.Button(ventana_grafica_flexion, text="Inicio", font=("Arial", 10, "bold"), command=cerrar_ventana_graficos_flexion)
    boton_inicio.grid(row=2, column=0, pady=10)

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ensayos de Resistencia de Materiales")
ventana_principal.geometry("600x400")
ventana_principal.iconbitmap('C:/Users/camil/Desktop/U/PG/PROGRAMA/logo_de_la_universidad_del_atl__ntico_svg_HDx_icon.ico')

# Maximizar la ventana principal
# ventana_principal.state("zoomed")

# Cargar imagenes
imagen_torsion = tk.PhotoImage(file="C:/Users/camil/Desktop/U/PG/PROGRAMA/torsion.png")
imagen_flexion = tk.PhotoImage(file="C:/Users/camil/Desktop/U/PG/PROGRAMA/flexion.png")

# Dividir la ventana principal en dos partes
marco_torsion = tk.Frame(ventana_principal, width=280, height=400, bg="lightgray")
marco_torsion.pack_propagate(False)
marco_torsion.pack(side="left", padx=10, pady=10)

marco_flexion = tk.Frame(ventana_principal, width=280, height=400, bg="lightgray")
marco_flexion.pack_propagate(False)
marco_flexion.pack(side="right", padx=10, pady=10)

def señalar(event):
    # Cambiar el cursor a una mano cuando pasa sobre el botón
    ventana_principal.config(cursor="hand2")

def quitar_señal(event):
    # Restaurar el cursor a la forma predeterminada cuando sale del botón
    ventana_principal.config(cursor="")

# Botón para abrir la ventana de datos de torsión
boton_torsion = tk.Button(marco_torsion, text="Torsión", font=("Arial", 30, "bold"), compound="bottom", pady=20, fg="gray", bg="lightgray", image=imagen_torsion, command=abrir_ventana_datos_torsion)
boton_torsion.pack(expand=True, fill="both")
boton_torsion.bind("<Enter>", señalar)  # Cuando el cursor entra en el botón
boton_torsion.bind("<Leave>", quitar_señal)  # Cuando el cursor sale del botón

# Botón para abrir la ventana de datos de flexión
boton_flexion = tk.Button(marco_flexion, text="Flexión", font=("Arial", 30, "bold"), compound="bottom", pady=20, fg="gray", bg="lightgray", image=imagen_flexion, command=abrir_ventana_datos_flexion)
boton_flexion.pack(expand=True, fill="both")
boton_flexion.bind("<Enter>", señalar)  # Cuando el cursor entra en el botón
boton_flexion.bind("<Leave>", quitar_señal)  # Cuando el cursor sale del botón

ventana_principal.mainloop()