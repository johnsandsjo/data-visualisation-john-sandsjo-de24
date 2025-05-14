import taipy.gui.builder as tgb
from taipy.gui import Gui
from frontend.charts import create_municipality_bar
from backend.data_processing import df, filter_df_municipality
from backend.updates import filter_data

number_municipalities = 5
selected_educational_area = "Data/IT"

municipalities_title = number_municipalities
educational_area_chart_title = selected_educational_area

df_municipilaty = filter_df_municipality(df, selected_educational_area).head(number_municipalities)

municipality_chart = create_municipality_bar(df_municipilaty, xlabel="# Ansökta Utbildningar", ylabel = "Kommun")


with tgb.Page() as dashboard_page:
    with tgb.part(class_name="container card stack"):
        tgb.navbar()
        tgb.text("# MYH Dashboard 2024", mode = "md")

        with tgb.layout(columns="2 1"):
            with tgb.part(class_name="card"):
                tgb.text("## Antalet ansökta YH-utbildningar per kommun (topp{municipalities_title}) för {educational_area_chart_title}", 
                         class_name="title-chart",
                         mode="md")
                tgb.chart(figure = "{municipality_chart}")

            with tgb.part(class_name="card left-margin-medium"):
                tgb.text("### Filter", mode="md")
                tgb.text("Filtrera antalet kommuner", mode="md")
                tgb.slider(
                    "{number_municipalities}", 
                    min=5, 
                    max=len(filter_df_municipality(df)),
                    continuous=False,
                    )
                
                tgb.text("Välj utbildningsområde")
                tgb.selector(
                    "{selected_educational_area}", 
                    lov=df["Utbildningsområde"].unique(), 
                    dropdown=True
                )

                tgb.button("FILTRERA DATA", class_name="button-color", on_action=filter_data)