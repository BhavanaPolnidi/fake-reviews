import numpy as np
from models import scaler, xgb_model
from features import get_bert_embeddings_for_new_instance, calculate_features, preprocess_meta

def preprocess_text_features(product_title, review_title, review_text):
    X_title = get_bert_embeddings_for_new_instance(product_title)
    X_review_title = get_bert_embeddings_for_new_instance(review_title)
    X_review_text = get_bert_embeddings_for_new_instance(review_text)
    bert_embedding = np.hstack((X_title, X_review_title, X_review_text))
    return bert_embedding

def predict_fake_review(product_title, review_title, review_text, rating, verified_purchase, product_category):
    # Preprocess text features
    bert_embedding = preprocess_text_features(product_title, review_title, review_text)
    
    # Calculate features
    features = calculate_features(review_text, review_title, rating, verified_purchase)

    # Preprocess meta data
    meta = preprocess_meta(verified_purchase, rating, product_category)

    # Concatenate all features
    all_features = np.concatenate((bert_embedding, features, meta))

    # Scale features
    scaled_features = scaler.transform([all_features])

    # Make prediction
    prediction = xgb_model.predict(scaled_features)

    return prediction[0]