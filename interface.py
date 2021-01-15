import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import projet
import datetime as dt
import urllib.request
import xmltodict   
import praw
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H2("Analyse de corpus Arxiv et Reddit"),
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Arxiv',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Reddit',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
], className="banner")


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        corpus = projet.Corpus("chess")
        url = 'http://export.arxiv.org/api/query?search_query=all:chess&start=0&max_results=50'
        data =  urllib.request.urlopen(url).read().decode()
        docs = xmltodict.parse(data)['feed']['entry']
        coauthor = []
        for i in docs:
            datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
            try:
                author = [aut['name'] for aut in i['author']][0]
            except:
                author = i['author']['name']
            if len(i['author']) != 0:
                for y in range(1,len(i['author'])):
                     try:
                         coauthor.append([aut['name'] for aut in i['author']][y])
                     except: pass
            txt = i['title']+ ". " + i['summary']
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            doc = projet.ArxivDocument(datet,
                           i['title'],
                           author,
                           txt,
                           i['id'],
                           coauthor)
            corpus.add_doc(doc)
        
        voc_arxiv = corpus.stat()    
        
        voc = voc_arxiv.sort_values(by=[1], ascending=False)
        hist_arxiv = voc.head(6)
        
        long_df = hist_arxiv
        long_df['name'] = long_df[0]
        long_df['count'] = long_df[1]
        fig = px.bar(long_df, x = "name", y="count")
        return html.Div(
               dcc.Graph(
        id='example-graph',
        figure=fig
    ) )
        
    elif tab == 'tab-2':
        corpus2 = projet.Corpus("chess")
        reddit = praw.Reddit(client_id='4h9QntGTMSiK-w', client_secret='BsZTgGuRBvkOvAI4HT2iBXaa-ipD6A', user_agent='bst')
        hot_posts = reddit.subreddit('chess').hot(limit=50)
        for post in hot_posts:
            datet = dt.datetime.fromtimestamp(post.created)
            txt = post.title + ". "+ post.selftext
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            doc = projet.RedditDocument(datet,
                           post.title,
                           post.author_fullname,
                           txt,
                           post.url,
                           post.num_comments)
            corpus2.add_doc(doc)
        voc_reddit = corpus2.stat() 
        voc2 = voc_reddit.sort_values(by=[1], ascending=False)
        hist_reddit = voc2.head(6)
        import plotly.express as px
        
        long_df2 = hist_reddit
        long_df2['name'] = long_df2[0]
        long_df2['count'] = long_df2[1]
        fig2 = px.bar(long_df2, x = "name", y="count")
        return html.Div(
            dcc.Graph(
        id='graph2',
        figure=fig2
    ) )

       
        

     
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    
    