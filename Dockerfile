FROM python:3.9

WORKDIR app/
COPY ./app .

RUN apt-get update
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app/app.py"]