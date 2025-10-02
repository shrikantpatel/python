class Movie :

    def __init__(self, title, rating, year) :
        self.title = title
        self.rating = rating
        self.year = year

    def display_info(self) :
        print(f"Title: {self.title}, Rating: {self.rating}, Year: {self.year}")

class IndianMovie(Movie) :

    def __init__(self, title, rating, year, language) :
        super().__init__(title, rating, year)
        self.language = language

    def display_info(self) :
        super().display_info()
        print(f"Language: {self.language}")

def print_movie_info(movie: Movie) :
    print(f"Title: {movie.title}, Rating: {movie.rating}, Year: {movie.year}")

if __name__ == "__main__":
    movie1 = Movie("Inception", 8.8, 2010)
    movie2 = IndianMovie("3 Idiots", 8.4, 2009, "Hindi")

    movie1.display_info()
    movie2.display_info()

    print_movie_info(movie1)
    print_movie_info(movie2)