from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# My app
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView, RedirectView
from django.db.models.loading import get_app, get_models, get_model
from django.contrib.admin.views.decorators import staff_member_required
from core.views import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'librewary.views.home', name='home'),
    # url(r'^librewary/', include('librewary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Core urls
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # static information views
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^faqs/$', TemplateView.as_view(template_name='faqs.html'), name='faqs'),
    url(r'^documentation/$', TemplateView.as_view(template_name='docs.html'), name='documentation'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^copyright/$', TemplateView.as_view(template_name='copyright.html'), name='copyright'),
    url(r'^twin-pints/$', TemplateView.as_view(template_name='twinpints.html'), name='twinpints'),
    # social auth, e.g. /facebook/login/
    url(r'', include('social_auth.urls')),
    url(r'^facebook/$', RedirectView.as_view(url='/login/facebook/', permanent=False), name='facebook-login'),
    # session views
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    # OLD: url(r'^register/$', RegisterView.as_view(template_name='register.html'), name='register'),
    url(r'^dashboard/$', 'core.views.DashboardView', name='dashboard'),
    url(r'^logout/$', logout, {'template_name': 'base.html'}, name='logout'),
    # authenticated views
    url(r'^brewer/(?P<pk>\d+)/$', ProtectedDetailView.as_view(model=Brewer), name='brewer-profile'),
    # brewer settings views
    url(r'^brewer/(?P<pk>\d+)/toggle-facebook/$', 'core.views.BrewerToggleFacebook', name='toggle-show-facebook'),
    url(r'^brewer/(?P<pk>\d+)/toggle-email/$', 'core.views.BrewerToggleEmail', name='toggle-show-email'),
    # brewer equipment management
    url(r'^brewer/(?P<pk>\d+)/equipment/$', BrewerEquipmentListView.as_view(model=Equipment), name='brewer-equipment'),
    url(r'^equipment/add/$', BrewerEquipmentAddView.as_view(extra_context={'extra_title': 'Add Tool to My Equipment'}), name='brewer-equipment-add'),
    url(r'^equipment/(?P<pk>\d+)/toggle-share/$', 'core.views.BrewerEquipmentToggleShare', name='equipment-toggle-share'),
    url(r'^equipment/(?P<pk>\d+)/toggle-in-out/$', 'core.views.BrewerEquipmentToggleInOut', name='equipment-toggle-in-out'),
    # action views - browse (PUBLIC)
    url(r'^browse/$', BrowseListView.as_view(), name='browse'),
    url(r'^browse/(?P<pk>\d+)/$', BrowseDetailView.as_view(model=Commodity), name='browse-detail'),
    url(r'^browse/(?P<pk>\d+)/request$', 'core.views.RequestToolView', name='request-tool'),
    url(r'^browse/(?P<tool_pk>\d+)/request/(?P<loan_pk>\d+)/cancel$', 'core.views.CancelRequestToolView', name='cancel-request-tool'),
    url(r'^brewers/', BrewerListView.as_view(), name='brewers'),
    # staff views
    url(r'^equipment/branch/add', BranchEquipmentAddView.as_view(extra_context={'extra_title': 'Add Branch Tool'}), name='add-branch-tool'),
    # action views - contributions (PROTECTED)
    # url(r'^contribute/$', OfferToolView.as_view(extra_context={'extra_title': 'Offer to Contribute Tool'}), name='contribute-tool'),
    # url(r'^contribute/pending/$', ProtectedListView.as_view(model=EquipmentOffer), name='browse-offers'),
    # url(r'^contribute/pending/(?P<pk>\d+)/$', ProtectedDetailView.as_view(model=EquipmentOffer), name='offer-detail'),
    # url(r'^contribute/pending/(?P<pk>\d+)/accept/$', AcceptToolView.as_view(extra_context={'extra_title': 'Add Pending Contribution'}), name='accept-offer'),
    # url(r'^contribute/pending/(?P<pk>\d+)/delete/$', ProtectedDeleteView.as_view(model=EquipmentOffer), name='delete-offer'),
    # staff views
)

# Add generic views for each model automagically
# These views may be overriden if they exist higher up in the urlpatterns
# Staff only
for model in get_models(get_app('core')):
    included = ['Equipment', 'Commodity']  # Any objects that should be included go here!
    if model.__name__ not in included:
        continue
    name = model.__name__
    lower = name.lower()
    list = "%s/$" % lower
    create = "%s/create/$" % lower
    detail = "%s/(?P<pk>\d+)/$" % lower
    update = "%s/(?P<pk>\d+)/update/$" % lower
    delete = "%s/(?P<pk>\d+)/delete/$" % lower
    urlpatterns += patterns('',
        url(r'^%s' % list, staff_member_required(ProtectedListView.as_view(model=model, extra_context={'extra_title': name + " List"})), name=lower + "_list"),
        url(r'^%s' % detail, staff_member_required(ProtectedDetailView.as_view(model=model, extra_context={'extra_title': name})), name=lower + "_detail"),
        url(r'^%s' % create, staff_member_required(ProtectedCreateView.as_view(model=model, extra_context={'extra_title': "Add " + name})), name=lower + "_create"),
        url(r'^%s' % update, staff_member_required(ProtectedUpdateView.as_view(model=model, extra_context={'extra_title': "Update " + name})), name=lower + "_update"),
        url(r'^%s' % delete, staff_member_required(ProtectedDeleteView.as_view(model=model, extra_context={'extra_title': "Delete " + name})), name=lower + "_delete"),
        )
