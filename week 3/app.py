import pandas as pd
import numpy as np
import requests
from shiny import App, ui, render, reactive

# --- UI (front end) ---
ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider("slider1","how old are you", 0, 10,5),
        ui.input_select("dropdown","Pick a option",
                    choices = ["option 1", "option 2"], selected=None)
        title = "Filters"
    ),
    ui.h1("My first TFL Dashboard"),
    ui.output_text("print_vlaue"),
    ui.output_text("health_badge")
 )

# --- Server (back end) ---
def server(input, output, session):
    @output
    @render.text
    def print_value():
        return f"Your input is {input.slider1()}"
    
    @reactive.Calc
    def network_status():
        BASE = "https://api.tfl.gov.uk"
        url = BASE + "/line/mode/tube.status"
        r = requests.get(url=url), timeout=10)
        data = r.json()
        return data
    
    @output
    @render.text
    def health_badge():
        data = network_status()
        first_status = data[0]['lineStatuses'][0]['statusSeverityDescription']
        name = data [0]['name']
        return f"{first_status on the {name} line}"
    
    return  # Add logic here later

# --- App (connect UI + server) ---
app = App(ui, server)
