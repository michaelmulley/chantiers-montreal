import json
import re

from django.contrib.gis.geos import LineString
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext

from chantiers.points.models import Chantier

def points_via_line(request):
    
    raw_line = request.REQUEST.get('line', None)
    if not line:
        raise Http404
    line = LineString(json.loads(raw_line))
    chantiers = Chantier.objects.get_near_line(line)
    t = loader.get_template("point_list.html")
    c = RequestContext(request, {'chantiers': chantiers})
    resp = t.render(c)
    if 'callback' in request.GET:
        resp = "%s(%s);" % (re.sub(r'[^a-zA-Z0-9_]', '', request.GET['callback']), resp)
    return HttpResponse(resp, mimetype="application/javascript")
    
def prototype(request):
    return render_to_response('prototype.html', {}, RequestContext(request))
        
    