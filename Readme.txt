developing on scrap2 virtualenv 

Remember to run scrapy from the uppermost project directory (/flask_allegro)

$ scrapy crawl <spider_name> 

and run flask from (/flask_allegro/<flaskr>) directory

$ export FLASK_APP=flaskr
$ export FLASK_DEBUG=1
$ flask run