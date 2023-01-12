FROM python:3.9-slim

WORKDIR /app
COPY ./app .

RUN apt-get update
RUN python3 -m pip install -r requirements.txt

EXPOSE 80
ENTRYPOINT ["streamlit", "run"] 
CMD ["app.py", "--server.port", "80"]

