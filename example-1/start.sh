pip install -r requirements.txt
gunicorn --bind=0.0.0.0:80--timeout 600 application:app