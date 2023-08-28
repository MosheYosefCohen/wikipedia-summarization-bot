import requests
from bs4 import BeautifulSoup
import openai
from autocorrect import Speller

spell = Speller(lang='en')


def scrape_wikipedia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = ""

    # Find relevant HTML elements and extract the text
    # Example: Extracting the main content from Wikipedia's paragraphs
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        if paragraph.find(class_='reference'):
            continue
        content += paragraph.get_text()
    print(content)
    return content

# Function to generate summary using OpenAI's API
def generate_summary(api_key, text):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=text,
        max_tokens=200,
        temperature=0.0,
        n=1,
        stop=None
    )
    summary = response.choices[0].text.strip()
    return summary

# Function to handle the search
def perform_search(search_topic, api_key):
    if search_topic:
        search_url = f"https://en.wikipedia.org/wiki/{spell(search_topic.replace(' ', '_'))}"
        scraped_content = scrape_wikipedia(search_url)

        if scraped_content:
            prompt = "summarise this page in a humares way"
            # Generate summary using OpenAI's API
            summary = generate_summary(api_key, prompt + "\n\n" + scraped_content)

            print(summary)
            print("Summary has been generated!")
        else:
            print("Failed to retrieve content from Wikipedia.")
    else:
        print("Please enter a search topic.")

# Set the search topic and API key
search_topic_input = input("Enter the topic to search on Wikipedia: ")
api_key = ""  # Replace with your OpenAI API key

# Perform the search
perform_search(search_topic_input, api_key)



