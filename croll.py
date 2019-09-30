# #from selenium import webdriver
# #driver.implicitly_wait(3)
# #driver.get('https://map.naver.com/')
#
# #driver.find_element_by_css_selector('#search-input ').send_keys('롯데시네마')
# #driver.find_element_by_css_selector('#header button[type="submit"]').click()
#
#
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from bs4 import BeautifulSoup
#
# driver = webdriver.Chrome('C:/informs/chromedriver_win32/chromedriver.exe')
# #암묵적으로 웹자원 로드를 위해 3초까지 기다려준다.
# driver.implicitly_wait(3)
# #driver = webdriver.Firefox()
#
#
# # url에 접근한다.
# driver.get('https://www.zeropay.or.kr/main.do?pgmId=PGM0081')
#
#
# select = Select(driver.find_element_by_id('skkCode'))
# # select by visible text
# #select.select_by_visible_text('강남구')
# # select by value
# select.select_by_value('01')
#
#
#
#
# driver.find_element_by_css_selector('.btn-set a[href="#none"]').click()  #검색버튼 클릭
#
#
# # Naver 페이 들어가기
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# notices = soup.select('.mw_table800 > tbody > tr > td[1] ')
#
# print(notices)