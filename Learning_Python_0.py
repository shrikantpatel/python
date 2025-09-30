movie_title = 'Inception'
release_year = 2010
rating = 8.8
movie_info = f'{movie_title} was released in {release_year}  and has rating of {rating}'

if (rating >= 9) :
    print ('This movie is a masterpiece!')
elif (rating >= 8.5):
    print ('This movie is a must-watch!')
else :
    print ('This movie is worth seeing.')

for number in range(3) :
    print('for loop iteration number:', number)

movies = ['Inception', 'The Matrix', 'Parasite']
for movie in movies :
    if (movie == 'Parasite') :
        print(movie)

movies = [
    {'title': 'Inception', 'year': 2010, 'rating': 8.8},
    {'title': 'The Matrix', 'year': 1999, 'rating': 8.7},
    {'title': 'Parasite', 'year': 2019, 'rating': 8.6}
]

for movie in movies :
    if (movie['title'] == 'The Matrix') :
        print(movie['title'])

def find_movie_rating(movie_list : list, movie_title: str) :
    for movie in movie_list :
        if (movie['title'] == movie_title) :
            return movie['rating']
    return None
print(find_movie_rating(movies, 'Inception'))

def find_movie_rating_comprehension(movie_list : list, movie_title: str) :
    ratings_list = next((movie['rating'] for movie in movies if movie['title'] == movie_title), None)
    return ratings_list
print(find_movie_rating_comprehension(movies, 'Inception'))

num = -1
while num != 0:
    num = int(input('Enter a number: '))
    if num == 999 :
        break
    if num < 0 :
        print('Negative numbers are not allowed.')
        continue

print(f'You entered: {num}')

def fruit_color(fruit: str) -> str:
    match fruit:
        case "apple":
            return "red"
        case "banana":
            return "yellow"
        case "grape":
            return "purple"
        case _:
            return "unknown"
        
print(fruit_color("banana"))

