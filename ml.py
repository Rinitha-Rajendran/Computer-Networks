import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def mlmodel1(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for style in soup(["script", "style"]):
            style.extract()
        text = soup.get_text()
        cleantext = re.sub(r'\s+', ' ', text)
        return cleantext.strip()
    except requests.RequestException as e:
        return f"Error fetching url {str(e)}\n"

def mlmodel(url):
    websitecontent = mlmodel1(url)
    data = pd.read_csv('website_classification.csv')
    x = data['cleaned_website_text']
    y = data['Category']
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)
    vectorizer = TfidfVectorizer()
    xtrainvect = vectorizer.fit_transform(xtrain)
    xtestvect = vectorizer.transform(xtest)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(xtrainvect, ytrain)
    websitevect = vectorizer.transform([websitecontent])
    predictc = model.predict(websitevect)[0]
    return f"The website belongs to the category: {predictc}"
