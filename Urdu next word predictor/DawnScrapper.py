from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import string
import re
import os
import csv
import matplotlib.pyplot as plt

class WebScrapper:
    def __init__(self):
        self.scrapped = []
        if (os.path.exists('scraps.csv')):
            with open('scraps.csv', 'r', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if len(row) >= 1:
                        self.scrapped.append(row[0])

        self.newScraps = []
        self.pageTexts = []

        self.uWords = {}
        self.uWordCount = 0
        self.wordCount = 0
    

    def getPageHtml(self, url):
        try:
            with closing(get(url, stream=True, allow_redirects=False)) as response:
                if self.isHtml(response):
                    return response.content
                else:
                    return None
        except RequestException as e:
            print('RequestException Error at {0}: {1}'.format(url, str(e)))
            return None


    def isHtml(self, response):
        if (response.status_code == 200):
            contentType = response.headers['Content-Type'].lower()
            if (contentType is not None and contentType.find('html') > -1):
                return True
        return False

    def scrape(self, pagePath, writer):
        raise NotImplementedError('Must override in child class.')


    def scrapePages(self, startId, endId):
        with open('scraps.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for pageId in range(startId, endId + 1):
                self.scrape(pageId, writer)


    def scrapePage(self, pageId):
        with open('scraps.csv', 'a', encoding='utf-8', newline='') as f:
            self.scrape(pageId, csv.writer(f))


    def saveScrap(self, writer):
        for page in self.newScraps:
            writer.writerow(page)
            self.scrapped.append(page[0])
        self.newScraps = []


    def cleanUnscrapped(self):
        self.scrapped = []
        succesful = []
        failed = 0
        if (os.path.exists('scraps.csv')):
            with open('scraps.csv', 'r', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if len(row) > 1:
                        succesful.append(row)
                        self.scrapped.append(row[0])
                    else:
                        failed += 1
            
            with open('scraps.csv', 'w', encoding='utf-8', newline='') as f:
                wrtier = csv.writer(f)
                wrtier.writerows(succesful)
            
            print('Succesful Scraps: ', len(succesful))
            print('Failed Scraps: ', failed)


    def createCorpus(self, filename, maxWords):
        self.pageTexts = []
        self.uWords = {}
        self.wordCount = 0
        self.uWordCount = 0
        sentences = []
        with open('scraps.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) > 1:    
                    pageText = [row[0]]
                    text = []

                    for p in row[1:]:
                        p = re.sub(r'[^ \u0620-\u063f\u0641-\u065f\u066e-\u06d5\u06ee\u06ef\u06fa-\u06fc\u06ff]', '', p)
                        p = p.split('۔')
                        p = [s.strip() for s in p if s.strip() != '']
                        text = text + p

                    # wCount, nwCount = self.extractWords(text)
                    # pageText.append(wCount)
                    # pageText.append(nwCount)
                    # pageText.append(text)
                    # self.pageTexts.append(pageText)

                    sentences = sentences + text
                    # if self.uWordCount >= maxWords:
                    #     break
            corpus = '\n'.join(sentences)
        
        self.saveCorpus(filename, corpus)
        

    def extractWords(self, text):
        words = text.split(' ')
        wordCount = 0
        nWordCount = 0
        for w in words:
            if w != '':
                if w in self.uWords:
                    self.uWords[w] = self.uWords[w] + 1
                else:
                    self.uWords[w] = 1
                    nWordCount += 1
                wordCount += 1
        
        self.wordCount += wordCount
        self.uWordCount += nWordCount
        return wordCount, nWordCount


    def saveCorpus(self, filename, corpus):
        with open(filename + '.txt', 'w', encoding='utf-8') as f:
            f.write(corpus)

        # with open(filename + 'words.csv', 'w', encoding='utf-8', newline='') as wordsFile:
        #     writer = csv.writer(wordsFile)
        #     for w in self.uWords:
        #         writer.writerow([w, self.uWords[w]])

    def plotWordCount(self):
        X = [0]
        Y = [0]
        for p in self.pageTexts:
            X.append(X[-1] + p[1])
            Y.append(Y[-1] + p[2])
        plt.plot(range(len(self.pageTexts) + 1), Y)
        plt.xlabel('Pages')
        plt.ylabel('Unique Words')
        plt.show()


class DawnScrapper(WebScrapper):
    def __init__(self):
        super().__init__()
        self.baseUrl = 'https://www.dawnnews.tv/news/'


    def scrape(self, pageId, writer):
        url = self.baseUrl + str(pageId)
        if url in self.scrapped:
            print(url, 'has already been scrapped.')
            return

        print('Scrapping for text at: ', url, end=' ')
        scrap = [url]
        self.newScraps.append(scrap)

        html = self.getPageHtml(url)
        if html == None or html == '':
            self.saveScrap(writer)
            print('- No Content!')
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        if soup == None:
            self.saveScrap(writer)
            print('- Soup Error!')
            return
        
        div = soup.find('div', {'class': 'story__content'})
        if div == None or div.text == '':
            self.saveScrap(writer)
            print('- No Story Found!')
            return

        i = 0
        for p in div.findAll('p', recursive=False):
            pText = p.text.strip()
            if pText != '' and pText.startswith('یہ بھی پڑھیں:') == False and pText.startswith('مزید پڑھیں:') == False:
                scrap.append(pText)
                i += 1

        self.saveScrap(writer)
        print('- Scrapped ', i, ' <p> tags.')
        return


scrapper = DawnScrapper()
# scrapper.scrapePages(1080000, 1091999)
# scrapper.createCorpus('corpus', 100000)
# print(scrapper.wordCount)
# print(scrapper.uWordCount)
# print(len(scrapper.pageTexts))
# scrapper.plotWordCount()