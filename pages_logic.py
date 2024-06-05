import solara
import solara.lab
import solara.express as px
from helper import PageHeader
from helper import import_params, load_data, fileter_search, load_custom_css, center_header_text


company_df, unique_industries, unique_states = load_data("fortune-500.csv")
unique_industries = list(unique_industries)
unique_states = list(unique_states)
min_revenue = min(company_df["Revenue (millions)"].min(), 0)
max_revenue = company_df["Revenue (millions)"].max()
min_valuation = min(company_df["Valuation (millions)"].min(), 0)
max_valuation = company_df["Valuation (millions)"].max()
min_profit = min(company_df["Profits (millions)"].min(), 0)
max_profit = company_df["Profits (millions)"].max()
max_employees = company_df["Number of Employees"].max()

params = import_params("params.yaml")

additional_params = solara.reactive(True)
included_states_multiselecet = solara.reactive([])
max_companies_input = solara.reactive(500)
global_frame = solara.reactive(company_df)


@solara.component
def SearchPage():
    load_custom_css()
    solara.lab.theme.themes.light.primary = "#006ec7"
    page_title = params["page_config"]["page_title"]
    with solara.Head():
            solara.Title(page_title)
    
    with solara.Column(classes = ["main_container"]):
        PageHeader(page_title = params["page_config"]["page_title"])
        with solara.Columns([.35, .65], gutters_dense = True):
            with solara.Column():
                with solara.Card("Company Selection Settings", elevation = 0, margin = 2, classes = ["border"]):

                    included_industries_multiselecet = solara.use_reactive([])
                    min_revenue_input = solara.use_reactive(min_revenue)
                    max_revenue_input = solara.use_reactive(max_revenue)
                    min_valuation_input = solara.use_reactive(min_valuation)
                    max_valuation_input = solara.use_reactive(max_valuation)
                    min_profit_input = solara.use_reactive(min_profit)
                    max_profit_input = solara.use_reactive(max_profit)
                    min_employees_input = solara.use_reactive(0)
                    max_employees_input = solara.use_reactive(max_employees)
                    min_rank_input = solara.use_reactive(1)
                    max_rank_input = solara.use_reactive(500)
                    

                    solara.Markdown("Industries to Include In Search")
                    solara.SelectMultiple("Leave Blank to Select All", values = included_industries_multiselecet, all_values = unique_industries, dense = False, classes = ["selection_border"])
                    solara.Markdown("")
                    

                    with solara.Row(classes = ["border"]):
                        with solara.lab.Tabs(color = "#006ec7", grow = True, align = "center"):
                            
                            with solara.lab.Tab("Set Revanue Range"):
                                with solara.Columns([.5, .5]):
                                    with solara.Column():
                                        solara.InputInt("Minimum Revenue (millions):", value = min_revenue_input, classes = ["input_border"])
                                    with solara.Column():
                                            solara.InputInt("Maximum Revenue (millions):", value = max_revenue_input, classes = ["input_border"])
                            
                            with solara.lab.Tab("Set Valuation Range"):
                                with solara.Columns([.5, .5]):
                                    with solara.Column():
                                        solara.InputInt("Minimum Valuation (millions):", value = min_valuation_input, classes = ["input_border"])
                                    with solara.Column():
                                            solara.InputInt("Maximum Valuation (millions):", value = max_valuation_input, classes = ["input_border"])
                            
                            with solara.lab.Tab("Set Profit Range"):
                                with solara.Columns([.5, .5]):
                                    with solara.Column():
                                        solara.InputInt("Minimum Profit (millions):", value = min_profit_input, classes = ["input_border"])
                                    with solara.Column():
                                            solara.InputInt("Maximum Profit (millions):", value = max_profit_input, classes = ["input_border"])
                    solara.Markdown("")


                    with solara.Row(classes = ["border"]):
                         
                         with solara.Columns([.5, .5]):
                            with solara.Column():
                                solara.InputInt("Minimum Number of Employees:", value = min_employees_input, classes = ["input_border"])
                                solara.InputInt("Minimum Company Rank:", value = min_rank_input, classes = ["input_border"])
                            with solara.Column():
                                    solara.InputInt("Maximum Number of Employees:", value = max_employees_input, classes = ["input_border"])
                                    solara.InputInt("Maximum Company Rank:", value = max_rank_input, classes = ["input_border"])
                    solara.Markdown("")


                    @solara.component
                    def ToggleAdditionalParams(additional_parameters = additional_params.value):
                        if additional_parameters:
                            with solara.Column(gap = "0px", classes = ["border"]):
                                solara.Markdown("States to Include In Search")
                                solara.SelectMultiple("Leave Blank to Select All", values = included_states_multiselecet, all_values = unique_states, dense = True, classes = ["selection_border"])
                                solara.Markdown("")
                                solara.InputInt("Max Number of Companies Returned (1-500)", value = max_companies_input, classes = ["input_border"])
                        else:
                            included_states_multiselecet.value = []
                            max_companies_input.value = 500
                            solara.Markdown("")

                    solara.Switch(label = "Additional Parameters", value = additional_params, on_value = ToggleAdditionalParams)
                    ToggleAdditionalParams()
                    with solara.CardActions():
                        def run_query():
                            display_frame = fileter_search(company_df, min_rank_input.value, max_rank_input.value, included_industries_multiselecet.value, included_states_multiselecet.value, min_employees_input.value, max_employees_input.value, max_companies_input.value, min_revenue_input.value, max_revenue_input.value, min_valuation_input.value, max_valuation_input.value, min_profit_input.value, max_profit_input.value)
                            display_frame.index = range(1, len(display_frame) + 1)
                            global_frame.value = display_frame
                        
                        solara.Button("Run Search", on_click = run_query, classes = ["submit_button"])
                        


            with solara.Column(gap = "0px"):
                num_matches = len(global_frame.value)
                with solara.Row(margin = 2, classes = ["center_border"]):
                    result_string = f"<h2>Result: There are {num_matches} Companies that Match Your Criteria</h2>"
                    solara.HTML(unsafe_innerHTML = result_string)
                with solara.Row(margin = 2, classes = ["dataframe_border"]):
                    solara.DataFrame(global_frame.value)


                
@solara.component
def TopResultsPage():
    load_custom_css()
    solara.lab.theme.themes.light.primary = "#006ec7"
    page_title = params["page_config"]["page_title"]
    with solara.Head():
            solara.Title(page_title)

    top_results_frame = global_frame.value
    num_results = len(top_results_frame)
    max_20_results = min(num_results, 20)
    graph_slider = solara.use_reactive(max_20_results)

    with solara.Column(classes = ["main_container"]):
        PageHeader(page_title = params["page_config"]["page_title"])
        if max_20_results == 0:
            solara.Markdown("#")
            solara.Markdown("#")
            with solara.Card():
                solara.HTML(unsafe_innerHTML = "<h2> No Matches to Graph </h2>") 
        else:

            @solara.component
            def set_graphs(df = top_results_frame):
                df = df.iloc[:graph_slider.value]

                with solara.lab.Tabs(color = "#006ec7", slider_color = "#006ec7", grow = True, align = "center"):
                    with solara.lab.Tab("Revenue"):
                        with solara.Column(classes = ["center_border"], gap = "0px"):
                            solara.Markdown("")
                            center_header_text("Revenue Graphs", 3)
                            px.bar(df, x = "Company", y = "Revenue (millions)", color_discrete_sequence = ["#006ec7"], width = 1300, height = 600)
                    
                    with solara.lab.Tab("Valuation"):
                        with solara.Column(classes = ["center_border"], gap = "0px"):
                            solara.Markdown("")
                            center_header_text("Valuation Graphs", 3)
                            px.bar(df, x = "Company", y = "Valuation (millions)", color_discrete_sequence = ["#006ec7"], width = 1300, height = 600)
                    
                    with solara.lab.Tab("Profits"):
                        with solara.Column(classes = ["center_border"], gap = "0px"):
                            solara.Markdown("")
                            center_header_text("Profits Graphs", 3)
                            px.bar(df, x = "Company", y = "Profits (millions)", color_discrete_sequence = ["#006ec7"], width = 1300, height = 600)
                        
                    with solara.lab.Tab("Profits Percentage of Sales"):
                        with solara.Column(classes = ["center_border"], gap = "0px"):
                            solara.Markdown("")
                            center_header_text("Profits Percentage of Sales Graphs", 3)
                            px.bar(df, x = "Company", y = "Profits (% of Sales)", color_discrete_sequence = ["#006ec7"], width = 1300, height = 600)
                    
                    with solara.lab.Tab("Number of Employees"):
                        with solara.Column(classes = ["center_border"], gap = "0px"):
                            solara.Markdown("")
                            center_header_text("Number of Employees Graphs", 3)
                            px.bar(df, x = "Company", y = "Number of Employees", color_discrete_sequence = ["#006ec7"], width = 1300, height = 600)


            with solara.Column(classes = ["border"]):
                centered_slider_text_html_string = '''
                                                   <h3 style = "text-align: center;">
                                                   Choose Number of Top Results to Graph
                                                   </h3>
                                                   '''
                solara.HTML(unsafe_innerHTML = centered_slider_text_html_string)
                solara.SliderInt(label = "", value = graph_slider, min = 1, max = max_20_results, on_value = set_graphs)
            set_graphs()