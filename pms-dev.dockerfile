FROM python:3.12-slim

WORKDIR /pms

COPY /app .
RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 443

CMD ["python", "main.py"]