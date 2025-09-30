from abc import ABC, abstractmethod

class Movie(ABC) :

    def __init__(self, title, rating, year) :
        self.title = title
        self.rating = rating
        self.year = year

    def display_info(self) :
        print(f"Title: {self.title}, Rating: {self.rating}, Year: {self.year}, Language: {self.get_language()}")

    @abstractmethod
    def get_language(self) :
        return "Unknown"

class IndianMovie(Movie) :

    def __init__(self, title, rating, year, language) :
        super().__init__(title, rating, year)
        self.language = language

    def get_language(self) :
        return self.language


if __name__ == "__main__":
    #movie1 = Movie("Inception", 8.8, 2010) # This will raise an error since Movie is abstract
    
    movie2 = IndianMovie("3 Idiots", 8.4, 2009, "Hindi")

    movie2.display_info()