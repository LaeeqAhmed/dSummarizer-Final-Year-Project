import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, to: str, username: str, key: str):
        sender_email = "domster.m@gmail.com"
        receiver_email = to
        password = "p3rc3ptr0n!"

        message = MIMEMultipart("alternative")
        message["Subject"] = "dSummarizer Email Verification"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
Hi {username},
This is the dSummarizer team, we thank you for application to access out API. Please verify your email by clicking the button below.
Sincerely,
Team dSummarizer
"""
        partA = """
        <!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
    <meta charset="utf-8">
    <title>
        How to create Neon Light
        Button using HTML and CSS?
    </title>

    <style>
        /*styling background*/
        /* styling the button*/
        .a {
            padding: 2px 2px;
            display: inline-block;
            color: #008000;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-decoration: none;
            font-size: 1em;
            overflow: hidden;
        }

        /*creating animation effect*/
        .a:hover {
            color: #111;
            background: #39ff14;
            box-shadow: 0 0 50px #39ff14;
        }
    </style>

    </head>
    <body>
        """

        partB = """
        <form action="http://127.0.0.1:5000/api/signup/confirmation" method="POST">
        
            <input type="hidden" name="email" value=
        """

        partC = """/>
            <input type="hidden" name="key" value=
        """

        partD = """/>
            <button class="a" href="#" onclick="this.parentNode.submit()">VERIFY</button>
        
        </form> 
        
    </body>
</html>"""

        html = partA + text + partB + f"'{to}'" + partC + f"'{key}'" + partD


        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

