"""Reusable analysis functions for Rosa's Pizza Assignment 1."""

import numpy as np

from starter import COSTS, TIME_BLOCKS, ZONES, delivery_times


def percentageLate(zone, time_block, promise):
    zones = ZONES if zone == "all" else [zone]
    time_blocks = TIME_BLOCKS if time_block == "all" else [time_block]
    late = 0
    total = 0

    for selected_zone in zones:
        for selected_block in time_blocks:
            times = delivery_times(selected_zone, selected_block, promise, seed=42)
            total += len(times)
            late += int(np.count_nonzero(times > promise))

    return round(late / total * 100) if total else 0


def averageDeliveryTime(zone, time_block, promise):
    zones = ZONES if zone == "all" else [zone]
    time_blocks = TIME_BLOCKS if time_block == "all" else [time_block]
    minutes_total = 0.0
    total = 0

    for selected_zone in zones:
        for selected_block in time_blocks:
            times = delivery_times(selected_zone, selected_block, promise, seed=42)
            total += len(times)
            minutes_total += float(np.sum(times))

    return round(minutes_total / total) if total else 0


def costPerLateOrder(costs):
    return costs["refund"] + costs["margin"] * costs["churn_orders"]


def evaluatePromiseTimes(zone, time_block, promiseTimes, costs):
    """Return notebook-style simulated profit results for each candidate time."""
    results = []
    late_cost = costPerLateOrder(costs)

    for promise in promiseTimes:
        times = delivery_times(zone, time_block, promise, seed=42)
        order_count = len(times)
        late_count = int(np.count_nonzero(times > promise))
        profit = order_count * costs["margin"] - late_count * late_cost
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


def costPerPromiseTime(zone, time_block, promiseTimes, costs):
    results = evaluatePromiseTimes(zone, time_block, promiseTimes, costs)
    if not results:
        raise ValueError("promiseTimes must contain at least one candidate")
    return max(results, key=lambda result: result["Estimated profit ($)"])


def main():
    print(
        "Scenario 1, zone and time block provided:",
        percentageLate("Central", "Fri/Sat eve", 45),
        "% late",
    )
    print(
        "Scenario 2, zone is all and time block is provided:",
        percentageLate("all", "Lunch", 45),
        "% late",
    )
    print(
        "Scenario 3, zone is provided and time block is all:",
        percentageLate("North", "all", 45),
        "% late",
    )
    print(
        "Scenario 4, zone and time block are all:",
        percentageLate("all", "all", 45),
        "% late",
    )
    print("Late cost per order:", costPerLateOrder(COSTS))

    promise_times = list(range(3, 61, 3))
    best = costPerPromiseTime("Central", "Fri/Sat eve", promise_times, COSTS)
    print(
        f"Best promise for Central, Fri/Sat eve: "
        f"{best['Promise (minutes)']} minutes "
        f"(${best['Estimated profit ($)']:.2f} estimated profit)"
    )


if __name__ == "__main__":
    main()