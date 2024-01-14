from bs4 import BeautifulSoup
import requests

class Billboard:
    def __init__(self):
        self.labels = []
        self.prompt = ""

    def retrieve_songs(self):
        self.prompt = input("Which year do you want to travel to? Type the date in this forma YYYY-MM-DD: ")
        print(self.prompt)

        response = requests.get(f"https://www.billboard.com/charts/hot-100/{self.prompt}/")
        print(response)

        soup = BeautifulSoup(response.text, "html.parser")
        labels = soup.select("div li #title-of-a-story")

        self.labels = [label.get_text().strip() for label in labels]