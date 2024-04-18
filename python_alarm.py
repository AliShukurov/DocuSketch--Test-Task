import requests
import psutil
import time

""" Пороог используемой памяти, после достижения которого, будет отправляться уведомление """
memory_threshold_value = 80

def memory_monitoring():
    """ Мониторит использование памяти и отправляет уведомление при достижении порога """
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent

    if memory_percent >= memory_threshold_value:
        send_alert(memory_percent)

def send_alert(memory_percent_usage):
    """ Отправка уведомление о критическом объеме использованой памяти на сервер """
    url = 'https://docusketch.com/alert'

    message = {'message': f'The memory usage exceeded: {memory_threshold_value}%. The usage memory now: {memory_percent_usage}%.'}

    try:
        response = requests.post(url, json=message)
        response.raise_for_status()
        print('Alert has been sent successfully.')
    except requests.exceptions.RequestException as e:
        print(f'Something went wrong. Error: {e}')

while True:
    memory_monitoring()
    time.sleep(60)