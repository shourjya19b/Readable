from celery import shared_task

from datetime import date
from smtplib import SMTP
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64

import os
import csv
from io import StringIO
from jinja2 import Template


from .models import db, User, Section, Book, Request, Issue

@shared_task
def daily_reminder():
    user_ids = []
    for request in Request.query.all():
        user_ids.append(request.user_id)

    server = SMTP(host="0.0.0.0",
                  port=1025)

    current_dir=os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_dir,"../templates/reminder.html"),'r') as file:
        template = Template(file.read())

    for user in User.query.filter(User.id.not_in(user_ids)).all():
        if 'admin' not in user.roles:
            content = template.render(user=user)
            message = MIMEMultipart()
            message["From"] = "harry.potter@hogwarts.edu"
            message["To"] = user.email
            message["Subject"] = "Daily Reminder"
            html = MIMEText(content, "html")
            message.attach(html)

            server.sendmail("harry.potter@hogwarts.edu", 
                            user.email, 
                            message.as_string())
        
    return True


@shared_task
def report():
    current_dir=os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_dir,"../templates/report.html"),'r') as file:
        template = Template(file.read())

    server = SMTP(host="localhost",
                  port=1025)
    
    for user in User.query.filter(User.id!=1).all():
        book_issues=[]
        issues = Issue.query.filter(Issue.user_id==user.id).all()

        for issue in issues:
            if issue.issue_date.month==date.today().month:
                book=Book.query.filter(Book.id==issue.book_id).first()
                section=Section.query.filter(Section.id==book.section_id).first()

                book_issue={}
                book_issue['issue_date']=issue.issue_date
                book_issue['book_name']=book.name
                book_issue['section_name']=section.name

                book_issues.append(book_issue)

        content = template.render(user=user, issues=book_issues)

        message = MIMEMultipart()
        message["From"] = "harry.potter@hogwarts.edu"
        message["To"] = user.email
        message["Subject"] = "Monthly Activity"
        html = MIMEText(content, "html")
        message.attach(html)

        server.sendmail("harry.potter@hogwarts.edu",
                        user.email,
                        message.as_string())
    
    return True

@shared_task
def autorevoke_issue():
    issues=Issue.query.filter(Issue.returned==False).all()

    for issue in issues:
        if issue.return_date.day>=date.today().day:
            issue.returned=True
            db.session.commit()

    return True