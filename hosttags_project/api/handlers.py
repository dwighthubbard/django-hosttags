from piston.handler import BaseHandler
from hosttags.models import Host

class HostHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = Host

   def read(self, request, tags=None,group=None):
        """
        Returns host records matching the tags and groups.

        """
        print request.REQUEST
        if 'tags' in request.REQUEST.keys():
            tags=request.REQUEST['tags']
        base = Host.objects        
        if tags:
            print type(tags)
            if type(tags) is str or type(tags) is unicode:
                print 'Splitting tags'
                tags=tags.split(',')            
            print tags
            base=base.filter(tags__name__in=tags)
            return base
        else:
            return base.all() # Or base.filter(...)
