# flask_feedback_mail

This is a basic feedback application built in flask which sends mail to all users who register on this app on basis of their feedback.

You have to edit these variables as per your needs and you can get a newly generated password from "app-passwords" section in Google accounts:

```
app.config['MAIL_USERNAME'] = 'yourID@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
```


All u need is flask,flask-sqlalchemy and flask-mail to get started , to run the application just run the file app.py 
