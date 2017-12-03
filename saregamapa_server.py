
"""
Created on Mon Nov 27 15:21:38 2017

@author: User
"""

import web
import json
import saregamapa_index as si

urls = (
    '/', 'saregamapa_ui',    
    '/search', 'apply_search',
    '/wordcloud', 'generate_wordcloud'
)

render = web.template.render('ui/')

class saregamapa_ui:
  def GET(self):
    return render.saregamapa_ui()

class apply_search:        
    def GET(self):
        gData = web.input()
        queryString = gData['qs']

        output = {
                'query': queryString,
                'search_results': si.sIndex.apply_search(queryString, False)
                }

        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class generate_wordcloud:        
    def GET(self):

        gData = web.input()
        qs = gData['qs']
        cc = int(gData['cc'])
        
        output = {
                'query': qs,
                'cluster_count': cc, 
                'cluster_results': si.sIndex.cluster_data(qs, cc, False)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    