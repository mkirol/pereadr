from flask import Flask, render_template
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    # URL сайта, на который вы хотите авторизоваться
    login_url = 'https://old-cam.powernet.com.ru/user-control/login'

    # Данные для аутентификации (логин и пароль)
    payload = {
        'login': 'user08232',
        'password': 'psFFHUrmA'
    }

    # Отправка POST-запроса для аутентификации
    session = requests.Session()
    response = session.post(login_url, data=payload)

    # Проверка статуса ответа
    if response.status_code == 200:
        print("Успешно авторизованы!")
        # Получение содержимого страницы после авторизации
        target_page_url = 'https://old-cam.powernet.com.ru/map/town/'
        target_page_response = session.get(target_page_url)
        
        # Поиск скрипта с переменной cameras_token
        script_text = target_page_response.text
        match = re.search(r"cameras_token\s*=\s*'([^']*)'", script_text)
        if match:
            token = match.group(1)
            print(token)
            return render_template('index.html', token=token)
        else:
            return "Переменная cameras_token не найдена на странице."
    else:
        return "Не удалось авторизоваться. Код ошибки:", response.status_code

if __name__ == '__main__':
    app.run(debug=True)
