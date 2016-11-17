import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as lite


"""
possible issues on Mac OS: 

from matplotlib.backends import _macosx
**RuntimeError**: Python is not installed as a framework.
http://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python

"""
plt.style.use('ggplot')

def load_db():
    
    con = lite.connect('AllegroSales.db') # The database will be created if it doesn't exist, if it does it will connect.
    df = pd.read_sql('SELECT * FROM Macs', con)
    
    # Parse the scraping results  
    df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], format = "%Y/%m/%d")
    df['price'] = df['price'].astype(float).astype(int)
    # getting only the month and year for a groupby operation for heatmap. Otherwise bins (daily) are too narrow on x-axis to make sense of the plot.
    df['month_date'] = df['date_of_sale'].map(lambda x: str(x.year) + ' ' + x.strftime('%B'))
    # Order by date because scrapy does not scrape in page order
    df = df.sort(columns = 'date_of_sale')
    
    return df
    
def heatmap(df):
    # Select only the columns for the heatmap plot
    parsed = df[['price', 'month_date']]
    # Bin the prices into price categories, so a small difference is treated as the same price
    binned, edges = pd.cut(parsed['price'], bins = 10, retbins = True, labels = False)
    # Round edges to the nearest hundred so they are more intuitive on the plot
    edges = [int(round(e,-2)) for e in edges]
    # Add the new created binned prices and substitute the old prices
    parsed['price'] = binned.as_matrix()
     
    # Count the number of sales in price category which occurs in each month
    count_df = parsed.groupby(["price", "month_date"]).size().reset_index(name="number_of_sales")
    fig = plt.figure(figsize = (18,12))
    
    # Plot it
    ax = sns.heatmap(count_df.pivot('price', 'month_date', 'number_of_sales'), yticklabels = edges)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
    ax.set_title('History of Macbook sales on Allegro')
    ax.invert_yaxis()
    plt.yticks(rotation=0) 

    fig.savefig('static/plots/heatmap.jpg', dpi = 100)
    print('Figure saved')        

    
def create_heatmap():
    """Loads the sqlite db into pandas, processes data ans saves figure into static/plots folder of the flask app."""
    heatmap(load_db())

if __name__ == '__main__':
    create_heatmap()
    