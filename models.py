from app import db
import re

def sligfy (s):
    p = 'r[^/w+]'
    return re.sub(p, '-', s)

class mod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # dont need slug right now
    #def __init__(self, *args, **kwargs):
        #super(mod, self).__init__(*args, **kwargs)
        #self.make_slug()
    #def make_slug(self):
        #if self.titl:
            #self.slug = sligfy(self.titl)
    # end slug
    def __repr__(self):
        return 'id = {},  title = {},  body = {},  slug = {},  '.format(self.id, self.titl, self.body, self.slug)
