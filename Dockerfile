FROM python:3.9-slim

WORKDIR /app
COPY ./app .

RUN apt-get update
RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN python3 -m pip install -r requirements.txt
RUN python3 -c "from transformers import AutoTokenizer; tokenizer = AutoTokenizer.from_pretrained('zhayunduo/roberta-base-stocktwits-finetuned')"

CMD ["streamlit run your_script.py --server.port 80"]

