FROM python:3.9

COPY ./scripts/load_data.py ./

COPY ./data/loans.csv ./

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

CMD ["python", "load_data.py"]


