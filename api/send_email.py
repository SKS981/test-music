import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def handler(event, context):
    try:
        import json
        data = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        
        recipient_email = data.get('to')
        subject = data.get('subject', '【时光留声】新遗物')
        body = data.get('body', '')
        
        if not sender_email or not sender_password or not recipient_email:
            return {
                'statusCode': 400,
                'body': json.dumps({'success': False, 'message': '缺少必要参数'})
            }
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'message': '邮件发送成功'})
        }
    
    except Exception as e:
        import json
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'message': str(e)})
        }
