from django.shortcuts import render, get_object_or_404, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from core.models import Candidate, Tweet, CandidateMeanSentiment
from math import pi

# Create your views here.


def index(request):
    tweet_query_set = Tweet.objects.all()
    tweet_date_list = []
    tweet_polarity_list = []

    for tweet in tweet_query_set:
        if tweet.polarity != 0:
            tweet_polarity_list.append(tweet.polarity)
            tweet_date_list.append(tweet.created_at)

    data = {'date': tweet_date_list, 'polarity': tweet_polarity_list}
    title = 'y = f(x)'
    source = ColumnDataSource(data)
    plot = figure(title=title,
                  x_axis_label='Date of Tweet',
                  x_axis_type="datetime",
                  y_axis_label='Polarity',
                  plot_width=1000,
                  plot_height=500)
    plot.circle('date', 'polarity', source=source)

    plot.xaxis.major_label_orientation = pi/4

    # plot.circle(tweet_polarity_list, tweet_polarity_list, legend='f(x)',
    #             size=5, color='blue', alpha=0.9)
    script, div = components(plot)

    candidates = Candidate.objects.all()
    return render_to_response('index.html',
                              {'script': script, 'div': div, 'candidates': candidates})



def candidates(request):
    candidates = Candidate.objects.all()

    return render(request, "candidates.html", context={'candidates': candidates})


def candidate_detail(request, slug):
    candidate = get_object_or_404(Candidate, slug=slug)
    # candidate = Candidate.objects.get(Candidate, id=id)

    candidate_mean_sentiment = CandidateMeanSentiment.objects.all()
    candidate_mean_sentiment_data = []
    candidate_mean_sentiment_date = []

    for tweet in candidate_mean_sentiment:
        if tweet.mean_sentiment != 0 and candidate.last_name == tweet.candidate.last_name:
            candidate_mean_sentiment_data.append(
                tweet.mean_sentiment)
            candidate_mean_sentiment_date.append(
                tweet.to_date_time)

    data = {'date': candidate_mean_sentiment_date,
            'sentiment': candidate_mean_sentiment_data}
    source = ColumnDataSource(data)
    plot = figure(x_axis_label='Date of Tweet',
                  x_axis_type='datetime',
                  y_axis_label='Sentiment',
                  plot_width=1000,
                  plot_height=500)
    plot.line('date', 'sentiment', source=source, line_width=2)
    plot.xaxis.major_label_orientation = pi/4
    script, div = components(plot)
    context = {'script': script, 'div': div, 'candidate': candidate}
    return render_to_response('candidate_detail.html', context=context)
    # tweet_query_set = Tweet.objects.all()
    # tweet_date_list = []
    # tweet_polarity_list = []

    # for tweet in tweet_query_set:
    #     if tweet.polarity != 0 and tweet.candidate.last_name == candidate.last_name:
    #         tweet_polarity_list.append(tweet.polarity)
    #         tweet_date_list.append(tweet.created_at)

    #     data = {'date': tweet_date_list, 'polarity': tweet_polarity_list}
    #     title = 'y = f(x)'
    #     source = ColumnDataSource(data)
    #     plot = figure(title=title,
    #                   x_axis_label='Date of Tweet',
    #                   x_axis_type="datetime",
    #                   y_axis_label='Polarity',
    #                   plot_width=1000,
    #                   plot_height=500)
    #     plot.circle('date', 'polarity', source=source)

    #     plot.xaxis.major_label_orientation = pi/4
    #     plot.circle(tweet_polarity_list, tweet_polarity_list, legend='f(x)',
    #                 size=5, color='blue', alpha=0.9)
    #     script, div = components(plot)
    #     context = {'script': script, 'div': div, 'candidate': candidate}
    #     return render_to_response('candidate_detail.html', context=context)

def methodology(request):
    return render(request, "methodology.html")

def about(request):
    return render(request, "about.html")
