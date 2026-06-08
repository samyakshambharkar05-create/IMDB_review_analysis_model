import streamlit as st
import pickle
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

# Download NLTK resources if not already present
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
try:
    WordNetLemmatizer()
except LookupError:
    nltk.download('wordnet')

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def text_preprocessing(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
    # Tokenize and remove stop words and lemmatize
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words and w.isalnum()]
    return words

# Load the model and vectorizer
@st.cache_resource
def load_resources():
    with open('tuned_logistic_regression_model.pkl', 'rb') as file:
        model = pickle.load(file)
    with open('tfidf_vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)
    return model, vectorizer

model, vectorizer = load_resources()

st.title('Movie Review Sentiment Predictor')
st.write('Enter a movie review below to predict its sentiment (positive/negative).')

# User input
user_review = st.text_area('Movie Review', '')

if st.button('Predict Sentiment'):
    if user_review:
        # Preprocess the input review
        processed_review = text_preprocessing(user_review)
        
        # Vectorize the processed review
        vectorized_review = vectorizer.transform([processed_review])
        
        # Make prediction
        prediction = model.predict(vectorized_review)
        
        # Display result
        sentiment = 'Positive' if prediction[0] == 1 else 'Negative'
        st.success(f'The sentiment of the review is: **{sentiment}**')
    else:
        st.warning('Please enter a review to predict sentiment.')
