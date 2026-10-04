# Namen: Abdullah Mubarok, M. Raditya Rafli Aldiansyah
# NIMs: (009), (063)
# Studienfach: PEMTEKS
# Datum: 27.09.2026

import pandas as PD;
import datetime;
import requests;
import random;
import time;

class WEB:
    def __init__(self, API_KEY: str, url: str, LATs: list, LONGs: list, dicts: dict):
        self.API_KEY: str = API_KEY;
        self.URL: str = url;
        self.LAT: list = LATs;
        self.LONG: list = LONGs;
        self.DICT_COUNTRY = dicts;

    def scraping(self):
        self.BigDataList: list = [];
        for lat, lon in zip(self.LAT, self.LONG):
            flexURL: str = self.URL.format(lat=lat, lon=lon, API_KEY=self.API_KEY);
            RES = requests.get(flexURL);
            DATA = RES.json();
            print(DATA)
            dataList: list = self.saveOutput(DATA);
            self.BigDataList.append(dataList);
            time.sleep(1.3); # for limit api (openweather api limits 60 requests/minutes lol hwhw)

    def saveOutput(self, DATA) -> list:
        name: str = DATA.get("name", "Unknown");
        sys_data = DATA.get("sys", {});
        country: str = sys_data.get("country", "Unknown");
        lat: float = DATA["coord"]["lat"];
        lon: float = DATA["coord"]["lon"];

        weather_list = DATA.get("weather", [])
        weather: str = weather_list[0].get("main", "Unknown") if len(weather_list)>0 else "Unknown";
        description: str = weather_list[0].get("description", "Unknown") if len(weather_list)>0 else "Unknown";

        temp: float = DATA["main"]["temp"];
        feels_like: float = DATA["main"]["feels_like"];
        temp_min: float = DATA["main"]["temp_min"];
        temp_max: float = DATA["main"]["temp_max"];
        pressure: int = DATA["main"]["pressure"];
        humidity: int = DATA["main"]["humidity"];
        sea_level: int = DATA["main"]["sea_level"];
        grnd_level: int = DATA["main"]["grnd_level"];
        
        visibility: int = DATA.get("visibility", 0);
        wind = DATA.get("wind", {});
        wind_speed: float = wind.get("speed", 0);
        clouds = DATA.get("clouds", {});
        clouds_closed_percent: float = clouds.get("all", 0);

        time_z: int = DATA.get("timezone", 0);
        time_zone = datetime.timezone(datetime.timedelta(seconds=time_z));

        dt = DATA.get("dt");
        if dt:
            dt_obj = datetime.datetime.fromtimestamp(dt, tz=time_zone);
            date: str = dt_obj.strftime("%Y-%m-%d");
            time: str = dt_obj.strftime("%H:%M:%S");
        else: date: str = "Unknown"; time: str = "Unknown";

        rise = sys_data.get("sunrise");
        set = sys_data.get("sunset");
        if rise or set:
            dt_obj = datetime.datetime.fromtimestamp(rise, tz=time_zone);
            sunrise: str = dt_obj.strftime("%Y-%m-%d %H:%M:%S");
            dt_obj = datetime.datetime.fromtimestamp(set, tz=time_zone);
            sunset: str = dt_obj.strftime("%Y-%m-%d %H:%M:%S");
        else: sunrise: str = "Unknown"; sunset: str = "Unknown";

        return [name, country, lat, lon, weather, description, temp, feels_like, temp_min, temp_max, pressure, humidity, sea_level, grnd_level, visibility, wind_speed, clouds_closed_percent, date, time, sunrise, sunset];

    def exportCSV(self):
        NEW_DATASET = PD.DataFrame(self.BigDataList, columns=[""
        "name_city", "country_id", "lat", "lon", "weather", "description", "temp", "feels_like", "temp_min", "temp_max", "pressure", "humidity", "sea_level", "grnd_level", "visibility", "wind_speed", "clouds_closed_percent", "date", "time", "sunrise", "sunset" 
        ]);
        new_cols_country = NEW_DATASET["country_id"].map(self.DICT_COUNTRY);
        NEW_DATASET.insert(2, "country_name", new_cols_country);
        NEW_DATASET.to_csv("web_scraping/data/sweater_weather.csv", index=False);

class DATASET:
    def __init__(self, PATH: str):
        self.FILE_PATH: str = PATH;
        self.DS = PD.read_csv(self.FILE_PATH);

    def getDataColumn(self, whatColumn: str) -> list: #unused hehe
        dataList: list = self.DS[whatColumn].tolist();
        return dataList;

    def randomIndexRow(self, manyRows: int) -> list:
        rows: int = len(self.DS);
        numList: list = [];
        for _ in range(manyRows):
            while True:
                rand_int = random.randint(0, rows-1);
                if rand_int not in numList:
                    numList.append(rand_int);
                    break;
                else:
                    continue;
        return numList;

    def getDict(self, key: str, value: str) -> dict:
        dicts: dict = dict(zip(self.DS[key], self.DS[value]));
        return dicts;

    def getRandomDataIndexColumn(self, whatColumn: str, randIndex: list) -> list:
        dataList: list = self.DS.loc[randIndex, whatColumn];
        return dataList;

def GET_DATA_CITY_LAT_LOT() -> list:
    filepath: str = "web_Scraping/data/worldcities.csv";
    DF = DATASET(filepath);
    randIdx: list = DF.randomIndexRow(1000); # i limit for 1000 request (1000 city), this searching for random city of lat and lot
    dataLat: list = DF.getRandomDataIndexColumn('lat', randIdx);
    dataLong: list = DF.getRandomDataIndexColumn('lng', randIdx);
    dicts_country: dict = DF.getDict("iso2", "country");

    return dataLat, dataLong, dicts_country;

def GET_DATA_WEATHER_API(LATs: list, LONGs: list, dictCountry: dict):
    API_key = "8b36ca2b82f435637f2b70ac338185f7"; # pls dont use my api
    url_api = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric";
  
    WEEB = WEB(API_key, url_api, LATs, LONGs, dictCountry);
    WEEB.scraping();
    WEEB.exportCSV();

def main():
    LATs, LONGs, dictCountry = GET_DATA_CITY_LAT_LOT();
    GET_DATA_WEATHER_API(LATs, LONGs, dictCountry);

main()

# Note: 
# i use worldcities.csv just for extract the coordinates. Cuz the APIs need lat long for city 
# API that i used is limited by 60 requests perminute, so i added timesleep(1.3). to limit it for 1 req/1.3 second maybe approx~ 46 request/min