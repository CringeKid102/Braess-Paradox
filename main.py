from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ----------------------------
# 1. Model parameters
# ----------------------------
TOTAL_DRIVERS = 4000
CONGESTION_DIVISOR = 100
FIXED_ROAD_TIME = 45
SHORTCUT_TIME = 0

OUTPUT_DIR = Path.cwd()
TXT_PATH = OUTPUT_DIR / "braess_paradox_tok_explanation.txt"
PNG_PATH = OUTPUT_DIR / "braess_paradox_tok_map.png"


def congested_time(flow: int) -> float:
    """Travel time, in minutes, for a congestion-sensitive road."""
    return flow / CONGESTION_DIVISOR


def main() -> None:
    # ----------------------------
    # 2. Calculate Scenario A:
    #    no shortcut; traffic splits evenly
    # ----------------------------
    upper_flow = TOTAL_DRIVERS // 2
    lower_flow = TOTAL_DRIVERS - upper_flow

    upper_route_time = congested_time(upper_flow) + FIXED_ROAD_TIME
    lower_route_time = FIXED_ROAD_TIME + congested_time(lower_flow)

    average_without = (
        upper_flow * upper_route_time + lower_flow * lower_route_time
    ) / TOTAL_DRIVERS

    # ----------------------------
    # 3. Calculate Scenario B:
    #    shortcut exists; all drivers use it at equilibrium
    # ----------------------------
    shortcut_route_time = (
        congested_time(TOTAL_DRIVERS)
        + SHORTCUT_TIME
        + congested_time(TOTAL_DRIVERS)
    )

    upper_only_time = congested_time(TOTAL_DRIVERS) + FIXED_ROAD_TIME
    lower_only_time = FIXED_ROAD_TIME + congested_time(TOTAL_DRIVERS)

    average_with = shortcut_route_time
    change = average_with - average_without

    # ----------------------------
    # 4. Print results
    # ----------------------------
    print("=" * 58)
    print("BRAESS'S PARADOX — TOK ESSAY SIMULATION")
    print("=" * 58)
    print(f"Total drivers: {TOTAL_DRIVERS:,}")
    print("\nSCENARIO A — WITHOUT SHORTCUT")
    print(f"Upper route: {upper_flow:,} drivers, {upper_route_time:.1f} min")
    print(f"Lower route: {lower_flow:,} drivers, {lower_route_time:.1f} min")
    print(f"Average trip time: {average_without:.1f} min")

    print("\nSCENARIO B — WITH SHORTCUT")
    print(
        f"Shortcut route: {TOTAL_DRIVERS:,} drivers, "
        f"{shortcut_route_time:.1f} min"
    )
    print(f"Upper-only alternative: {upper_only_time:.1f} min")
    print(f"Lower-only alternative: {lower_only_time:.1f} min")
    print(f"Average trip time: {average_with:.1f} min")
    print(f"Change per driver: +{change:.1f} min")

    # ----------------------------
    # 5. Write the explanatory TXT
    # ----------------------------
    explanation = f"""BRAESS'S PARADOX — RESULTS AND TOK CONNECTION
================================================

What the model represents
-------------------------
This simplified model represents {TOTAL_DRIVERS:,} drivers travelling from
Start to End. A congested road takes traffic_flow / {CONGESTION_DIVISOR}
minutes, each fixed-time road takes {FIXED_ROAD_TIME} minutes, and the
shortcut takes {SHORTCUT_TIME} minutes.

Numerical results
-----------------
SCENARIO A — WITHOUT THE SHORTCUT
- {upper_flow:,} drivers use the upper route.
- {lower_flow:,} drivers use the lower route.
- Upper route time: {upper_route_time:.1f} minutes.
- Lower route time: {lower_route_time:.1f} minutes.
- Average journey time: {average_without:.1f} minutes.

SCENARIO B — WITH THE SHORTCUT
- At the model's selfish-route-choice equilibrium, all {TOTAL_DRIVERS:,}
  drivers use Start -> Upper -> Lower -> End.
- The first congested road takes {congested_time(TOTAL_DRIVERS):.1f} minutes.
- The shortcut takes {SHORTCUT_TIME} minutes.
- The second congested road takes {congested_time(TOTAL_DRIVERS):.1f} minutes.
- Total journey time: {shortcut_route_time:.1f} minutes.
- The upper-only and lower-only alternatives each take
  {upper_only_time:.1f} and {lower_only_time:.1f} minutes respectively.
- Average journey time: {average_with:.1f} minutes.

COMPARISON
----------
Adding the shortcut increases the modelled average journey time from
{average_without:.1f} to {average_with:.1f} minutes: an increase of
{change:.1f} minutes per driver (about {change / average_without * 100:.1f}%).

Why this matters for a TOK essay
--------------------------------
The result challenges the intuitive claim that adding a road must improve
traffic. It shows what follows from a specific mathematical model and its
assumptions. The Python program makes the result observable and repeatable,
but the output is not independent proof that every real road network will
behave this way.

Limitations and evaluation
--------------------------
1. The model assumes drivers choose routes to minimize their own journey time.
2. It uses simplified road-time functions and a zero-time shortcut.
3. It assumes the traffic pattern reaches equilibrium.
4. Real drivers, road layouts, traffic signals, incidents, and changing demand
   can make actual traffic behave differently.

TOK interpretation:
Mathematics establishes the result within the model; applying that result to
the real world requires checking whether the assumptions are realistic and
comparing the model with empirical traffic evidence.
"""
    TXT_PATH.write_text(explanation, encoding="utf-8")

    # ----------------------------
    # 6. Draw a network map PNG
    # ----------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    positions = {
        "Start": (0.0, 0.0),
        "Upper": (1.0, 1.0),
        "Lower": (1.0, -1.0),
        "End": (2.0, 0.0),
    }

    def draw_arrow(ax, start, end, label, label_offset=(0, 0), color="#486581",
                   rad=0.0, linewidth=2.0):
        x1, y1 = positions[start]
        x2, y2 = positions[end]
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=linewidth,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=24,
            shrinkB=24,
        )
        ax.add_patch(arrow)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(
            mx + label_offset[0], my + label_offset[1], label,
            ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor="none", alpha=0.92),
        )

    def setup_axis(ax, title, subtitle):
        ax.set_xlim(-0.35, 2.35)
        ax.set_ylim(-1.55, 1.55)
        ax.axis("off")
        ax.set_title(title, fontsize=14, weight="bold", pad=14)
        ax.text(1.0, -1.42, subtitle, ha="center", va="center",
                fontsize=9, wrap=True)

    # Left: without shortcut
    ax = axes[0]
    setup_axis(
        ax,
        "A. WITHOUT THE SHORTCUT",
        f"Equilibrium: {upper_flow:,} drivers per route; average = "
        f"{average_without:.0f} min",
    )
    draw_arrow(ax, "Start", "Upper",
               f"{upper_flow:,} drivers\n{congested_time(upper_flow):.0f} min",
               (0.0, 0.15))
    draw_arrow(ax, "Upper", "End", f"{FIXED_ROAD_TIME} min", (0.0, 0.12))
    draw_arrow(ax, "Start", "Lower", f"{FIXED_ROAD_TIME} min", (0.0, -0.12))
    draw_arrow(ax, "Lower", "End",
               f"{lower_flow:,} drivers\n{congested_time(lower_flow):.0f} min",
               (0.0, -0.15))

    # Right: with shortcut
    ax = axes[1]
    setup_axis(
        ax,
        "B. WITH THE SHORTCUT",
        f"Selfish-route equilibrium: {TOTAL_DRIVERS:,} use shortcut route; "
        f"average = {average_with:.0f} min",
    )
    draw_arrow(ax, "Start", "Upper",
               f"{TOTAL_DRIVERS:,} drivers\n{congested_time(TOTAL_DRIVERS):.0f} min",
               (0.0, 0.15))
    draw_arrow(ax, "Upper", "End", f"{FIXED_ROAD_TIME} min", (0.0, 0.12))
    draw_arrow(ax, "Start", "Lower", f"{FIXED_ROAD_TIME} min", (0.0, -0.12))
    draw_arrow(ax, "Lower", "End",
               f"{TOTAL_DRIVERS:,} drivers\n{congested_time(TOTAL_DRIVERS):.0f} min",
               (0.0, -0.15))
    draw_arrow(ax, "Upper", "Lower",
               f"SHORTCUT: {SHORTCUT_TIME} min",
               (-0.30, 0.0), color="#c05621", rad=-0.28, linewidth=2.8)

    # Draw nodes after roads so they appear on top.
    for ax in axes:
        for name, (x, y) in positions.items():
            ax.scatter([x], [y], s=850, color="#e6f0f7",
                       edgecolor="#486581", linewidth=1.5, zorder=5)
            ax.text(x, y, name, ha="center", va="center",
                    fontsize=9, weight="bold", zorder=6)

    fig.suptitle(
        "Braess's Paradox: when adding a road increases journey time",
        fontsize=16, weight="bold", y=0.98,
    )
    fig.text(
        0.5, 0.02,
        "TOK focus: a model can challenge intuition, but its conclusions depend "
        "on assumptions and need real-world validation.",
        ha="center", fontsize=10,
    )
    fig.tight_layout(rect=[0.02, 0.07, 0.98, 0.92])
    fig.savefig(PNG_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("\nFiles created:")
    print(f"  Text explanation: {TXT_PATH}")
    print(f"  Network map PNG:  {PNG_PATH}")


if __name__ == "__main__":
    main()