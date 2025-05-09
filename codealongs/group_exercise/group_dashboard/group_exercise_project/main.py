import plotly.express as px
import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import duckdb

df_size = pd.read_csv("nordic_size.csv")
df = pd.read_csv("nordic_company_ranking.csv")

df_slim = pd.read_csv("nordic_company_ranking.csv")[["Rank", "Company", "Industry", "Revenue (billion $)"]]


df["Headquarters"] = df["Headquarters"].str.split(",")
df["Headquarters"] = df["Headquarters"].str[-1].str.strip()


def grouper(top_list):
    group_df = duckdb.query(f"""--sql
        SELECT Headquarters as Country, count("Company") as num_companies
        FROM df
        GROUP BY Headquarters
                            LIMIT {top_list}
        """).df()
    return group_df

def filter_table(df, industry="Banking"):
    return df.query("Industry == @industry")

def update_table(state):
    state.df_industry = filter_table(df_slim, state.industry_selector)
    group_df = state.grouper(state.top_list) 

def graph_plotter():
    fig = px.bar(
    df_size,
    y = "Employees",
    x = "Company",
    color = "Company",
    title = "Top Nordic companies by employees"
    )
    fig.update_layout(showlegend=False)
    return fig

industry_selector = "Banking"
top_list = 10
df_industry = filter_table(df_slim, industry_selector)
the_graph = graph_plotter()
group_df = grouper(10)


with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Dashboard for largest Nordic companies", mode="md")

    with tgb.part(class_name="container card"):
        tgb.chart(figure="{the_graph}")

    with tgb.part(class_name="container card"):
        with tgb.layout(columns= "2 1"):
            with tgb.part(class_name="card"):
                tgb.text("### Table of top companies filterable by industry", mode="md")
                tgb.table("{df_industry}")
            with tgb.part(class_name="card"):
                tgb.selector(value="{industry_selector}", lov=df["Industry"].unique(), dropdown=True, on_change=update_table)

    with tgb.part(class_name="container card"):
        with tgb.layout(columns= "2 1"):
            with tgb.part(class_name="card"):
                tgb.text("### Table of top by country", mode="md")
                tgb.table("{group_df}")
            with tgb.part(class_name="card"):
                tgb.slider(
                    "{top_list}", 
                    min=5, 
                    max=50,
                    continuous=False,
                    on_change=update_table
                    )


if __name__ == '__main__':
    Gui(page).run( use_reloader=True, port=8080)

