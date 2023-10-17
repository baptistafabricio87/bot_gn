# from config import settings
#
# try:
#     user = settings['sap_ser']
#     logging.info(user)
# except KeyError:
#     logging.error("Usuário não encontrado")
#
# try:
#     pswd = settings['sap_pswd']
#     logging.info(pswd)
# except KeyError:
#     logging.error("Senha não encontrada")
import logging as log

log.basicConfig(
    filename=r'exemplo.log',
    encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO,
)

log.debug('This message should go to the log file')
log.info('So should this')
log.warning('And this, too')
log.error('And non-ASCII stuff, too, like Øresund and Malmö')
