from .base_parser import BaseParser
import time
from bs4 import BeautifulSoup
import re


class ParimatchParser(BaseParser):

	__main_urls = ['https://pm-290.info/']
	__hockey_buttons = ["КХЛ. Статистика", "NHL. Статистика матча. Броски в створ ворот",  "NHL. Статистика матча"]
	__prefix_dict = {"SOT": ["бр.в створ"], "PT": ["штр.время"]}

	def get_page_data(self, way):
		if (way == 'Hockey'):
			data = self.__get_hockey_data()
		return(data)

	def __get_hockey_data(self):
		self.get_base_page(self.__main_urls)
		
		self.driver.find_element_by_xpath(u'//a[text()="Хоккей"]').click()

		for text in self.__hockey_buttons:
			try:
				self.driver.find_element_by_xpath(u'//a[text()="' + text + '"]').find_element_by_xpath(".//em").click()
			except:
				print("NO_TOURNAMENT")
		time.sleep(1)

		self.driver.find_element_by_xpath(u'//button[text()="Показать"]').click()
		

		out = self.__source_page_data()
		return(out)

	def __source_page_data(self):
		bs = BeautifulSoup(self.driver.page_source, "html.parser")
		html = bs.findAll(True, {'class':'bk'})
		out = []
		for match in html:
			row_out = {}
			for index, row in enumerate(match.findAll('td')):
				s = str(row)
				print(s)
				if (index == 1):
					try:
						row_out['datetime'] = ' '.join(list(map(self.clear_tag, s.split('<br/>'))))
					except:
						pass
				elif (index == 2):
					try:
						row_out['home_team'], row_out['away_team'] = list(map(self.clear_tag, s.split('<br/>')))
					except:
						pass
				elif (index == 3):
					try:
						row_out['spread'] = list(map(self.clear_tag, s.split('</b><b>')))[0]
					except:
						pass
				elif (index == 4):
					try:
						row_out['type'] = ''
						s = list(map(self.clear_tag, s.split('</a></u><u>')))[0]
						for key, array in self.__prefix_dict.items():
							for test in array:
								print(test)
								if test in s:
									row_out['type'] = key
									break
						row_out['home'] = list(map(self.clear_tag, s.split('</a></u><u>')))[0].replace(row_out['type'], ' ')
						row_out['away'] = list(map(self.clear_tag, s.split('</a></u><u>')))[1].replace(row_out['type'], ' ')
					except:
						pass
				elif (index == 5):
					try:
						row_out['total'] = self.clear_tag(s)
					except:
						pass
				elif (index == 6):
					try:
						row_out['under'] = self.clear_tag(s)
					except:
						pass
				elif (index == 7):
					try:
						row_out['over'] = self.clear_tag(s)
					except:
						pass
				elif (index == 8):
					try:
						row_out['home_win'] = self.clear_tag(s)
					except:
						pass
				elif (index == 9):
					try:
						row_out['draw'] = self.clear_tag(s)
					except:
						pass
				elif (index == 10):
					try:
						row_out['away_win'] = self.clear_tag(s)
					except:
						pass
				elif (index == 14):
					try:
						row_out['total_1'], row_out['total_2'] = list(map(self.clear_tag, s.split('</b><b>')))
					except:
						pass
				elif (index == 15):
					try:
						row_out['total_1_over'], row_out['total_1_under'] = list(map(self.clear_tag, s.split('</a></u><u>')))
					except:
						pass
				elif (index == 16):
					try:
						row_out['total_2_over'], row_out['total_2_under'] = list(map(self.clear_tag, s.split('</a></u><u>')))
					except:
						pass
			out.append(row_out)
		return(out)			

