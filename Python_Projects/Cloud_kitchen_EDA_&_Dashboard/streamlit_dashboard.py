

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Kitchen PNL Dashboard",
    layout="wide",
    page_icon="🍽️",
)

# custom css for dark theme and styling 
st.markdown("""
<style>
    .main { background-color: #1a1a2e; }
    .stSelectbox label, .stMultiSelect label, .stSlider label { color: #f5a623 !important; font-weight: bold; }
    .metric-card {
        background-color: #16213e;
        border: 1px solid #e94560;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #f5a623; }
    .metric-label { font-size: 13px; color: #aaa; }
    h1, h2, h3 { color: #f5a623 !important; }
</style>
""", unsafe_allow_html=True)


# caching the data load so it doesnt reload on every interaction
@st.cache_data
def load_data():
    df = pd.read_csv("Kittchen_PNL_Data.csv")

    df["GM%"] = (df["GROSS MARGIN"] / df["NET REVENUE"]) * 100
    df["CM"] = df["NET REVENUE"] - df["IDEAL FOOD COST"]
    df["CM%"] = (df["CM"] / df["NET REVENUE"]) * 100
    df["EBITDA"] = df["KITCHEN EBITDA"]
    df["EBITDA%"] = (df["KITCHEN EBITDA"] / df["NET REVENUE"]) * 100
    df["VARIANCE%"] = (df["VARIANCE"] / df["NET REVENUE"]) * 100

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

    month_order = ["Oct-23", "Nov-23", "Dec-23", "Jan-24", "Feb-24", "Mar-24"]
    df["MONTH"] = pd.Categorical(df["MONTH"], categories=month_order, ordered=True)

    return df


df = load_data()

PLOT_THEME = dict(
    plot_bgcolor="#0f3460",
    paper_bgcolor="#16213e",
    font_color="#eaeaea",
    margin=dict(l=40, r=20, t=40, b=40),
)

st.title("🍽️ Kitchen PNL Dashboard")

tab1, tab2 = st.tabs(["📊 Dashboard 1 – Kitchen Level PNL", "📉 Dashboard 2 – Variance Level PNL"])


# ===================== DASHBOARD 1 =====================
with tab1:
    st.subheader("Filters")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        sel_store = st.multiselect("Store", sorted(df["STORE"].unique()), key="d1_store")
    with c2:
        sel_month = st.multiselect("Month", list(df["MONTH"].cat.categories), key="d1_month")
    with c3:
        sel_rev_cohort = st.multiselect("Revenue Cohort", sorted(df["REVENUE COHORT"].unique()), key="d1_rc")
    with c4:
        sel_cm_cohort = st.multiselect("CM Cohort", sorted(df["CM COHORT"].unique()), key="d1_cmc")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        sel_ebitda_cat = st.multiselect("EBITDA Category", sorted(df["EBITDA CATEGORY"].unique()), key="d1_ec")
    with c6:
        sel_ebitda_cohort = st.multiselect("EBITDA Cohort", sorted(df["EBITDA COHORT"].unique()), key="d1_ehc")
    with c7:
        sel_zone = st.multiselect("Zone", sorted(df["ZONE MAPPING"].unique()), key="d1_zone")
    with c8:
        sel_city = st.multiselect("City", sorted(df["CITY"].unique()), key="d1_city")

    st.markdown("**Range Filters**")
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        ebitda_range = st.slider("EBITDA Range (₹)",
                                  float(df["EBITDA"].min()), float(df["EBITDA"].max()),
                                  (float(df["EBITDA"].min()), float(df["EBITDA"].max())),
                                  key="d1_er")
    with rc2:
        cm_range = st.slider("CM Range (₹)",
                              float(df["CM"].min()), float(df["CM"].max()),
                              (float(df["CM"].min()), float(df["CM"].max())),
                              key="d1_cmr")
    with rc3:
        rev_range = st.slider("Net Revenue Range (₹)",
                               float(df["NET REVENUE"].min()), float(df["NET REVENUE"].max()),
                               (float(df["NET REVENUE"].min()), float(df["NET REVENUE"].max())),
                               key="d1_rvr")

    # apply filters
    filtered = df.copy()
    if sel_store:
        filtered = filtered[filtered["STORE"].isin(sel_store)]
    if sel_month:
        filtered = filtered[filtered["MONTH"].isin(sel_month)]
    if sel_rev_cohort:
        filtered = filtered[filtered["REVENUE COHORT"].isin(sel_rev_cohort)]
    if sel_cm_cohort:
        filtered = filtered[filtered["CM COHORT"].isin(sel_cm_cohort)]
    if sel_ebitda_cat:
        filtered = filtered[filtered["EBITDA CATEGORY"].isin(sel_ebitda_cat)]
    if sel_ebitda_cohort:
        filtered = filtered[filtered["EBITDA COHORT"].isin(sel_ebitda_cohort)]
    if sel_zone:
        filtered = filtered[filtered["ZONE MAPPING"].isin(sel_zone)]
    if sel_city:
        filtered = filtered[filtered["CITY"].isin(sel_city)]
    filtered = filtered[
        (filtered["EBITDA"] >= ebitda_range[0]) & (filtered["EBITDA"] <= ebitda_range[1]) &
        (filtered["CM"] >= cm_range[0]) & (filtered["CM"] <= cm_range[1]) &
        (filtered["NET REVENUE"] >= rev_range[0]) & (filtered["NET REVENUE"] <= rev_range[1])
    ]

    # KPI row
    st.markdown("---")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Net Revenue", f"₹{filtered['NET REVENUE'].sum()/1e7:.2f} Cr")
    m2.metric("Avg GM%", f"{filtered['GM%'].mean():.1f}%" if len(filtered) else "N/A")
    m3.metric("Avg CM%", f"{filtered['CM%'].mean():.1f}%" if len(filtered) else "N/A")
    m4.metric("Total EBITDA", f"₹{filtered['EBITDA'].sum()/1e7:.2f} Cr")
    m5.metric("Stores", str(filtered["STORE"].nunique()))

    st.markdown("---")

    # charts
    ch1, ch2 = st.columns(2)
    with ch1:
        rev_month = filtered.groupby("MONTH", observed=True)["NET REVENUE"].sum().reset_index()
        fig1 = px.bar(rev_month, x="MONTH", y="NET REVENUE", title="Net Revenue by Month",
                      color_discrete_sequence=["#f5a623"])
        fig1.update_layout(**PLOT_THEME)
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        ebitda_month = filtered.groupby("MONTH", observed=True)["EBITDA"].sum().reset_index()
        fig2 = px.bar(ebitda_month, x="MONTH", y="EBITDA", title="EBITDA by Month",
                      color="EBITDA", color_continuous_scale=["red", "green"])
        fig2.update_layout(**PLOT_THEME)
        st.plotly_chart(fig2, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        fig3 = px.scatter(filtered, x="GM%", y="CM%", color="EBITDA CATEGORY",
                          hover_data=["STORE", "MONTH"],
                          title="GM% vs CM% by EBITDA Category",
                          color_discrete_map={"EBITDA +ve": "#27ae60", "EBITDA -ve": "#e74c3c"})
        fig3.update_layout(**PLOT_THEME)
        st.plotly_chart(fig3, use_container_width=True)

    with ch4:
        rc_dist = filtered.groupby("REVENUE COHORT", observed=True)["STORE"].count().reset_index()
        rc_dist.columns = ["REVENUE COHORT", "Count"]
        fig4 = px.pie(rc_dist, names="REVENUE COHORT", values="Count",
                      title="Store Count by Revenue Cohort")
        fig4.update_layout(**PLOT_THEME)
        st.plotly_chart(fig4, use_container_width=True)

    # kitchen snapshot table
    st.subheader("🏪 Kitchen Snapshot")
    snap = filtered[["STORE", "MONTH", "NET REVENUE", "GM%", "CM%", "CM",
                      "EBITDA", "EBITDA%", "REVENUE COHORT", "EBITDA CATEGORY"]].copy()
    snap["MONTH"] = snap["MONTH"].astype(str)
    snap = snap.sort_values("NET REVENUE", ascending=False).reset_index(drop=True)
    st.dataframe(snap, use_container_width=True, height=400)


# ===================== DASHBOARD 2 =====================
with tab2:
    st.subheader("Variance Filters")

    vc1, vc2 = st.columns(2)
    with vc1:
        sel_var_cat = st.multiselect("Variance Category",
                                      sorted(df["VARIANCE CATEGORY"].unique()),
                                      key="d2_vc")
    with vc2:
        sel_d2_month = st.multiselect("Month", list(df["MONTH"].cat.categories), key="d2_month")

    d2 = df.copy()
    if sel_var_cat:
        d2 = d2[d2["VARIANCE CATEGORY"].isin(sel_var_cat)]
    if sel_d2_month:
        d2 = d2[d2["MONTH"].isin(sel_d2_month)]

    month_order = ["Oct-23", "Nov-23", "Dec-23", "Jan-24", "Feb-24", "Mar-24"]
    rev_order = ["(a) Below INR 15 lacs", "(b) INR 15 to 25 lacs",
                 "(c) INR 25 to 35 lacs", "(d) INR 35 to 45 lacs", "(e) Above INR 45 lacs"]

    st.markdown("---")

    # Sub-dashboard 1
    st.subheader("Sub-Dashboard 1 – Average Variance % by Revenue Category")
    st.caption("Average variance % of kitchens under each revenue category and month")

    sub1 = d2.groupby(["REVENUE COHORT", "MONTH"], observed=True)["VARIANCE%"].mean().reset_index()
    pivot1 = sub1.pivot(index="REVENUE COHORT", columns="MONTH", values="VARIANCE%")
    pivot1 = pivot1.reindex(columns=[m for m in month_order if m in pivot1.columns])

    grand1 = d2.groupby("MONTH", observed=True)["VARIANCE%"].mean()
    grand_row1 = pd.DataFrame(
        [["Grand Total"] + [round(grand1.get(m, np.nan), 4) for m in pivot1.columns]],
        columns=["Revenue Cohort"] + list(pivot1.columns)
    )
    pivot1_r = pivot1.reset_index().rename(columns={"REVENUE COHORT": "Revenue Cohort"})
    sub1_disp = pd.concat([pivot1_r, grand_row1], ignore_index=True)

    for c in sub1_disp.columns[1:]:
        sub1_disp[c] = sub1_disp[c].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")

    st.dataframe(sub1_disp.set_index("Revenue Cohort"), use_container_width=True)

    # chart
    chart1 = sub1.copy()
    chart1["MONTH"] = chart1["MONTH"].astype(str)
    fig_s1 = px.line(chart1, x="MONTH", y="VARIANCE%", color="REVENUE COHORT",
                     title="Avg Variance % by Revenue Cohort", markers=True)
    fig_s1.update_layout(**PLOT_THEME)
    st.plotly_chart(fig_s1, use_container_width=True)

    st.markdown("---")

    # Sub-dashboard 2
    st.subheader("Sub-Dashboard 2 – Store Count by Revenue Range")
    st.caption("Count of kitchen stores per revenue bucket per month")

    sub2 = d2.groupby(["REV BUCKET", "MONTH"], observed=True)["STORE"].nunique().reset_index()
    sub2.columns = ["Revenue Bucket", "Month", "Store Count"]
    pivot2 = sub2.pivot(index="Revenue Bucket", columns="Month", values="Store Count").fillna(0).astype(int)
    pivot2 = pivot2.reindex(index=[r for r in rev_order if r in pivot2.index])
    pivot2 = pivot2.reindex(columns=[m for m in month_order if m in pivot2.columns])

    grand2 = pd.DataFrame(
        [["Grand Total"] + [int(pivot2[c].sum()) for c in pivot2.columns]],
        columns=["Revenue Bucket"] + list(pivot2.columns)
    )
    pivot2_r = pivot2.reset_index()
    sub2_disp = pd.concat([pivot2_r, grand2], ignore_index=True)
    st.dataframe(sub2_disp.set_index("Revenue Bucket"), use_container_width=True)

    # heatmap
    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot2.values,
        x=[str(c) for c in pivot2.columns],
        y=list(pivot2.index),
        colorscale="YlOrRd",
        text=pivot2.values,
        texttemplate="%{text}",
        showscale=True,
    ))
    fig_heat.update_layout(title="Store Count Heatmap – Revenue Bucket vs Month", **PLOT_THEME)
    st.plotly_chart(fig_heat, use_container_width=True)
