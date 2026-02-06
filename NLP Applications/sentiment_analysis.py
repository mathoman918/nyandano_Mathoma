"""
sentiment_analysis.py

This script performs sentiment analysis on Amazon product reviews
using spaCy and TextBlob.
"""

import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


def load_data(file_path):
    """
    Load the Amazon reviews dataset from a CSV file.

    :param file_path: Path to the CSV file
    :return: Cleaned pandas DataFrame
    """
    dataframe = pd.read_csv(file_path)
    dataframe = dataframe.dropna(subset=["reviews.text"])
    return dataframe


def preprocess_text(nlp, text):
    """
    Preprocess text by removing stop words and punctuation.

    :param nlp: spaCy language model
    :param text: Raw review text
    :return: Cleaned text string
    """
    doc = nlp(str(text).lower().strip())
    tokens = [
        token.text for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)


def analyze_sentiment(nlp, review):
    """
    Analyze the sentiment of a product review.

    :param nlp: spaCy language model
    :param review: Product review text
    :return: Polarity score and sentiment label
    """
    doc = nlp(review)
    polarity = doc._.blob.polarity
    sentiment = doc._.blob.sentiment

    if polarity > 0:
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return polarity, label, sentiment


def compare_similarity(nlp, review1, review2):
    """
    Compare similarity between two reviews.

    :param nlp: spaCy language model
    :param review1: First review
    :param review2: Second review
    :return: Similarity score
    """
    doc1 = nlp(review1)
    doc2 = nlp(review2)
    return doc1.similarity(doc2)


def main():
    """
    Main execution function.
    """
    # Load spaCy model
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe("spacytextblob")

    # Load dataset
    data = load_data("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv")

    # Preprocess reviews
    data["cleaned_reviews"] = data["reviews.text"].apply(
        lambda review: preprocess_text(nlp, review)
    )

    # Test sentiment analysis on sample reviews
    sample_reviews = data["cleaned_reviews"].head(5)

    print("SENTIMENT ANALYSIS RESULTS\n")

    for idx, review in enumerate(sample_reviews, start=1):
        polarity, label, sentiment = analyze_sentiment(nlp, review)
        print(f"Review {idx}:")
        print(f"Polarity Score: {polarity}")
        print(f"Sentiment: {label}")
        print("-" * 40)

    # Similarity comparison example
    review_a = data["reviews.text"].iloc[0]
    review_b = data["reviews.text"].iloc[1]

    similarity_score = compare_similarity(nlp, review_a, review_b)

    print("\nREVIEW SIMILARITY")
    print(f"Similarity score between review 1 and 2: {similarity_score}")


if __name__ == "__main__":
    main()
