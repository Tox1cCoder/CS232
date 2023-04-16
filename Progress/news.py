import time

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge("./msedgedriver.exe")

url = 'https://vnexpress.net/goc-nhin/binh-luan-nhieu'
driver.get(url)

elements = driver.find_elements(By.CLASS_NAME, 'title-news')
links = [ele.find_element(By.TAG_NAME, 'a').get_attribute('href') for ele in elements]
titles = []
post_contents_box = []
comments_box = []
nums_articles = int(input("Please provide the number of articles to crawl: "))

for link in links[:nums_articles]:
    text = str()
    driver.get(link)
    title = driver.find_element(By.CLASS_NAME, 'title-detail').text
    comments = driver.find_elements(By.CSS_SELECTOR, ".content-comment")
    post_content = driver.find_element(By.CLASS_NAME, 'fck_detail').text
    titles.append(title)
    post_contents_box.append(post_content)

    for id, comment in enumerate(comments, start=1):
        comment_sender = driver.find_element(By.XPATH, f'''//*[@id="list_comment"]/div[{id}]/div[2]/p/span''').text
        comment_text = driver.find_element(By.XPATH, f'''//*[@id="list_comment"]/div[{id}]/div[2]/p''').text
        text = text + comment_sender + '\n' + comment_text.strip() + '\n'
    comments_box.append(text)
    time.sleep(2)
driver.quit()

D = {'Title': titles,
     'Content': post_contents_box,
     'Comment': comments_box
     }

path = "csv"
exist = os.path.exists(path)
if not exist:
    os.makedirs(path)

df = DataFrame(D, columns=['Title', 'Content', 'Comment'])
export_csv = df.to_csv('csv/news.csv', index=None, header=True)
