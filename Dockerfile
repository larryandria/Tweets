FROM python:3.6.9

WORKDIR /app

ENV FLASK_APP =webapp.py

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","webapp.py"]