import solara
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

custom_css = Path("assets/custom.css")
@solara.component
def load_custom_css(path = custom_css):
    solara.Style(path)

@solara.component
def PageHeader(page_title: str, logo_path: str = "assets/pd_logo_light_mode.png"):
    """Displays a header with a title and logo and sets page title"""

    with solara.Row(gap="40vw", justify="center", margin = 5):
        solara.HTML(unsafe_innerHTML = f"<h1>{page_title}</h1>")
        solara.Image(logo_path, width = "230px")


def import_params(path):
    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)
        return config
    
def center_header_text(text, header_level):
    center_string = f'''
                    <h{header_level} style = "text-align: center;">
                    {text}
                    </h{header_level}>
                     '''
    solara.HTML(unsafe_innerHTML = center_string)

def clean_columns(column_series):
    column_series = column_series.fillna('0')
    int_string_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
    column_series = ["".join([char for char in entry if char in int_string_list]) for entry in column_series]
    column_series = [int(entry) for entry in column_series]
    return column_series

def load_data(file_path):
    company_df = pd.read_csv(file_path)
    columns_to_clean = ["Number of Employees", "Revenue (millions)", "Valuation (millions)", "Profits (millions)"]
    company_df[columns_to_clean] = company_df[columns_to_clean].apply(clean_columns)
    unique_industries = company_df["Industry"].unique()
    unique_states = company_df["State"].unique()
    return company_df, unique_industries, unique_states

def fileter_search(df, min_rank, max_rank, industries, states, min_employees, max_employees, max_companies, min_revenue, max_revanue, min_valuation, max_valuation, min_profit, max_profit):
    display_frame = df
    if min_rank is not None:
        display_frame = df[df["Rank"] >= min_rank]
    if max_rank is not None:
        display_frame = df[df["Rank"] <= max_rank]
    if min_employees is not None:
        display_frame = display_frame[display_frame["Number of Employees"] >= min_employees]
    if max_employees is not None:
        display_frame = display_frame[display_frame["Number of Employees"] <= max_employees]
    if min_revenue is not None:
        display_frame = display_frame[display_frame["Revenue (millions)"] >= min_revenue]
    if max_revanue is not None:
        display_frame = display_frame[display_frame["Revenue (millions)"] <= max_revanue]
    if min_valuation is not None:
        display_frame = display_frame[display_frame["Valuation (millions)"] >= min_valuation]
    if max_valuation is not None:
        display_frame = display_frame[display_frame["Valuation (millions)"] <= max_valuation]
    if min_profit is not None:
        display_frame = display_frame[display_frame["Profits (millions)"] >= min_profit]
    if max_profit is not None:
        display_frame = display_frame[display_frame["Profits (millions)"] <= max_profit]
    if len(industries) > 0:
        display_frame = display_frame[display_frame["Industry"].isin(industries)]
    if len(states) > 0:
        display_frame = display_frame[display_frame["State"].isin(states)]
    display_frame = display_frame.iloc[:max_companies]
    return display_frame