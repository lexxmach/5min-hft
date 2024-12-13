FROM python:3.10

WORKDIR /backend

ADD ./core/src/requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./core/src /backend

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]