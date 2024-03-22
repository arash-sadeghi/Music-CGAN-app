FROM python:3.11.5
WORKDIR /app
RUN git clone https://github.com/arash-sadeghi/Music-CGAN-app.git
RUN cd Music-CGAN-app 
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
RUN ./file_downloader.sh
EXPOSE 3009
CMD ["python", "app.py"]