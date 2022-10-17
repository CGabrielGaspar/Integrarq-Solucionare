import os
import solucionare
import exportdriver
import traceback
from datetime import datetime
import time


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


def daily_loop(target_time, secs_min, secs_hr, secs_day, check=False):
    """
    Loop diário para disparo. Verifica se é dia de semana e loga o tempo de disparo (normalmente 4min).
    Bool 'Check' determina se o usuário deverá verificar as informações de cada formulário antes do disparo.

    :param target_time: list[int]
    :param secs_min: int
    :param secs_hr: int
    :param secs_day: int
    :param check: bool
    :return:
    """
    weekday = datetime.today().isoweekday()
    start_time = datetime.now()
    if int(weekday) <= 5:
        input("Realizar disparos: \n")
        send("TAVAD", check)
        send("Bermudes_RJ", check)
        send("JG", check)
        send("Bermudes_DF", check)

    end_time = datetime.now()
    hour = end_time.hour
    minute = end_time.minute

    hour_min_now = f"{hour}:{minute}"
    if hour_min_now == f"{target_time[0]}:{target_time[1]}":
        wait_time = secs_day  # wait 24hrs
        print(f"Os e-mails foram disparados no horário, às {end_time.strftime('%H:%M')}.")
    else:
        hr_delta = (hour - target_time[0]) * secs_hr
        minute_delta = (minute - target_time[1]) * secs_min
        time_delta = secs_day - (hr_delta + minute_delta)
        wait_time = time_delta  # wait 24 - however many extra hours and/or minutes elapsed
        print(
            f"Processo de disparo inicou às {start_time.strftime('%H:%M')} e encerrou às {end_time.strftime('%H:%M')}. "
            f"O processou encerrou-se {int(hr_delta / secs_hr)} horas e {int(minute_delta / secs_min)} minutos após o "
            f"horário marcado para disparo e durou {':'.join(str(end_time - start_time).split(':')[:2])}h")
    time.sleep(wait_time)


if __name__ == "__main__":
    target_time = [10, 00]
    secs_min = 60
    secs_hr = 60 * secs_min
    secs_day = 24 * secs_hr

    Solucionare = solucionare.Module_SOLUCIONARE()
    Gdrive = exportdriver.Module_drive()
    while True:
        daily_loop(target_time, secs_min, secs_hr, secs_day, False)
