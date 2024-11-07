import joblib
from transformers import BertTokenizer, BertModel

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert_tokenizer')

# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert_model')

# load the scaler
scaler = joblib.load('scaler.pkl')

# load the model
xgb_model = joblib.load('xbg_bert_individual.pkl')

category_index = {'Apparel': 0, 'Automotive': 1, 'Baby': 2, 'Beauty': 3, 'Books': 4, 'Camera': 5, 'Electronics': 6, 'Furniture': 7, 'Grocery': 8, 'Health & Personal Care': 9, 'Home': 10, 'Home Entertainment': 11, 'Home Improvement': 12, 'Jewelry': 13, 'Kitchen': 14, 'Lawn and Garden': 15, 'Luggage': 16, 'Musical Instruments': 17, 'Office Products': 18, 'Outdoors': 19, 'PC': 20, 'Pet Products': 21, 'Shoes': 22, 'Sports': 23, 'Tools': 24, 'Toys': 25, 'Video DVD': 26, 'Video Games': 27, 'Watches': 28, 'Wireless': 29}