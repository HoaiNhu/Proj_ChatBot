from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

class NLPService:
    def __init__(self, model_path):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
    
    def predict_intent(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        intent = torch.argmax(predictions).item()
        confidence = predictions[0][intent].item()
        return intent, confidence