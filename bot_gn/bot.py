import logging as log
import os
from datetime import date, datetime

import pandas as pd
import pyautogui
from botcity.core import DesktopBot
from dotenv import find_dotenv, load_dotenv

# Carrega arquivo de configuracao
load_dotenv(find_dotenv())

# Define data para compor nome do arquivo de log
current_date = date.today().strftime("%d_%m_%Y")

# Define caminho para criar arquivo de log
file_name_log = rf"C:\BOT_GN\bot_gn_{current_date}.log"

# Configura arquivo de log
log.basicConfig(
    filename=file_name_log,
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=log.INFO,
)

# Instancia objeto DesktopBot
bot = DesktopBot()


def action():
    """Função principal"""

    sap_user = os.getenv("SAP_USER")
    sap_pswd = os.getenv("SAP_PSWD")

    login_sap(user=sap_user, password=sap_pswd)
    exec_transacao(transaction_code="ZGN103")
    exec_grupo_gn()
    close_sap()


def login_sap(user, password):
    """Executa e realiza login no SAP GUI.

    Args:
        user (str): usuario SAP
        password (str): senha SAP
    """

    bot.execute(r"saplogon.exe")

    if bot.find_text("PD4", waiting_time=5000):
        bot.double_click(wait_after=3000)
    elif bot.find_text("PD4_azul", waiting_time=5000):
        bot.double_click(wait_after=3000)
    else:
        not_found("PD4")

    bot.type_keys(user)
    bot.tab(wait=500)
    bot.type_keys(password)
    bot.key_enter(wait=3000)


def exec_transacao(transaction_code):
    """Executa transacao SAP

    Args:
        transaction_code (_str_): Codigo da transacao SAP.
    """

    if not bot.find("campo_transacao", matching=0.97, waiting_time=5000):
        not_found("campo_transacao")
    bot.click_relative(40, 10)
    bot.type_keys(transaction_code)
    bot.key_enter(wait=1000)


def load_file(file_path):
    """Carrega arquivo GRP_GN e o retorna para cadastro no SAP

    Args:
        file_path (_str_): Caminho do arquivo.
    """

    try:
        os.path.exists(path=file_path)
        with open(file_path, "rb") as file_open:
            loaded_file = pd.read_excel(io=file_path, dtype="unicode")
        return loaded_file, file_open
    except FileNotFoundError:
        log.error("Arquivo não encontrado!")


def screenshot(grp):
    """Salva screenshot com nome dinâmico
    grupo_dia_mes_ano_horaminuto
    "GRPXXXXXXX_06_11_2023_2245.png"
    """

    nome_arquivo = datetime.now().strftime(f"{grp}_%d_%m_%Y_%H%M")
    pic = pyautogui.screenshot()
    pic.save(rf"C:\BOT_GN\prints\{nome_arquivo}.png")
    bot.wait(1000)


def exec_grupo_gn():
    """Função de preenchimento de grupo GN - ZGN103"""

    xlsx, file_open = load_file(file_path=r"C:\BOT_GN\GRP_GN.xlsx")
    log.info(f"Inicio do processamento: {datetime.now().strftime('%H:%M:%S')}")

    for line in xlsx.values:
        bot.type_keys(line[0])
        bot.key_f8(wait=200)

        if bot.find_text("ja_esta_cadastrado", waiting_time=5000):
            log.warning(f"{line[0]} | já está cadastrado.")
            continue

        bot.type_keys(line[1])
        bot.type_down(wait=100)
        bot.shift_tab(wait=100)
        bot.type_keys(line[2])
        bot.key_enter()
        bot.type_keys(keys=["ctrl", "s"])

        if bot.find_text("cliente_nao_cadastrado", waiting_time=3000):
            log.error(f"Cliente | {line[2]} | não cadastrado no GN")
            bot.key_esc()
            if not bot.find_text("encerrar_processamento", waiting_time=5000):
                not_found("encerrar_processamento")
            bot.click_relative(38, 57)
            log.error(f"Processamento encerrado para {line[0]}")
            continue

        log.info(f"{line[0]} | cadastrado com suceeso!")
        screenshot(line[0])
        continue

    log.info(f"Fim do processamento: {datetime.now().strftime('%H:%M:%S')}")
    file_open.close()


def close_sap():
    """Encerra instancia SAP"""

    bot.key_f12()
    bot.hold_shift()
    bot.key_f3()
    bot.release_shift()
    bot.tab()
    bot.key_enter()
    log.info("Processamento encerrado!")


def not_found(label):
    print(f"Elemento nao encontrado: {label}")
    log.warning(f"Elemento nao encontrado: {label}")


if __name__ == "__main__":
    action()
