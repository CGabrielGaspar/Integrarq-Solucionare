import os
import solucionare
import exportdriver
import traceback

Solucionare = solucionare.Module_SOLUCIONARE()
Gdrive = exportdriver.Module_drive()


def send(client, confirm=True):
    """
    Envia os andamentos e salva o relat no Google Drive.

    :param str client: Must be: "Bermudes_DF"; "Bermudes_RJ"; "JG"; "TAVAD"; "tests"
    :param bool confirm: True/False - Aguardar verificação dos dados antes de realizar o envio. Normally True
    """
    try:
        report = Solucionare.run_processes(client, confirm)
        response = Gdrive.run_processes(report, client)

        if response:
            os.remove(report)

    except Exception:
        print(traceback.format_exc())


send("TAVAD")

input("Bermudes_RJ\n")
send("Bermudes_RJ", False)

input("JG\n")
send("JG", False)

input("Bermudes_DF\n")
send("Bermudes_DF")
