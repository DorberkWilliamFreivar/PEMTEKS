# Namen: Abdullah Mubarok, M. Raditya Rafli Aldiansyah
# NIMs: (009), (063)
# Studienfach: PEMTEKS
# Datum: 27.09.2026

#!pip install gensim umap-learn plotly pandas kaleido

from gensim.models import FastText, Word2Vec;
import numpy as np;
import pandas as pd;
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer;
import matplotlib.pyplot as plt;
from umap import UMAP;
import plotly.express as px;

class FEATURE_ENGINEERING:
    def __init__(self, DF_col):
        self.texts = DF_col.tolist();
        self.df = DF_col;
        self.get_sentences();
        self.PATH_MODEL = "03_featuree_engineering/models/";
        self.PATH_IMG = "03_featuree_engineering/data/img/";
        self.PATH_HTML = "03_featuree_engineering/data/html/";

    def ONE_HOT_ENCODING(self):
        vectorizer = CountVectorizer(binary=True);
        X = vectorizer.fit_transform(self.texts);
        df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out());
        return df;
 
    def BOW(self):
        vectorizer = CountVectorizer();
        X = vectorizer.fit_transform(self.texts);
        df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out());
        return df;
 
    def TF_IDF(self):
        vectorizer = TfidfVectorizer();
        X = vectorizer.fit_transform(self.texts);
        df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out());
        return df;

    def get_sentences(self):
        import nltk;
        nltk.download('punkt');
        nltk.download('punkt_tab');
        from nltk import word_tokenize;
        from tqdm import tqdm;

        self.sentences = [word_tokenize(ripiu.lower()) for ripiu in tqdm(self.df)];
    
    def WORD_2VECT(self):
        model = Word2Vec(self.sentences, min_count=1, vector_size=100, window=5, sg=0);
        model.save(self.PATH_MODEL+'review_ark.w2v');
        model = Word2Vec.load(self.PATH_MODEL+'review_ark.w2v');
        self.MODEL_W2V = model.wv;

        print(self.MODEL_W2V.vectors.shape, self.MODEL_W2V.vector_size);
        print(self.MODEL_W2V.similar_by_key('bug'));

        X_features = np.array([self.get_document_vector(doc, model) for doc in self.sentences]);
        X_f_df = pd.DataFrame(X_features);
        return X_f_df;

    def FASTEXT(self):
        model_ft = FastText(self.sentences, min_count=1,
                            vector_size=100, window=5,
                            min_n=3, max_n=6,
                            sg=1, epochs=10);
        model_ft.save(self.PATH_MODEL+'reviews_ark.fasttext');
        model_ft = FastText.load(self.PATH_MODEL+'reviews_ark.fasttext');
        self.MODEL_FASTEXT = model_ft.wv;

        print(self.MODEL_FASTEXT.vectors.shape);
        print(self.MODEL_FASTEXT.similar_by_key('bug'));

        X_features = np.array([self.get_document_vector(doc, model_ft) for doc in self.sentences]);
        X_f_df = pd.DataFrame(X_features);
        return X_f_df;
    
    def get_document_vector(self, tokens, model):
        valid_vectors = [model.wv[word] for word in tokens if word in model.wv]
        # if not valid_vectors:
        #   return np.zeros(model.vector_size)
        return np.mean(valid_vectors, axis=0);

    def GENERATE_UMAP_PLOT(self, model, model_name):
        X = UMAP().fit_transform(model.vectors);

        df_umay = pd.DataFrame(X, columns=['umap1', 'umap2']);
        df_umay['word'] = model.index_to_key;

        fig = px.scatter(df_umay, x='umap1', y='umap2', text='word');
        fig.update_traces(textposition='top center');
        fig.update_layout(height = 800, title_text = model_name+'Visualization');
        fig.show();
        fig.write_image(self.PATH_IMG+model_name+'_hd.png', scale=2);
        fig.write_html(self.PATH_HTML+model_name+'_web.html');

def main():
    PATH = "03_featuree_engineering/data/csv/";
    DF_PREPROCESS = pd.read_csv(PATH+"ark_reviews_playstore_preprocess.csv");
    DF_PREPROCESS = DF_PREPROCESS.dropna().reset_index().drop(columns=['index']);
    FE = FEATURE_ENGINEERING(DF_PREPROCESS['text_after']);

    DF_OHE = FE.ONE_HOT_ENCODING();
    DF_BOW = FE.BOW();
    DF_TFIDF = FE.TF_IDF();
    DF_W2V = FE.WORD_2VECT();
    DF_FTEXT = FE.FASTEXT();

    LIST_DF_OUT = [DF_OHE, DF_BOW, DF_TFIDF, DF_W2V, DF_FTEXT];
    LIST_DF_OUT_NAME = ["csv_onehot.csv", "csv_bow.csv", "csv_tfidf.csv", "csv_word2vec.csv", "csv_fasttext.csv"];
    for DF, DF_NM in zip(LIST_DF_OUT, LIST_DF_OUT_NAME):
        DF.to_csv(PATH+DF_NM, index=False);

    FE.GENERATE_UMAP_PLOT(FE.MODEL_W2V, "Word2Vec");
    FE.GENERATE_UMAP_PLOT(FE.MODEL_FASTEXT, "FastText");

main();
