from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from .models import CreatorProfile, SocialPlatform, Quote
from .forms import SocialPlatformForm, QuoteForm
from managers.models import Campaign


class CreatorSignupView(SignupView):
    template_name = 'account/creators_signup.html'
    form_class = SignupForm
    group = Group.objects.get(id=4)

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


def get_data(request, user):
    usar = CreatorProfile.objects.get(user)
    try:
		# make requests
	    user_request = requests.get("https://www.instagram.com/{}/".format(user.lower()))
	    user_soup = BeautifulSoup(user_request.text, 'html.parser')

		# case for incorrect username
	    if len(user_soup.findAll('div', attrs={'class':'error-container'})) > 0:
			# flash("Error loading profile: user does not exist")
		    return redirect('index')

	    all_data = {}

		# find json in page
	    for src in user_soup.findAll('script'):
		    if "window._sharedData" in src.text: 
			    raw_json_src = src.text.replace("window._sharedData = ", "")[:-1]

				# load as json object
			    json_src = json.loads(raw_json_src)

			    raw_user_data = json_src['entry_data']['ProfilePage'][0]['graphql']['user']

				# case for private user
			    if raw_user_data['is_private']:
					# flash("Error loading profile: user is private")
			    	return redirect('index')

				# catch if data is missing
			    try:
				    user_data = {
						"username" : raw_user_data['username'],
						"followed_by" : raw_user_data['edge_followed_by']['count'],
						"following" : raw_user_data['edge_follow']['count'],
						"profile_picture" : raw_user_data['profile_pic_url']
					}

			    except KeyError:
			    	flash("Error loading profile.")
			    	return redirect(url_for("home"))

				# weekdays list
			    weekdays_count = []

			    for wd in list(calendar.day_abbr):
				    weekdays_count.append([wd, 0])

				# re-arrange for media counts
			    weekdays_count.insert(0, weekdays_count[-1])
			    weekdays_count.pop()

				# hours list
			    hours_count = []

			    for hr in range(0, 24):
				    hours_count.append([str(hr), 0])

				# collect all media
			    media_arr = []

				# max 12 media
			    for med in raw_user_data['edge_owner_to_timeline_media']['edges']:
				    media_dict = {
						"likes" : med['node']['edge_liked_by']['count'],
						"video" : med['node']['is_video'],
						"comments" : med['node']['edge_media_to_comment']['count'],
						"date" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%y/%m/%d'),
						"weekday" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%w'),
						"hour" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%-H')
					}

				    media_arr.append(media_dict)

				    weekdays_count[int(media_dict['weekday'])][1] += 1
				    hours_count[int(media_dict['hour'])][1] += 1




				# zero pad hours
			    for x in range(0, len(hours_count)):
				    hours_count[x][0] = str(hours_count[x][0]).zfill(2)


				# make new data structure
			    all_data['user_info'] = user_data
			    all_data['media_info'] = media_arr
			    all_data['weekdays_count'] = weekdays_count
			    all_data['hours_count'] = hours_count

			    break

	    return render_template('chart.html', all_data=all_data)

    except Exception as e:
	    print(e)
		# flash("Something went wrong!")
	    return redirect("index")