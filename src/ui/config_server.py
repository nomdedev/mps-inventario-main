import configparser

config_path = './config/databaseConfig.ini'

def configure_server():
    config = configparser.ConfigParser()
    config['database'] = {}
    
    config['database']['server'] = input("Ingrese el nombre del servidor: ")
    config['database']['database'] = input("Ingrese el nombre de la base de datos: ")
    config['database']['user'] = input("Ingrese el usuario: ")
    config['database']['password'] = input("Ingrese la contraseña: ")
    config['database']['port'] = input("Ingrese el puerto (default 1433): ") or "1433"

    with open(config_path, 'w') as configfile:
        config.write(configfile)
        print("Configuración guardada exitosamente.")

if __name__ == "__main__":
    configure_server()
