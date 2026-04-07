import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template

app = Flask(__name__)

# --- НАСТРОЙКИ (ЗАПОЛНИТЕ ЭТИ ПОЛЯ) ---
# Ваш email, на который будут приходить резюме
MY_EMAIL = "post@vpoint.ru" 
MY_PASSWORD = "Follow_Line17" 

# Если вы используете Gmail, может потребоваться включить "Ненадежные приложения" или создать "Пароль приложения"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# -------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        data = request.form

        # Формируем текст письма из полученных данных
        body = "Новое резюме оператора колл-центра 'Вьюпоинт':\n\n"
        for key, value in data.items():
            body += f"{key}: {value}\n"
        
        # Отправка письма
        try:
            msg = MIMEMultipart()
            msg['From'] = MY_EMAIL
            msg['To'] = MY_EMAIL
            msg['Subject'] = "Новое резюме: " + data.get('Имя', 'Без имени') + " " + data.get('Фамилия', '')
            
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(MY_EMAIL, MY_PASSWORD)
            server.send_message(msg)
            server.quit()

            return "✅ Резюме успешно отправлено! Мы свяжемся с вами в ближайшее время."
        
        except Exception as e:
            return f"❌ Ошибка при отправке: {str(e)}"
    
    # Если метод GET — просто показываем страницу с формой
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
