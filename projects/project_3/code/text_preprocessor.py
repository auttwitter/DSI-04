from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

class TextPreprocessor(BaseEstimator, TransformerMixin):
    '''
    The purpose of TextPreprocessor is to prepare text documents in a pandas Series
    by converting to lowercase, tokenizing, removing stop words, and applying stemming.
    '''
    def __init__(self, add_stopwords = None):
        self.add_stopwords = add_stopwords
        
    def fit(self, X, y = None):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words('english'))
        
        if self.add_stopwords:
            if isinstance(self.add_stopwords, str):
                self.stop_words.add(self.add_stopwords.lower())
            elif isinstance(self.add_stopwords, (list, set)):
                self.stop_words.update([word.lower() for word in self.add_stopwords])
                
        self.stemmer = PorterStemmer()
        return self
        
    def transform(self, X):
        processed_docs = []
        for doc in X:
            doc = "" if doc is None else str(doc)
            doc = doc.lower()
            tokens = self.tokenizer.tokenize(doc)
            tokens = [token for token in tokens if token not in self.stop_words]
            tokens = [self.stemmer.stem(token) for token in tokens]
            processed_docs.append(' '.join(tokens))
        return processed_docs