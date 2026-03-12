from __future__ import annotations

from manim import *


class CentralLimitTheoremScene(Scene):
    def construct(self) -> None:
        title = Text("Central Limit Theorem", weight=BOLD).to_edge(UP)
        subtitle = Text(
            "Means of uniform samples approach a normal distribution",
            font_size=28,
        ).next_to(title, DOWN, buff=0.25)

        self.play(Write(title), FadeIn(subtitle, shift=0.2 * DOWN))
        self.wait(0.5)

        sample_sizes = [1, 2, 5, 10, 30]
        colors = [BLUE_D, GREEN_D, TEAL_D, YELLOW_D, RED_D]
        previous_chart: BarChart | None = None
        previous_caption: Text | None = None

        for sample_size, color in zip(sample_sizes, colors):
            means = np.mean(np.random.uniform(0, 1, size=(4000, sample_size)), axis=1)
            hist, _ = np.histogram(means, bins=24, range=(0, 1), density=True)
            values = np.clip(hist, 0, 8)

            chart = BarChart(
                values=list(values),
                y_range=[0, 8, 2],
                x_length=10.0,
                y_length=4.5,
                bar_width=1.0,
                bar_fill_opacity=0.85,
                bar_stroke_width=0.5,
                bar_colors=[color],
                y_axis_config={"font_size": 20, "label_constructor": Text},
            )
            chart.next_to(subtitle, DOWN, buff=0.5)

            caption = Text(f"Sample size n = {sample_size}", font_size=32).next_to(
                chart, DOWN, buff=0.4
            )

            if previous_chart is None:
                self.play(Create(chart), FadeIn(caption, shift=0.2 * UP), run_time=1.5)
            else:
                self.play(
                    ReplacementTransform(previous_chart, chart),
                    ReplacementTransform(previous_caption, caption),
                    run_time=1.2,
                )

            previous_chart = chart
            previous_caption = caption
            self.wait(0.35)

        closing = Text(
            "As n grows, the histogram becomes bell-shaped",
            font_size=30,
            color=YELLOW_A,
        ).to_edge(DOWN)
        self.play(FadeIn(closing, shift=0.2 * UP))
        self.wait(1.5)
