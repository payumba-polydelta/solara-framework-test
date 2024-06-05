import solara
from pages_logic import SearchPage, TopResultsPage
from helper import import_params, load_custom_css


params = import_params("params.yaml")

current_page = solara.reactive(0)


@solara.component
def Page():
    load_custom_css
    with solara.Div(classes = ["page_wrapper"]):    
        with solara.AppBarTitle():
            with solara.Sidebar():
                with solara.Column():
    
                    def click_search():
                        if (current_page.value != 0):
                            current_page.value = 0
                    
                    def click_top_result():
                        if (current_page.value != 1):
                            current_page.value = 1
    
                    solara.Button(label = "Search", value = current_page, on_click = click_search, classes = ["submit_button"])
                    solara.Button(label = "Top Results", value = current_page, on_click = click_top_result, classes = ["submit_button"])
        
        @solara.component
        def LoadPage(page = current_page.value):
            if page == 0:
                SearchPage()
            else:
                TopResultsPage()
    
        LoadPage()



@solara.component
def Layout(children=[]):
    return solara.AppLayout(children = children,
                            sidebar_open = True,
                            title = None,
                            navigation = False,
                            toolbar_dark = False,
                            color = 'white')

solara.autorouting.DefaultLayout = Layout



