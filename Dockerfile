FROM python:3.11.5
WORKDIR /app
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
COPY . .

EXPOSE 3009
CMD ["python", "app.py"]