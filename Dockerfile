FROM python:3.8.13-slim-buster

WORKDIR app/
COPY ./app .

RUN apt-get update
RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN python3 -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]