Allegro project
---------------
This project scrapes allegro archive and analyzes trends in sales history.


Scrapy is used for web scraping. 


Scrapy saves the data to sqlite db (AllegroSales.db), flask reads it from there.


Flask is used to diplay the results in a web-app.


Project is running in docker.



Instructions for docker build
-----------------------------


`$ docker pull ryscet/allegroproject_web`

`$ docker run -p 5000:5000 ryscet/allegroproject_web`

For linux go to localhost:5000 in the browser

For mac and windows check the ip of the virtual machine:

`$ docker-machine ip`
and enter it instead of local host.

Scrapy instructions
-------------------
The sqlite db is already in the project. However, it can be updated.
Run scrapy from the uppermost project directory (allegro_project/)

`$ scrapy crawl crawl_allegro`

Sales Heatmap
-------------
This heatmap is produced from the data scraped from allegro, and is visible in the flask app under '/plots' url.
![alt text](https://github.com/ryscet/allegro_project/blob/master/allegro_flask_app/static/plots/heatmap.jpg "Sales Heatmap")

