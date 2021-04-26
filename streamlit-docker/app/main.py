import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from src.utils import add_custom_css
from src.pages import PAGE_MAP
from src.state import provide_state

add_custom_css()

st.title('Segmenting Country Information')

st.set_option('deprecation.showPyplotGlobalUse', False)


@provide_state()
def main(state=None):
    current_page = st.sidebar.radio("Go To", list(PAGE_MAP))
    PAGE_MAP[current_page](state=state).write()


@st.cache
def load_data():
    data = pd.read_csv('./data/euro_cluster.csv')
    data['Country'] = data['a_id_'].str.split('_')[0]
    return(data)


load_data = st.sidebar.radio('Load Data', ('Country Data', 'European Data'))

if load_data == 'Country Data':

    data = pd.read_csv('./data/country_cluster.csv')

else:

    data = pd.read_csv('./data/euro_cluster.csv')


@st.cache
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text(encoding="utf8")


dict_check = st.sidebar.checkbox("Assignment")
dict_markdown = read_markdown_file("assignment.md")

if dict_check:
    st.markdown(dict_markdown, unsafe_allow_html=True)


@ st.cache
def get_clusters(data):
    cluster = list(data['ClusterID'].unique())
    return(cluster)


@ st.cache
def show_cluster(data, clusterID):
    places = data[data['ClusterID'] == clusterID]['a_id_'].reset_index()
    return(places)


def hist_show(data):
    numbers = data.groupby(['ClusterID']).size()
    st.bar_chart(numbers)


tab_check = st.sidebar.checkbox("Raw Table")
if tab_check:
    st.subheader('Raw data')
    st.write(data)


cluster = get_clusters(data)
cluster = map(int, cluster)
clusterID = st.sidebar.slider('cluster', 0, max(cluster), 0)
places = show_cluster(data, clusterID)

clust_check = st.sidebar.checkbox("Show Clusters")
if clust_check:

    st.subheader('Show Clustered Areas')
    st.write(places)

    chart = st.sidebar.radio(
        'Country Cluster', ('Show graph', 'Show Pie char'))
    if chart == 'Show graph':
        hist_show(data)


def get_countries(data):
    countr = data['a_id_'].str.split('_', expand=True)[0].unique()
    return(countr)


def compare_country(data, value):
    datacountry = data[data['a_id_'].str.contains(value)]
    # datacountry.set_index('a_id_', inplace=True)
    # datacountry = datacountry.iloc[:, 3:].T
    return(datacountry)


countr = get_countries(data)
value = st.sidebar.selectbox("Hello", countr)
st.write(value)


chart_data = compare_country(data, value)
st.line_chart(chart_data.iloc[:, 3:].T)
st.write(chart_data['a_id_'])


if __name__ == "__main__":
    main()
