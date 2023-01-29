from transformers import AutoModelForQuestionAnswering,  AutoTokenizer, pipeline
from sentiment import get_news

model_name = "deepset/minilm-uncased-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def get_tldr(search_term, news):

    " ".join(news["description"])
    QA_input = {
        'question': f"What is happening at {search_term}?",
        'context': " ".join(news["description"])
    }
    res = nlp(QA_input)
    return res["answer"]

# from transformers import pipeline

# classifier = pipeline("summarization")

# def get_tldr(news):
#     return classifier(" ".join(news["description"]))
