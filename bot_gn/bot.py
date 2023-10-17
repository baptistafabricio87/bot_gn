"""WARNING:
Please make sure you install the bot with `pip install -e .`
in order to get all the dependencies on your Python environment.
"""
import os
import logging as log
import pandas as pd
from config import settings
from botcity.core import DesktopBot

# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *

bot = DesktopBot()

log.basicConfig(
    filename=r'C:\ArquivosSuspeitos\bot_gn.log',
    encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.INFO,
)


def action(execution=None):
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

    sap_user = settings["sap_user"]
    sap_pswd = settings["sap_pswd"]

    login_sap(user=sap_user, password=sap_pswd)
    exec_transacao(codigo_transacao="ZGN103")

    diretorio = r"C:\ArquivosSuspeitos"
    arquivo = r"\GRP_GN.xlsx"

    xlsx, file_open = load_file(diretorio=diretorio, arquivo=arquivo)

    for linha in xlsx.values:
        bot.paste(linha[0])
        bot.key_f8(wait=100)

        if bot.find_text("ja_esta_cadastrado", waiting_time=3000):
            log.info(f"{linha[0]}, já está cadastrado.")
            continue

        if bot.find_text("campo_descricao", waiting_time=3000):
            log.info(f"Cadastrando {linha[0]}")
            bot.click_relative(98, 1)
            bot.paste(linha[1], wait=100)
            bot.type_down(wait=100)
            bot.shift_tab(wait=100)
            bot.paste(linha[2], wait=100)
            bot.type_keys(keys=["ctrl", "s"])
            bot.wait(200)

            if bot.find_text(
                "cliente_nao_cadastrado", waiting_time=3000
            ):
                log.warning(f"Cliente {linha[2]} não cadastrado no GN")
                bot.key_esc()
                if not bot.find_text(
                    "encerrar_processamento", waiting_time=3000
                ):
                    not_found("encerrar_processamento")
                bot.click_relative(38, 57)
                log.error(f'Processamento encerrado para {linha[0]}')
                continue

            log.info(f"{linha[0]} cadastrado com suceeso!")
            continue

    # TODO Gerar logs do processamento.

    file_open.close()


def login_sap(user, password):
    """Executa e realiza login no SAP GUI.

    Args:
        user (str): usuario SAP
        password (str): senha SAP
    """

    bot.execute(r"saplogon.exe")

    if bot.find_text("PD4", waiting_time=5000):
        bot.double_click(wait_after=3000)
    elif not bot.find_text("PD4_azul", waiting_time=5000):
        not_found("PD4")
    bot.double_click(wait_after=2000)

    bot.paste(user)
    bot.tab(wait=100)
    bot.paste(password)
    bot.key_enter()
    bot.wait(1000)


def exec_transacao(codigo_transacao):
    """Executa transacao SAP

    Args:
        codigo_transacao (_str_): Codigo da transacao SAP
    """

    if not bot.find("campo_transacao", matching=0.97, waiting_time=5000):
        not_found("campo_transacao")
    bot.click_relative(40, 10)

    bot.type_keys(codigo_transacao)
    bot.key_enter()


def load_file(diretorio, arquivo):
    file = diretorio + arquivo

    try:
        os.path.exists(path=file)
        with open(file, "rb") as file_open:
            print("Arquivo carregado:", file)

        meus_dados = pd.read_excel(io=file, dtype="unicode")
    except FileNotFoundError:
        print("Arquivo não encontrado!")

    # Renomeando coluna
    meus_dados = meus_dados.rename(
        columns={"Grupo - Mundo TIM GN": "grp_cliente"}
    )

    return meus_dados, file_open


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == "__main__":
    action(bot)
