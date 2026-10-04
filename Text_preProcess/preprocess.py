# Namen: Abdullah Mubarok, M. Raditya Rafli Aldiansyah
# NIMs: (009), (063)
# Studienfach: PEMTEKS
# Datum: 04.10.2026

# !pip install --upgrade git+https://github.com/ariaghora/mpstemmer.git
# !pip install Levenshtein
# !pip install demoji
# !pip install nltk
# !pip install nlp-id

def importAllLibs():
    global demoji, nltk, stopwords, Lemmatizer, MPStemmer, pd, re, plt, WordCloud, Counter;
    import demoji; import nltk; from nltk.corpus import stopwords;
    from nlp_id.lemmatizer import Lemmatizer;
    from mpstemmer import MPStemmer;
    import pandas as pd;  import re;
    import matplotlib.pyplot as plt; 
    from wordcloud import WordCloud;
    from collections import Counter;
    nltk.download('stopwords');
    # WAREG LIBRARY

class DF_TEXT_RAW:
    def __init__(self, filename: str):
        self.DF = pd.read_csv(filename, encoding="utf-8-sig");

        print("Initate of modul or clases neded from libs");
        self.html_pattern = re.compile('<.*?>');
        another_sw = {'nya', 'game'};
        self.sw = set(stopwords.words('indonesian'));
        self.sw = self.sw.union(another_sw);
        self.lemmatizer = Lemmatizer();
        self.stemmer = MPStemmer();

    # removal
    def removeHtml(self, text:str):
        return self.html_pattern.sub(r'', text);

    def removeHastag(self, text:str):
        return re.sub(r'#\w+', '', text);

    def removeRLS(self, text:str):
        text = re.sub(r'https?\/\/S+', '',  str(text));
        text = re.sub(r'http\S+', '',  str(text));
        text = re.sub(r'www\S+', '',  str(text));
        text = re.sub(r'\S+@\S+', '', str(text));
        return text;

    def removePunctuation(self, text:str):
        import string;
        punc = string.punctuation;
        return text.translate(str.maketrans('', '', punc));

    def removePunctuationList(self, text: str):
        text = re.sub(r'(:\)|:-\)|:D|:-D|;\)|;-\))', '', text);
        text = re.sub(r'(:\(|:-\()', '', text);
        text = re.sub(r'(:v|:-v)', '', text);
        text = re.sub(r'[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]', ' ', text);
        text = re.sub(r'\s+', ' ', text).strip();
        return text;

    def removeEmoji(self, text:str):
        cleaned_text = demoji.replace(text, repl=""); # replaces emojis with an empty string
        #cleaned_text = demoji.replace_with_desc(text) # replaces emojis with text
        return cleaned_text;

    def removeStopWords(self, text:str):
        return " ".join([word for word in str(text).split() if word not in self.sw]);

    # stemmers
    def stemmers(self, text:str):
        return self.stemmer.stem_kalimat(text);

    def lemmatize(self, text:str):
        return self.lemmatizer.lemmatize(text);

    def tokenize(self, text:str):
        # ga kepake
        pass;

    def topWords(self, name_col:str):
        text = ' '.join(self.DF[name_col].dropna().astype(str));
        wordcloud = WordCloud(width=1000, height=500, background_color='white', collocations=False, max_words=500).generate(text);

        plt.figure(figsize=(7, 4));
        plt.imshow(wordcloud, interpolation='bilinear');
        plt.axis('off');
        plt.savefig(f"{PATH}{name_col}_lematize.png", bbox_inches='tight', dpi=300);
        plt.show();

    def toLower(self, text: str):
        return str.lower(text);

    def preprocess(self):
        self.DF['text_before'] = self.DF['text_before'].apply(self.toLower);
        self.DF.insert(1, 'no_html', self.DF['text_before'].apply(self.removeHtml));
        self.DF.insert(2, 'no_hastag', self.DF['no_html'].apply(self.removeHastag));
        self.DF.insert(3, 'no_urls', self.DF['no_hastag'].apply(self.removeRLS));
        self.DF.insert(4, 'no_punc', self.DF['no_urls'].apply(self.removePunctuation));
        self.DF.insert(5, 'no_puncList', self.DF['no_punc'].apply(self.removePunctuationList));
        self.DF.insert(6, 'no_emoji', self.DF['no_puncList'].apply(self.removeEmoji));
        self.DF.insert(7, 'no_stopwords', self.DF['no_emoji'].apply(self.removeStopWords));
    
        self.DF.insert(8, 'lemmatize', self.DF['no_stopwords'].apply(self.lemmatize));
        self.DF.insert(1, 'text_after', self.DF['lemmatize']);
        # self.stemmers();
        # self.tokenize();
        self.topWords('text_after');
    
    def saveCSV(self, filename_o: str):
        self.DF.to_csv(filename_o, index=False, encoding="utf-8-sig");

def main():
    global PATH;
    importAllLibs(); # WAREG LIBRARRYS
    PATH = "Text_preProcess/";
    DF_RAW = PATH + "ark_reviews_playstore.csv";
    FILENAME_O = PATH + "ark_reviews_playstore_preprocess.csv"
    TEXT = DF_TEXT_RAW(DF_RAW);
    TEXT.preprocess();
    TEXT.saveCSV(FILENAME_O);

main();