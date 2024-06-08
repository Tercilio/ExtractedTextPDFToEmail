# RESTful API for PDF Email Extraction

This repository contains a RESTful API developed in [Python] for extracting the first 30 lines of a PDF file and sending them via email.

## 1 - Requirements:
  * [Python]
  * [Flask/Express] framework
  * [PyPDF2/pdfreader] library (for Python)



## 2 - Installation

2.1- Clone this repository:
  ```bash
    git clone https://github.com/your-username/pdf-email-extraction.git
  ````
2.2- Navigate to the project directory::
  ```bash
    cd pdf-email-extraction
  ````

2.3- Install the dependencies:
  ```bash
    pip install -r requirements.txt
    npm install
  ````

## 3 -  Configuration
* Before running the application, make sure to add your own credentials to the credentials.py file.
```python
    # file = credentials.py

     mail_server = 'your_mail_server'
     mail_port = 'your_mail_port'
     mail_username = 'your_mail_username'
     mail_password = 'your_mail_password'
  ````

## 4 - Usage
4.1 - Start the server:
  ```bash
    python app.py
  ````

4.2 - Use a tool like [Postman] to send a POST request to the /upload endpoint with the PDF file and email address as form data:
  * A) REQUEST
  ```http
    POST /upload
    Content-Type: multipart/form-data

    {
        "file": <pdf-file>,
        "email": "example@example.com"
    }
  ````

  * B) REQUEST
  ```json
    POST /upload
    Content-Type: multipart/form-data

    {
        "success": true,
      "message": "The email has been successfully sent to example@example.com"
    }
   ````

5 - Folder Structure
  * `app.py`: Main application file.
  * `requirements.txt`: List of Python dependencies.
  * `README.md`: Instructions and documentation.

6 - License
* This project is licensed under the MIT License.
