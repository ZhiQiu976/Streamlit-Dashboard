# app.py
"""
A simple streamlit app for Doctorate Data Visualization
run the app by installing streamlit with pip and typing
> streamlit run app.py
"""

import streamlit as st

import pandas as pd
import numpy as np

import altair as alt


session = st.sidebar.selectbox("Category", ["Recipients Info", "Institutions Info - Ranking", "Institutions Info - Disciplinary"])
st.title("**Doctorate Data Visualization**")

st.write("This dashboard uses data from *Doctorate Recipients from U.S. Universities:* *2017* and mainly focuses on information about recipients and institutions.")


if session == "Recipients Info": 
    st.header('Doctorate recipients from U.S. colleges and universities: 1958–2017')
    
    df = pd.read_excel('df.xlsx', index_col=0)
    
    mode = st.selectbox("Variable", ['Number of Doctorate Recipents', 'Percentage Change from Previous Year'])
    
    #sidebar
    st.sidebar.subheader("Recipients Info")
    year_range =  st.sidebar.slider('Select a range of years',
        min(df.Year+1), max(df.Year), (1990, 2005))
    
    if mode == 'Number of Doctorate Recipents':
        
        years = [i in range(year_range[0],year_range[1]+1) for i in df.Year]
        filtered = df[years]
        
        #graph
        source = filtered.copy().loc[:, ['Year', 'Doctorate recipients']]
        source.columns = ['year', 'y']
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['year'], empty='none')

        line = alt.Chart(source).mark_line().encode(
            x='year',
            y=alt.Y('y:Q', axis=alt.Axis(title='Number of People'))
        )
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='year',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'y:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='year',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        output = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        )

        #show graph
        st.subheader('Doctorate Recipients Number Each Year')
        st.altair_chart(output, use_container_width = True)
        
    elif mode == 'Percentage Change from Previous Year':
        
        years = [i in range(year_range[0],year_range[1]+1) for i in df.Year]
        filtered = df[years]
        
        #graph
        source = filtered.copy().loc[:, ['Year', '% change from previous year']]
        source.columns = ['year', 'y']
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['year'], empty='none')

        line = alt.Chart(source).mark_line().encode(
            x='year',
            y=alt.Y('y:Q', axis=alt.Axis(title='Percentage Change'))
        )
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(source).mark_point().encode(
            x='year',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'y:Q', alt.value(' '))
        )

        # Draw a rule at the location of the selection
        rules = alt.Chart(source).mark_rule(color='gray').encode(
            x='year',
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        output = alt.layer(
            line, selectors, points, rules, text
        ).properties(
            width=600, height=300
        )

        #show graph
        st.subheader('Percentage Change from Previous Year over Year')
        st.altair_chart(output, use_container_width = True)
        st.write("Note that some years have percentage change less than |0.05%|, thus shown as 0 in this line.")
    

if session == "Institutions Info - Ranking": 
    st.header('State/University, ranked by number of doctorate recipients: 2017')
    
    df2 = pd.read_excel('df2.xlsx')
    df3 = pd.read_excel('df3.xlsx')
    
    mode = st.selectbox("Rankings", ['State', 'University'])
    
    #sidebar
    st.sidebar.subheader("Institutions Info - Ranking")
    rank_range =  st.sidebar.slider('Select the ranking you want to see',
                                    min(df3.Rank+1), max(df3.Rank), (1, 5))
    
    if mode == 'State':
        rank = [i in range(rank_range[0],rank_range[1]+1) for i in df2.Rank]
        filtered = df2[rank]
        st.table(filtered)
        
        
    elif mode == 'University':
        rank = [i in range(rank_range[0],rank_range[1]+1) for i in df3.Rank]
        filtered = df3[rank]
        st.table(filtered)
        
    
elif session == "Institutions Info - Disciplinary":
    
    st.header("Doctorates awarded, by state or location, broad field of study, and sex of doctorate recipients: 2017")
    
    df4_new = pd.read_excel('df4_new.xlsx', index_col=0)
    
    field = st.selectbox("Choose a field/discipline", list(np.unique(df4_new['field'])))
    tmp = df4_new.loc[df4_new['field']==field,]
    
    graph = alt.Chart(tmp).mark_line(point=True).encode(
        x = 'State or location', 
        y = 'value',
        color='sex:N').interactive()
    st.altair_chart(graph, use_container_width=True)
   
    
    
    
    



