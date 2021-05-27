# Se importan las librerías necesarias para establecer la conexión con el servidor
import smtplib, ssl
from email import encoders
from email.mime.multipart import MIMEMultipart          # Librería para enviar documentos
from email.mime.base import MIMEBase                    # Librería para darle formato al correo
from email.mime.text import MIMEText                    # Librería para enviar texto

# Por cuestiones de seguridad es recomendable almacenar tu usuario y contraseña en otro archivo .py
# Aquí importamos la función mycred del programa credentials.py
from credentials import mycred

username, password = mycred()                               # Se importan el usuario y la contraseña
context = ssl.create_default_context()

def send_email(receiver, subject, message, archive):        # Función para enviar el correo con formato
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login(username, password)

    email = MIMEMultipart("alternative")
    email['From'] = username
    email['To'] = receiver
    email['Subject'] = subject

    html = message

    html_part = MIMEText(html, "html")
    email.attach(html_part)

    with open(archive, "rb") as adjunto:
        contenido_adjunto = MIMEBase("application", "octet-stream")
        contenido_adjunto.set_payload(adjunto.read())

    encoders.encode_base64(contenido_adjunto)

    contenido_adjunto.add_header(
        "Content-Disposition",
        f"attachment; filename= {archive}",
    )

    email.attach(contenido_adjunto)
    text = email.as_string()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, text)
        server.quit()

# En las siguientes variables se escribe el contenido del correo
destinatario = "Aquí se introduce el correo del destinatario"
asunto = "Asunto del email"
mensaje = f"""
<html>
<body>
    Aquí se introduce el contenido del correo
</body>
</html>
"""
archivo = "Aquí se nombra el documento que se quiere anexar al correo"

# Llamamos la función send_email con nuestras variables
send_email(destinatario, asunto, mensaje, archivo)

print("\nCorreo enviado exitosamente!")
