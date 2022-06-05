FROM pytorch/pytorch

WORKDIR app/
COPY ./app .

RUN apt-get update
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]