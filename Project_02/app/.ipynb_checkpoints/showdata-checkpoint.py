import pandas as pd
from plotly.graph_objs import Bar, Pie
from sqlalchemy import create_engine

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', engine)

def return_figures():
    """Creates two plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the two plotly visualizations

    """
    # Creates a pie chart of the source of training data
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    data_one=[Pie(labels=genre_names, values=genre_counts)]
    layout_one = dict(title = 'Source of Training Data (Genre)')

    # Creates a bar chart of the distribution of categories
    cat_df = df.drop(['id', 'message', 'original', 'genre'], axis=1)
    cat_names = list(cat_df.columns.values)
    cat_counts = cat_df.sum()

    data_two = [Bar(x=cat_names, y=cat_counts)]
    layout_two = dict(title = 'Distribution of Categories in Training Data',
                  xaxis = dict(title = 'Categories'),
                  yaxis = dict(title = 'Count'))

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=data_one, layout=layout_one))
    figures.append(dict(data=data_two, layout=layout_two))

    return figures
