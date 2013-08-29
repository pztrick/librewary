# Create your views here.

### Activities
# Add Commodity (STAFF)

# Register User (or group as User)
# Contribute Tool

# Register Deposit (STAFF)
# Register Tool (STAFF)
# Remove Tool (STAFF)

# Request Tool
# Vouch For Rental
# Un-vouch For Rental

# Loan Tool (STAFF)
# Check In Tool (STAFF)
# -- Apply Late Fines (STAFF)

# Foreclose Rental (STAFF)
# -- Remove Tool (STAFF)
# -- Apply Replacement Fees (STAFF)

# Enter Beginning Bank Balance (STAFF)
# -- Deposit Cash To Bank (STAFF)
# -- Deposit Checks To Bank (STAFF)
# -- Adjusting Journal Entry (STAFF)
# -- -- //Useful for opening balances//

#from django.http import HttpResponse
from django.views.generic import View, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from core.models import *
from core.forms import *
from django.contrib.auth import authenticate, login
from django.conf import settings

# class RegisterView(CreateView):
#     model = Brewer
#     form_class = BrewerForm
#     template_name = 'register.html'

#     def get_success_url(self):
#         return settings.LOGIN_REDIRECT_URL

#     def form_valid(self, form):
#         # This function is called after form has been validated successfully

#         # I need to call the parent form_valid() function at the top as it invokes form.save()
#         # and it needs to save the user before I can attempt to login manually
#         ret = super(RegisterView, self).form_valid(form)

#         # Override #1 - Log the user in after registering them
#         user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
#         login(self.request, user)

#         return ret


class MixinView(View):
    """ 1) accepts keyword extra_context, 2) accepts keyword default_template, 3) disallows un-auth'd users """
    extra_context = dict()  # Users may optionally pass an additional context dictionary
    default_template = None  # Users may optional pass a default_template keyword

    def get_context_data(self, *args, **kwargs):
        # If an extra_context keyword argument is passed, we include that dictionary in template context
        context = super(MixinView, self).get_context_data(*args, **kwargs)
        for k, v in self.extra_context.items():
            context[k] = v
        return context

    def get_template_names(self, *args, **kwargs):
        templates = super(MixinView, self).get_template_names(*args, **kwargs)
        if self.default_template:
            templates.append(self.default_template)
        return templates

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MixinView, self).dispatch(*args, **kwargs)


def DashboardView(request):
    return HttpResponseRedirect(reverse('brewer-profile', kwargs={'pk': request.user.pk}))

# class OfferToolView(MixinView, CreateView):
#     model = EquipmentOffer
#     form_class = EquipmentOfferForm
#     template_name = 'core/_form.html'

#     def get_success_url(self):
#         return reverse('browse-offers')

#     def form_valid(self, form):
#         # Override #1 - Force the owner field to be request.user
#         form.instance.owner = self.request.user
#         return super(OfferToolView, self).form_valid(form)


# class AcceptToolView(MixinView, CreateView):
#     model = Equipment
#     form_class = AcceptEquipmentForm
#     template_name = 'core/equipmentoffer_accept_form.html'

#     def get_context_data(self, *args, **kwargs):
#         # add passed parameters to context
#         offer = EquipmentOffer.objects.get(pk=self.kwargs['pk'])
#         context = super(AcceptToolView, self).get_context_data(*args, **kwargs)
#         context['offer'] = offer
#         return context

#     def get_success_url(self):
#         return reverse('browse-offers')

#     def form_valid(self, form):
#         # Override #1 - Force the contributor field to be offer.owner
#         offer = EquipmentOffer.objects.get(pk=self.kwargs['pk'])
#         form.instance.contributor = offer.owner
#         # Override #2 - Delete the offer as we are converting it into a tool
#         offer.delete()
#         return super(AcceptToolView, self).form_valid(form)


class BrewerEquipmentAddView(MixinView, CreateView):
    model = Equipment
    form_class = BrewerEquipmentForm
    template_name = 'core/_form.html'

    def get_success_url(self):
        #reverse('brewer-equipment', kwargs={'pk': self.request.user.id})
        return reverse('brewer-equipment', kwargs={'pk': self.request.user.id})  # FIXME

    def form_valid(self, form):
        # Override #1 - Force the contributor field to be request.user
        form.instance.contributor = self.request.user
        form.instance.contributed = False

        return super(BrewerEquipmentAddView, self).form_valid(form)


class BranchEquipmentAddView(MixinView, CreateView):
    model = Equipment
    form_class = BrewerEquipmentForm
    template_name = 'core/_form.html'

    def get_success_url(self):
        return reverse('browse')

    def form_valid(self, form):
        # Override #1 - Force the contributor field to be pk=1 AKA admin/branch user
        form.instance.contributor = Brewer.objects.get(pk=1)
        form.instance.contributed = True

        return super(BranchEquipmentAddView, self).form_valid(form)


class ProtectedCreateView(MixinView, CreateView):
    default_template = 'core/_form.html'

    def get_success_url(self):
        return reverse(self.model.__name__.lower() + "_list")


class ProtectedDeleteView(MixinView, DeleteView):
    default_template = 'core/_confirm_delete.html'

    def get_success_url(self):
        return reverse(self.model.__name__.lower() + "_list")


class ProtectedListView(MixinView, ListView):
    default_template = 'core/_list.html'


class ProtectedDetailView(MixinView, DetailView):
    default_template = 'core/_detail.html'


class ProtectedUpdateView(MixinView, UpdateView):
    default_template = 'core/_form.html'

    def get_success_url(self):
        return super(ProtectedUpdateView, self)
        return reverse(self.model.__name__.lower() + "_list")


class BrowseDetailView(DetailView):
    template_name = 'browse_detail.html'


class BrowseListView(ListView):
    template_name = 'browse.html'
    model = Commodity

    def get_queryset(self):
        return Commodity.objects.all().order_by('name')


class BrewerListView(ListView):
    template_name = 'core/brewer_list.html'
    model = Brewer

    def get_queryset(self):
        return Brewer.objects.filter(is_staff=False)


class BrewerEquipmentListView(ProtectedListView):
    template_name = 'brewer_equipment_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BrewerEquipmentListView, self).get_context_data(*args, **kwargs)
        brewer = Brewer.objects.get(pk=self.kwargs['pk'])
        context['brewer'] = brewer
        return context

    def get_queryset(self):
        return Equipment.objects.filter(contributor=self.kwargs['pk']).order_by('commodity')

    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


def BrewerEquipmentToggleShare(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    if equipment.contributor == request.user:
        equipment.shared = not equipment.shared
        equipment.save()
        return HttpResponseRedirect(reverse('brewer-equipment', kwargs={'pk': request.user.id}))
    else:
        return HttpResponseForbidden()


def BrewerEquipmentToggleInOut(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    if equipment.contributor == request.user:
        equipment.p2p_is_checked_out = not equipment.p2p_is_checked_out
        equipment.save()
        return HttpResponseRedirect(reverse('brewer-equipment', kwargs={'pk': request.user.id}))
    else:
        return HttpResponseForbidden()


def BrewerToggleEmail(request, pk):
    brewer = Brewer.objects.get(pk=pk)
    if brewer == request.user:
        brewer.show_email = not brewer.show_email
        brewer.save()
        return HttpResponseRedirect(reverse('brewer-profile', kwargs={'pk': request.user.id}))
    else:
        return HttpResponseForbidden()


def BrewerToggleFacebook(request, pk):
    brewer = Brewer.objects.get(pk=pk)
    if brewer == request.user:
        brewer.show_facebook = not brewer.show_facebook
        brewer.save()
        return HttpResponseRedirect(reverse('brewer-profile', kwargs={'pk': request.user.id}))
    else:
        return HttpResponseForbidden()


def RequestToolView(request, pk):
    commodity = Commodity.objects.get(pk=pk)
    loan = Loan()
    loan.commodity = commodity
    loan.borrower = request.user
    if Loan.objects.filter(borrower=request.user, commodity=commodity).count() == 0:
        # only save if it hasn't been requested yet, i.e. == 0
        loan.save()
    return HttpResponseRedirect(reverse('browse-detail', kwargs={'pk': pk}))


def CancelRequestToolView(request, tool_pk, loan_pk):
    loan = Loan.objects.get(pk=loan_pk)
    loan.delete()
    if loan.borrower == request.user:
        return HttpResponseRedirect(reverse('browse-detail', kwargs={'pk': tool_pk}))
    else:
        return HttpResponseForbidden()
