from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk
import string


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, methods=["GET", "POST"])

nltk.download("stopwords")
nltk.download("vader_lexicon")

# function to load tokenizer and bert model , scaler , xgb model
from transformers import BertTokenizer, BertModel
import joblib
class FakeReviewDetector:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.scaler = None
        self.xgb_model = None

    def load_models(self):
        print("---loading tokenizer-----")
        self.tokenizer = BertTokenizer.from_pretrained('bert_tokenizer')
        print("Done ✅")
        print("---loading bert model-----")
        self.model = BertModel.from_pretrained('bert_model')
        print("Done ✅")
        print("---loading scaler-----")
        self.scaler = joblib.load('scaler.pkl')
        print("Done ✅")
        print("---loading xgb model-----")
        self.xgb_model = joblib.load('xbg_bert_individual.pkl')
        self.xgb_model.set_params(device='cpu')
        print("Done ✅")


model = FakeReviewDetector()
model.load_models()

class Review:

    category_index = {'Apparel': 0, 'Automotive': 1, 'Baby': 2, 'Beauty': 3, 'Books': 4, 'Camera': 5, 'Electronics': 6, 'Furniture': 7, 'Grocery': 8, 'Health & Personal Care': 9, 'Home': 10, 'Home Entertainment': 11, 'Home Improvement': 12, 'Jewelry': 13, 'Kitchen': 14, 'Lawn and Garden': 15, 'Luggage': 16, 'Musical Instruments': 17, 'Office Products': 18, 'Outdoors': 19, 'PC': 20, 'Pet Products': 21, 'Shoes': 22, 'Sports': 23, 'Tools': 24, 'Toys': 25, 'Video DVD': 26, 'Video Games': 27, 'Watches': 28, 'Wireless': 29}

    def __init__(self, product_title, review_title, review_text, rating, verified_purchase, product_category, reviewDetector: FakeReviewDetector):
        self.product_title = product_title
        self.review_title = review_title
        self.review_text = review_text
        self.rating = rating
        self.verified_purchase = 1 if verified_purchase == 'Yes' else 0
        self.product_category = product_category
        self.reviewDetector = reviewDetector

    def get_embeddings(self, text):
        input_text = f"{text}"
        inputs = self.reviewDetector.tokenizer(input_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.reviewDetector.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embedding

    def preprocess_text_features(self):
        X_title = self.get_embeddings(self.product_title)
        X_review_title = self.get_embeddings(self.review_title)
        X_review_text = self.get_embeddings(self.review_text)
        bert_embedding = np.hstack((X_title, X_review_title, X_review_text))
        return bert_embedding.reshape(1, -1)
    
    def calculate_features(self):
        sid = SentimentIntensityAnalyzer()
        stop_words = set(stopwords.words('english'))

        features = {
        'review_length': len(self.review_text),
        'title_length': len(self.review_title),
        'num_words': len(self.review_text.split()),
        'num_sentences': len(self.review_text.split('.')),
        'avg_word_length': np.mean([len(word) for word in self.review_text.split()]) if len(self.review_text.split()) > 0 else 0,
        'num_unique_words': len(set(self.review_text.split())),
        'num_stop_words': len([word for word in self.review_text.split() if word in stop_words]),
        'punctuation_count': sum(1 for char in self.review_text if char in string.punctuation),
        'num_capitalized_words': len([word for word in self.review_text.split() if word.isupper()]),
        'sentiment_score': sid.polarity_scores(self.review_text)['compound'],
        'review_length_x_rating': len(self.review_text) * self.rating,
        'verified_purchase_x_rating': self.verified_purchase * self.rating
        }

        return np.array(list(features.values()))
     
    def preprocess_meta_features(self):
        meta_features = np.array([self.rating, self.verified_purchase])
        category_vector = np.zeros(30)
        category_vector[self.category_index[self.product_category]] = 1
        meta_features = np.concatenate((meta_features, category_vector))
        additional_features = self.calculate_features()
        return self.reviewDetector.scaler.transform(np.concatenate((meta_features, additional_features)).reshape(1, -1))
    
    def predict(self, X_meta, X_text): 
        prediction = self.reviewDetector.xgb_model.predict_proba(np.hstack((X_text, X_meta)))
        return f"Fake: {prediction[0][0]:.4f}, Real: {prediction[0][1]:.4f}"

@app.route('/')
def home():
    return "Fake Reviews Detector"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    product_title = data['product_title']
    review_title = data['review_title']
    review_text = data['review_text']
    rating = int(data['rating'])
    verified_purchase = data['verified_purchase']
    product_category = data['product_category']
    review = Review(product_title, review_title, review_text, rating, verified_purchase, product_category, model)
    prediction = review.predict(review.preprocess_meta_features(), review.preprocess_text_features())
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(port=5000, debug=True)