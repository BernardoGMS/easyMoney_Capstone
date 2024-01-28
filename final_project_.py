import pandas as pd
import numpy as np
import warnings as ws
import plotly.graph_objs as go
import plotly.io as pio
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import unicodeit as ut

from plotly.subplots import make_subplots
pio.templates.default = "plotly_white"
pd.options.plotting.backend = "plotly"

ws.filterwarnings("ignore")

commercial_act_df = pd.read_csv("data/commercial_activity_df.csv")
commercial_act_df = commercial_act_df.rename(columns={"Unnamed: 0": "id"})

products_df = pd.read_csv("data/products_df.csv")
products_df = products_df.rename(columns={"Unnamed: 0": "id"})

socio_demo_df = pd.read_csv("data/sociodemographic_df.csv")
socio_demo_df = socio_demo_df.rename(columns={"Unnamed: 0": "id"})

commercial_prod_temp = commercial_act_df.merge(products_df, on=["pk_cid","pk_partition"],how="inner")
full_commercial_temp_df = commercial_prod_temp.merge(socio_demo_df, on=["pk_cid","pk_partition"],how="inner")
full_commercial_df = full_commercial_temp_df.drop(columns={"id_x","id_y","id"})

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# Multivariate analysis of data #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

## 1. Distribution of variables 2 to 2 (scatter-plots) / 10. Visualization of distributions

### 1.1  Boxplots Numeric
def show_boxplots(df):

    for col in df.loc[:, ["age","salary"]]:
        
        fig = px.box(df,x=col,title=col)
        fig.show()

#show_boxplots(full_commercial_df)

### 1.2  Barcharts Categorical
def show_frequency_plots(df):

    df_cat = df[["entry_channel","segment","country_id",'region_code','gender','deceased']]

    for col in df_cat:
        data = pd.crosstab(df_cat[col], "Count").sort_values(by="Count", ascending=False).reset_index().head(20)
        fig = px.bar(data_frame=data, x=data[col], y=data["Count"], text=data["Count"])
        fig.update_layout(
                    title={
                    'text' : str(col),
                    'x':0.5,
                    'xanchor': 'center'
                })
        fig.update_layout(
            font_family="Courier New",
            title_font_family="Courier New",

        )
        fig.update_xaxes(title_font_family="Courier New", title_font_size=20)
        fig.update_yaxes(title_font_family="Courier New", title_font_size=20)
        fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False, hovertemplate="%{text}<br>%{x}")

        fig.show()
    
#show_frequency_plots(full_commercial_df)

## 1.3 Barcharts Categorical vs Categorical

def plot_cat_vs_cat(x, y,df, norm=True, cutoff_count_x=10):
    p_df = (
        df[["pk_cid", x, y]]
        .dropna(how="any", axis=0)
        .pivot_table(index=y, columns=x, values="pk_cid", aggfunc="count")
    )
    p_df = p_df.loc[:, p_df.sum(axis=0) > cutoff_count_x]
    if norm:
        p_df = p_df.div(p_df.sum(axis=0), axis=1) * 100
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=p_df.columns,
                y=p_df.loc[cat],
                name=str(cat),
                showlegend=True
            )
            for cat in np.sort(p_df.index)
        ],
        layout=go.Layout(
            title="{} vs {}".format(y, x),
            barmode="stack"
        )
    )
    fig.show()

boxplots_xs = ["entry_channel","segment","active_customer","short_term_deposit","loans","pension_plan"]
#boxplots_xs = ["entry_channel","segment","mortgage","funds","securities","payroll"]
#boxplots_xs = ["entry_channel","segment","long_term_deposit","em_account_pp","credit_card","payroll_account"]
#boxplots_xs = ["entry_channel","segment","emc_account","debit_card","em_account_p","em_acount"]
#boxplots_xs = ["entry_channel","segment","country_id","region_code","gender","deceased"]
for x in boxplots_xs:
    for y in boxplots_xs:
        if y != x:
            plot_cat_vs_cat(x, y, full_commercial_df, norm=True, cutoff_count_x=10)


