# Función de cifrado César
def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            resultado += chr((ord(char) + desplazamiento - offset) % 26 + offset)
        else:
            resultado += char
    return resultado

# Función para mostrar el menú principal
def mostrar_menu_principal():
    print("\n--- Menú Principal ---")
    print("1. Agregar Usuario")
    print("2. Iniciar Sesión")
    print("0. Salir")

# Función para mostrar el menú de gestión de contraseñas
def mostrar_menu():
    print("\nGestor de Contraseñas")
    print("1. Registrar nueva contraseña")
    print("2. Ver contraseña registrada")
    print("3. Modificar contraseña o datos de servicio")
    print("4. Eliminar contraseña registrada")
    print("5. Mostrar servicios registrados")
    print("6. Cerrar sesión")

# Función para agregar un nuevo usuario
def agregar_usuario(usuarios, claves_maestras):
    while True:
        username = input("Ingrese un nombre de usuario (máximo 10 caracteres): ")
        if len(username) <= 10:
            break
        else:
            print("El nombre de usuario no puede ser mayor a 10 caracteres.")
    
    while True:
        pin = input("Ingrese un PIN de acceso (3 dígitos, entre 001 y 999): ")
        if pin.isdigit() and 1 <= int(pin) <= 999:
            pin = pin.zfill(3)  # Esta parte del código asegura que el PIN tenga siempre 3 dígitos
            break
        else:
            print("El PIN debe ser un número de 3 dígitos entre 001 y 999.")
    
    usuarios[username.lower()] = pin
    claves_maestras[username.lower()] = None  # El usuario en un principio no tiene una clave maestra definida
    print(f"Usuario {username} registrado exitosamente.")

# Función para iniciar sesión
def iniciar_sesion(usuarios, claves_maestras):
    if not usuarios:  # Se verifican si existen usuarios registrados
        print("No hay usuarios registrados.")
        return None, None
    
    username = input("Ingrese su nombre de usuario: ").lower()
    if username in usuarios:
        pin = input("Ingrese su PIN: ").zfill(3)
        if pin == usuarios[username]:
            print(f"Bienvenido {username}!")
            clave_maestra = claves_maestras.get(username)
            if not clave_maestra:
                print("Es necesario que configure su clave maestra para realizar cambios almacenados en su usuario.")
                clave_maestra = pedir_clave()
                claves_maestras[username] = clave_maestra  # Se almacena la clave maestra asociada al usuario
            return username, clave_maestra  # Se retorna el nombre de usuario junto con su clave maestra
        else:
            print("PIN incorrecto. Inténtelo de nuevo.")
            return None, None
    else:
        print("Usuario no encontrado.")
        return None, None

# Función para registrar una nueva contraseña
def registrar_contraseña(contraseñas):
    servicio = input("Ingrese el nombre del servicio que desea registrar: ").lower()
    usuario = input("Ingrese el nombre de usuario o correo electrónico: ")
    contraseña = input("Ingrese la contraseña para este servicio: ")
    
    contraseña_cifrada = cifrado_cesar(contraseña, 3)
    contraseñas[servicio] = {'usuario': usuario, 'contraseña': contraseña_cifrada}
    print(f"\nContraseña para {servicio} registrada exitosamente.")

# Función para ver las contraseñas registradas
def ver_contraseña(contraseñas):
    servicio = input("\nIngrese el nombre del servicio del cual desea ver la contraseña: ").lower()
    if servicio in contraseñas:
        datos = contraseñas[servicio]
        contraseña_descifrada = cifrado_cesar(datos['contraseña'], -3)
        print(f"\nServicio: {servicio}")
        print(f"  Usuario: {datos['usuario']}")
        print(f"  Contraseña: {contraseña_descifrada}")
    else:
        print(f"\nEl servicio '{servicio}' no se encuentra registrado.")

# Función para modificar datos de un servicio
def modificar_contraseña(contraseñas):
    servicio = input("\nIngrese el nombre del servicio a modificar: ").lower()
    if servicio in contraseñas:
        print("¿Qué desea modificar?")
        print("1. Modificar usuario")
        print("2. Modificar contraseña")
        print("3. Modificar ambos")
        opcion = input("Escoga una opción: ")
        
        if opcion == '1' or opcion == '3':
            nuevo_usuario = input("Ingrese el nuevo nombre de usuario o correo electrónico: ")
            contraseñas[servicio]['usuario'] = nuevo_usuario
        if opcion == '2' or opcion == '3':
            nueva_contraseña = input("Ingrese la nueva contraseña: ")
            contraseñas[servicio]['contraseña'] = cifrado_cesar(nueva_contraseña, 3)
        
        print(f"\nDatos de {servicio} actualizados exitosamente.")
    else:
        print(f"\nEl servicio {servicio} no se encuentra registrado.")

# Función para eliminar un servicio registrado
def eliminar_contraseña(contraseñas):
    servicio = input("\nIngrese el nombre del servicio a eliminar: ").lower()
    if servicio in contraseñas:
        del contraseñas[servicio]
        print(f"\nEl servicio {servicio} ha sido eliminado.")
    else:
        print(f"\nEl servicio {servicio} no se encuentra registrado.")

# Función para mostrar los servicios registrados
def mostrar_servicios_registrados(contraseñas):
    if contraseñas:
        print("\nServicios registrados:")
        for servicio in contraseñas.keys():
            print(f" - {servicio}")
    else:
        print("\nNo existen servicios registrados.")

# Función para solicitar y validar la clave maestra
def pedir_clave():
    clave = input("Ingrese una clave maestra para esta cuenta: ")
    return cifrado_cesar(clave, 3)

def validar_clave(clave_almacenada, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        clave_ingresada = input("\nIngrese la clave maestra asociada a esta cuenta para continuar con la acción: ")
        clave_ingresada_cifrada = cifrado_cesar(clave_ingresada, 3)
        if clave_ingresada_cifrada == clave_almacenada:
            return True
        else:
            intentos += 1
            print(f"Clave incorrecta. Intentos restantes: {max_intentos - intentos}")
    
    print("\nDemasiados intentos fallidos. Volviendo al menú.")
    return False

# Función principal del programa
def main():
    usuarios = {}  # Diccionario para almacenar los usuarios y sus PINES
    claves_maestras = {}  # Diccionario para almacenar la clave maestra de cada usuario
    contraseñas = {}  # Diccionario para almacenar las contraseñas registradas
    usuario_actual = None
    clave_maestra = None  # Clave maestra que se asignará después de iniciar sesión

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':  # Registrar un nuevo usuario en el sistema
            agregar_usuario(usuarios, claves_maestras)
        elif opcion == '2':  # Iniciar sesión en el sistema
            usuario_actual, clave_maestra = iniciar_sesion(usuarios, claves_maestras)
            if usuario_actual:  # Si el inicio de sesión fue exitoso se ejecuta el menú de gestión de contraseñas
                while usuario_actual:
                    mostrar_menu()
                    opcion = input("Seleccione una opción: ")

                    if opcion in {'1', '2', '3', '4', '5'}:
                        if validar_clave(clave_maestra):  # Usamos la clave maestra aquí
                            if opcion == '1':
                                registrar_contraseña(contraseñas)
                            elif opcion == '2':
                                ver_contraseña(contraseñas)
                            elif opcion == '3':
                                modificar_contraseña(contraseñas)
                            elif opcion == '4':
                                eliminar_contraseña(contraseñas)
                            elif opcion == '5':
                                mostrar_servicios_registrados(contraseñas)
                    elif opcion == '6':  # Esta función cierrar sesión del usuario
                        print("Cerrando sesión...\n")
                        break
                    else:
                        print("Opción no válida.")
        elif opcion == '0':  # Esta opción cierra el programa
            print("Saliendo del gestor de contraseñas...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()