# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# create empty list
college_links = []


# scrape the data
r = requests.get('https://collegedunia.com/btech-colleges')
html = r.text

colleges_html = BeautifulSoup(html, 'html.parser')
links = colleges_html.find_all("a", {'class': 'college_name'})
for link in links:
    college_links.append(link['href'])
print(college_links)

college_info = []
courses_fees = []
admission = []
reviews = []
for college_link in college_links[0:10]:
    r = requests.get(college_link)
    html = r.text
    college_data_html = BeautifulSoup(html, 'html.parser')

    # get college info
    college_data = college_data_html.find("div", {'class': 'college_data'})
    info = college_data.get_text()
    college_info.append(info)

    # get courses and fees
    coursesFees = college_data_html.find("table", {'class': 'table-striped'}).get_text()
    courses_fees.append(coursesFees)

    # get admission info
    admission_link = str(college_link) + '/admission'
    r = requests.get(admission_link)
    html = r.text
    admission_data_html = BeautifulSoup(html, 'html.parser')
    admission2020 = admission_data_html.find("div", {'class': 'admission_content_wrapper automate_client_img_article'}).get_text()
    admission.append(admission2020)

    # get reviews info
    review_link = str(college_link) + '/reviews'
    r = requests.get(review_link)
    html = r.text
    review_data_html = BeautifulSoup(html, 'html.parser')
    review = review_data_html.find("div", {'class': 'review_content content-side'}).get_text()
    reviews.append(review)

df = pd.DataFrame(list(zip(college_info, courses_fees, admission, reviews)),
               columns =['Info', 'courses & fees', 'admission', 'reviews'])

df.to_excel("scrape.xlsx")
