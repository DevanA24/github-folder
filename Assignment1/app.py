"""Streamlit app for optimizing Rosa's Pizza delivery promises."""

from __future__ import annotations

import numpy as np
import streamlit as st

from starter import TIME_BLOCKS, ZONES, delivery_times


SIMULATION_SEED = 42


def evaluate_promises(
    zone: str,
    time_block: str,
    promise_times: list[int],
    margin: float,
    churn_orders: float,
    refund: float,
) -> list[dict[str, float | int]]:
    """Return simulated order and profit results for each promise time."""
    late_cost = refund + margin * churn_orders
    results = []

    for promise in promise_times:
        times = delivery_times(zone, time_block, promise, seed=SIMULATION_SEED)
        order_count = len(times)
        late_count = int(np.count_nonzero(times > promise))
        profit = order_count * margin - late_count * late_cost
        results.append(
            {
                "Promise (minutes)": promise,
                "Orders": order_count,
                "Late orders": late_count,
                "Late rate (%)": round(late_count / order_count * 100, 1)
                if order_count
                else 0.0,
                "Estimated profit ($)": round(profit, 2),
            }
        )

    return results


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
            "Profit margin ($)", min_value=0.0, value=9.0, step=0.5
        )
    with churn_col:
        churn_orders = st.number_input(
            "Future orders lost per late order",
            min_value=0.0,
            value=1.8,
            step=0.1,
        )
    with refund_col:
        refund = st.number_input(
            "Refund cost per late order ($)", min_value=0.0, value=10.0, step=1.0
        )

    submitted = st.form_submit_button("Find best promise", type="primary")

if submitted:
    promise_times = list(range(min_promise, max_promise + 1, promise_step))
    if promise_times[-1] != max_promise:
        promise_times.append(max_promise)

    results = evaluate_promises(
        zone, time_block, promise_times, margin, churn_orders, refund
    )
    best_result = max(results, key=lambda result: result["Estimated profit ($)"])

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