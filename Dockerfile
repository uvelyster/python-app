FROM python:alpine
RUN pip install flask pymysql 
WORKDIR /app
COPY app.py .
CMD python app.py 
