from django.shortcuts import render, get_object_or_404, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from core.models import Candidate, Tweet, CandidateMeanSentiment
from math import pi
from django.db.models import Min, Max
from datetime import timezone

def index(request):
    sentiment_list = []
    candidates_list = []
    # candidates = Candidate.objects.all()
    # for candidate in candidates:
        # # candidate_from_date_times = CandidateMeanSentiment.objects.values_list('from_date_time')
        # # candidate_from_date_times = CandidateMeanSentiment.objects.datetimes('from_date_time', 'second')
        # mean_sentiment_min_from = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(Min('from_date_time'))
        # mean_sentiment_max_to = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(Max('to_date_time'))
        # print(candidate.id)
        # # print(mean_sentiment_min_from)

        # print(mean_sentiment_min_from, mean_sentiment_min_from['from_date_time__min'])
        # print(mean_sentiment_max_to, mean_sentiment_max_to['to_date_time__max'])
        
        # total_mean_sentiment = CandidateMeanSentiment.objects.filter(
        #     candidate = candidate,
        #     from_date_time = mean_sentiment_min_from['from_date_time__min'],
        #     to_date_time = mean_sentiment_max_to['to_date_time__max'],
        # )
        # print(total_mean_sentiment)
        # breakpoint()





    candidates_mean_sentiments = CandidateMeanSentiment.objects.all()
    candidates = Candidate.objects.all()
    # print(candidates_mean_sentiments)
    c_count = []
    n = 0
    for candidate in candidates_mean_sentiments:
        # print(candidate)
        # breakpoint()
        if candidate.mean_sentiment != 0:
            # sentiment_list.append(candidate.mean_sentiment)
            # candidate.first_name + candidate.last_name)
            if str(candidate.candidate) not in candidates_list:
                candidates_list.append(str(
                    candidate.candidate))
                sentiment_list.append(candidate.mean_sentiment)
                c_count.append(n)
                n += 1
            else:
                continue
        else:
            continue
    # data = {'Candidates': candidates_list,
    #         'Sentiment': sentiment_list}

    # source = ColumnDataSource(data)
    plot = figure(x_range=candidates_list, y_range=(-0.5, .5),
                  x_axis_label='Candidates', y_axis_label='Sentiment',
                  plot_height=500, plot_width=800, title="Mean Sentiment Per Candidate", tools="")
    # breakpoint()
    # print(candidates_list)
    plot.line([])
    plot.vbar(x=candidates_list, top=sentiment_list, width=0.4)
    plot.xaxis.major_label_orientation = pi/4
    plot.xgrid.grid_line_color = None
    # plot.y_range.start = -1
    script, div = components(plot)
    context = {'script': script, 'div': div, 'candidate': candidates}
    return render_to_response('index.html', context=context)


def candidates(request):
    candidates = Candidate.objects.all()

    return render(request, "candidates.html",
                  context={'candidates': candidates})


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
    plot = figure(x_axis_label='Date of sentiment',
                  x_axis_type='datetime',
                  y_axis_label='Sentiment',
                  plot_width=1000,
                  plot_height=500,
                  toolbar_lacation=None,
                  y_range=(-0.5, 0.5))
    plot.line('date', 'sentiment', source=source, line_width=4)
    plot.xaxis.major_label_orientation = pi/4
    # plot.y_range.start = -1
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
