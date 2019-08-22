from django.shortcuts import render, get_object_or_404, render_to_response
from core.models import Candidate, CandidateMeanSentiment, Tweet
from math import pi
from django.db.models import Min, Max
from datetime import timedelta, datetime, timezone
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.models.widgets import Panel, Tabs
from bokeh.transform import factor_cmap
from bokeh.models import NumeralTickFormatter

def index(request):
    color_list = []
    sentiment_list = []
    candidates_list = []
    candidates_sentiments_dict = {}
    candidates = Candidate.objects.all()
    candidate_accordian_list = []
    for candidate in candidates:
        tweet_from_dt = Tweet.objects.filter(candidate = candidate).aggregate(Min('created_at'))
        from_dt = datetime(tweet_from_dt['created_at__min'].year, tweet_from_dt['created_at__min'].month, tweet_from_dt['created_at__min'].day, tzinfo=timezone.utc)
        max_to_date_time = CandidateMeanSentiment.objects.filter(candidate = candidate).aggregate(Max('to_date_time'))
        total_mean_sentiment = CandidateMeanSentiment.objects.filter(
            candidate = candidate,
            from_date_time = from_dt,
            to_date_time = max_to_date_time['to_date_time__max'],
        )
        if total_mean_sentiment:
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
                            y_range=(-0.35, .35),
                            x_axis_label='Candidates', 
                            y_axis_label='Sentiment',
                            plot_height=600, 
                            title="Average Sentiment Per Candidate",
                            tools=[hover],
                            toolbar_location=None,
                            sizing_mode="stretch_both"
                            )
    index_bar_graph.title.text_font_size = "1.18rem"
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
    print(min_from_time)
    if min_from_time:
        utcnow = datetime.utcnow()

        day_delta = utcnow.replace(tzinfo=timezone.utc) - min_from_time

        for day in range(day_delta.days + 1): # add 1 to account for the current day
            daily_sentiment = CandidateMeanSentiment.objects.filter(
                candidate = candidate,
                from_date_time = min_from_time + timedelta(days=day),
                to_date_time = min_from_time + timedelta(days=day+1)).order_by('-created_at')
            # records ordered by to_date_time asc and created_at desc
            if daily_sentiment: 
                daily_mean_sentiment_objs.append(daily_sentiment[0])
        
        date_list = [obj.to_date_time for obj in daily_mean_sentiment_objs]
        sentiment_list = [obj.mean_sentiment for obj in daily_mean_sentiment_objs]

        agg_candidate_mean_sentiments = CandidateMeanSentiment.objects.filter(
            candidate = candidate,
            from_date_time = min_from_time).order_by('to_date_time', 'created_at')

        agg_data = {}
        agg_list = []
        for sent_obj in agg_candidate_mean_sentiments:
            agg_list.append(sent_obj)
            key = sent_obj.to_date_time
            if key not in agg_data:
                # initialize empty list
                agg_data[key] = []
            agg_data[key].append(sent_obj.mean_sentiment)
        
        for date_time, mean_sent_list in agg_data.items():
            agg_mean_sentiment_dates.append(date_time)
            agg_mean_sentiments.append(mean_sent_list[0])

        detail_line_graph = figure(x_axis_label='Date of sentiment',
                                x_axis_type='datetime',
                                y_axis_label='Sentiment',
                                plot_width=800,
                                plot_height=500,
                                toolbar_location=None,
                                tools=['wheel_zoom', 'reset'],
                                y_range=(-0.55, 0.55), 
                                sizing_mode="stretch_both"
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

        # daily_mean_sentiment_objs - the last element is the latest
        today_pos_engagement = daily_mean_sentiment_objs[-1].positive_engagement
        today_neg_engagement = daily_mean_sentiment_objs[-1].negative_engagement
        today_engagement = daily_mean_sentiment_objs[-1].total_engagement

        today_pos_percent = (today_pos_engagement / today_engagement)
        today_neg_percent = (today_neg_engagement / today_engagement)

        overall_obj = agg_list[-1]

        overall_pos_engagement = overall_obj.positive_engagement
        overall_neg_engagement = overall_obj.negative_engagement
        total_engagement = overall_obj.total_engagement

        overall_pos_percent = (overall_pos_engagement / total_engagement)
        overall_neg_percent = (overall_neg_engagement / total_engagement)

        time_spans = ['TODAY', 'OVERALL']
        engagement_splits = ["POSITIVE Tweets", "NEGATIVE Tweets"]

        data = {
            'daily/overall': time_spans,
            'Positive': [today_pos_percent, overall_pos_percent],
            'Negative': [today_neg_percent, overall_neg_percent]
        }

        palette = ['#b3d9ff', '#00264d']

        # this creates [ ("daily", "Positive Percent"), ("daily", "Negative Percent"), ("overall", "Positive Percent"), ("overall", "Negative Percent") ]
        x = [ (time_span, engagement_split) for time_span in time_spans for engagement_split in engagement_splits ]
        counts = sum(zip(data['Positive'], data['Negative']), ())
        print(counts)
        engage = [today_pos_engagement, today_neg_engagement, overall_pos_engagement, overall_neg_engagement]

        source = ColumnDataSource(data=dict(x=x, counts=counts, engage=engage))

        hover = HoverTool(
            tooltips = [
                ("Number of Retweets/Likes", "@engage"),
                ("POS-NEG Percent Split", "@counts{0%}")
            ],
            mode = 'vline'
        ) 

        detail_engagement_bar_graph = figure(x_range=FactorRange(*x), 
                                plot_height=500,
                                plot_width=800, 
                                title="Nagative and Positive Engagement (Engagemenet = Retweets + Likes)",
                                sizing_mode="stretch_both",
                                toolbar_location=None,
                                y_range=(0,1),
                                tools=[hover])
                
        detail_engagement_bar_graph.vbar(x='x', top='counts', width=0.9, source=source, line_color="white", alpha=0.7,
                                fill_color=factor_cmap('x', palette=palette, factors=engagement_splits, start=1, end=2)
                                )

        detail_engagement_bar_graph.x_range.range_padding = 0.1
        detail_engagement_bar_graph.xaxis.major_label_orientation = 'horizontal'

        detail_engagement_bar_graph.xgrid.grid_line_color = None
        detail_engagement_bar_graph.yaxis[0].formatter = NumeralTickFormatter(format="0%")

        tab1 = Panel(child=detail_line_graph, title="---Twitter Sentiment Trends---")
        tab2 = Panel(child=detail_engagement_bar_graph, title="---Twitter Engagement Metrics---")
        tabs = Tabs(tabs=[tab1, tab2])
        script, div = components(tabs)
        context = {'script': script, 'div': div, 'candidate': candidate, 'candidates': candidates}
        return render_to_response('candidate_detail.html', context=context)
    
    return render_to_response('candidate_detail.html')

def methodology(request):
    candidates = Candidate.objects.all()
                  
    return render(request, "methodology.html", context={'candidates': candidates})

def about(request):
    candidates = Candidate.objects.all()

    return render(request, "about.html", context={'candidates': candidates})
