from django.shortcuts import render, get_object_or_404, render_to_response
from core.models import Candidate, CandidateMeanSentiment
from math import pi
from django.db.models import Min, Max
from datetime import timedelta, datetime, timezone
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import cumsum
from bokeh.models.widgets import Panel, Tabs

def index(request):
    color_list = []
    sentiment_list = []
    candidates_list = []
    candidates_sentiments_dict = {}
    candidates = Candidate.objects.all()
    candidate_accordian_list = []
    for candidate in candidates:
        min_from_date_time = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(Min('from_date_time'))
        max_to_date_time = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(Max('to_date_time'))

        total_mean_sentiment = CandidateMeanSentiment.objects.filter(
            candidate = candidate,
            from_date_time = min_from_date_time['from_date_time__min'],
            to_date_time = max_to_date_time['to_date_time__max'],
        )

        if total_mean_sentiment[0].mean_sentiment > 0.009 or total_mean_sentiment[0].mean_sentiment < -.009:
            candidates_sentiments_dict[str(candidate)] = [total_mean_sentiment[0].mean_sentiment]
            if candidate.party == 'democrat':
                candidates_sentiments_dict[str(candidate)].append('#415caa')
            elif candidate.party == 'republican':
                candidates_sentiments_dict[str(candidate)].append('#ed2024')
            else:
                candidates_sentiments_dict[str(candidate)].append('#696969')
        if total_mean_sentiment[0].mean_sentiment > .125:
            candidate_accordian_list.append(candidate)

    candidates_list = list(candidates_sentiments_dict.keys())
    sentiment_color_list = candidates_sentiments_dict.values()
    for sentiment_color in sentiment_color_list:
        sentiment_list.append(sentiment_color[0])
        color_list.append(sentiment_color[1])

    source = ColumnDataSource(data=dict(candidates_list=candidates_list, sentiment_list=sentiment_list, color=color_list))

    hover = HoverTool(
        tooltips = [
        ("candidate name", "@candidates_list"),
        ("sentiment value", "@sentiment_list{-0.000}"),
    ],
    mode = 'vline'
    ) 

    plot = figure(x_range=candidates_list, y_range=(-0.5, .5),
                  x_axis_label='Candidates', y_axis_label='Sentiment',
                  plot_height=600, plot_width=950, title="Average Sentiment Per Candidate for April 2019",
                  tools=[hover, 'wheel_zoom', 'reset'], sizing_mode="scale_both")
    plot.title.text_font_size = "21px"
    plot.xaxis.axis_label_text_font_size = "19px"
    plot.yaxis.axis_label_text_font_size = "19px"
    plot.vbar(x='candidates_list', top='sentiment_list', width=0.4, color='color', source=source)
    plot.xaxis.major_label_orientation = pi/4
    plot.xgrid.grid_line_color = None
    # plot.legend.orientation = "vertical"
    # plot.legend.location = "top_center"
    script, div = components(plot)
    context = {'script': script, 'div': div, 'candidates': candidates, 'candidate_accordian_list': candidate_accordian_list}
    return render_to_response('index.html', context=context)


def candidate_detail(request, slug):
    candidate = get_object_or_404(Candidate, slug=slug)
    candidates = Candidate.objects.all()
    agg_mean_sentiments = []
    agg_mean_sentiment_dates = []
    daily_mean_sentiments = []
    daily_mean_sentiment_dates = []
    min_from_date_time_dict = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(min_from_date_time = Min('from_date_time'))
    
    # minimum from_date_time in CandidateMeanSentiment for candidate in database
    min_from_time = min_from_date_time_dict['min_from_date_time']

    utcnow = datetime.utcnow()

    day_delta = utcnow.replace(tzinfo=timezone.utc) - min_from_time

    for day in range(day_delta.days):
        daily_sentiment = CandidateMeanSentiment.objects.filter(
            candidate = candidate,
            from_date_time = min_from_time + timedelta(days=day),
            to_date_time = min_from_time + timedelta(days=day+1)
        )
        if daily_sentiment: # we should also order by created_at time in addition to to_date_time
            daily_mean_sentiment_dates.append(daily_sentiment[0].to_date_time)
            daily_mean_sentiments.append(daily_sentiment[0].mean_sentiment)

    agg_candidate_mean_sentiments = CandidateMeanSentiment.objects.filter(
        candidate = candidate,
        from_date_time = min_from_time
    )
    print(daily_mean_sentiment_dates)
    print(daily_mean_sentiments)
    for mean_sentiment in agg_candidate_mean_sentiments:
        agg_mean_sentiment_dates.append(mean_sentiment.to_date_time)
        agg_mean_sentiments.append(mean_sentiment.mean_sentiment)
    print("agg sentiments: ", agg_mean_sentiments)
    print("agg Dates: ", agg_mean_sentiment_dates)

    detail_line_graph = figure(x_axis_label='Date of sentiment',
                            x_axis_type='datetime',
                            y_axis_label='Sentiment',
                            plot_width=700,
                            plot_height=350,
                            toolbar_location=None,
                            y_range=(-0.5, 0.5), 
                            sizing_mode="scale_both")

    detail_line_graph.line(agg_mean_sentiment_dates, 
                            agg_mean_sentiments,  
                            line_color='black', 
                            line_width=3, 
                            line_dash=[5,5],
                            alpha=.9,
                            legend="Aggregate")
    detail_line_graph.line(daily_mean_sentiment_dates, 
                            daily_mean_sentiments,  
                            line_color='blue', 
                            line_width=3, 
                            alpha=.5,
                            legend="Daily")

    # detail_line_graph.xaxis.major_label_orientation = pi/4
    tab1 = Panel(child=detail_line_graph, title="line")

    # latest_engagement_pie_chart = figure(plot_height=350, 
    #                         title="Number of Negative and Positive Activity Today", 
    #                         toolbar_location=None,
    #                         tools="hover",
    #                         tooltips=""
    #                         )
    # latest_engagement_pie_chart.wedge(x=0, y=1, radius=0.4, start_angle=cumsum(
    # tab2 = Panel(child=latest_engagement_pie_chart, title="pie")

    tabs = Tabs(tabs=[tab1])

    script, div = components(tabs)
    context = {'script': script, 'div': div, 'candidate': candidate, 'candidates': candidates}
    return render_to_response('candidate_detail.html', context=context)

def methodology(request):
    candidates = Candidate.objects.all()
                  
    return render(request, "methodology.html", context={'candidates': candidates})


def about(request):
    candidates = Candidate.objects.all()

    return render(request, "about.html", context={'candidates': candidates})
