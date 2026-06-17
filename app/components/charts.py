import streamlit as st
from collections import defaultdict
from app.utils import formatted
import pandas as pd
import altair as alt
import time

def render_graph_card(data, graph_type):
    graph_name = graph_type.title()
    if not data: st.error(f"No {graph_name}")

    if graph_type == "crop":
        metric =  ["Cost", "Revenue", "Yield", "Profit"]
        value = [data.prod_cost, data.revenue, data.crop_yield, data.profit]
    elif graph_type == "livestock":
        pass
    df = pd.DataFrame({
        "Metric": metric,
        "Value" : value,
        "colors": ["#e74c3c","#3498db","#f1c40f", "#2ecc71"]
    })
    gf = alt.Chart(df).mark_bar().encode(

    x=alt.X("Metric:N", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True), sort=None),
    y=alt.Y("Value:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
    color = alt.Color("colors:N", scale=None)
    ).properties(
    width=200,
    height=200,
    )
    prod_start_year = data.prod_start_year
    prod_end_year = data.prod_end_year
    planted_date = formatted(data.planted_date) if data.planted_date else "Unknown"
    harvest_date = formatted(data.harvest_date) if data.harvest_date else "Unknown"
    with st.container(border=True):
        col = st.columns(2)
        with col[0]:
            st.button(f"**{data.name}**", type="secondary", width="stretch", key=f"card {data.name} {data.id} ")
        with col[1]:
            if prod_start_year != prod_end_year:
                st.button(f"**{prod_start_year}/{prod_end_year}**", type="secondary", width="stretch", key=f"{data.id}{data.prod_start_year}{data.prod_end_year}")
            else:
                st.button(f"**{prod_start_year}**", type="secondary", width="stretch", key=f"{data.id}{data.prod_start_year}{data.prod_end_year}")
        graph = st.empty()
        space = st.empty()
        space.button(f"**{planted_date} -- {harvest_date}**", type="tertiary",width="stretch", key=f"{data.id}{data.planted_date}{data.harvest_date}")
        
        graph.altair_chart(gf)# height and width not specified for the smooth left to right auto adjestment animation
        time.sleep(0.1) # Animation effect and prevent flicker

def render_profit_trend(data, trend_type, show_table = False):
    trend_name = trend_type.title()
    if not data: st.error(f"No {trend_name}")

    profit_dict = defaultdict(float)
    table_dict = defaultdict(float)
    label_dates = []
    for item in data[::-1]: #in order of earliest to latest.
        
        start_year = item.prod_start_year
        end_year = item.prod_end_year
        profit = item.profit
        label_dates.append(start_year)
        
        if profit:
            if start_year == end_year:
                profit_dict[start_year] += profit
                table_dict[f"{start_year}"] += profit
            else:
                table_dict[f"{start_year} - {end_year}"]  += profit
                profit_dict[(start_year + end_year)/2] += profit
    
    label_dates = list(set(label_dates))
 
    graph_df = pd.DataFrame({
        "Date"   : profit_dict.keys(),
        "Profit" : profit_dict.values(),
    })

    table_df = pd.DataFrame({
        "Date"   : table_dict.keys(),
        "Profit" : profit_dict.values(),  
    })

    area_gf = alt.Chart(graph_df).mark_area(color="#86f3b3ff", opacity=0.4).encode(
            x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values = label_dates),sort=None),
            y=alt.Y("Profit:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        ).properties(
            width=200,
            height=300,
        )   

    profit_gf = alt.Chart(graph_df).mark_line(color="#2fa342ff", point=True).encode(
        x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values=label_dates),sort=None),
        y=alt.Y("Profit:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),

        ).properties(
            width=200,
            height=300,
        )
  
    gf = area_gf +profit_gf
        
    if show_table:
        col = st.columns(2)
        with col[0]:
            st.badge("Profit", color="green")            
            st.altair_chart(gf)
        with col[1]: 
            st.table(table_df)
    else:
        st.altair_chart(gf)



def render_cost_revenue_trend(data, trend_type, show_table = False):
    if not data:
        st.error("No Crops")
    cost_revenue = defaultdict(lambda: [0,0])
    table_dict = defaultdict(lambda:[0,0])
    label_dates = []
    for data in data[::-1]: #in order of earliest to latest.
        
        start_year = data.prod_start_year
        end_year = data.prod_end_year
        prod_cost = data.prod_cost
        revenue = data.revenue
        label_dates.append(start_year)

        if revenue and prod_cost:
            if start_year == end_year:
                cost_revenue[start_year][0] += prod_cost
                cost_revenue[start_year][1]+= revenue
            
                table_dict[f"{start_year}"][0] += prod_cost
                table_dict[f"{start_year}"][1] += revenue
            else:  
                table_dict[f"{start_year} - {end_year}"][0]  += prod_cost
                table_dict[f"{start_year} - {end_year}"][1]  += revenue

                cost_revenue[(start_year + end_year)/2][0] += prod_cost
                cost_revenue[(start_year + end_year)/2][1] += revenue
    
    
    label_dates = list(set(label_dates))
    prod_cost_list = [x[0] for x in list(cost_revenue.values())]
    revenue_list = [x[1] for x in list(cost_revenue.values())]

    graph_df = pd.DataFrame({
        "Date"   : cost_revenue.keys(),
        "Prod" : prod_cost_list,
        "Revenue": revenue_list,

    })
    table_df = pd.DataFrame({
        "Date"   : table_dict.keys(),
        "Prod" : prod_cost_list,
        "Revenue": revenue_list,
    
    })
    prod_gf = alt.Chart(graph_df).mark_line(color="#e74c3c", point=True).encode(
        x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values=label_dates),sort=None),
        y=alt.Y("Prod:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        
    ).properties(
        width=200,
        height=300,
    )
    revenue_gf = alt.Chart(graph_df).mark_line(color="#3498db", point=True).encode(
        x=alt.X("Date:O", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True, values=label_dates),sort=None),
        y=alt.Y("Revenue:Q", axis=alt.Axis(title=None, labels=True, ticks=False, grid=True)),
        
    ).properties(
        width=200,
        height=300,
    )
    gf = prod_gf + revenue_gf
    
    if show_table:
        col = st.columns(2)
        with col[0]:  
            st.markdown(":red-badge[Cost] :blue-badge[Revenue]")           
            st.altair_chart(gf)
        with col[1]: 
            st.table(table_df)
    else:
        st.altair_chart(gf)


def render_yield_trend(data,trend_type, show_table = False):
    trend_name = trend_type.title()
    if not data: st.error(f"No {trend_name}")

    yield_dict = defaultdict(float)
    table_dict = defaultdict(float)
    label_dates = []
    for item in data[::-1]: # in order of earliest to latest

        start_year = item.prod_start_year
        end_year = item.prod_end_year
        crop_yield = item.crop_yield
        label_dates.append(start_year)
        if start_year == end_year and crop_yield:
            yield_dict[start_year] += crop_yield
            table_dict[f"{start_year}"] += crop_yield
        elif crop_yield:
            yield_dict[(start_year + end_year )/ 2] += crop_yield
            table_dict[f"{start_year} - {end_year}"] += crop_yield
    label_dates = list(set(label_dates))

    graph_df = pd.DataFrame({
        "Date": yield_dict.keys(),
        "Yield": yield_dict.values(),
    })
    table_df = pd.DataFrame({
        "Date" : table_dict.keys(),
        "Yield": table_dict.values(),
    })
    area_gf = alt.Chart(graph_df).mark_area(color="#f1c40f", opacity=0.4).encode(
        x = alt.X("Date:O", axis = alt.Axis(title=None, ticks=False, grid=True, values=label_dates), sort=None),
        y = alt.Y("Yield:Q", axis=alt.Axis(title=None, ticks=False,grid=True))
    ).properties(
        width=200,
        height=300,
    )
    line_gf = alt.Chart(graph_df).mark_line(color="#bd9804", point=True).encode(
        x = alt.X("Date:O", axis = alt.Axis(title=None, ticks=False, grid=True, values=label_dates), sort=None),
        y = alt.Y("Yield:Q", axis=alt.Axis(title=None, ticks=False, grid=True))
    ).properties(
        width=200,
        height=300,
    )
    gf = area_gf + line_gf
    if show_table:
        col = st.columns(2)
        with col[0]:
            st.badge("Yield", color="yellow") 
            st.altair_chart(gf)
        with col[1]: 
            st.table(table_df)
    else:
        st.altair_chart(gf)