FROM python:3.11.5
WORKDIR /app
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]