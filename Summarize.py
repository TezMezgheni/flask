from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer


def summarize(article, type):
    if (type == "T5"):
        # initialize the model architecture and weights
        model = T5ForConditionalGeneration.from_pretrained("t5-base")
        # initialize the model tokenizer
        tokenizer = T5Tokenizer.from_pretrained("t5-base")
        # encode the text into tensor of integers using the appropriate tokenizer
        inputs = tokenizer.encode("summarize: " + article, return_tensors="pt", max_length=512, truncation=True)
        # generate the summarization output
        outputs = model.generate(
            inputs,
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True)
        # just for debugging
        print(outputs)
        return tokenizer.decode(outputs[0])
    else:
        summarization = pipeline("summarization")
        summary_text = summarization(article)[0]['summary_text']
    return summary_text
