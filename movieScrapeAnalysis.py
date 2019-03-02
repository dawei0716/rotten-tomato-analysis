from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import requests
import csv

#scrapes audience reviews from rottentomatoes.com 

class MovieReviews:
	def __init__(self, movieName, endPage):
		self.movieName = movieName
		self.endPage = endPage
		self.url = 'https://www.rottentomatoes.com/m/{}'.format(self.movieName)
	
	def printReviews(self):
		for num in range(1, self.endPage+1):
			reviews = self.scrapPage(num)
			for review in reviews:
				print(review.text)

	def runAnalysis(self):
		self.neg = 0
		self.neu = 0
		self.pos = 0
		self.compound = 0
		self.numberOfReviews = 0
		analyser = SentimentIntensityAnalyzer()
		for num in range(1 ,self.endPage+1):
			reviews = self.scrapPage(num)
			print(f'analysing page: {num}/{self.endPage}')
			for review in reviews:
				vs = analyser.polarity_scores(review.text)
				self.neg += vs['neg']
				self.neu += vs['neu']
				self.pos += vs['pos']
				self.compound += vs['compound']
				self.numberOfReviews += 1
		self.neg /= self.numberOfReviews
		self.neu /= self.numberOfReviews
		self.pos /= self.numberOfReviews
		self.compound /= self.numberOfReviews
		print()
		print('analysis complete')
		print()
		self.printScore()
	
	def printScore(self):
		print(f'sentiment for {self.numberOfReviews} audience reviews of {self.movieName}:')
		print(f'negative score: {self.neg}')
		print(f'neutral score: {self.neu}')
		print(f'positive score: {self.pos}')
		print(f'compound score: {self.compound}')
		print()
		# compound score ranges -1 to 1. higher score means positive sentiment. 

	def createCSVfile(self):
		csv_file = open(f'{self.movieName}_scrape.csv', 'w')
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(['review'])
		for num in range(1, self.endPage+1):
			reviews = self.scrapPage(num)
			for review in reviews:
				csv_writer.writerow([review.text.encode("utf-8")])
		csv_file.close()

	def scrapPage(self, num):
		source = requests.get(self.url+'/reviews/?page={}&type=user'.format(num)).text
		soup = BeautifulSoup(source, 'lxml')
		reviews = soup.find_all('div', class_= "user_review")
		return reviews
	


towering_inferno = MovieReviews('towering_inferno', 51)
towering_inferno.runAnalysis()
#towering_inferno.createCSVfile()

# terminator_genisys = MovieReviews('terminator_genisys', 246)
# terminator_genisys.runAnalysis()

#TAKES WAY LONG FOR MOVIES WITH MANY REVIEWS. HOW TO INCREASE PERFORMANCE? 
# shawshank_redemption = MovieReviews('shawshank_redemption',2746)
# shawshank_redemption.runAnalysis()



#format for top critic reviews 
#'https://www.rottentomatoes.com/m/apollo_11_2019/reviews/?page={}&sort='.format(num)
