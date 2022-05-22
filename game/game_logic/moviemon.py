import requests
from django.conf import settings


class Moviemon:
    def __init__(self, title, year, director, poster, rating, plot, actors):
        self.title = title
        self.year = year
        self.director = director
        self.poster = poster
        self.rating = rating
        self.plot = plot
        self.actors = actors

    def __str__(self):
        return str({
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "poster": self.poster,
            "rating": self.rating,
            "plot": self.plot,
            "actors": self.actors,
        })

    @classmethod
    def get_move_by_imdb_id(cls, imdb_id):
        URL = "http://www.omdbapi.com/"
        params = {"apikey": settings.OMDB_API_KEY, "i": imdb_id}
        try:
            data = requests.get(URL, params=params).json()
            print(data)
            return Moviemon(
                data["Title"],
                data["Year"],
                data["Director"],
                data["Poster"],
                float(data["imdbRating"]),
                data["Plot"],
                data["Actors"])
        except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    the_host = Moviemon("title", "year", "director", "poster", "rating", "plot", "actors")
    print(the_host)
    print(Moviemon.get_move_by_imdb_id("tt1663662"))
