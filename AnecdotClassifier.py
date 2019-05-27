import requests
from bs4 import BeautifulSoup
import argparse
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
import pickle


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('option', nargs='?')

    return parser


def classify(train_set, sample_text):
    if os.path.exists('./classifier.mdl') and os.path.exists('./pca.mdl') and os.path.exists('./vec.mdl'):
        with open('classifier.mdl', 'rb') as clf_file:
            clf = pickle.load(clf_file)
        with open('pca.mdl', 'rb') as pca_file:
            pca = pickle.load(pca_file)
        with open('vec.mdl', 'rb') as vec_file:
            vec = pickle.load(vec_file)
    else:
        X_train, X_test, y_train, y_test = train_test_split(train_set[0], train_set[1], test_size=0.20, random_state=42)
        vec = TfidfVectorizer()
        clf = XGBClassifier()
        pca = PCA(1000)
        X_train_vec = vec.fit_transform(X_train)
        X_test_vec = vec.transform(X_test)
        X_train_vec = X_train_vec.toarray()
        X_test_vec = X_test_vec.toarray()
        X_train_vec_pca = pca.fit_transform(X_train_vec)
        X_test_vec_pca = pca.transform(X_test_vec)
        clf = clf.fit(X_train_vec_pca, y_train, n_jobs=4)
        
        with open('classifier.mdl', 'wb') as clf_file:
            pickle.dump(clf, clf_file)
        with open('pca.mdl', 'wb') as pca_file:
            pickle.dump(pca, pca_file)
        with open('vec.mdl', 'wb') as vec_file:
            pickle.dump(vec, vec_file)

    y_pred = clf.predict(pca.transform(vec.transform([sample_text]).toarray()))
    return y_pred


def load_page_data(tags):
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })
    if not os.path.exists('./html_source'):
        os.makedirs('./html_source')
        for tag in tags:
            for page in range(tag.get('max_page')):
                url = 'https://www.anekdot.ru/tags/%s/%d"' % (tag.get('tag_rus'), page)
                print(f"Downloading {url}")
                data = s.get(url).text
                with open('./html_source/%s_page_%d.html' % (
                tag.get('tag_eng'), page), 'w', encoding='utf-8') as output_file:
                    output_file.write(data)


def parse_to_list(tags):
    marked_list = []
    story_list = []
    labels = []
    for tag in tags:
        for page in range(tag.get('max_page')):
            with open('./html_source/%s_page_%d.html' % (tag.get('tag_eng'), page), 'r', encoding='utf-8') as input_file:
                text = input_file.read()
                soup = BeautifulSoup(text, features='lxml')
                stories = soup.findAll('div', {'class': 'text'})
                for story in stories:
                    story_text = str(story).replace(
                        '<br>', '').replace(
                        '<div class="text">', '').replace(
                        '</div>', '').replace(
                        '<br/>', '')
                    story_list.append(story_text)
                    labels.append(tag.get('val'))

    marked_list.insert(0, story_list)
    marked_list.insert(1, labels)
    return marked_list


if __name__ == '__main__':
    tags = [{'tag_rus': 'армия', 'tag_eng': 'army', 'max_page': 20, 'val': 0},
            {'tag_rus': 'деньги', 'tag_eng': 'money', 'max_page': 20, 'val': 1},
            {'tag_rus': 'школа', 'tag_eng': 'school', 'max_page': 24, 'val': 2}]

    names_map = {0: 'Армия', 1: 'Деньги', 2: 'Школа'}

    load_page_data(tags)
    sample_story = input()
    marked_list = parse_to_list(tags)
    prediction = classify(marked_list, sample_story)[0]
    print(names_map.get(prediction))