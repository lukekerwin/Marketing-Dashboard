import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

from classes.insights import Insights
from classes.sdn import sdn

import pandas as pd

st.set_page_config(page_title="Marketing Dashboard", page_icon=":bar_chart:", layout="wide")

# Title
st.title(":orange[SDN] Marketing Dashboard :bar_chart:")


# Session State
if 'page' not in st.session_state:
    st.session_state.page = 'Insights'

# Tabs
page1, page2, page3, page4, page5 = st.columns(5)

if page1.button('Insights', key='insights'):
    st.session_state.page = 'Insights'


if st.session_state.page == 'Insights':

    st.header("Insights")

    # # Checkboxes
    # parlays = st.checkbox('Aggregate Parlays', value=True)

    # Date Range
    start_date, end_date, odds, line, unit, result = st.columns(6)
    with start_date:
        start = st.date_input('Start Date')
    with end_date:
        end = st.date_input('End Date')

    # Row 1
    league, bet_type, subtype, prop, length, sportsbook = st.columns(6)

    with league:
        league_filter = st.multiselect('League', sdn.filter_format(sdn.leagues, type='league'))
    with bet_type:
        bet_type_filter = st.multiselect('Bet Type', sdn.filter_format(sdn.bet_types))
    with subtype:
        subtype_filter = st.multiselect('Subtype', sdn.filter_format(sdn.subtypes))
    with prop:
        prop_filter = st.multiselect('Prop', sdn.filter_format(sdn.props))
    with length:
        length_filter = st.multiselect('Length', sdn.filter_format(sdn.lengths))
    with sportsbook:
        sportsbook_filter = st.multiselect('Sportsbook', sdn.filter_format(sdn.sportsbooks))
    with odds:
        # range slider
        odds_filter = st.slider('Odds', -10000, 10000, (-10000, 10000))
    with line:
        # range slider
        line_filter = st.slider('Line', 0, 300, (0, 300))
    with unit:
        # range slider
        unit_filter = st.slider('Unit', 0, 200, (0, 200))
    with result:
        result_filter = st.multiselect('Result', ['H','M','P'])
    
    # Table
    if start_date and end_date:
        bets = sdn.get_bets(start_date=start, end_date=end)

        # if parlays:
        #     bets = sdn.aggregate_parlays(bets)

        bets = [bet for bet in bets if bet['parlay_id'] == None]
        
        # Filter
        if league_filter:
            bets = [bet for bet in bets if bet['league_id'] in [item['id'] for item in sdn.leagues if item['abbreviation'].upper()+' - '+item['name'] in league_filter]]
        if bet_type_filter:
            bets = [bet for bet in bets if bet['bet_type']['name'] in bet_type_filter]
        if subtype_filter:
            bets = [bet for bet in bets if bet['bet_subtype']['name'] in subtype_filter]
        if prop_filter:
            bets = [bet for bet in bets if bet['bet_prop']['name'] in prop_filter]
        if length_filter:
            bets = [bet for bet in bets if bet['bet_length']['name'] in length_filter]
        if sportsbook_filter:
            bets = [bet for bet in bets if bet['sportsbook']['name'] in sportsbook_filter]
        if odds_filter:
            bets = [bet for bet in bets if bet['odds'] != None]
            bets = [bet for bet in bets if bet['odds'] >= odds_filter[0] and bet['odds'] <= odds_filter[1]]
        if line_filter:
            bets = [bet for bet in bets if bet['line'] != None]
            bets = [bet for bet in bets if bet['line'] >= line_filter[0] and bet['line'] <= line_filter[1]]
        if unit_filter:
            bets = [bet for bet in bets if bet['unit'] != None]
            bets = [bet for bet in bets if bet['unit'] >= unit_filter[0] and bet['unit'] <= unit_filter[1]]
        if result_filter:
            bets = [bet for bet in bets if bet['result'] in result_filter]

        insights = Insights()
        i, res = insights.gain_insights(bets)
        st.write(i)
        st.write(res)


