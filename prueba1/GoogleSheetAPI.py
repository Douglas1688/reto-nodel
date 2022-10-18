"""
GOOGLE SHEET API CON PYTHON
PREREQUISITOS
1.- pip install pandas.
2.- Contar con una cuenta Gmail y seguir las instrucciones detalladas en: 
    "https://developers.google.com/sheets/api/quickstart/python".
    2.1.- Habilitar la API Google Drive.
    2.2.- Autorizar las credenciales para la aplicación de escritorio, luego descargar las credenciales 
          en formato json y a su vez ubicar el archivo en la carpeta del proyecto.
    2.3.- Instalar las bibliotecas de Google para Python ejecutando el la terminal: 
          pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
3.- pip gspread.

El identificador del spreadsheet ejemplo es: "1DRD97TAw2WIuTCG0Nh6BW-aVvDKAgY1wvJb38V-3vU8".
Link del archivo generado: 
"https://docs.google.com/spreadsheets/d/1imLAmkMw8AHMMnFv5irDki2CMJOcnO55lEiMzAd1uRA/edit?usp=sharing"
"""

import gspread
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import pandas as pd

# Páginas de alcance para el uso de la API de Google
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]
# Ruta de las credenciales
SERVICE_ACCOUNT_FILE = 'prueba1/<<credential.json>>'
creds = None
# Solicitamos el permiso
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

def create(title):
    """
    Crea la Hoja a la que el usuario tiene acceso.
    Cargue las credenciales de usuario preautorizadas del entorno.
    TODO (desarrollador): consulte https://developers.google.com/identity
    para obtener guías sobre la implementación de OAuth2 para la aplicación.

    Args:
        title (str): Nombre que se le asignará al archivo.

    Returns:
        str: Retorna el id del spreadsheet creado.

    """
    try:
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        # Se llama a la API Sheet
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        print(f"Ha ocurrido un error: {error}")
        return error


def share_file(real_file_id, real_user):
    """Modificación de permisos por lotes.
    Args:
        real_file_id: identificación del archivo
        real_user: correo personal de la person a quien se le compartirá el archivo creado.
        
    Imprime permisos modificados

    Cargue las credenciales de usuario preautorizadas del entorno.
    TODO (desarrollador): consulte https://developers.google.com/identity
    para obtener guías sobre la implementación de OAuth2 para la aplicación.
    
    Returns:
        str: Retorna el id del permiso otorgado.
    
    """

    try:        
        ids = []
        file_id = real_file_id

        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f'Request_Id: {request_id}')
                print(F'Permission Id: {response.get("id")}')
                ids.append(response.get('id'))

        batch = service.new_batch_http_request(callback=callback)
        # Se establecen los permisos al usuario con el correo ingresado para que visualice el archivo en la sección 
        # "Compartidos conmigo" en Google Drive.
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': real_user
        }
        batch.add(service.permissions().create(fileId=file_id,
                                               body=user_permission,
                                               fields='id',))
        # Ejecutamos las instrucciones añadidas.
        batch.execute()

    except HttpError as error:
        print(F'Ha ocurrido un error: {error}')
        ids = None
    return ids


def pivot_tables(spreadsheet_id):
    """
    Crea el batch_update al que tiene acceso el usuario.
    Cargue las credenciales de usuario preautorizadas del entorno.
    TODO (desarrollador): consulte https://developers.google.com/identity
    para obtener guías sobre la implementación de OAuth2 para la aplicación.
    
    Args:
        spreadsheet_id (str): Recibe el identificado del archivo creado.

    Returns:
        object: Retorna el objeto respuesta de la API    
    """
    try:
        # Se crea una hoja para la tabla dinámica.
        body = {
            'requests': [{
                'addSheet': {}
            }]
        }
        batch_update_response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        # Obtenemos el id de la nueva hoja en la que se creará la tabla dinámica.
        source_sheet_id = batch_update_response.get('replies')[0] \
            .get('addSheet').get('properties').get('sheetId')

        requests = []
        # Configuramos la tabla dinámica.
        requests.append({
            'updateCells': {
                'rows': {
                    'values': [
                        {
                            'pivotTable': {
                                'source': {
                                    'sheetId': '0',
                                    'startRowIndex': 0,
                                    'startColumnIndex': 0,
                                    'endRowIndex': 16,
                                    'endColumnIndex': 3
                                },
                                'rows': [
                                    {
                                        'sourceColumnOffset': 0,
                                        'showTotals': False,
                                        'sortOrder': 'ASCENDING',
                                        'repeatHeadings': True,
                                    },
                                    {
                                        'sourceColumnOffset': 1,
                                        'showTotals': False,
                                        'sortOrder': 'ASCENDING',
                                        'repeatHeadings': True,
                                    },
                                ],
                                'columns': [
                                    {
                                        'sourceColumnOffset': 2,
                                        'sortOrder': 'ASCENDING',
                                        'showTotals': False,

                                    },

                                ],
                                'values': [
                                    {
                                        'summarizeFunction': 'COUNTA',
                                        'sourceColumnOffset': 0
                                    }

                                ],
                                'valueLayout': 'HORIZONTAL'
                            }
                        }
                    ]
                },
                'start': {
                    'sheetId': source_sheet_id,
                    'rowIndex': 0,
                    'columnIndex': 0
                },
                'fields': 'pivotTable'
            }
        })
        body = {
            'requests': requests
        }
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        return response

    except HttpError as error:
        print(f"Ha ocurrido un error: {error}")
        return error


if __name__ == '__main__':
    # Se solicita por terminal el id spreadsheet origen: 1DRD97TAw2WIuTCG0Nh6BW-aVvDKAgY1wvJb38V-3vU8
    id_origin = input("Ingrese id spreadsheet origen: ")
    personal_email = input("Ingrese su correo electrónico: ")
    filename = input("Dele nombre al archivo de salida: ")
    # Se crea el archivo en Google Drive y se guarda el id spreadsheet
    idspread = create(filename)
    # Compartimos el archivo con el usuario ingresado.
    share_file(real_file_id=idspread,
               real_user=personal_email)
    # Obtenemos los registros del archivo de muestra y almacenamos el contenido en formato csv.
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{id_origin}/export?format=csv")
    cliente = gspread.authorize(creds)
    sheet = cliente.open(filename).sheet1
    # Subimos la tabla del ejemplo base al archivo creado.
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    # Se crea la tabla dinámica enviando el id spreadsheet del archivo que se creó inicialmente.
    pivot_tables(idspread)
