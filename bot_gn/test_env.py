from config import settings

try:
    user = settings['sap_user']
    print(user)
    pswd = settings['sap_pswd']
    print(pswd)
except KeyError:
    print('Valor não existe')
