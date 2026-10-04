# Namen: Abdullah Mubarok, M. Raditya Rafli Aldiansyah
# NIMs: (009), (063)
# Studienfach: PEMTEKS
# Datum: 04.10.2026

from google_play_scraper import Sort, reviews;
import pandas as pd;

class GPS:
    def __init__(self, APP_ID: str):
        self.params = {
            "app_id": APP_ID,
            "lang": "id",                          
            "country": "id",                  
            "sort": Sort.NEWEST,                   
            "count": 2000                      
        };

    def process(self):
        self.LIST_REQUEST, TOKEN = reviews(**self.params);

    def saveCols(self, key: str) -> list:
        list_cols: list = [];
        for dict in self.LIST_REQUEST:
            col_str: str = dict[key];
            if key == 'at':
                col_str: str = dict[key].strftime("%Y-%m-%d %H:%M:%S");
                col_str: str = f"""{col_str}""";
            elif key == 'content':
                col_str: str = str(dict[key]).replace('\n', '').replace('\r', '');
            list_cols.append(col_str);
        return list_cols;

    def saveCSV(self):
        df = pd.DataFrame({
            'text_before': self.saveCols('content'),
            'username': self.saveCols('userName'),
            'score': self.saveCols('score'),
            'date': self.saveCols('at')
        })
        df.to_csv('Text_preProcess/ark_reviews_playstore.csv', index=False, encoding='utf-8-sig');

def main():
    APP_ID: str = 'com.studiowildcard.arkuse';
    ARK_REVIEWS = GPS(APP_ID);
    ARK_REVIEWS.process();
    ARK_REVIEWS.saveCSV();

main();