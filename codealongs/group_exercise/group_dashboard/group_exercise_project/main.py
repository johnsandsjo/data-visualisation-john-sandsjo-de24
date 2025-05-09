import plotly.express as px
import taipy.gui.builder as tgb
from taipy.gui import Gui
import pandas as pd
import duckdb

#nordic_size = pd.read_csv("nordic_size.csv")
df = pd.read_csv("nordic_company_ranking.csv")


def filter_table(df, industry="Banking"):
    return df.query("Industry == @industry")

print(filter_table(df,"Transportation"))

def update_table(state):
    state.df_industry = filter_table(df, state.industry_selector)


industry_selector = "Banking"
df_industry = filter_table(df, industry_selector)


with tgb.Page() as page:
    with tgb.part(class_name="container card"): # Stack ger space mellan korten
        tgb.text("Dashboard for largest Nordic companies", mode="md")
        
    with tgb.part():
        with tgb.layout(columns= "2 1"):
            with tgb.part():
                tgb.table("{df_industry}")
            with tgb.part():
                tgb.selector(value="{industry_selector}", lov=df["Industry"].unique(), dropdown=True,)
                tgb.button(label= "FILTER", on_action=update_table)



if __name__ == '__main__':
    Gui(page).run( use_reloader=True, port=8080)

