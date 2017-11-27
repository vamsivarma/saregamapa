
"""
Created on Mon Nov 27 15:21:38 2017

@author: User
"""

import web

urls = (
    '/index', 'index',    
    '/search', 'apply_search',
    '/wordcloud', 'generate_wordcloud'
)

render = web.template.render('ui/')

class index:
  def GET(self):
    return render.index()

class apply_search:        
    def GET(self):
        output = ['This', 'is', 'a', 'sample', 'output']
        return output

class generate_wordcloud:        
    def GET(self):
        output = ['This', 'is', 'a', 'word', 'cloud']
        return output

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    