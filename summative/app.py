# Import libraries
from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('attendance_anonymised-1.csv')

# Drop planned end date column; not needed for this analysis 
df = df.drop('Planned End Date', axis=1)

# Rename columns to be clear
df = df.rename(columns={
    'Long Description': 'Module Name',
    'Planned Start Date': 'Date',
    'Postive Marks' : 'Attended'
})

# Change data to date time
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Attended'] = pd.to_numeric(df['Attended'], errors='coerce')

# UI - sidebar for module selection, main panel for plot and summary
# Sidebar with module selector
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Select Module"),
        ui.input_select(
            # ID, label, choices
            "module_selector", 
            "Module", 
            choices=sorted(df['Module Name'].dropna().unique())
        )
    ),
    # Main panel shows title, plot and statitcs
    ui.h1("Module Attendance Dashboard"),
    ui.output_plot("attendance_plot"),
    ui.output_text("attendance_summary")
)

# Server 
# Define server logic 
def server(input, output, session):

    # Plot attendance over time for selected module
    @output
    @render.plot
    def attendance_plot():
        # Find select module
        module = input.module_selector()

        if not module:
            # If no module selected, give none
            return None
        
        # Filter data for select module
        module_df = df[df['Module Name'] == module]

        # Calculate mean attendance rate over time
        attendance_over_time = module_df.groupby("Date")['Attended'].mean()
        
        # Create line graph
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(attendance_over_time.index, attendance_over_time.values, marker='o')
        ax.set_title(f"Attendance Over Time: {module}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Attendance Rate")
        ax.set_ylim(0, 1) # Binary attendance rate
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    # Show summary statistics below plot
    @output
    @render.text
    def attendance_summary():
        # Find selected module
        module = input.module_selector()
        
        # Deal with no module selected
        if not module:
            return "Select a module to see statistics."
        
        # Filter for select module
        module_df = df[df['Module Name'] == module]
        # Calculate attendance statistics

        attendance_over_time = module_df.groupby("Date")['Attended'].mean()

        # Calculate average, min and max attendance
        avg = attendance_over_time.mean()
        mn = attendance_over_time.min()
        mx = attendance_over_time.max()
        
        # Return statement with statistics
        return f"Average: {avg:.1%} | Min: {mn:.1%} | Max: {mx:.1%}"

# Run app
app = App(app_ui, server)
