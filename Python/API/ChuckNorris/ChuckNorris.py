import requests

def main():
    while True:
        action = int(input("1 for category research, 2 for word research: "))
        if action == 1:
            categories = requests.get('https://api.chucknorris.io/jokes/categories')
            print(categories.json())
            category = input("Insert the category: ")
            if category not in categories.json():
                print("This category doesn't exist")
            else:
                r = requests.get(f'https://api.chucknorris.io/jokes/random?category={category}')
                print(r.json()['value'])

        elif action == 2:
            query = input("Insert the word: ")
            r = requests.get(f'https://api.chucknorris.io/jokes/search?query={query}')
            for i in r.json()['result']:
                print(i['value'])

        else:
            print("It isn't so difficult...just choose 1 or 2!")
            break

if __name__ == "__main__":
    main()