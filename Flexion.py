import math

def ensayo_flexion():
    # Solicitar tipo de sección al usuario
    tipo_seccion = input("Ingrese el tipo de sección (circular o rectangular): ").lower()
    
    if tipo_seccion == "rectangular":
        # Solicitar datos de entrada para sección rectangular
        B = float(input("Ingrese la longitud de la base en mm: "))
        H = float(input("Ingrese la longitud de la altura en mm: "))
        L = float(input("Ingrese la longitud de la barra en mm: "))
        a = float(input("Ingrese la sección 1 de aplicación de la carga en mm: "))
        W = float(input("Ingrese el peso en N: "))
        Pd = int(input("Ingrese donde se mide la deflexion (1: centro, 2: x<=a, 3: x>a): "))
        rect = input("Ingrese la disposición del rectángulo (vertical/horizontal): ").lower()
        x = float(input("Ingrese el punto donde se mide la deflexion en mm: "))
        delta = float(input("Ingrese la deflexion medida en mm: "))
        
        # Calcular Sección 2 de aplicación de la carga en mm
        b = L - a

        # Calcular Distancia al Eje neutro en mm
        if rect == "vertical":
            c = H / 2
            # Calcular Momento de inercia en mm^4
            I = (B * (H ** 3)) / 12
            
        elif rect == "horizontal":
            c = B / 2
            # Calcular Momento de inercia en mm^4
            I = (H * (B ** 3)) / 12
            
        else:
            print("Opcion de disposicion no valida.")
            return None
                
        # Calcular Momento flector máximo en Nmm
        M_max = a * (W * (L - a) / L)

        # Calcular Esfuerzo flector máximo en MPa
        sigma_max = (M_max * c) / I
        
        # Calcular Módulo Elástico en MPa
        if Pd == 1:
            E = (W * b * (3 * L ** 2 - 4 * b **2))/(48 * delta * I)
            
        elif Pd == 2:
            E = ((W * b * x) * (L ** 2 - b ** 2 - x **2))/(6 * L * I * delta)
            
        elif Pd == 3:
           # E = sigma_max
           print("Opcion aun no disponible")
            
        else:
            print("Opcion de medicion de deflexion no valida.")
            return None
        
        # Calcular Deflexión máxima
        delta_max = (W * b *(L ** 2 - b ** 2)**(3/2))/(9 * 1.732 * L * E * I)
        
        return M_max, I, sigma_max, E, delta_max

    elif tipo_seccion == "circular":
        # Solicitar datos de entrada para sección circular
        D = float(input("Ingrese el diametro de la barra en mm: "))
        L = float(input("Ingrese la longitud de la barra en mm: "))
        a = float(input("Ingrese la seccion 1 de aplicacion de la carga en mm: "))
        W = float(input("Ingrese el peso en N: "))
        Pd = int(input("Ingrese donde se mide la deflexion (1: centro, 2: x<=a, 3: x>a): "))
        x = float(input("Ingrese el punto donde se mide la deflexion en mm: "))
        delta = float(input("Ingrese la deflexion medida en mm: "))
        
        # Calcular Sección 2 de aplicación de la carga en mm
        b = L - a
        
        # Calcular Distancia al Eje neutro en mm
        c = D / 2

        # Calcular Momento flector máximo en Nmm
        M_max = a * (W * (L - a) / L)

        # Calcular Momento de inercia en mm^4
        I = (math.pi / 32) * (D ** 4)

        # Calcular Esfuerzo flector máximo en MPa
        sigma_max = (M_max * c) / I
                
        # Calcular Módulo Elástico en MPa
        if Pd == 1:
            E = (W * b * (3 * L ** 2 - 4 * b **2))/(48 * delta * I)
            
        elif Pd == 2:
            E = ((W * b * x) * (L ** 2 - b ** 2 - x ** 2))/(6 * L * I * delta)
            
        elif Pd == 3:
           # E = sigma_max
           print("Opcion aun no disponible")
            
        else:
            print("Opcion de medicion de deflexion no valida.")
            return None
        
        # Calcular Deflexión máxima
        delta_max = (W * b * (L ** 2 - b ** 2) ** (3/2))/(9 * math.sqrt(3) * L * E * I)
        
        return M_max, I, sigma_max, E, delta_max

    else:
        print("Tipo de seccion no reconocido.")
        return None

# Obtener los resultados llamando a la función y desempaquetarlos
resultado = ensayo_flexion()

# Imprimir los resultados
print("Momento flector maximo (Nmm):", resultado[0])
print("Momento de inercia (mm^4):", resultado[1])
print("Esfuerzo flector maximo (MPa):", resultado[2])
print("Modulo Elastico (MPa):", resultado[3])
print("Deflexion maxima (mm):", resultado[4])