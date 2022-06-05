FROM python:3.9

WORKDIR app/
COPY ./app .

RUN apt-get update
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]