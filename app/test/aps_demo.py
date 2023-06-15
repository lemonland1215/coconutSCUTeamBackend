from flask import Flask
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from configures.development import QqMailConfig, MsMailConfig
from datetime import datetime, timedelta

app = Flask(__name__)
scheduler = APScheduler()

# Configure Flask app and Flask-Mail
app.config['SCHEDULER_API_ENABLED'] = True
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587  # Update with your mail server's port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

# mail = Mail(app)

# Start the scheduler
scheduler.init_app(app)
scheduler.start()

# app.app_context().push()

# # Create the email message for the first task
# msg1 = Message("Helloqq", recipients=["winshine_new@qq.com"])
# msg1.body = "Hello Flask message sent from Flask-Mail"

# # Create the email message for the second task
# msg2 = Message("Helloms", recipients=["winshine_new@qq.com"])
# msg2.body = "Hello Flask message sent from Flask-Mail"


@app.route('/')
def index():
    return 'Flask-APScheduler Demo'

def send_email(x):
    print(x, datetime.now())

start_date = datetime.now() + timedelta(seconds=1)
end_date = datetime.now() + timedelta(minutes=20)

@app.route("/task1")
def task1():
    # Add the first task to the scheduler
    scheduler.add_job(func=send_email, args=('循环任务1：',), trigger='interval', seconds=3, id='send_email_job_1', start_date=start_date, end_date=end_date)
    return "task1 add"

@app.route("/task2")
def task2():
    # Add the second task to the scheduler
    scheduler.add_job(func=send_email, args=('循环任务2：',), trigger='interval', seconds=0.5, id='send_email_job_2', start_date=start_date, end_date=end_date)
    return("task2 added")

@app.route("/rm2")
def del_task2():
    # Add the second task to the scheduler
    scheduler.remove_job(id='send_email_job_2')
    return("task2 removed")

@app.route("/pause2")
def pause_task2():
    # Add the second task to the scheduler
    scheduler.pause_job(id='send_email_job_2')
    return("task2 paused")

@app.route("/res2")
def re_task2():
    # Add the second task to the scheduler
    scheduler.resume_job(id='send_email_job_2')
    return("task2 resumed")



if __name__ == '__main__':
    app.run(debug=True)
