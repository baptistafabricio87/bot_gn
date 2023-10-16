"""WARNING:
Please make sure you install the bot with `pip install -e .`
in order to get all the dependencies on your Python environment.
"""
import os
import pandas as pd
from config import settings
from botcity.core import DesktopBot

# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *

bot = DesktopBot()


def action(bot, execution=None):
    # Uncomment to silence Maestro errors when disconnected
    # if bot.maestro:
    #     bot.maestro.RAISE_NOT_CONNECTED = False
    #
    # Fetch the Activity ID from the task:
    # task = bot.maestro.get_task(execution.task_id)
    # activity_id = task.activity_id
    #
    # Uncomment to mark this task as finished on BotMaestro
    # bot.maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

    sap_user = settings['sap_user']
    sap_pswd = settings['sap_pswd']

    login_sap(user=sap_user, password=sap_pswd)
    exec_transacao(codigo_transacao='ZGN103')

    diretorio = r'C:\ArquivosSuspeitos'
    arquivo = r'\GRP_GN.xlsx'
    xlsx, file_open = load_file(diretorio=diretorio, arquivo=arquivo)

    for linha in xlsx.values:
        print(linha)
        for celula in linha:
            pass

    file_open.close()


def login_sap(user, password):
    """Executa e realiza login no SAP GUI.

    Args:
        user (str): usuario SAP
        password (str): senha SAP
    """

    bot.execute(r"saplogon.exe")

    if bot.find_text( "PD4", waiting_time=10000):
        bot.double_click(wait_after=3000)
    elif not bot.find_text( "PD4_azul", waiting_time=10000):
        not_found("PD4")
    bot.double_click(wait_after=3000)

    bot.paste(user)
    bot.tab(wait=10)
    bot.paste(password)
    bot.key_enter()
    bot.wait(1000)


def exec_transacao(codigo_transacao):
    """Executa transacao SAP

    Args:
        codigo_transacao (_str_): Codigo da transacao SAP
    """

    bot.type_keys(codigo_transacao)
    bot.key_enter()


def load_file(diretorio, arquivo):
    file = diretorio + arquivo

    try:
        os.path.exists(path=file)
        with open(file, 'rb') as file_open:
            print('Arquivo carregado:', file)

        meus_dados = pd.read_excel(io=file, dtype='unicode')
    except FileNotFoundError:
        print('Arquivo não encontrado!')

    # Renomeando coluna
    meus_dados = meus_dados.rename(
        columns={'Grupo - Mundo TIM GN': 'grp_cliente'}
    )

    return meus_dados, file_open


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == "__main__":
    action(bot)
