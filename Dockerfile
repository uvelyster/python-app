FROM python:alpine
RUN pip install flask pymysql 
COPY app.py /
CMD python app.py 

