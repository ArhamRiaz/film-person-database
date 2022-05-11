import sqlite3
import requests
import random
import re
from bs4 import BeautifulSoup

conn = sqlite3.connect('movies.db')

c = conn.cursor()

# c.execute("""DROP TABLE movies""")
# conn.commit()
c.execute("""CREATE TABLE IF NOT EXISTS movies (
            title text,
            director text,
            writer text,
            year text,
            runtime text,
            actors text, 
            id text primary key UNIQUE
            )""")

conn.commit()
# c.execute("""DROP TABLE streamers""")
# conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS streamers (
            movie text,
            streamer text,
            id text primary key UNIQUE
            )""")

conn.commit()

# c.execute("""DROP TABLE sites""")
# conn.commit()
c.execute("""CREATE TABLE IF NOT EXISTS sites (
            name text,
            movies text,
            id integer primary key
            )""")

conn.commit()

# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Netflix", 'movies': "", 'id': 1})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Prime Video", 'movies': "", 'id': 2})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "BBC iPlayer", 'movies': "", 'id': 3})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Criterion Collection", 'movies': "", 'id': 4})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "ARES Reserve", 'movies': "", 'id': 5})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "HBO Max", 'movies': "", 'id': 6})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Hulu", 'movies': "", 'id': 7})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Disney+", 'movies': "", 'id': 8})
# c.execute("INSERT INTO sites VALUES (:name, :movies, :id)",
#           {'name': "Apple TV+", 'movies': "", 'id': 9})


def insert_emp(emp):
    with conn:
        c.execute("INSERT OR IGNORE INTO movies VALUES (:title, :director, :writer, "
                  ":year, :runtime, :actors, :id)",
                  {'title': emp.get("Title"), 'director': emp.get("Director"),
                   'writer': emp.get("Writer"), 'year': emp.get("Released"),
                   'runtime': emp.get("Runtime"), 'actors': emp.get("Actors"),
                   'id': emp.get("imdbID")})


def insert_streamer(emp):
    streamers = ["Netflix", "Prime Video", "BBC iPlayer",
                 "Criterion Collection",
                 "ARES Reserve", "HBO Max", "Hulu", "Disney+", "Apple TV+"]
    stream = ""
    streamy = []
    for i in range(3):
        a = random.randint(0, 8)
        if streamers[a] not in stream:
            stream += streamers[a]
            stream += ", "
            streamy.append(streamers[a])

    with conn:
        c.execute("INSERT OR IGNORE INTO streamers VALUES (:movie, :streamer, :id)",
                  {'movie': emp.get("Title"), 'streamer': stream,
                   'id': emp.get("imdbID")})
        for sitee in streamy:
            j = emp.get("Title")
            j += ", "
            c.execute("UPDATE sites SET movies = movies || :movie WHERE "
                      "name=:site", {'movie': (j), 'site': sitee})


# d = requests.get("http://www.omdbapi.com/?i=tt0042876&apikey=8f838e17")
# d = d.json()
# print(d)
#
# insert_emp(d)
# insert_streamer(d)
#
#
# d = requests.get("http://www.omdbapi.com/?i=tt0111161&apikey=8f838e17")
# d = d.json()
#
# insert_emp(d)
# insert_streamer(d)

films = ["tt0042876", "tt0111161", "tt0068646", "tt0468569", "tt0071562", "tt0050083"
         , "tt0108052", "tt0167260", "tt0110912", "tt0120737", "tt0060196", "tt0109830",
         "tt0137523", "tt1375666", "tt0167261", "tt0080684", "tt0133093", "tt0099685", "tt0073486",
         "tt0114369", 'tt0047478', 'tt0038650', "tt0102926", "tt0120815", 'tt0317248', 'tt0118799',
         "tt0120689", "tt0076759", 'tt0816692', "tt0103064", "tt0088763", "tt0245429",
         "tt0054215", "tt0110413", "tt0253474", "tt6751668", "tt0110357", "tt0172495",  "tt0120586",
         'tt0114814', "tt0407887", "tt0482571", "tt0034583", "tt2582802", "tt1675434", "tt0027977",
         "tt0064116", "tt0056058", "tt0095327"]


url = 'https://www.imdb.com/chart/bottom?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=470df400-70d9-4f35-bb05-8646a1195842&pf_rd_r=MK7C3ZZND5F5Y10H5RP5&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_ql_8'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]

for film in links:
    a = film.split("/")[2]
    d = requests.get("http://www.omdbapi.com/?i=" + a + "&apikey=8f838e17")
    d = d.json()
    insert_emp(d)
    insert_streamer(d)

# url = 'http://www.imdb.com/chart/top'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# movies = soup.select('td.titleColumn')
# links = [a.attrs.get('href') for a in soup.select('td.img_primary a')]
#
# print(soup)


# for film in links:
#     a = film.split("/")[2]
#     d = requests.get("http://www.omdbapi.com/?i=" + a + "&apikey=8f838e17")
#     d = d.json()
#     insert_emp(d)
#     insert_streamer(d)


# url = 'https://www.imdb.com/chart/moviemeter?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=470df400-70d9-4f35-bb05-8646a1195842&pf_rd_r=46RP49P1TM50PT2SZBNA&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_2'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# movies = soup.select('td.titleColumn')
# links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
#
# for film in links:
#     a = film.split("/")[2]
#     d = requests.get("http://www.omdbapi.com/?i=" + a + "&apikey=8f838e17")
#     d = d.json()
#     insert_emp(d)
#     insert_streamer(d)

conn.close()
