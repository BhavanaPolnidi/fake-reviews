import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import torch
import nltk
import string
from models import tokenizer, model, category_index
nltk.download("stopwords")
nltk.download("vader_lexicon")

stop_words = set(stopwords.words('english'))

def get_bert_embeddings_for_new_instance(text):
    input_text = f"{text}"
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the mean of the last hidden state as the embedding
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

def calculate_features(review_text, review_title, rating, verified_purchase):
    sid = SentimentIntensityAnalyzer()

    features = {
        'review_length': len(review_text),
        'title_length': len(review_title),
        'num_words': len(review_text.split()),
        'num_sentences': len(review_text.split('.')),
        'avg_word_length': np.mean([len(word) for word in review_text.split()]) if len(review_text.split()) > 0 else 0,
        'num_unique_words': len(set(review_text.split())),
        'num_stop_words': len([word for word in review_text.split() if word in stop_words]),
        'punctuation_count': sum(1 for char in review_text if char in string.punctuation),
        'num_capitalized_words': len([word for word in review_text.split() if word.isupper()]),
        'sentiment_score': sid.polarity_scores(review_text)['compound'],
        'review_length_x_rating': len(review_text) * rating,
        'verified_purchase_x_rating': verified_purchase * rating
    }

    return np.array(list(features.values()))

def preprocess_meta(verified_purchase, rating, product_category):
    verified_purchase = 1 if verified_purchase == 'Yes' else 0
    meta_features = np.array([rating, verified_purchase])
    category_vector = np.zeros(30)
    category_vector[category_index[product_category]] = 1
    return np.concatenate((meta_features, category_vector))