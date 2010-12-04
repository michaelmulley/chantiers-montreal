import json
from lxml import objectify
import re
import urllib2

#http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def scrape_chantiers():
    f = urllib2.urlopen('http://applicatif.ville.montreal.qc.ca/e-cite/kml/chantiers_vgml.asp')
    doc = objectify.parse(f)
    results = []
    places = doc.getroot().findall('.//Placemark')
    for place in places:
        #import pudb; pudb.set_trace();
        r = {}
        coords = str(place.Point.coordinates).split(',')
        r['point'] = {'lat': float(coords[1]), 'lng': float(coords[0])}
        r['name'] = unescape(unicode(place.name))
        where = unescape(unicode(place.info_side_bar).replace('<BR>', ' '))
        if '<UL>' in where:
            components = []
            for line in where.split('</LI>'):
                line = re.sub(r'</?[lLuUiI]+>', '', line).replace(';', '').strip()
                if line:
                    components.append(line)
            where = components
        else:
            where = [where]
        r['where'] = where
        
        r['raw_description'] = unescape(unicode(place.description))
        results.append(r)
    return results
    
if __name__ == '__main__':
    print json.dumps(scrape_chantiers(), indent=4)