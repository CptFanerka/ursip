FROM python:3.7
WORKDIR /ursip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD [ "python", "./excel_parser.py" ]