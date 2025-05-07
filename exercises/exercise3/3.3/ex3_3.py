from taipy.gui import Gui
import taipy.gui.builder as tgb
import plotly.express as px
import duckdb

#data
df= px.data.gapminder()

#continent data
df_continent = duckdb.query("""--sql
                            SELECT continent, year, avg(lifeExp) as avg_life_exp, avg(gdpPercap) as avg_gdp_person
                            FROM df
                            GROUP BY continent, year
                            ORDER BY year, continent
             """).df()

#functions
def stater(state):
    global df
    state.fig = bar_year(df, state.year)
    state.fig4 = map_life_exp(df, state.continento.lower())
    #print(state.continent)

def map_life_exp(df, continento):
    continento = continento.lower()
    fig = px.choropleth(df, locations="iso_alpha",
                        color="lifeExp",
                        scope=continento.lower(),
                        hover_name="country",
                        title = f"Life expectancy by country in {continento}"
                        )
    return fig

def bar_year(df, year):
    year = int(year)
    pop_df = df[df["year"] == year].groupby(["continent"]).sum("pop").reset_index()
    fig = px.bar(pop_df,
                 x= "continent",
                 y= "pop",
                 color= "continent",
                 title= f"Population by continent in {year}",
                 labels=dict(pop="Population", continent="Continent")
                 )
    return fig

def line_plotter(df, metric):
    if metric == "avg_gdp_person":
        title="Yearly average GDP per person per continent"
        yen = "Avg life expectancy"
    elif metric == "avg_life_exp":
        title="Yearly average life expectancy per continent"
        yen = "Avg GDP per person"
    else:
        title = "Standard headline"
        yen = "default"

    fig = px.line(df, 
              x= "year", 
              y=metric, 
              color="continent", 
              title=title,
              labels=dict(continent= "Continent", ylabel = yen, year = "Year")
              )

    fig.update_layout(plot_bgcolor="white", hovermode="x unified")

    fig.update_xaxes(
        showspikes=True,
        spikemode = "across",
        spikesnap = "cursor",
        )

    return fig

def map_life_exp(df, continento="europe"):
    fig = px.choropleth(df, locations="iso_alpha",
                        color="lifeExp",
                        scope=continento,
                        hover_name="country",
                        )
    return fig

#starting data
year = 2007
continento = "asia"
fig = bar_year(df, year)
fig2 = line_plotter(df_continent, 'avg_life_exp')
fig3 = line_plotter(df_continent, 'avg_gdp_person')
fig4 = map_life_exp(df, continento)


#main
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Gapminder dashboard", mode="md")
    with tgb.part(class_name="container card"):
        with tgb.layout("2 1"):
            with tgb.part(class_name="container card"):
                tgb.text("## Map of {continento}", mode="md")
                tgb.chart(figure = "{fig4}", rebuild=True)
            with tgb.part(class_name="container card"):
                tgb.text("### What continent do you want to see?", mode="md")
                tgb.selector(value = "{continento}",
                             lov=df["continent"].unique().tolist(),
                             on_change=stater,
                             dropdown=True,
                             )
    with tgb.part(class_name="container card"):
        with tgb.layout("2 1"):
            with tgb.part(class_name="container card"):
                tgb.text("## Population by year", mode="md")
                tgb.chart(figure = "{fig}", rebuild=True)
            with tgb.part(class_name="container card"):
                tgb.text("### What year do you want to see?", mode="md")
                tgb.selector(value = "{year}",
                             lov=df["year"].unique().tolist(),
                             on_change=stater,
                             dropdown=True,
                             )
    with tgb.part(class_name="container card"):    
        tgb.text("### Two line charts", mode="md")
        with tgb.layout("1 1"):
            with tgb.part(class_name="container card"):
                tgb.chart(figure="{fig2}")
            with tgb.part(class_name="container card"):
                tgb.chart(figure="{fig3}")
                


if __name__ == '__main__':
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)