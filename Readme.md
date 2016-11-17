Allegro project
---------------
This project scrapes allegro archive and analyzes trends in sales history,
Scrapy is used for web scraping. Flask is used to diplay the results, computed with pandas.
Scrapy saves the data to sqlite db (AllegroSales.db), flask reads it from there.
Project is running in docker.



Instructions for docker build
-----------------------------
cd to allegro_project/allegro_flask_app
$ docker-compose build
$ docker-compose up

On mac and windows check the vm ip
$ docker-machine ip

in the browser go to <docker-machine ip>:5000

Scrapy instructions
-------------------
The sqlite db is already in the project. However, it can be updated.
Run scrapy from the uppermost project directory (allegro_project/)

$ scrapy crawl crawl_allegro 
