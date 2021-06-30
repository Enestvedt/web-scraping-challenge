
def scrape_all():

    # Import Dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    from webdriver_manager.chrome import ChromeDriverManager

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False) #if headless True will execute but not open browser

    return(scrape_articles(browser, bs), scrape_image(browser, bs), scrape_facts(), scrape_hems(browser, bs))
    
    #quit the browser
    browser.quit()


# # Mars News Site
def scrape_articles(browser, bs):
    # Open the website in browser using splinter and webdriver
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # create soup object and find the article divs
    html = browser.html
    soup = bs(html, 'html.parser')

    articles = soup.find_all('div', class_='list_text')

    #set variables for title and news_p for the first news item
    news_title = articles[0].find("div", class_="content_title").text
    news_p = articles[0].find("div", class_="article_teaser_body").text

    return(news_title, news_p)


# # JPL Mars Space Images - Featured Image
def scrape_image(browser, bs):
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)

    #create soup object and and find path to file
    html = browser.html
    soup = bs(html, 'html.parser')

    location = soup.find('a', class_='showimg')['href']

    #create url by adding the path to the base url
    featured_image_url = (url2 + '/' + location)
    return(featured_image_url)


# # Mars Facts
def scrape_facts():
    # Connect pandas to website with html tables
    import pandas as pd
    
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)
    df = tables[1]

    #rename the columns so they make sense in html table
    df.columns = ['Mars_Profile', 'Mars_Data']

    #remove index colunn
    df = df.set_index(df.columns[0])

    #remove index so that it displays properly in html
    df.columns.name = df.index.name
    df.index.name = None

    # Generate and HTML Table from a dataframe 
    html_table = df.to_html()

    # strip new lines from table - clean-up the html
    html_table = html_table.replace('\n', '')

    # save table to file.html and open it (Mac only)
    df.to_html('table.html')



# # Mars Hemispheres
def scrape_hems(browser, bs):

    # Open the website in browser using splinter and webdriver
    url3 = "https://marshemispheres.com"
    browser.visit(url3)

    #create a soup object containing the page markup
    html = browser.html
    soup = bs(html, 'html.parser')

    # grab content from soup object
    items = soup.find_all('div', class_='item')

    #loop through content and push data into list
    hemisphere_image_urls = []
    for x in range(0, 4):
        partial_link = items[x].a['href']
        browser.visit(url3 + "/" + partial_link)
        new_html = browser.html
        soup = bs(new_html, 'html.parser')
        
        title = soup.find("h2", class_="title").text
        
        my_link = soup.find('img', class_="wide-image")["src"]
        my_link = (url3 + '/' + my_link)

        dict = {"title": title, "img_url": my_link}
        hemisphere_image_urls.append(dict)
        
        return(hemisphere_image_urls)
        print(hemisphere_image_urls)


scrape_all()
