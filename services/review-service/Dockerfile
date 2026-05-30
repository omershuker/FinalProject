FROM python:3.11-slim
RUN pip install flask
WORKDIR /app
COPY app.py .
EXPOSE 5002
CMD ["python", "app.py"]