from frontend.charts import create_municipality_bar
from backend.data_processing import df, filter_df_municipality

def filter_data(state):
    df_municipality = filter_df_municipality(state.df, state.selected_educational_area)

    state.municipality_chart = create_municipality_bar(
        df_municipality.head(state.number_municipalities),
        xlabel="# ANSÖKTA UTBILDNINGAR",
        ylabel="KOMMUN",
    )
    state.municipalities_title = state.number_municipalities
    state.educational_area_chart_title = state.selected_educational_area