from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from .models import CreatorProfile, SocialPlatform, Quote
from .forms import SocialPlatformForm, QuoteForm
from managers.models import Campaign


class CreatorSignupView(SignupView):
    template_name = 'account/creators_signup.html'
    form_class = SignupForm
    group = Group.objects.get(id=2)

    def form_valid(self, form):
        response = super(CreatorSignupView, self).form_valid(form)
        user = self.user
        self.group.user_set.add(user)
        CreatorProfile.objects.create(user=user)
        return response


class CreatorUpdateView(UpdateView):
    template_name = 'creators/creator_form.html'
    model = CreatorProfile
    fields = ['bio', 'niches', 'audience_demographic']
    success_url = "/"


def platform_create(request):
    if request.method == 'POST':
        form = SocialPlatformForm(request.POST)
        if form.is_valid():
            platform = form.save(commit=False)
            platform.creator = request.user.creatorprofile
            platform.save()
            messages.success(request, 'Your social profile has been added')
    else:
        form = SocialPlatformForm()
    return render(request, 'creators/creator_form.html', {'form': form})


class PlatformUpdateView(UpdateView):
    template_name = 'creators/creator_form.html'
    model = SocialPlatform
    fields = ['account_name', 'url', 'metrics']
    success_url = reverse_lazy('index')


class PlatformDeleteView(DeleteView):
    template_name = 'creators/creator_confirm_delete.html'
    model = SocialPlatform
    success_url = reverse_lazy('index')


def quote_create(request, pk):
    campaign = Campaign.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.creator = request.user.creatorprofile
            quote.campaign = campaign
            quote.save()
            messages.success(request, 'Your quote has been submitted')
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'creators/creator_form.html', {'form': form})


class QuoteUpdateView(UpdateView):
    model = Quote
    fields = ['offering', 'price']


class QuoteDeleteView(DeleteView):
    model = Quote
    success_url = reverse_lazy('index')
