
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p




# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url



def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped table-hover")
    

# Scrape High-Resolution Mars’ Hemisphere Images and Titles
def hemispheres(browser):
    
    # Visit the URL 
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Retrieve the image urls and titles for each hemisphere.
    # Convert the browser html to a soup object
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    pics_elem = hemisphere_soup.find('div', class_='collapsible results')
    pics = pics_elem.find_all('div', class_='description')

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

        # find the full-res-image's relative url and add it to the base url
        img_url_rel = img_soup.find('img', class_='wide-image').get('src')
        image_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'

        # Add the full-resolution image URL string to the dictionary
        hemispheres['img_url'] = image_url

        # Append the dictionary to the Hemisphere image list
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls
    



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


   