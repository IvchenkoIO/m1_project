FROM python:3.9


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [".\venv\Scripts\activate"]
CMD ["cd","metanit"]
CMD ["python","manage.py","loaddata","data.json"]
CMD ["python","manage.py","runserver","0.0.0.0:8000"]

