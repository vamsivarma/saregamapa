
"""
Created on Mon Nov 27 15:21:38 2017

@author: User
"""

import web
from saregamapa_searchindex import search_endpoint
urls = (
    '/index', 'index',    
    '/search/(.*)', 'apply_search',
    '/wordcloud/(.*)', 'generate_wordcloud'
)

render = web.template.render('ui/')

class index:
  def GET(self):
    return render.index()

class apply_search:        
    def GET(self, qs):
        output = {
                'query': qs,
                'parse_meta': search_endpoint()
                }
        return output

class generate_wordcloud:        
    def GET(self, qs):
        
        output = {
                'query': qs,
                'parse_meta': search_endpoint()
                }
        
        return output

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    