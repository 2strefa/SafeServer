from django.shortcuts import  render_to_response

from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from django.conf import settings



def index(request):

    return render_to_response('home/index.html', context_instance=RequestContext(request))

def regulamin(request):

    return render_to_response('home/regulamin.html', context_instance=RequestContext(request))

def okres_testowy(request):

    return render_to_response('home/okres_testowy.html', context_instance=RequestContext(request))

def przeniesienie_hostingu(request):

    return render_to_response('home/przeniesienie_hostingu.html', context_instance=RequestContext(request))
