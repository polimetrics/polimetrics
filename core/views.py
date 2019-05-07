from django.shortcuts import render, get_object_or_404, render_to_response
from core.models import Candidate, CandidateMeanSentiment
from math import pi
from django.db.models import Min, Max
from datetime import timedelta, datetime, timezone
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.models.widgets import Panel, Tabs
from bokeh.transform import factor_cmap

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

    index_bar_graph = figure(x_range=candidates_list, 
                            y_range=(-0.5, .5),
                            x_axis_label='Candidates', 
                            y_axis_label='Sentiment',
                            plot_height=600, 
                            plot_width=950,
                            title="Average Sentiment Per Candidate for April 2019",
                            tools=[hover, 'wheel_zoom', 'reset'],
                            sizing_mode="scale_both")
    index_bar_graph.title.text_font_size = "21px"
    index_bar_graph.xaxis.axis_label_text_font_size = "19px"
    index_bar_graph.yaxis.axis_label_text_font_size = "19px"
    index_bar_graph.vbar(x='candidates_list', top='sentiment_list', width=0.4, color='color', source=source)
    index_bar_graph.xaxis.major_label_orientation = pi/4
    index_bar_graph.xgrid.grid_line_color = None
    # index_bar_graph.legend.orientation = "vertical"
    # index_bar_graph.legend.location = "top_center"
    script, div = components(index_bar_graph)
    context = {'script': script, 'div': div, 'candidates': candidates, 'candidate_accordian_list': candidate_accordian_list}
    return render_to_response('index.html', context=context)


def candidate_detail(request, slug):
    candidate = get_object_or_404(Candidate, slug=slug)
    candidates = Candidate.objects.all()
    agg_mean_sentiments = []
    agg_mean_sentiment_dates = []
    daily_mean_sentiment_objs = []
    min_from_date_time_dict = CandidateMeanSentiment.objects.filter(
        candidate = candidate).aggregate(min_from_date_time = Min('from_date_time'))

    # minimum from_date_time in CandidateMeanSentiment for candidate in database
    min_from_time = min_from_date_time_dict['min_from_date_time']

    utcnow = datetime.utcnow()

    day_delta = utcnow.replace(tzinfo=timezone.utc) - min_from_time

    for day in range(day_delta.days + 1): # add 1 to account for the current day
        daily_sentiment = CandidateMeanSentiment.objects.filter(
            candidate = candidate,
            from_date_time = min_from_time + timedelta(days=day),
            to_date_time = min_from_time + timedelta(days=day+1))
        # records ordered by to_date_time asc and created_at desc
        if daily_sentiment: 
            daily_mean_sentiment_objs.append(daily_sentiment[0])
    
    date_list = [obj.to_date_time for obj in daily_mean_sentiment_objs]
    sentiment_list = [obj.mean_sentiment for obj in daily_mean_sentiment_objs]

    agg_candidate_mean_sentiments = CandidateMeanSentiment.objects.filter(
        candidate = candidate,
        from_date_time = min_from_time)

    agg_data = {}

    for sent_obj in agg_candidate_mean_sentiments:
        key = sent_obj.to_date_time
        if key not in agg_data:
            # initialize empty list
            agg_data[key] = []
        agg_data[key].append(sent_obj.mean_sentiment)
        print(sent_obj.pk, sent_obj.to_date_time, sent_obj.created_at, sent_obj.mean_sentiment)
    
    for date_time, mean_sent_list in agg_data.items():
        agg_mean_sentiment_dates.append(date_time)
        agg_mean_sentiments.append(mean_sent_list[0])
    

    # hover = HoverTool(
    #     tooltips = [
    #         ('date', '@date_list'),
    #         ('daily sentiment', '@sentiment_list')
    #     ],
    #     mode = 'vline'
    # )

    detail_line_graph = figure(x_axis_label='Date of sentiment',
                            x_axis_type='datetime',
                            y_axis_label='Sentiment',
                            plot_width=800,
                            plot_height=400,
                            tools=['wheel_zoom', 'reset'],
                            y_range=(-0.5, 0.5), 
                            sizing_mode="scale_both"
                            )

    detail_line_graph.line(date_list, 
                            sentiment_list,  
                            line_color='blue', 
                            line_width=3, 
                            alpha=.5,
                            legend="Daily")

    detail_line_graph.line(agg_mean_sentiment_dates, 
                            agg_mean_sentiments,  
                            line_color='black', 
                            line_width=3, 
                            line_dash=[5,5],
                            alpha=.9,
                            legend="Aggregate")


    # detail_line_graph.xaxis.major_label_orientation = pi/4
    # daily_mean_sentiment_objs - the last element is the latest
    today_pos_engagement = daily_mean_sentiment_objs[-1].positive_engagement
    today_neg_engagement = daily_mean_sentiment_objs[-1].negative_engagement
    today_engagement = daily_mean_sentiment_objs[-1].total_engagement

    today_pos_percent = (today_pos_engagement / today_engagement)*100
    today_neg_percent = (today_neg_engagement / today_engagement)*100
    
    max_pos_engagement = agg_candidate_mean_sentiments.last().positive_engagement
    max_neg_engagement = agg_candidate_mean_sentiments.last().negative_engagement
    total_engagement = agg_candidate_mean_sentiments.last().total_engagement

    max_pos_percent = (max_pos_engagement / total_engagement)*100
    max_neg_percent = (max_neg_engagement / total_engagement)*100

    time_spans = ['daily', 'overall']
    engagement_splits = ["Postive Percent", "Negative Percent"]

    data = {
        'daily/overall': time_spans,
        'Positive Percent': [today_pos_percent, max_pos_percent],
        'Negative Percent': [today_neg_percent, max_neg_percent]
    }

    palette = ['#41b6c4', '#FD9F6C']

    # this creates [ ("daily", "Positive Percent"), ("daily", "Negative Percent"), ("overall", "Positive Percent"), ("overall", "Negative Percent") ]
    x = [ (time_span, engagement_split) for time_span in time_spans for engagement_split in engagement_splits ]
    counts = sum(zip(data['Positive Percent'], data['Negative Percent']), ()) # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    # hover = HoverTool(
    #     tooltips = [
    #         (),
    #         (),
    #     ],
    #     mode = 'vline'
    # ) 

    detail_engagement_bar_graph = figure(x_range=FactorRange(*x), 
                            plot_height=400,
                            plot_width=800, 
                            title="Daily/Overall Engagement Percentages",
                            sizing_mode="scale_both",
                            tools=['wheel_zoom', 'reset'])
            
    detail_engagement_bar_graph.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
                            fill_color=factor_cmap('x', palette=palette, factors=engagement_splits, start=1, end=2))
    
    detail_engagement_bar_graph.y_range.start = 0
    detail_engagement_bar_graph.x_range.range_padding = 0.1
    detail_engagement_bar_graph.xaxis.major_label_orientation = 1
    detail_engagement_bar_graph.xgrid.grid_line_color = None

    tab1 = Panel(child=detail_line_graph, title="line")

    tab2 = Panel(child=detail_engagement_bar_graph, title="bar")

    tabs = Tabs(tabs=[tab1, tab2])

    script, div = components(tabs)
    context = {'script': script, 'div': div, 'candidate': candidate, 'candidates': candidates}
    return render_to_response('candidate_detail.html', context=context)

def methodology(request):
    candidates = Candidate.objects.all()
                  
    return render(request, "methodology.html", context={'candidates': candidates})


def about(request):
    candidates = Candidate.objects.all()

    return render(request, "about.html", context={'candidates': candidates})
