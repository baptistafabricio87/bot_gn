import os
import logging as log
import pandas as pd
from botcity.core import DesktopBot
from dotenv import load_dotenv

bot = DesktopBot()

load_dotenv()

log.basicConfig(
    filename=r"C:\ArquivosSuspeitos\bot_gn.log",
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=log.INFO,
)


def action(execution=None):
    """Função principal"""
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

    sap_user = os.getenv("SAP_USER")
    sap_pswd = os.getenv("SAP_PSWD")

    login_sap(user=sap_user, password=sap_pswd)
    exec_transacao(transaction_code="ZGN103")
    exec_grupo_gn()


def login_sap(user, password):
    """Executa e realiza login no SAP GUI.

    Args:
        user (str): usuario SAP
        password (str): senha SAP
    """

    bot.execute(r"saplogon.exe")

    if bot.find_text("PD4", waiting_time=10000):
        bot.double_click(wait_after=3000)
    elif bot.find_text("PD4_azul", waiting_time=10000):
        bot.double_click(wait_after=3000)
    else:
        not_found("PD4")

    bot.paste(user)
    bot.tab(wait=1000)
    bot.paste(password)
    bot.key_enter()
    bot.wait(1000)


def exec_transacao(transaction_code):
    """Executa transacao SAP

    Args:
        transaction_code (_str_): Codigo da transacao SAP.
    """

    if not bot.find("campo_transacao", matching=0.97, waiting_time=5000):
        not_found("campo_transacao")
    bot.click_relative(40, 10)
    bot.wait(1000)
    bot.type_keys(transaction_code)
    bot.key_enter(wait=1000)


def load_file(file_path):
    '''Carrega arquivo GRP_GN e o retorna para cadastro no SAP

    Args:
        file_path (_str_): Caminho do arquivo.
    '''

    try:
        os.path.exists(path=file_path)
        with open(file_path, "rb") as file_open:
            print("Arquivo carregado:", file_path)

        loaded_file = pd.read_excel(io=file_path, dtype="unicode")
        # Renomeando coluna
        loaded_file = loaded_file.rename(
            columns={"Grupo - Mundo TIM GN": "grp_cliente"}
        )

        return loaded_file, file_open
    except FileNotFoundError:
        print("Arquivo não encontrado!")


def exec_grupo_gn():
    """Função de preenchimento de grupo GN - ZGN103"""

    xlsx, file_open = load_file(file_path=r"C:\ArquivosSuspeitos\GRP_GN.xlsx")

    for line in xlsx.values:
        bot.paste(line[0])
        bot.key_f8(wait=100)

        if bot.find_text("ja_esta_cadastrado", waiting_time=10000):
            log.info(f"{line[0]}, já está cadastrado.")
            continue

        if bot.find_text("campo_descricao", waiting_time=3000):
            log.info(f"Cadastrando {line[0]}")
            bot.click_relative(98, 1)
            bot.paste(line[1], wait=100)
            bot.type_down(wait=100)
            bot.shift_tab(wait=100)
            bot.paste(line[2], wait=100)
            bot.type_keys(keys=["ctrl", "s"])
            bot.wait(200)

            if bot.find_text("cliente_nao_cadastrado", waiting_time=3000):
                log.warning(f"Cliente {line[2]} não cadastrado no GN")
                bot.key_esc()
                if not bot.find_text(
                    "encerrar_processamento", waiting_time=3000
                ):
                    not_found("encerrar_processamento")
                bot.click_relative(38, 57)
                log.error(f"Processamento encerrado para {line[0]}")
                continue

            log.info(f"{line[0]} cadastrado com suceeso!")
            continue
    file_open.close()

    # Encerra SAP
    bot.key_f12()
    bot.hold_shift()
    bot.key_f3()
    bot.release_shift()
    bot.tab()
    bot.key_enter()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == "__main__":
    action(bot)
