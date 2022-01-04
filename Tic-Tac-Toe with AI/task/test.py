potential_dates = [{"name": "Julia", "gender": "female", "age": 29,
                    "hobbies": ["jogging", "music"], "city": "Hamburg"},
                   {"name": "Sasha", "gender": "male", "age": 18,
                    "hobbies": ["rock music", "art"], "city": "Berlin"},
                   {"name": "Maria", "gender": "female", "age": 35,
                    "hobbies": ["art"], "city": "Berlin"},
                   {"name": "Daniel", "gender": "non-conforming", "age": 50,
                    "hobbies": ["boxing", "reading", "art"], "city": "Berlin"},
                   {"name": "John", "gender": "male", "age": 41,
                    "hobbies": ["reading", "alpinism", "museums"], "city": "Munich"}]

def select_dates(potential_dates):
    city = "Berlin"
    age = 30
    art = 'art'

    return ", ".join([
        person["name"] for person in potential_dates
        if person["city"] == "Berlin" and person["age"] > 30 and "art" in person["hobbies"]
    ])


def say_bye(names):
    for name in names:
        print("Au revoir,", name)
        print("See you on", names[name]["next appointment"])
        print()


humans = {"Laura": {"next appointment": "Tuesday"},
          "Robin": {"next appointment": "Friday"}}


iris = {}


def add_iris(id_n, species, petal_length, petal_width, **kwargs):
    iris[id_n] = {"species": species, 'petal_length': petal_length, 'petal_width': petal_width}
    for key, value in kwargs.items():
        iris[id_n].update({key: value})


add_iris(0, 'Iris versicolor', 4.0, 1.3, petal_hue='pale lilac')
