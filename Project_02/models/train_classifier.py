import sys
import nltk
import time
import joblib
import numpy as np
import pandas as pd
import sqlalchemy as db
nltk.download(['punkt', 'wordnet'])

from sklearn.svm import SVC
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def load_data(database_filepath):
    # load data from database
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('DisasterResponse', engine)
    X = df.message.values
    Y = df.drop(['id', 'message', 'original', 'genre'], axis=1).values
    category_names = list(df.drop(['id', 'message', 'original', 'genre'], axis=1))
    return X, Y, category_names


def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidif', TfidfTransformer()),
            # Reducing number of estimators to 10
            # to accomodate GitHub file size restrictions
            ('multiclf', MultiOutputClassifier(RandomForestClassifier(n_estimators=10)))
            ])

    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    y_preds = model.predict(X_test)

    for i in range(len(category_names)):
        print("Column:", category_names[i])
        print(classification_report(Y_test[:,i], y_preds[:,i]))
        print("-----------------------------------------------------")

    accuracy = (y_preds == Y_test).mean()
    print("Accuracy:", accuracy)


def save_model(model, model_filepath):
    # Save the GridSearch model
    joblib.dump(model, model_filepath)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
