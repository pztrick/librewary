import httpagentparser
#from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import render

BAD_BROWSERS = ['empty', ]


class MsieView(TemplateView):
    template_name = "base_msie.html"


class RedirectBadBrowsersMiddleware(object):
    """ Redirects MSIE to getfirefox.com """

    def process_request(self, request):
        browser = httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']['name']
        if browser in BAD_BROWSERS:
            return render(request, template_name="base_bad_browser.html")
        return None
