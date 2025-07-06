import os
import json

ARCHIVO_USUARIOS = "usuarios.json"

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

# Funciones de color con ANSI Escape Codes
class Colores:
    ROJO = "\033[31m"
    VERDE = "\033[32m"
    AMARILLO = "\033[33m"
    AZUL = "\033[34m"
    MORADO = "\033[35m"
    CIAN = "\033[36m"
    BLANCO = "\033[37m"
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    SUBRAYADO = "\033[4m"

# Función para limpiar la terminal
def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para pausar la ejecución
def pausar():
    input("\nPresione Enter para continuar...")

# Función para mostrar el menú principal
def mostrar_menu_principal():
    print(Colores.CIAN + Colores.NEGRITA + "\n--- Menú Principal ---")
    print(Colores.RESET + "1. Agregar Usuario")
    print("2. Iniciar Sesión")
    print("0. Salir")

# Función para mostrar el menú de gestión de contraseñas
def mostrar_menu():
    print(Colores.CIAN + Colores.NEGRITA + "\nGestor de Contraseñas")
    print(Colores.RESET + "1. Registrar nueva contraseña")
    print("2. Ver contraseña registrada")
    print("3. Modificar contraseña o datos de servicio")
    print("4. Eliminar contraseña registrada")
    print("5. Mostrar servicios registrados")
    print("6. Cerrar sesión")

# Archivo JSON: usuarios
def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2)

# Función para agregar un nuevo usuario
def agregar_usuario(usuarios):
    limpiar_terminal()
    while True:
        username = input("Ingrese un nombre de usuario (máximo 10 caracteres): ").lower()
        if len(username) <= 10 and username not in usuarios:
            break
        print(Colores.ROJO + "Nombre inválido o ya existe." + Colores.RESET)
   
    while True:
        pin = input("Ingrese un PIN de acceso (3 dígitos, entre 001 y 999): ")
        if pin.isdigit() and 1 <= int(pin) <= 999:
            pin = pin.zfill(3)
            break
        print(Colores.ROJO + "PIN inválido." + Colores.RESET)
   
    usuarios[username] = {
        "pin": pin,
        "clave_maestra": None,
        "servicios": {}
    }
    guardar_usuarios(usuarios)
    print(Colores.VERDE + f"Usuario {username} registrado exitosamente." + Colores.RESET)
    pausar()

# Función para configurar la clave maestra
def pedir_clave():
    limpiar_terminal()
    clave = input("Ingrese una clave maestra para esta cuenta: ")
    return cifrado_cesar(clave, 3)

# Función para iniciar sesión en un usuario del gestor
def iniciar_sesion(usuarios):
    limpiar_terminal()
    if not usuarios:
        print(Colores.AMARILLO + "No hay usuarios registrados." + Colores.RESET)
        pausar()
        return None, None

    username = input("Ingrese su nombre de usuario: ").lower()
    if username not in usuarios:
        print(Colores.ROJO + "Usuario no encontrado." + Colores.RESET)
        pausar()
        return None, None

    pin = input("Ingrese su PIN: ").zfill(3)
    limpiar_terminal()
    if pin != usuarios[username]["pin"]:
        print(Colores.ROJO + "PIN incorrecto." + Colores.RESET)
        pausar()
        return None, None

    print(Colores.VERDE + f"Bienvenido {username}!" + Colores.RESET)
    if not usuarios[username]["clave_maestra"]:
        print(Colores.MORADO + "Primera vez: configure una clave maestra." + Colores.RESET)
        usuarios[username]["clave_maestra"] = pedir_clave()
        guardar_usuarios(usuarios)
    pausar()
    return username, usuarios[username]["clave_maestra"]

# Función para validar la clave maestra
def validar_clave(clave_almacenada, max_intentos=3):
    for i in range(max_intentos):
        limpiar_terminal()
        clave = input("Ingrese su clave maestra para continuar: ")
        if cifrado_cesar(clave, 3) == clave_almacenada:
            return True
        print(Colores.ROJO + f"Clave incorrecta. Intentos restantes: {max_intentos - i - 1}" + Colores.RESET)
        pausar()
    print(Colores.ROJO + "Demasiados intentos. Volviendo al menú." + Colores.RESET)
    pausar()
    return False

# Función para registrar una nueva contraseña
def registrar_contraseña(usuario, usuarios):
    limpiar_terminal()
    servicio = input("Servicio: ").lower()
    usuario_servicio = input("Usuario/correo: ")
    contraseña = input("Contraseña: ")
    usuarios[usuario]["servicios"][servicio] = {
        "usuario": usuario_servicio,
        "contraseña": cifrado_cesar(contraseña, 3)
    }
    guardar_usuarios(usuarios)
    print(Colores.VERDE + f"Contraseña para {servicio} registrada." + Colores.RESET)
    pausar()

# Función para ver las contraseñas registradas
def ver_contraseña(usuario, usuarios):
    limpiar_terminal()
    servicio = input("Servicio: ").lower()
    servicios = usuarios[usuario]["servicios"]
    if servicio in servicios:
        datos = servicios[servicio]
        print(Colores.CIAN + f"Usuario: {datos['usuario']}")
        print(f"Contraseña: {cifrado_cesar(datos['contraseña'], -3)}" + Colores.RESET)
    else:
        print(Colores.ROJO + "Servicio no registrado." + Colores.RESET)
    pausar()

# Función para modificar datos de un servicio
def modificar_contraseña(usuario, usuarios):
    limpiar_terminal()
    servicio = input("Servicio a modificar: ").lower()
    servicios = usuarios[usuario]["servicios"]
    if servicio in servicios:
        print("1. Modificar usuario")
        print("2. Modificar contraseña")
        print("3. Modificar ambos")
        op = input("Opción: ")
        if op == '1' or op == '3':
            servicios[servicio]["usuario"] = input("Nuevo usuario/correo: ")
        if op == '2' or op == '3':
            nueva = input("Nueva contraseña: ")
            servicios[servicio]["contraseña"] = cifrado_cesar(nueva, 3)
        guardar_usuarios(usuarios)
        print(Colores.VERDE + "Datos actualizados." + Colores.RESET)
    else:
        print(Colores.ROJO + "Servicio no registrado." + Colores.RESET)
    pausar()

# Función para eliminar un servicio registrado
def eliminar_contraseña(usuario, usuarios):
    limpiar_terminal()
    servicio = input("Servicio a eliminar: ").lower()
    servicios = usuarios[usuario]["servicios"]
    if servicio in servicios:
        del servicios[servicio]
        guardar_usuarios(usuarios)
        print(Colores.VERDE + "Servicio eliminado." + Colores.RESET)
    else:
        print(Colores.ROJO + "Servicio no registrado." + Colores.RESET)
    pausar()

# Función para mostrar los servicios registrados de un usuario
def mostrar_servicios_registrados(usuario, usuarios):
    limpiar_terminal()
    servicios = usuarios[usuario]["servicios"]
    if servicios:
        print(Colores.CIAN + "Servicios registrados:")
        for s in servicios:
            print(f" - {s}")
        print(Colores.RESET)
    else:
        print(Colores.AMARILLO + "No hay servicios registrados." + Colores.RESET)
    pausar()

# Función principal del programa
def main():
    usuarios = cargar_usuarios()

    while True:
        limpiar_terminal()
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_usuario(usuarios)
        elif opcion == '2':
            usuario_actual, clave_maestra = iniciar_sesion(usuarios)
            if usuario_actual:
                while True:
                    limpiar_terminal()
                    mostrar_menu()
                    op = input("Seleccione una opción: ")
                    if op in {'1', '2', '3', '4', '5'}:
                        if validar_clave(clave_maestra):
                            if op == '1':
                                registrar_contraseña(usuario_actual, usuarios)
                            elif op == '2':
                                ver_contraseña(usuario_actual, usuarios)
                            elif op == '3':
                                modificar_contraseña(usuario_actual, usuarios)
                            elif op == '4':
                                eliminar_contraseña(usuario_actual, usuarios)
                            elif op == '5':
                                mostrar_servicios_registrados(usuario_actual, usuarios)
                    elif op == '6':
                        print(Colores.AMARILLO + "Cerrando sesión..." + Colores.RESET)
                        pausar()
                        break
                    else:
                        print(Colores.ROJO + "Opción no válida." + Colores.RESET)
                        pausar()
        elif opcion == '0':
            print(Colores.AMARILLO + "Saliendo del programa." + Colores.RESET)
            pausar()
            break
        else:
            print(Colores.ROJO + "Opción no válida." + Colores.RESET)
            pausar()

if __name__ == "__main__":
    main()