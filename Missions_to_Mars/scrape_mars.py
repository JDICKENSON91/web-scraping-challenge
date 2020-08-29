def scrape_info():
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import time
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    
    def init_browser():
        # @NOTE: Replace the path with your actual path to the chromedriver
        executable_path = {'executable_path':ChromeDriverManager().install()}
        return Browser("chrome", **executable_path, headless=False)
    

    browser = init_browser()
    
    mars_dict = {}

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get News Title
    #news_title = soup.find_all("a", class_="/news/8744/nasa-engineers-checking-insights-weather-sensors/", target="_self")[0].get_text()
    #print(f"News Title: {news_title}")
    
    #mars_dict["news_title"] = news_title

    # Get News Paragraph
    #news_para = soup.find_all("a", href="/news/8744/nasa-engineers-checking-insights-weather-sensors/", target="_self")[0].get_text()
    #print(f"News Title: {news_para}")
    
    #mars_dict["news_para"] = news_para

       
    
    browser.quit()
    
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get Picture URL
    image_line = soup.find("a", class_="button fancybox")
    image_url = image_line["data-fancybox-href"]
    jpl_url = "https://www.jpl.nasa.gov"
    
    featured_image_url = jpl_url + image_url
    
    mars_dict["image_line"] = image_line
    mars_dict["featured_image_url"] = featured_image_url
    
    
    
    browser.quit()
    print(image_line)
    
    mars_url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(mars_url)
    mars_facts_df = mars_df[0]
    
    mars_dict["mars_facts_df"] = mars_facts_df
    
    mars_facts_html = mars_facts_df.to_html()
    
    mars_dict["mars_facts_html"] = mars_facts_html
    print(mars_facts_html)
    
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
    ]
    
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_dict