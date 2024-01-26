from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# # Load the tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

print(sum(p.numel() for p in model.parameters() if p.requires_grad))
# # Example text
# text = "I love using transformers. They are easy to use and very powerful."

# # Tokenize the text
# inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# output = model(**inputs)
# print(output)

# Predict
# with torch.no_grad():
#     logits = model(**inputs).logits

# # Convert to probabilities
# predictions = torch.nn.functional.softmax(logits, dim=-1)

# # Print the output
# print(predictions)


# from transformers import pipeline
# unmasker = pipeline('fill-mask', model='distilbert-base-uncased')
# print(unmasker("3 little [MASK] jumping on the bed."))