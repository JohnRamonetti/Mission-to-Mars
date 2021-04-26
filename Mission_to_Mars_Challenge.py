
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p



# ### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Convert the browser html to a soup object and then quit the browser
html = browser.html
hemisphere_soup = soup(html, 'html.parser')

pics_elem = hemisphere_soup.find('div', class_='collapsible results')

pics = pics_elem.find_all('div', class_='description')

pics[0]


for pic in pics:
    # Initialize an empty dictionary
    hemispheres = {}
    # find the picture title and add it to the dictionary
    title = pic.find('h3').get_text()
    hemispheres['title'] = title
    
    # find the relative link to the page with the full resolution image(jpg) and add it to the base URL
    pic_link = pic.find('a').get('href')
    full_pic_link = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{pic_link}'
    
    # Go to the page with the full image
    browser.visit(full_pic_link)
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # find the full-res-image relative url and add it to the base url
    img_url_rel = img_soup.find('img', class_='wide-image').get('src')
    image_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'
    
    # Add the full-resolution image URL string to the dictionary
    hemispheres['img_url'] = image_url
    
    # Append the dictionary to the Hemisphere image list
    hemisphere_image_urls.append(hemispheres)


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()




