"""Streamlit app for optimizing Rosa's Pizza delivery promises."""

from __future__ import annotations

import streamlit as st

from assignment1 import (
    COSTS,
    TIME_BLOCKS,
    ZONES,
    costPerPromiseTime,
    evaluatePromiseTimes,
)


st.set_page_config(page_title="Rosa's Pizza | Delivery Promise", page_icon="🍕")
st.title("Rosa's Pizza")
st.subheader("Delivery promise optimizer")
st.write("Compare estimated profit across delivery promise times.")

with st.form("optimization_inputs"):
    location_col, schedule_col = st.columns(2)
    with location_col:
        zone = st.selectbox("Zone", ZONES)
    with schedule_col:
        time_block = st.selectbox("Time block", TIME_BLOCKS)

    st.markdown("**Promise times to evaluate**")
    range_col, step_col = st.columns(2)
    with range_col:
        min_promise, max_promise = st.slider(
            "Range (minutes)", min_value=1, max_value=120, value=(3, 60)
        )
    with step_col:
        promise_step = st.number_input(
            "Interval (minutes)", min_value=1, max_value=30, value=3
        )

    st.markdown("**Per-order economics**")
    margin_col, churn_col, refund_col = st.columns(3)
    with margin_col:
        margin = st.number_input(
            "Profit margin ($)", min_value=0.0, value=COSTS["margin"], step=0.5
        )
    with churn_col:
        churn_orders = st.number_input(
            "Future orders lost per late order",
            min_value=0.0,
            value=COSTS["churn_orders"],
            step=0.1,
        )
    with refund_col:
        refund = st.number_input(
            "Refund cost per late order ($)",
            min_value=0.0,
            value=COSTS["refund"],
            step=1.0,
        )

    submitted = st.form_submit_button("Find best promise", type="primary")

if submitted:
    promise_times = list(range(min_promise, max_promise + 1, promise_step))
    if promise_times[-1] != max_promise:
        promise_times.append(max_promise)

    costs = {
        "margin": margin,
        "churn_orders": churn_orders,
        "refund": refund,
    }
    results = evaluatePromiseTimes(zone, time_block, promise_times, costs)
    best_result = costPerPromiseTime(zone, time_block, promise_times, costs)

    st.success(
        f"Recommended promise: {best_result['Promise (minutes)']} minutes "
        f"for {zone}, {time_block}."
    )
    metric_col, orders_col, late_col = st.columns(3)
    metric_col.metric("Estimated profit", f"${best_result['Estimated profit ($)']:,.2f}")
    orders_col.metric("Estimated orders", best_result["Orders"])
    late_col.metric("Late-order rate", f"{best_result['Late rate (%)']:.1f}%")

    st.dataframe(
        results,
        hide_index=True,
        use_container_width=True,
    )