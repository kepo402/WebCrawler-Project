import requests
from bs4 import BeautifulSoup
from queue import Queue
from urllib.parse import urlparse

class PorterStemmer:
    def __init__(self):
        self.vowels = 'aeiou'
        self.consonants = 'bcdfghjklmnpqrstvwxyz'
        
    def is_consonant(self, letter):
        return letter in self.consonants
    
    def is_vowel(self, letter):
        return letter in self.vowels
    
    def ends_double_consonant(self, word):
        if len(word) < 2:
            return False
        return word[-1] == word[-2] and self.is_consonant(word[-1])
    
    def cvc(self, word):
        if len(word) < 3:
            return False
        if not (self.is_consonant(word[-3]) and self.is_vowel(word[-2]) and self.is_consonant(word[-1])):
            return False
        if word[-1] in 'wxy':
            return False
        return True
    
    def step_1a(self, word):
        if word.endswith('sses'):
            return word[:-2]
        elif word.endswith('ies'):
            return word[:-2]
        elif word.endswith('ss'):
            return word
        elif word.endswith('s'):
            return word[:-1]
        return word
    
    def step_1b(self, word):
        if word.endswith('eed'):
            if self.measure(word[:-3]) > 0:
                return word[:-1]
            else:
                return word
        if word.endswith('ed'):
            if self.contains_vowel(word[:-2]):
                return self.step_1b_helper(word[:-2])
            else:
                return word
        if word.endswith('ing'):
            if self.contains_vowel(word[:-3]):
                return self.step_1b_helper(word[:-3])
            else:
                return word
        return word
    
    def step_1b_helper(self, word):
        if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
            return word + 'e'
        if self.ends_double_consonant(word) and not word.endswith('l') and not word.endswith('s') and not word.endswith('z'):
            return word[:-1]
        if self.measure(word) == 1 and self.cvc(word):
            return word + 'e'
        return word
    
    def step_1c(self, word):
        if word.endswith('y'):
            if self.contains_vowel(word[:-1]):
                return word[:-1] + 'i'
        return word
    
    def measure(self, word):
        count = 0
        if len(word) == 0:
            return 0
        if self.is_vowel(word[0]):
            prev = 'v'
        else:
            prev = 'c'
        for letter in word:
            if (prev == 'c' and self.is_vowel(letter)) or (prev == 'v' and self.is_consonant(letter)):
                count += 1
                prev = 'o' if prev == 'c' else 'c'
        return count
    
    def contains_vowel(self, word):
        return any(char in self.vowels for char in word)
    
    def step_2(self, word):
        if word.endswith('ational'):
            if self.measure(word[:-6]) > 0:
                return word[:-6] + 'ate'
        if word.endswith('tional'):
            if self.measure(word[:-6]) > 0:
                return word[:-6] + 'tion'
        if word.endswith('enci'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'ence'
        if word.endswith('anci'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'ance'
        if word.endswith('izer'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'ize'
        if word.endswith('abli'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'able'
        if word.endswith('alli'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'al'
        if word.endswith('entli'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ent'
        if word.endswith('eli'):
            if self.measure(word[:-3]) > 0:
                return word[:-3] + 'e'
        if word.endswith('ousli'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ous'
        if word.endswith('ization'):
            if self.measure(word[:-7]) > 0:
                return word[:-7] + 'ize'
        if word.endswith('ation'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ate'
        if word.endswith('ator'):
            if self.measure(word[:-4]) > 0:
                return word[:-4] + 'ate'
        if word.endswith('alism'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'al'
        if word.endswith('iveness'):
            if self.measure(word[:-7]) > 0:
                return word[:-7] + 'ive'
        if word.endswith('fulness'):
            if self.measure(word[:-7]) > 0:
                return word[:-7] + 'ful'
        if word.endswith('ousness'):
            if self.measure(word[:-7]) > 0:
                return word[:-7] + 'ous'
        if word.endswith('aliti'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'al'
        if word.endswith('iviti'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ive'
        if word.endswith('biliti'):
            if self.measure(word[:-6]) > 0:
                return word[:-6] + 'ble'
        return word
    
    def step_3(self, word):
        if word.endswith('icate'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ic'
        if word.endswith('ative'):
            if self.measure(word[:-5]) > 0:
                return word[:-5]
        if word.endswith('alize'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'al'
        if word.endswith('iciti'):
            if self.measure(word[:-5]) > 0:
                return word[:-5] + 'ic'
        if word.endswith('ful'):
            if self.measure(word[:-3]) > 0:
                return word[:-3]
        if word.endswith('ness'):
            if self.measure(word[:-4]) > 0:
                return word[:-4]
        return word
    
    def step_4(self, word):
        if word.endswith('al'):
            if self.measure(word[:-2]) > 1:
                return word[:-2]
        if word.endswith('ance'):
            if self.measure(word[:-4]) > 1:
                return word[:-4]
        if word.endswith('ence'):
            if self.measure(word[:-4]) > 1:
                return word[:-4]
        if word.endswith('er'):
            if self.measure(word[:-2]) > 1:
                return word[:-2]
        if word.endswith('ic'):
            if self.measure(word[:-2]) > 1:
                return word[:-2]
        if word.endswith('able'):
            if self.measure(word[:-4]) > 1:
                return word[:-4]
        if word.endswith('ible'):
            if self.measure(word[:-4]) > 1:
                return word[:-4]
        if word.endswith('ant'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ement'):
            if self.measure(word[:-5]) > 1:
                return word[:-5]
        if word.endswith('ment'):
            if self.measure(word[:-4]) > 1:
                return word[:-4]
        if word.endswith('ent'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ism'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ate'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('iti'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ous'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ive'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        if word.endswith('ize'):
            if self.measure(word[:-3]) > 1:
                return word[:-3]
        return word
    
    def step_5a(self, word):
        if word.endswith('e'):
            if self.measure(word[:-1]) > 1:
                return word[:-1]
            elif self.measure(word[:-1]) == 1 and not self.cvc(word[:-1]):
                return word[:-1]
        return word
    
    def step_5b(self, word):
        if self.measure(word) > 1 and self.ends_double_consonant(word) and word.endswith('l'):
            return word[:-1]
        return word
    
    def stem(self, word):
        word = self.step_1a(word)
        word = self.step_1b(word)
        word = self.step_1c(word)
        word = self.step_2(word)
        word = self.step_3(word)
        word = self.step_4(word)
        word = self.step_5a(word)
        word = self.step_5b(word)
        return word

class WebCrawler:
    def __init__(self, starting_url, max_pages=500):
        self.starting_url = starting_url
        self.max_pages = max_pages
        self.url_frontier = Queue()
        self.url_frontier.put(starting_url)
        self.visited_urls = set()
        self.documents = []
        self.stemmer = PorterStemmer()

    def extract_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ')
        return text

    def crawl(self):
        while not self.url_frontier.empty() and len(self.visited_urls) < self.max_pages:
            current_url = self.url_frontier.get()
            if current_url in self.visited_urls:
                continue
            try:
                response = requests.get(current_url, timeout=10)
                if response.status_code == 200:
                    html_content = response.content
                    text = self.extract_text(html_content)
                    self.process_page(current_url, text)
                    self.visited_urls.add(current_url)
                    self.extract_links(html_content)
            except Exception as e:
                print("Error:", e)

    def extract_links(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and urlparse(href).scheme in ['http', 'https']:
                self.url_frontier.put(href)

    def process_page(self, url, text):
        # Perform stemming on the extracted text
        stemmed_text = [self.stemmer.stem(word) for word in text.split()]
        self.documents.append((url, stemmed_text))

    def run(self):
        self.crawl()
        self.print_statistics()

    def print_statistics(self):
        num_documents = len(self.documents)
        num_tokens = sum(len(document[1]) for document in self.documents)
        unique_terms = len(set(term for _, document in self.documents for term in document))
        print("Start Time: <start_time>")
        print("Indexing Complete, write to disk: <end_time>")
        print(f"Documents {num_documents} Terms {num_tokens} Tokens {unique_terms}")
        print("End Time: <end_time>")

if __name__ == "__main__":
    starting_url = input("Enter URL to crawl (must be in the form http://www.domain.com): ")
    crawler = WebCrawler(starting_url)
    crawler.run()