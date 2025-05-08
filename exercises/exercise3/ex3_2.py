from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import duckdb
import plotly.express as px

def update_state(state):
    state.df = generate_dices(state.num_dices, state.throws)
    state.the_mean = df_mean(state.df)
    state.diff= 3.5 - state.the_mean
    state.mean_values_per_throw = state.df.set_index("Throw").mean(axis=1)
    state.fig = px.histogram(state.mean_values_per_throw, nbins=30)


def generate_dices(num_dices= 1, throws=10):
    df = pd.DataFrame()
    for num in range(1,num_dices+1):
        df[f"Dice {num}"] = duckdb.query(f"""--sql
            SELECT FLOOR(RANDOM()*6+1)
            FROM generate_series({throws-1})
        """).df().astype(int)
    df.index.name = "Throw"

    return df.reset_index()

def df_mean(df):
    total = 0
    for column in df.columns[1:]:
        total += df[column].sum()/df[column].count()
    return total/len(df.columns[1:])

def mean_difference(the_mean):
    return 3.5 - the_mean

num_dices= 1
#state.num_dices is updating this. using it in slider
throws=10
df = generate_dices(10, 1000)
the_mean = df_mean(df)
diff = mean_difference(the_mean)
theoretical_mean = 3.5

mean_values_per_throw = df.set_index("Throw").mean(axis=1)
fig = px.histogram(mean_values_per_throw, nbins=30)


with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.text("# Dices simulations", mode="md")

    with tgb.part(class_name="container card"):
        with tgb.layout(columns="1 1"):
            with tgb.part(class_name="container card"):
                tgb.table("{df}", rebuild=True, page_size=10)
                tgb.text("Number of dices chosen {num_dices}")
                tgb.slider("{num_dices}", min= 1, max=10, continuous=False)
                tgb.text("Number of throws {throws}")
                tgb.slider("{throws}", min= 1, max=3000, continuous=False)

                tgb.button("SIMULATE", on_action=update_state)

                
            with tgb.part(class_name="container"):
                with tgb.layout(columns="1 1 1"):
                    with tgb.part(class_name="card"):
                        tgb.text("Theroetical mean")
                        tgb.text("## 3.5", mode="md")
                    with tgb.part(class_name="card"):
                        tgb.text("Calculated mean")
                        tgb.text("## {the_mean:.4f}", mode="md")
                    with tgb.part(class_name= "card"):
                        tgb.text("Difference mean")
                        tgb.text("## {diff:.4f}", mode = "md")
                with tgb.part(class_name="card"):
                    tgb.text("Mean value of {num_dices} for {throws} throws")
                    tgb.chart(figure = "{fig}")
                    tgb.text("This histogram have been calculated through taking mean values for each throw")


style = """
.card {
    margin: 100px;
    padding: 100px;
}
"""

if __name__ == '__main__':
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)