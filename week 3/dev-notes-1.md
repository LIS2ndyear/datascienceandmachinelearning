# Dev notes to create a TfL Shiny dashboard

## Session 1: Shiny Basics & First TfL Call
1. Hello Shiny (Core, not Express)

    - [I] Create `app.py` with minimal UI + server.

    - [I] Add one `input_slider` + one `output_text`.

    - [I] Change the layout to `ui.page_sidebar()`.

    - [I] Give a title to the sidebar and to the main component

    - [I] Demonstrate reactive flow.

    - [I] Add a dropdown menu

2. Simple TfL request outside Shiny

    - [I] Using a scratchpad notebook, use `requests` to call `/line/mode/tube/status` 
    
    - [I] Use the `.json()` method to turn the results into a list of dict-like data. Store the list into a variable called `data`.

    - [I] Print out the tfl data retrieved.

3. Display API result in Shiny

    - [ ] Create `network_status()` reactive calculation to fetch line statuses and return the data (i.e. the `r.json()`).

    - [ ] Create a function `health_badge()` that renders a simple `output_text` showing the status of the first line.

4. Table output

    - [ ] Convert `network_status()` API reponse into a `pandas.DataFrame` and return this dataframe.

    - [ ] Create a function `status_table()` rendering it as a table using the `@render.table` decorator.

**Checkpoint**: If you completed all tasks above, the app should show a live table of tube line statuses.

## Session 2: Interactivity & Multiple Outputs

5. Add network health summary

    - [ ] Modify the `health_badge()` function to compute #lines “Good Service” vs total.

    - [ ] Render the result as `output_text`.

6. Add a status bar chart

    - [ ] Plot counts of each status (Good Service, Minor Delays, etc.) in a `status_plot()` function.

    - [ ] Render with `@render.plot`.

7. Modes checkbox control

    - [ ] Add `input_checkbox_group` for modes (tube, dlr, overground, etc.).

    - [ ] Make `network_status()` depend on `input.modes()`.

    - [ ] Watch table + chart update.

8. Dynamic line dropdown

    - [ ] Add `input_select("line")` (empty initially).

    - [ ] Create a `_populate_lines()` function that populates the line dropdown with `/line/mode/{modes}` API results (using `ui.update_select`). You will need to add a reactive.Effect decorator to `_populate_lines()`

9. Dynamic station dropdown

    - [ ] Add `input_select("station")`.

    - [ ] Create a function called `_populate_stations()`, which populates with `/line/{line}/stoppoints` when line changes.

**Checkpoint**:
If you completed all tasks above, the app should show network table, health summary, and a bar chart. Sidebar filters (modes, line, station) should now update dynamically.

## Session 3

10. Arrivals board

    - [ ] Add `input_slider("n_arrivals")`. You can reuse the first slider we implemented.

    - [ ] Create a function called `arrivals_table()`, which calls `/StopPoint/{station}/arrivals`.

    - [ ] Display next N arrivals in a table.

11. Disruptions panel

    - [ ] Create a new function, called `disruptions_panel()` that calls the `/StopPoint/{station}/disruption` API endpoint.

    - [ ] Display disruptions in a bullet list or say “🎉 No disruptions”.

    - Hint: use `ui.tags.li` and `ui.tags.ul` to create list items and bullet points in the ui.

12. Error handling

    - [ ] Add `try/except` around API calls.

    - [ ] Show fallback text in the UI if API is down.

13. Refresh button

    - [ ] Add `input_action_button("refresh")`.

    - [ ] Wrap API calls so they depend on both inputs and refresh clicks.

14. Polish the layout

    - [ ] Use ``ui.page_sidebar(...)``.

    - [ ] Sidebar: modes, line, station, arrivals slider, refresh.

    - [ ] Main component: Top row → network health + bar chart.

    - [ ] Main component: Middle → arrivals board.

    - [ ] Main component: Bottom → disruptions.

15. Stretch (if time / homework)

    - [ ] Add a “journey planner” panel using /`journey/journeyresults/{from}/to/{to}`.

    - [ ] Or a [leaflet map](https://shiny.posit.co/py/docs/jupyter-widgets.html#efficient-updates) of stations on the selected line.

**Checkpoint**: If you completed all exercises, you should be able to: 
- Choose modes → update network table & chart.

- Choose line → see its stations.

- Choose station → see live arrivals + disruptions.

- Refresh data on demand. 