from selenium.webdriver import Chrome

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service

import time

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys


from datetime import datetime


from pathlib import Path

import os

# Config
with open("config.txt", "r") as archivo:
    # Lee todas las líneas del archivo
    lineas = archivo.readlines()

# Inicializa un diccionario para almacenar las constantes
constantes = {}

# Itera sobre las líneas del archivo
for linea in lineas:
    # Divide cada línea en nombre de la constante y su valor
    nombre, valor = linea.strip().split("=")
    # Elimina espacios en blanco alrededor del nombre y del valor
    nombre = nombre.strip()
    valor = valor.strip()
    # Almacena la constante en el diccionario
    constantes[nombre] = eval(valor)


# usar Path para que funcione en cualquier sistema
ruta_archivo_subir = f'{Path.cwd()}\In\{constantes["NombreArchivoSubir"]}'

# ENV VAR
USER = constantes["Usuario"]
PASSWORD = constantes["Contrasena"]

NAME_LIST = constantes["NombreArchivo"]
PATH_FILE = ruta_archivo_subir

server_sql = constantes["server"]
database_sql = constantes["database"]
username_sql = constantes["username"]
password_sql = constantes["password"]


def main():
    from selenium.webdriver.chrome.service import Service as ChromeService

    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")
    service = ChromeService(chromedriver_path)

    option = webdriver.ChromeOptions()
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--headless")
    option.add_experimental_option(
        "prefs",
        {
            "download.default_directory": f"{Path.cwd()}\out",
            "download.prompt_for_download": False,  # Evitar la ventana de confirmación de descarga
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    # Init serv
    driver = Chrome(service=service, options=option)
    driver.get("https://mailerball.com/")

    # Our logic goes here
    time.sleep(3)

    # Looking for login and click
    login = driver.find_element(
        By.XPATH, "/html/body/div[1]/nav/div/ul/li[3]/a/span"
    ).click()
    time.sleep(3)

    # Modifying session
    user = driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div[2]/div/div/div/form/div[2]/div/div[1]/div[2]/input",
    ).send_keys(USER)
    time.sleep(1)

    pwd = driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
    time.sleep(1)

    # Acces
    acc_btn = driver.find_element(
        By.XPATH, "//*[@id='new_user']/div[2]/div/div[1]/div[5]/input"
    ).click()
    print("Login...")
    time.sleep(3)

    # Menu Acc
    menu = driver.find_element(By.XPATH, "//*[@id='sidenav']/i").click()
    time.sleep(1)

    # Acces to list
    menu_list = driver.find_element(By.XPATH, "//*[@id='slide-out']/li[2]/a").click()
    time.sleep(1)

    # Add button
    add_btn = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/a/i").click()
    print("Iniciando procesador de archivo CSV...")
    time.sleep(2)

    # Type Name
    name_list = driver.find_element(By.XPATH, "//*[@id='lista_nombre']").send_keys(
        NAME_LIST
    )
    time.sleep(1)

    # Upload file CSV
    file_to_up = driver.find_element(By.XPATH, "//*[@id='archivo']").send_keys(
        PATH_FILE
    )

    # Select Encode
    encode_opt = driver.find_element(
        By.XPATH, "//*[@id='new_lista']/div[2]/div[2]/div/div/input"
    )
    encode_opt.click()
    encode_opt.send_keys(Keys.ARROW_DOWN)
    encode_opt.send_keys(Keys.ENTER)
    time.sleep(1)

    # Submit
    encode_opt = driver.find_element(
        By.XPATH, "//*[@id='new_lista']/div[3]/div/input"
    ).click()
    print("Enviando datos para generar CSV...")
    time.sleep(5)

    # Menu Acc
    menu = driver.find_element(By.XPATH, "//*[@id='sidenav']/i").click()
    time.sleep(1)

    # Acces to list
    menu_list = driver.find_element(By.XPATH, "//*[@id='slide-out']/li[2]/a").click()
    time.sleep(1)

 
        
    def buscar_columna(i):
        fila = driver.find_element(By.XPATH, f"/html/body/div[2]/div/table/tbody/tr[{i+1}]/td[1]/a")

        print("Buscando documento...")
        
        if fila.text == NAME_LIST:
            print("Documento encontrado")
            celda = driver.find_element(By.XPATH, f"/html/body/div[2]/div/table/tbody/tr[{i+1}]/td[3]/a")
            

            if celda.text != "0 destinatarios":
                print("destinarios listos")
                celda.click()
                time.sleep(3)
                
            else:               
                print("Esperando se actualice los destinatarios...")
                time.sleep(30)
                driver.refresh()
                buscar_columna(0)
        else:
            i+=1
            buscar_columna(i)
    buscar_columna(0)
                
        
       
                
            

    # Download csv
    table_dest = driver.find_element(
        By.XPATH, "/html/body/div[2]/div/ul[1]/li[2]/a"
    ).click()
    print("Descargando archivo csv...")
    time.sleep(5)

    # To close navigator
    driver.quit()





def dataToSQL():

    import pandas as pd
    
    try:
        file_path = f"{Path.cwd()}\out\list_{NAME_LIST}__.xls.crdownload"
        time.sleep(2)
        output_path = f"{Path.cwd()}/out/{NAME_LIST}.txt"

        os.rename(file_path, output_path)
    except:
        file_path = f"{Path.cwd()}\out\list_{NAME_LIST}__.xls"
        time.sleep(2)
        output_path = f"{Path.cwd()}/out/{NAME_LIST}.txt"

        os.rename(file_path, output_path)
    
    time.sleep(2)
    # Cargar el archivo Excel
    ruta_excel = f"{Path.cwd()}/out/{NAME_LIST}.txt"
    df = pd.read_csv(ruta_excel, sep='\t', encoding='ISO-8859-1')

    # Obtener las columnas 1 y 3
    # En pandas, las columnas están indexadas desde 0, así que 1 y 3 son 0 y 2 respectivamente
    columna_1 = df.iloc[:, 0]  # Primera columna
    columna_3 = df.iloc[:, 2]  # Tercera columna

    # Crear la cadena con el formato deseado
    cadena_resultante = "¬".join(
        [f"{correo}¦{estado}" for correo, estado in zip(columna_1, columna_3)]
    )

    # Imprimir el resultado
    return cadena_resultante


def dataBaseCon(str_to_sql):
    import pyodbc

    server = server_sql
    database = database_sql
    username = username_sql
    password = password_sql

    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + server
        + ";DATABASE="
        + database
        + ";UID="
        + username
        + ";PWD="
        + password
    )
    cursor = conn.cursor()

    data = str_to_sql
    # Ejecutar el procedimiento almacenado
    procedure_name = "dbo.CSV_ESTADO_CORREO_EDUCACION_UPDATE_SP"

    try:
        cursor.execute("EXEC " + procedure_name + " @lstParametros = ?", data)
        conn.commit()
        print("Procedimiento almacenado ejecutado correctamente.")
    except pyodbc.Error as e:
        print(f"Error al ejecutar el procedimiento almacenado: {e}")

    # Cerrar la conexión
    cursor.close()
    conn.close()


if __name__ == "__main__":
    try:
        main()
        dataBaseCon(dataToSQL())
        
    except Exception as e:
        # Definir el nombre del archivo
        nombre_archivo = f"error{NAME_LIST}.txt"
        carpeta = "errors-log"
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        
        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Abrir el archivo en modo escritura (esto creará el archivo si no existe)
        with open(ruta_completa, "w") as archivo:
            # Escribir texto en el archivo
            archivo.write(f"{e}\n")
            archivo.close()
        # El archivo se cierra automáticamente cuando sales del bloque 'with'
        print("error")



