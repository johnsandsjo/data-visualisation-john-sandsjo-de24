import taipy.gui.builder as tgb
from taipy.gui import Gui
from utils.constants import data_directory
import pandas as pd
from frontend.charts import create_municipality_bar

df = pd.read_excel(data_directory/"resultat-ansokningsomgang-2024 (4).xlsx", sheet_name="Tabell 3", skiprows=5)


def filter_df_municipality(df, educational_area="Data/IT"):
    return df.query("Utbildningsområde == @educational_area")["Kommun"].value_counts().reset_index().rename({"count": "Ansökta utbildningar"}, axis=1)

def filter_data(state):
    df_municipality = filter_df_municipality(state.df, educational_area=state.selected_educational_area)
    state.municiapality_chart = create_municipality_bar(df_municipality.head(state.number_municipalities), 
                                                        ylabel="KOMMUN", 
                                                        xlabel= "# ANÖKTA UTBILDNINGAR")
    state.municipality_title = state.number_municipalities
    state.educational_area_title= state.selected_educational_area
    


df_municipality = filter_df_municipality(df)
municiapality_chart = create_municipality_bar(df_municipality.head(9), ylabel="KOMMUN", xlabel= "# ANÖKTA UTBILDNINGAR")
number_municipalities = 5
municipality_title = number_municipalities
selected_educational_area = "Data/IT"
educational_area_title= selected_educational_area

with tgb.Page() as page:
    with tgb.part(class_name="container stack"):
        with tgb.part(class_name="card"):
            tgb.text("# MYH Dashboard", mode="md")
            tgb.text("A dashboard to show stats and information about application round 2024", mode = "md")

        with tgb.layout(columns= "2 1"):
            with tgb.part(class_name="card") as column_chart:
                tgb.text("## Number of apllication per municipality (top {municipality_title} for {educational_area_title})", mode = "md")
                tgb.chart(figure= "{municiapality_chart}")
            
            with tgb.part(class_name="card") as column_filters:
                tgb.text("## Filter data", mode = "md")
                tgb.text("Filter amount of minicipalities", mode = "md")

                tgb.slider(value= "{number_municipalities}", min = 5, max = len(df_municipality), continuous=False)
                tgb.text("Choose educational area", mode = "md")
                tgb.selector(value= "{selected_educational_area}", lov= df["Utbildningsområde"].unique(), dropdown=True)
                tgb.button("FILTER DATA", on_action=filter_data, class_name="plain")

        with tgb.part(class_name="card"):
            tgb.text("## Raw data", mode="df")
            tgb.table("{df}")



Gui(page, css_file="assets/main.css").run(dark_mode=False, use_reloader=True, port= 8080)