class Movie :

    def __init__(self, title, rating, year) :
        self.title = title
        self.rating = rating
        self.year = year

    def display_info(self) :
        print(f"Title: {self.title}, Rating: {self.rating}, Year: {self.year}")


if __name__ == "__main__":
    movie1 = Movie("Inception", 8.8, 2010)
    movie2 = Movie("The Matrix", 8.7, 1999)

    movie1.display_info()
    movie2.display_info()
