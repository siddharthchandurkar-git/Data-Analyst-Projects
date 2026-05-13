"""
Kitchen PNL Dashboard - Plotly Dash
Python 3.10+
Required packages: dash==2.17.0, plotly==5.22.0, pandas==2.2.2
Run: python plotly_dashboard.py
"""

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go


# load and prepare data
def load_data():
    df = pd.read_csv("Kittchen_PNL_Data.csv")

    df["GM%"] = (df["GROSS MARGIN"] / df["NET REVENUE"]) * 100
    df["CM"] = df["NET REVENUE"] - df["IDEAL FOOD COST"]
    df["CM%"] = (df["CM"] / df["NET REVENUE"]) * 100
    df["EBITDA"] = df["KITCHEN EBITDA"]
    df["EBITDA%"] = (df["KITCHEN EBITDA"] / df["NET REVENUE"]) * 100
    df["VARIANCE%"] = (df["VARIANCE"] / df["NET REVENUE"]) * 100

    # variance category buckets
    def var_cat(v):
        if v < 2:
            return "(a) Var < 2%"
        elif v < 3:
            return "(b) Var 2% to 3%"
        elif v <= 5:
            return "(c) Var 3% to 5%"
        else:
            return "(d) Var > 5%"

    df["VARIANCE CATEGORY"] = df["VARIANCE%"].apply(var_cat)

    # revenue buckets for variance dashboard
    def rev_bucket(r):
        lacs = r / 100000
        if lacs < 15:
            return "(a) Below INR 15 lacs"
        elif lacs < 25:
            return "(b) INR 15 to 25 lacs"
        elif lacs < 35:
            return "(c) INR 25 to 35 lacs"
        elif lacs < 45:
            return "(d) INR 35 to 45 lacs"
        else:
            return "(e) Above INR 45 lacs"

    df["REV BUCKET"] = df["NET REVENUE"].apply(rev_bucket)

    # month ordering
    month_order = ["Oct-23", "Nov-23", "Dec-23", "Jan-24", "Feb-24", "Mar-24"]
    df["MONTH"] = pd.Categorical(df["MONTH"], categories=month_order, ordered=True)

    return df


df = load_data()

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Kitchen PNL Dashboard"

# color scheme
COLORS = {
    "bg": "#1a1a2e",
    "card": "#16213e",
    "accent": "#e94560",
    "yellow": "#f5a623",
    "text": "#eaeaea",
    "green": "#27ae60",
    "red": "#e74c3c",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "padding": "16px",
    "borderRadius": "8px",
    "marginBottom": "16px",
    "border": f"1px solid {COLORS['accent']}",
}

LABEL_STYLE = {
    "color": COLORS["yellow"],
    "fontWeight": "bold",
    "marginBottom": "4px",
    "fontSize": "13px",
}

DROPDOWN_STYLE = {
    "backgroundColor": "#0f3460",
    "color": "#000",
    "border": f"1px solid {COLORS['accent']}",
    "borderRadius": "4px",
}


def make_dropdown(id, options, placeholder, multi=True):
    return dcc.Dropdown(
        id=id,
        options=[{"label": o, "value": o} for o in sorted(options)],
        placeholder=placeholder,
        multi=multi,
        style=DROPDOWN_STYLE,
        className="dark-dropdown",
    )


# ---- layout ----
app.layout = html.Div(
    style={"backgroundColor": COLORS["bg"], "minHeight": "100vh", "fontFamily": "Arial, sans-serif", "color": COLORS["text"], "padding": "20px"},
    children=[
        html.H1("🍽️ Kitchen PNL Dashboard", style={"color": COLORS["yellow"], "textAlign": "center", "marginBottom": "8px"}),

        dcc.Tabs(
            id="tabs",
            value="tab1",
            style={"marginBottom": "20px"},
            colors={"border": COLORS["accent"], "primary": COLORS["accent"], "background": COLORS["card"]},
            children=[
                dcc.Tab(label="Dashboard 1 – Kitchen Level PNL", value="tab1",
                        style={"color": COLORS["text"], "backgroundColor": COLORS["card"]},
                        selected_style={"color": COLORS["yellow"], "backgroundColor": COLORS["bg"], "fontWeight": "bold"}),
                dcc.Tab(label="Dashboard 2 – Variance Level PNL", value="tab2",
                        style={"color": COLORS["text"], "backgroundColor": COLORS["card"]},
                        selected_style={"color": COLORS["yellow"], "backgroundColor": COLORS["bg"], "fontWeight": "bold"}),
            ],
        ),

        html.Div(id="tab-content"),
    ],
)


# ---- Dashboard 1 layout ----
def dashboard1_layout():
    return html.Div([
        # KPI cards row
        html.Div(id="kpi-row", style={"display": "flex", "gap": "12px", "marginBottom": "16px"}),

        # filters section
        html.Div(style=CARD_STYLE, children=[
            html.H3("Filters", style={"color": COLORS["yellow"], "marginTop": 0}),

            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "12px"}, children=[
                html.Div([html.P("Store", style=LABEL_STYLE),
                          make_dropdown("d1-store", df["STORE"].unique(), "All Stores")]),
                html.Div([html.P("Month", style=LABEL_STYLE),
                          make_dropdown("d1-month", df["MONTH"].unique(), "All Months")]),
                html.Div([html.P("Revenue Cohort", style=LABEL_STYLE),
                          make_dropdown("d1-rev-cohort", df["REVENUE COHORT"].unique(), "All Revenue Cohorts")]),
                html.Div([html.P("CM Cohort", style=LABEL_STYLE),
                          make_dropdown("d1-cm-cohort", df["CM COHORT"].unique(), "All CM Cohorts")]),
                html.Div([html.P("EBITDA Category", style=LABEL_STYLE),
                          make_dropdown("d1-ebitda-cat", df["EBITDA CATEGORY"].unique(), "All EBITDA Categories")]),
                html.Div([html.P("EBITDA Cohort", style=LABEL_STYLE),
                          make_dropdown("d1-ebitda-cohort", df["EBITDA COHORT"].unique(), "All EBITDA Cohorts")]),
                html.Div([html.P("Zone", style=LABEL_STYLE),
                          make_dropdown("d1-zone", df["ZONE MAPPING"].unique(), "All Zones")]),
                html.Div([html.P("City", style=LABEL_STYLE),
                          make_dropdown("d1-city", df["CITY"].unique(), "All Cities")]),
            ]),

            # range sliders
            html.Div(style={"marginTop": "16px", "display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "24px"}, children=[
                html.Div([
                    html.P(f"EBITDA Range (₹): {int(df['EBITDA'].min()):,} to {int(df['EBITDA'].max()):,}", style=LABEL_STYLE),
                    dcc.RangeSlider(id="d1-ebitda-range",
                                    min=df["EBITDA"].min(), max=df["EBITDA"].max(),
                                    value=[df["EBITDA"].min(), df["EBITDA"].max()],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks=None),
                ]),
                html.Div([
                    html.P(f"CM Range (₹): {int(df['CM'].min()):,} to {int(df['CM'].max()):,}", style=LABEL_STYLE),
                    dcc.RangeSlider(id="d1-cm-range",
                                    min=df["CM"].min(), max=df["CM"].max(),
                                    value=[df["CM"].min(), df["CM"].max()],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks=None),
                ]),
                html.Div([
                    html.P(f"Net Revenue Range (₹): {int(df['NET REVENUE'].min()):,} to {int(df['NET REVENUE'].max()):,}", style=LABEL_STYLE),
                    dcc.RangeSlider(id="d1-rev-range",
                                    min=df["NET REVENUE"].min(), max=df["NET REVENUE"].max(),
                                    value=[df["NET REVENUE"].min(), df["NET REVENUE"].max()],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks=None),
                ]),
            ]),

            html.Button("Reset Filters", id="d1-reset", n_clicks=0,
                        style={"marginTop": "12px", "backgroundColor": COLORS["accent"], "color": "#fff",
                               "border": "none", "padding": "8px 20px", "borderRadius": "4px", "cursor": "pointer"}),
        ]),

        # charts row
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px", "marginBottom": "16px"}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id="d1-bar-revenue")]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id="d1-bar-ebitda")]),
        ]),

        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px", "marginBottom": "16px"}, children=[
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id="d1-scatter")]),
            html.Div(style=CARD_STYLE, children=[dcc.Graph(id="d1-pie-rev-cohort")]),
        ]),

        # kitchen snapshot table
        html.Div(style=CARD_STYLE, children=[
            html.H3("Kitchen Snapshot", style={"color": COLORS["yellow"], "marginTop": 0}),
            html.Div(id="d1-table"),
        ]),
    ])


# ---- Dashboard 2 layout ----
def dashboard2_layout():
    return html.Div([
        html.Div(style=CARD_STYLE, children=[
            html.H3("Variance Filter", style={"color": COLORS["yellow"], "marginTop": 0}),
            html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}, children=[
                html.Div([html.P("Variance Category", style=LABEL_STYLE),
                          make_dropdown("d2-var-cat", df["VARIANCE CATEGORY"].unique(), "Select Variance Category")]),
                html.Div([html.P("Month", style=LABEL_STYLE),
                          make_dropdown("d2-month", df["MONTH"].unique(), "All Months")]),
            ]),
        ]),

        # sub-dashboard 1: avg variance % by revenue category
        html.Div(style=CARD_STYLE, children=[
            html.H3("Sub-Dashboard 1 – Average Variance % by Revenue Category", style={"color": COLORS["yellow"], "marginTop": 0}),
            html.P("Average variance % of kitchens under each revenue category across months", style={"color": "#aaa", "marginTop": 0}),
            html.Div(id="d2-sub1-table"),
            dcc.Graph(id="d2-sub1-chart"),
        ]),

        # sub-dashboard 2: count of stores by revenue bucket
        html.Div(style=CARD_STYLE, children=[
            html.H3("Sub-Dashboard 2 – Store Count by Revenue Range", style={"color": COLORS["yellow"], "marginTop": 0}),
            html.P("Count of kitchen stores per revenue bucket per month", style={"color": "#aaa", "marginTop": 0}),
            html.Div(id="d2-sub2-table"),
            dcc.Graph(id="d2-sub2-heatmap"),
        ]),
    ])


# render tab content
@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    if tab == "tab1":
        return dashboard1_layout()
    return dashboard2_layout()


# helper: apply d1 filters
def apply_d1_filters(store, month, rev_cohort, cm_cohort, ebitda_cat, ebitda_cohort, zone, city,
                     ebitda_range, cm_range, rev_range):
    d = df.copy()
    if store:
        d = d[d["STORE"].isin(store)]
    if month:
        d = d[d["MONTH"].isin(month)]
    if rev_cohort:
        d = d[d["REVENUE COHORT"].isin(rev_cohort)]
    if cm_cohort:
        d = d[d["CM COHORT"].isin(cm_cohort)]
    if ebitda_cat:
        d = d[d["EBITDA CATEGORY"].isin(ebitda_cat)]
    if ebitda_cohort:
        d = d[d["EBITDA COHORT"].isin(ebitda_cohort)]
    if zone:
        d = d[d["ZONE MAPPING"].isin(zone)]
    if city:
        d = d[d["CITY"].isin(city)]
    if ebitda_range:
        d = d[(d["EBITDA"] >= ebitda_range[0]) & (d["EBITDA"] <= ebitda_range[1])]
    if cm_range:
        d = d[(d["CM"] >= cm_range[0]) & (d["CM"] <= cm_range[1])]
    if rev_range:
        d = d[(d["NET REVENUE"] >= rev_range[0]) & (d["NET REVENUE"] <= rev_range[1])]
    return d


PLOT_LAYOUT = dict(
    plot_bgcolor="#0f3460",
    paper_bgcolor=COLORS["card"],
    font_color=COLORS["text"],
    margin=dict(l=40, r=20, t=40, b=40),
)


# KPI cards
@app.callback(
    Output("kpi-row", "children"),
    [Input("d1-store", "value"), Input("d1-month", "value"),
     Input("d1-rev-cohort", "value"), Input("d1-cm-cohort", "value"),
     Input("d1-ebitda-cat", "value"), Input("d1-ebitda-cohort", "value"),
     Input("d1-zone", "value"), Input("d1-city", "value"),
     Input("d1-ebitda-range", "value"), Input("d1-cm-range", "value"),
     Input("d1-rev-range", "value")],
)
def update_kpis(store, month, rc, cmc, ec, ehc, zone, city, er, cmr, rvr):
    d = apply_d1_filters(store, month, rc, cmc, ec, ehc, zone, city, er, cmr, rvr)

    def kpi_card(label, value, color):
        return html.Div(style={
            "flex": "1", "backgroundColor": COLORS["card"], "padding": "16px",
            "borderRadius": "8px", "border": f"2px solid {color}", "textAlign": "center"
        }, children=[
            html.P(label, style={"color": "#aaa", "margin": 0, "fontSize": "12px"}),
            html.H3(value, style={"color": color, "margin": "4px 0 0 0"}),
        ])

    total_rev = d["NET REVENUE"].sum()
    avg_gm = d["GM%"].mean() if len(d) else 0
    avg_cm = d["CM%"].mean() if len(d) else 0
    total_ebitda = d["EBITDA"].sum()
    stores = d["STORE"].nunique()

    return [
        kpi_card("Total Net Revenue", f"₹{total_rev/1e7:.2f} Cr", COLORS["yellow"]),
        kpi_card("Avg GM%", f"{avg_gm:.1f}%", COLORS["green"]),
        kpi_card("Avg CM%", f"{avg_cm:.1f}%", "#3498db"),
        kpi_card("Total EBITDA", f"₹{total_ebitda/1e7:.2f} Cr", COLORS["accent"]),
        kpi_card("Stores", str(stores), "#9b59b6"),
    ]


# charts callbacks
@app.callback(
    [Output("d1-bar-revenue", "figure"),
     Output("d1-bar-ebitda", "figure"),
     Output("d1-scatter", "figure"),
     Output("d1-pie-rev-cohort", "figure"),
     Output("d1-table", "children")],
    [Input("d1-store", "value"), Input("d1-month", "value"),
     Input("d1-rev-cohort", "value"), Input("d1-cm-cohort", "value"),
     Input("d1-ebitda-cat", "value"), Input("d1-ebitda-cohort", "value"),
     Input("d1-zone", "value"), Input("d1-city", "value"),
     Input("d1-ebitda-range", "value"), Input("d1-cm-range", "value"),
     Input("d1-rev-range", "value")],
)
def update_d1_charts(store, month, rc, cmc, ec, ehc, zone, city, er, cmr, rvr):
    d = apply_d1_filters(store, month, rc, cmc, ec, ehc, zone, city, er, cmr, rvr)

    # bar: revenue by month
    rev_by_month = d.groupby("MONTH", observed=True)["NET REVENUE"].sum().reset_index()
    fig1 = px.bar(rev_by_month, x="MONTH", y="NET REVENUE",
                  title="Net Revenue by Month",
                  color_discrete_sequence=[COLORS["yellow"]])
    fig1.update_layout(**PLOT_LAYOUT)

    # bar: EBITDA by month
    ebitda_by_month = d.groupby("MONTH", observed=True)["EBITDA"].sum().reset_index()
    fig2 = px.bar(ebitda_by_month, x="MONTH", y="EBITDA",
                  title="EBITDA by Month",
                  color="EBITDA",
                  color_continuous_scale=["red", "green"])
    fig2.update_layout(**PLOT_LAYOUT)

    # scatter: GM% vs CM%
    fig3 = px.scatter(d, x="GM%", y="CM%", color="EBITDA CATEGORY",
                      hover_data=["STORE", "MONTH", "NET REVENUE"],
                      title="GM% vs CM% by EBITDA Category",
                      color_discrete_map={"EBITDA +ve": COLORS["green"], "EBITDA -ve": COLORS["red"]})
    fig3.update_layout(**PLOT_LAYOUT)

    # pie: revenue cohort distribution
    rc_dist = d.groupby("REVENUE COHORT", observed=True)["STORE"].count().reset_index()
    rc_dist.columns = ["REVENUE COHORT", "Count"]
    fig4 = px.pie(rc_dist, names="REVENUE COHORT", values="Count",
                  title="Store Count by Revenue Cohort",
                  color_discrete_sequence=px.colors.sequential.Plasma)
    fig4.update_layout(**PLOT_LAYOUT)

    # table
    table_df = d[["STORE", "MONTH", "NET REVENUE", "GM%", "CM%", "CM", "EBITDA", "EBITDA%", "REVENUE COHORT", "EBITDA CATEGORY"]].copy()
    table_df["NET REVENUE"] = table_df["NET REVENUE"].apply(lambda x: f"₹{x:,.0f}")
    table_df["GM%"] = table_df["GM%"].apply(lambda x: f"{x:.1f}%")
    table_df["CM%"] = table_df["CM%"].apply(lambda x: f"{x:.1f}%")
    table_df["CM"] = table_df["CM"].apply(lambda x: f"₹{x:,.0f}")
    table_df["EBITDA"] = table_df["EBITDA"].apply(lambda x: f"₹{x:,.0f}")
    table_df["EBITDA%"] = table_df["EBITDA%"].apply(lambda x: f"{x:.1f}%")
    table_df["MONTH"] = table_df["MONTH"].astype(str)

    tbl = dash_table.DataTable(
        data=table_df.head(500).to_dict("records"),
        columns=[{"name": c, "id": c} for c in table_df.columns],
        page_size=15,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#0f3460", "color": COLORS["yellow"], "fontWeight": "bold"},
        style_data={"backgroundColor": COLORS["card"], "color": COLORS["text"]},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#1a1a2e"},
        ],
    )
    return fig1, fig2, fig3, fig4, tbl


# dashboard 2 callbacks
@app.callback(
    [Output("d2-sub1-table", "children"),
     Output("d2-sub1-chart", "figure"),
     Output("d2-sub2-table", "children"),
     Output("d2-sub2-heatmap", "figure")],
    [Input("d2-var-cat", "value"), Input("d2-month", "value")],
)
def update_d2(var_cat, month):
    d = df.copy()
    if var_cat:
        d = d[d["VARIANCE CATEGORY"].isin(var_cat)]
    if month:
        d = d[d["MONTH"].isin(month)]

    rev_order = ["(a) Below INR 15 lacs", "(b) INR 15 to 25 lacs",
                 "(c) INR 25 to 35 lacs", "(d) INR 35 to 45 lacs", "(e) Above INR 45 lacs"]
    month_order = ["Oct-23", "Nov-23", "Dec-23", "Jan-24", "Feb-24", "Mar-24"]

    # sub1: avg variance % by revenue cohort per month
    sub1 = d.groupby(["REVENUE COHORT", "MONTH"], observed=True)["VARIANCE%"].mean().reset_index()
    sub1["VARIANCE%"] = sub1["VARIANCE%"].round(2)
    pivot1 = sub1.pivot(index="REVENUE COHORT", columns="MONTH", values="VARIANCE%")
    pivot1 = pivot1.reindex(columns=[m for m in month_order if m in pivot1.columns])

    # grand total row
    grand = d.groupby("MONTH", observed=True)["VARIANCE%"].mean()
    grand_row = pd.DataFrame([["Grand Total"] + [round(grand.get(m, np.nan), 2) for m in pivot1.columns]],
                              columns=["Revenue Category"] + list(pivot1.columns))
    pivot1_reset = pivot1.reset_index().rename(columns={"REVENUE COHORT": "Revenue Category"})
    sub1_display = pd.concat([pivot1_reset, grand_row], ignore_index=True)

    # format as %
    for c in sub1_display.columns[1:]:
        sub1_display[c] = sub1_display[c].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")

    tbl1 = dash_table.DataTable(
        data=sub1_display.to_dict("records"),
        columns=[{"name": c, "id": c} for c in sub1_display.columns],
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#0f3460", "color": COLORS["yellow"], "fontWeight": "bold"},
        style_data={"backgroundColor": COLORS["card"], "color": COLORS["text"]},
        style_data_conditional=[
            {"if": {"filter_query": '{Revenue Category} = "Grand Total"'},
             "backgroundColor": "#0f3460", "fontWeight": "bold", "color": COLORS["yellow"]},
        ],
    )

    # chart for sub1
    chart_df = sub1.copy()
    chart_df["MONTH"] = chart_df["MONTH"].astype(str)
    fig_sub1 = px.line(chart_df, x="MONTH", y="VARIANCE%", color="REVENUE COHORT",
                       title="Avg Variance % by Revenue Cohort over Months",
                       markers=True)
    fig_sub1.update_layout(**PLOT_LAYOUT)

    # sub2: count of stores by rev bucket per month
    sub2 = d.groupby(["REV BUCKET", "MONTH"], observed=True)["STORE"].nunique().reset_index()
    sub2.columns = ["Revenue Bucket", "Month", "Store Count"]
    pivot2 = sub2.pivot(index="Revenue Bucket", columns="Month", values="Store Count").fillna(0).astype(int)
    pivot2 = pivot2.reindex(index=[r for r in rev_order if r in pivot2.index])
    pivot2 = pivot2.reindex(columns=[m for m in month_order if m in pivot2.columns])

    grand2_vals = ["Grand Total"] + [int(pivot2[c].sum()) for c in pivot2.columns]
    grand2 = pd.DataFrame([grand2_vals], columns=["Revenue Bucket"] + list(pivot2.columns))
    pivot2_reset = pivot2.reset_index()
    sub2_display = pd.concat([pivot2_reset, grand2], ignore_index=True)

    tbl2 = dash_table.DataTable(
        data=sub2_display.to_dict("records"),
        columns=[{"name": c, "id": c} for c in sub2_display.columns],
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#0f3460", "color": COLORS["yellow"], "fontWeight": "bold"},
        style_data={"backgroundColor": COLORS["card"], "color": COLORS["text"]},
        style_data_conditional=[
            {"if": {"filter_query": '{Revenue Bucket} = "Grand Total"'},
             "backgroundColor": "#0f3460", "fontWeight": "bold", "color": COLORS["yellow"]},
        ],
    )

    # heatmap for sub2
    heat_data = pivot2.copy()
    fig_sub2 = go.Figure(data=go.Heatmap(
        z=heat_data.values,
        x=[str(c) for c in heat_data.columns],
        y=list(heat_data.index),
        colorscale="YlOrRd",
        text=heat_data.values,
        texttemplate="%{text}",
    ))
    fig_sub2.update_layout(title="Store Count Heatmap by Revenue Bucket & Month", **PLOT_LAYOUT)

    return tbl1, fig_sub1, tbl2, fig_sub2


if __name__ == "__main__":
    app.run(debug=True, port=8050)
