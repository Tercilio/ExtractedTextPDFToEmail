import logging

from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from PyPDF2 import PdfReader

from credentials import mail_password, mail_username, mail_server, mail_port

app = Flask(__name__)
app.secret_key= 'keycode'

# Configuring Error logging configure
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

# Configuring Flask-Mail settings
mail_settings = {
    "MAIL_SERVER": mail_server,
    "MAIL_PORT": mail_port,
    "MAIL_USE_SSL": False,
    "MAIL_USE_TLS": True,
    "MAIL_USERNAME": mail_username,
    "MAIL_PASSWORD": mail_password,
}

app.config.update(mail_settings)

mail = Mail(app)


def send_email(subject, recipient, extracted_text):
    try:
        # create mensagem
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])

        # HTML to style the extracted text
        html_body = f"""
        <html>
            <head>
                <style>
                    /* Styles CSS for formated text */
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        width: 80%;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: #f5f5f5;
                        border-radius: 8px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Text extracted from PDF</h1>
                    <p>{extracted_text.replace('\n', '<br>')}</p>
                </div>
            </body>
        </html>
        """

        # body html message
        msg.html = html_body

        # send email
        mail.send(msg)
        
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar o e-mail: {str(e)}")
        return False

    
# Function to extract text from PDF
def extract_text_from_pdf(file):
    
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)
    extracted_text = ""
    
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    
    # Take the first 30 lines of text
    lines = extracted_text.split('\n')[:30]
    formatted_text = "\n".join(f"{i}. {line}" for i, line in enumerate(lines, start=1))
    
    return formatted_text


@app.route('/upload', methods=['POST'])
def upload_file():
    
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "File not found"}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected!"}), 400

    # Check if the file is a PDF
    if file.mimetype != 'application/pdf':
        return jsonify({"success": False, "message": "The uploaded file is not a PDF!"}), 400

    # Extract the email from the request body
    email = request.form.get('email')

    if not email:
        return jsonify({"success": False, "message": "Email address not provided"}), 400

    try:
        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file)

        # Send the extracted text via email
        if send_email("Extracted Text from PDF", email, extracted_text):
            return jsonify({"success": True, "message": f"The email has been successfully sent to {email}"}), 200
        else:
            return jsonify({"success": False, "message": "Error sending email"}), 500

    except Exception as err:
        logging.error(f"Unexpected error: {err}")
        return jsonify({"success": False, "message": "An unexpected error occurred, please try again later"}), 500

if __name__ == '__main__':
    app.run()