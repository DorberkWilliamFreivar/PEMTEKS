# Namen: Abdullah Mubarok, M. Raditya Rafli Aldiansyah
# NIMs: (009), (063)
# Studienfach: PEMTEKS
# Datum: 27.09.2026

from scipy.cluster.hierarchy import dendrogram, linkage;
from sklearn.cluster import AgglomerativeClustering;
import pandas as pd; import os as linux;
from sklearn.cluster import KMeans;
import matplotlib.pyplot as plt;
from wordcloud import WordCloud;
from sklearn import metrics;

class CLUSTERING:
    def __init__(self, BP, DF, fename):
        self.DF = DF;
        self.BP:str = str(BP);
        self.fename:str = str(fename);
        self.RS:int = int(67);
        self.DF_PREPROCESS = pd.read_csv(str(get_path(BASEPATH, "ark_reviews_playstore_preprocess.csv")));
        self.DF_PREPROCESS['text_after'] = self.DF_PREPROCESS['text_after'].fillna(' ');
        self.DF_PREPROCESS = self.DF_PREPROCESS.reset_index().drop(columns=['index']);

    def hierarchyy_clust(self):
        linkage_data = linkage(self.DF, method='ward', metric='euclidean');
        dendrogram(linkage_data);
        plt.tight_layout();
        filename: str = str(linux.path.join(self.BP, "img", self.fename+"_hirarki_clust_"+".png"));
        plt.savefig(filename);
        plt.show();

        hierarchical_cluster = AgglomerativeClustering(n_clusters=self.nclust, linkage='ward');
        nth = hierarchical_cluster.fit(self.DF);
        labels = pd.Series(hierarchical_cluster.labels_);
        self.DF_PREPROCESS.insert(1, "Ward_label", labels);
        print("\n","Metric Hierarki Silhouttenya: ", self.silhoute_scoren(labels));

        for c in list_k:
            self.word_cloud(c, 'Ward_label', '_Hierariki_');

    def kmeans_clust(self):
        global k_choosen_one, list_k;
        k_choosen_one, list_k = self.elbow_k();
        model = KMeans(n_clusters=k_choosen_one, random_state=self.RS);
        model.fit(self.DF);
        labels = model.labels_;
        self.DF_PREPROCESS.insert(0, "Kmeans_label", labels);
        print("\n","Metric Kmeans Silhouttenya: ", self.silhoute_scoren(labels));

        for c in list_k:
            self.word_cloud(c, 'Kmeans_label', '_kmeans_');

    def elbow_k(self):
        bb:int = 1; ba:int = 7;
        k: list = list(range(bb,ba));
        inertia: list = [];

        for i in k:
            model_kms = KMeans(n_clusters=i, random_state=self.RS);
            model_kms.fit(self.DF);
            inertia.append(model_kms.inertia_);

        plt.figure(figsize=(10, 6));
        plt.plot(k, inertia, marker='o');
        plt.xlabel('k value');
        plt.ylabel('inertia');
        plt.grid();
        filename: str = str(linux.path.join(self.BP, "img", self.fename+"_kmeans_k="+str(k[0])+'-'+str(k[-1])+".png"));
        plt.savefig(filename);
        plt.show();

        return self.select_kelbwo(), list(range(0, self.select_kelbwo()));

    def select_kelbwo(self):
        return 4;

    def silhoute_scoren(self, labels):
        return metrics.silhouette_score(self.DF, labels, metric='euclidean');

    def word_cloud(self, c, labelnya, clustname):
        print(self.fename+clustname+' for cluster '+str(c));
        df_c = self.DF_PREPROCESS[self.DF_PREPROCESS[labelnya] == c];
        long_string = ','.join(list(df_c['text_after'].values));
        wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3);
        wordcloud.generate(long_string);

        filename: str = str(linux.path.join(self.BP, "img", self.fename+clustname+"_wordcloude_c="+str(c)+".png"));
        wordcloud.to_file(filename);

    def save_csv(self):
        filename: str = str(linux.path.join(self.BP, "data", self.fename+"_afterclust.csv"));
        self.DF_PREPROCESS.to_csv(filename, index=False, encoding="utf-8-sig");

    def clusteringing(self):
        self.kmeans_clust();
        self.hierarchyy_clust();
        self.save_csv();

def get_path(BP: str, TF: str):
    for root, dirs, files in linux.walk(BP):
        if TF in files:
            return linux.path.join(root, TF);
    return None;
            
def main():
    global BASEPATH;
    BASEPATH = str("04_clustering");
    DF_ONEHOT = pd.read_csv(str(get_path(BASEPATH, "csv_onehot.csv")));
    DF_TFIDF = pd.read_csv(str(get_path(BASEPATH, "csv_tfidf.csv")));

    OHE_CLUST = CLUSTERING(BASEPATH, DF_ONEHOT, "OHE");
    TFIDF_CLUST = CLUSTERING(BASEPATH, DF_TFIDF, "TFIDF");

    # OHE_CLUST.clusteringing();
    TFIDF_CLUST.clusteringing();

main();