import json

from django.contrib.gis.geos import LineString
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext

from chantiers.points.models import Chantier


def points_via_line(request):
    
    if request.POST and request.is_ajax():
        raw_line = request.POST.get('line', None)
        print 'hi'
        line = LineString(json.loads(raw_line))
        chantiers = Chantier.objects.get_near_line(line)
        print 'there'
        t = loader.get_template("point_list.html")
        c = RequestContext(request, {'chantiers': chantiers})
        return HttpResponse(t.render(c), mimetype="application/javascript")
        
    raise Http404
    
def prototype(request):
    return render_to_response('prototype.html', {}, RequestContext(request))
        
    