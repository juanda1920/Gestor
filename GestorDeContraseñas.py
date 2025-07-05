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
    while True:
        username = input("Ingrese un nombre de usuario (máximo 10 caracteres): ").lower()
        if len(username) <= 10 and username not in usuarios:
            break
        print("Nombre inválido o ya existe.")
   
    while True:
        pin = input("Ingrese un PIN de acceso (3 dígitos, entre 001 y 999): ")
        if pin.isdigit() and 1 <= int(pin) <= 999:
            pin = pin.zfill(3)  # Esta parte del código asegura que el PIN tenga siempre 3 dígitos
            break
        print("PIN inválido.")
   
    usuarios[username] = {
        "pin": pin,
        "clave_maestra": None,
        "servicios": {}
    }
    guardar_usuarios(usuarios)
    print(f"Usuario {username} registrado exitosamente.")

# Función para configurar la clave maestra
def pedir_clave():
    clave = input("Ingrese una clave maestra para esta cuenta: ")
    return cifrado_cesar(clave, 3)

# Función para iniciar sesión en un usuario del gestor
def iniciar_sesion(usuarios):
    if not usuarios:
        print("No hay usuarios registrados.")
        return None, None

    username = input("Ingrese su nombre de usuario: ").lower()
    if username not in usuarios:
        print("Usuario no encontrado.")
        return None, None

    pin = input("Ingrese su PIN: ").zfill(3)
    if pin != usuarios[username]["pin"]:
        print("PIN incorrecto.")
        return None, None

    print(f"Bienvenido {username}!")
    if not usuarios[username]["clave_maestra"]:
        print("Primera vez: configure una clave maestra.")
        usuarios[username]["clave_maestra"] = pedir_clave()
        guardar_usuarios(usuarios)

    return username, usuarios[username]["clave_maestra"]

# Función para validar la clave maestra
def validar_clave(clave_almacenada, max_intentos=3):
    for i in range(max_intentos):
        clave = input("Ingrese su clave maestra para continuar: ")
        if cifrado_cesar(clave, 3) == clave_almacenada:
            return True
        print(f"Clave incorrecta. Intentos restantes: {max_intentos - i - 1}")
    print("Demasiados intentos. Volviendo al menú.")
    return False

# Función para registrar una nueva contraseña
def registrar_contraseña(usuario, usuarios):
    servicio = input("Servicio: ").lower()
    usuario_servicio = input("Usuario/correo: ")
    contraseña = input("Contraseña: ")
    usuarios[usuario]["servicios"][servicio] = {
        "usuario": usuario_servicio,
        "contraseña": cifrado_cesar(contraseña, 3)
    }
    guardar_usuarios(usuarios)
    print(f"Contraseña para {servicio} registrada.")

# Función para ver las contraseñas registradas
def ver_contraseña(usuario, usuarios):
    servicio = input("Servicio: ").lower()
    servicios = usuarios[usuario]["servicios"]
    if servicio in servicios:
        datos = servicios[servicio]
        print(f"Usuario: {datos['usuario']}")
        print(f"Contraseña: {cifrado_cesar(datos['contraseña'], -3)}")
    else:
        print("Servicio no registrado.")

# Función para modificar datos de un servicio
def modificar_contraseña(usuario, usuarios):
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
        print("Datos actualizados.")
    else:
        print("Servicio no registrado.")

# Función para eliminar un servicio registrado
def eliminar_contraseña(usuario, usuarios):
    servicio = input("Servicio a eliminar: ").lower()
    servicios = usuarios[usuario]["servicios"]
    if servicio in servicios:
        del servicios[servicio]
        guardar_usuarios(usuarios)
        print("Servicio eliminado.")
    else:
        print("Servicio no registrado.")

#Función para mostrar los servicios registrados de un usuario
def mostrar_servicios_registrados(usuario, usuarios):
    servicios = usuarios[usuario]["servicios"]
    if servicios:
        print("Servicios registrados:")
        for s in servicios:
            print(f" - {s}")
    else:
        print("No hay servicios registrados.")

# Función principal del programa
def main():
    usuarios = cargar_usuarios()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_usuario(usuarios)
        elif opcion == '2':
            usuario_actual, clave_maestra = iniciar_sesion(usuarios)
            if usuario_actual:
                while True:
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
                        print("Cerrando sesión...")
                        break
                    else:
                        print("Opción no válida.")
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()