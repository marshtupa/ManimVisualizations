from dataclasses import dataclass
import math

from manim import *


@dataclass
class MetricExample:
    label: str
    p1: float   # conversion in version 1, in [0, 1]
    n1: int
    p2: float   # conversion in version 2, in [0, 1]
    n2: int


def proportion_ci(p: float, n: int, z: float = 1.96):
    margin = z * math.sqrt(p * (1 - p) / n)
    return p - margin, p + margin, margin


def diff_ci(p1: float, n1: int, p2: float, n2: int, z: float = 1.96):
    delta = p2 - p1
    margin = z * math.sqrt(
        p1 * (1 - p1) / n1 +
        p2 * (1 - p2) / n2
    )
    return delta - margin, delta + margin, delta, margin


def pct(value: float, decimals: int = 1, signed: bool = False):
    if signed:
        return f"{value:+.{decimals}f}%"
    return f"{value:.{decimals}f}%"


class CompareTwoConversions(Scene):
    BG = "#0F1220"
    V1_COLOR = BLUE_C
    V2_COLOR = GREEN_C
    DELTA_COLOR = YELLOW_C
    ZERO_COLOR = RED_C

    def construct(self):
        self.camera.background_color = self.BG

        significant_example = MetricExample(
            label="Onboarding completion",
            p1=0.868,
            n1=6240,
            p2=0.823,
            n2=15648,
        )

        nonsignificant_example = MetricExample(
            label="Sent at least 10 messages",
            p1=0.162,
            n1=6240,
            p2=0.153,
            n2=15648,
        )

        self.show_intro()
        self.show_single_conversion_intervals(significant_example)
        self.show_difference_interval(significant_example, title_text="Example 1: statistically significant")
        self.show_difference_interval(
            nonsignificant_example,
            title_text="Example 2: not statistically significant",
            replace=True,
        )
        self.show_outro()

    def show_intro(self):
        title = Text(
            "Comparing two conversion rates",
            font_size=42,
            weight=BOLD,
        )
        subtitle = Text(
            "Observed conversions, confidence intervals, and significance of the gap",
            font_size=24,
            color=GRAY_B,
        ).next_to(title, DOWN, buff=0.2)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
        self.wait(0.7)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_single_conversion_intervals(self, ex: MetricExample):
        ci1_lo, ci1_hi, _ = proportion_ci(ex.p1, ex.n1)
        ci2_lo, ci2_hi, _ = proportion_ci(ex.p2, ex.n2)

        formula = MathTex(
            r"CI_{95\%}(p)=p \pm 1.96\sqrt{\frac{p(1-p)}{n}}",
            font_size=42,
        ).to_edge(UP)

        label = Text(
            f"Each observed conversion is only an estimate of the true conversion",
            font_size=24,
            color=GRAY_B,
        ).next_to(formula, DOWN, buff=0.25)

        x_min = math.floor(min(ci1_lo, ci2_lo) * 100) - 1
        x_max = math.ceil(max(ci1_hi, ci2_hi) * 100) + 1

        rate1 = self.make_rate_visual(
            "Version 1",
            ex.p1 * 100,
            ci1_lo * 100,
            ci1_hi * 100,
            self.V1_COLOR,
            x_min=x_min,
            x_max=x_max,
        )
        rate2 = self.make_rate_visual(
            "Version 2",
            ex.p2 * 100,
            ci2_lo * 100,
            ci2_hi * 100,
            self.V2_COLOR,
            x_min=x_min,
            x_max=x_max,
        )

        rates = VGroup(rate1, rate2).arrange(DOWN, buff=0.9)
        rates.next_to(label, DOWN, buff=0.6)

        self.play(Write(formula), FadeIn(label, shift=UP * 0.2))
        self.play(FadeIn(rate1, shift=RIGHT * 0.2), FadeIn(rate2, shift=LEFT * 0.2))
        self.play(
            Indicate(rate1[2], color=self.V1_COLOR, scale_factor=1.05),
            Indicate(rate2[2], color=self.V2_COLOR, scale_factor=1.05),
        )
        self.wait(1.0)

        self.single_formula = formula
        self.single_label = label
        self.rates_group = rates

    def show_difference_interval(self, ex: MetricExample, title_text: str, replace: bool = False):
        ci_lo, ci_hi, delta, _ = diff_ci(ex.p1, ex.n1, ex.p2, ex.n2)

        diff_formula_group = VGroup(
            MathTex(r"\Delta = p_2 - p_1", font_size=42),
            MathTex(
                r"CI_{95\%}(\Delta)=\Delta \pm 1.96\sqrt{\frac{p_1(1-p_1)}{n_1}+\frac{p_2(1-p_2)}{n_2}}",
                font_size=34,
            ),
        ).arrange(DOWN, buff=0.25).to_edge(UP)

        top_label = Text(
            title_text,
            font_size=28,
            weight=BOLD,
            color=WHITE,
        ).next_to(diff_formula_group, DOWN, buff=0.25)

        observed_gap = Text(
            f"Observed gap = {pct(delta * 100, 1, signed=True)} p.p.",
            font_size=28,
            color=self.DELTA_COLOR,
        ).next_to(top_label, DOWN, buff=0.3)

        x_min = min(-1, math.floor(ci_lo * 100) - 1)
        x_max = max(1, math.ceil(ci_hi * 100) + 1)

        diff_visual, status_group = self.make_diff_visual(
            delta_pct=delta * 100,
            ci_lo_pct=ci_lo * 100,
            ci_hi_pct=ci_hi * 100,
            x_min=x_min,
            x_max=x_max,
        )
        diff_visual.next_to(observed_gap, DOWN, buff=0.6)
        status_group.next_to(diff_visual, DOWN, buff=0.45)

        if not replace:
            self.play(
                FadeOut(self.rates_group, shift=DOWN * 0.2),
                FadeOut(self.single_label),
                ReplacementTransform(self.single_formula, diff_formula_group),
            )
            self.play(FadeIn(top_label, shift=UP * 0.2))
            self.play(FadeIn(observed_gap, shift=UP * 0.2))
            self.play(FadeIn(diff_visual, shift=UP * 0.2))
            self.play(FadeIn(status_group, shift=UP * 0.2))
            self.play(Circumscribe(status_group, color=status_group[0].get_color()))
            self.wait(1.2)

            self.diff_formula_group = diff_formula_group
            self.top_label = top_label
            self.observed_gap = observed_gap
            self.diff_visual = diff_visual
            self.status_group = status_group
        else:
            new_group = VGroup(diff_formula_group, top_label, observed_gap, diff_visual, status_group)
            old_group = VGroup(
                self.diff_formula_group,
                self.top_label,
                self.observed_gap,
                self.diff_visual,
                self.status_group,
            )
            self.play(ReplacementTransform(old_group, new_group))
            self.play(Circumscribe(status_group, color=status_group[0].get_color()))
            self.wait(1.2)

            self.diff_formula_group = diff_formula_group
            self.top_label = top_label
            self.observed_gap = observed_gap
            self.diff_visual = diff_visual
            self.status_group = status_group

    def show_outro(self):
        summary = VGroup(
            Text("Decision rule", font_size=34, weight=BOLD),
            Text("CI of the difference does not cross 0  →  statistically significant", font_size=24),
            Text("CI of the difference crosses 0         →  may be noise", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        summary_box = SurroundingRectangle(summary, buff=0.35, corner_radius=0.15, color=WHITE)
        summary_group = VGroup(summary_box, summary).scale(0.9)
        summary_group.to_edge(DOWN)

        self.play(FadeIn(summary_group, shift=UP * 0.25))
        self.wait(2)

    def make_rate_visual(
        self,
        label: str,
        center_pct: float,
        ci_lo_pct: float,
        ci_hi_pct: float,
        color,
        x_min: float,
        x_max: float,
    ):
        number_line = NumberLine(
            x_range=[x_min, x_max, 1],
            length=8,
            include_numbers=True,
            include_tip=False,
            decimal_number_config={"num_decimal_places": 0, "font_size": 22},
        )

        title = Text(label, font_size=28, weight=BOLD, color=color)
        title.next_to(number_line, UP, buff=0.3).align_to(number_line, LEFT)

        interval = Line(
            number_line.n2p(ci_lo_pct),
            number_line.n2p(ci_hi_pct),
            color=color,
            stroke_width=12,
        )

        lo_dot = Dot(number_line.n2p(ci_lo_pct), radius=0.05, color=color)
        hi_dot = Dot(number_line.n2p(ci_hi_pct), radius=0.05, color=color)
        center_dot = Dot(number_line.n2p(center_pct), radius=0.09, color=color)

        center_label = Text(
            pct(center_pct, 1),
            font_size=24,
            color=color,
        ).next_to(center_dot, UP, buff=0.18)

        ci_label = Text(
            f"95% CI: [{pct(ci_lo_pct, 2)} ; {pct(ci_hi_pct, 2)}]",
            font_size=22,
            color=color,
        ).next_to(number_line, DOWN, buff=0.22)

        return VGroup(
            title,
            number_line,
            interval,
            lo_dot,
            hi_dot,
            center_dot,
            center_label,
            ci_label,
        )

    def make_diff_visual(
        self,
        delta_pct: float,
        ci_lo_pct: float,
        ci_hi_pct: float,
        x_min: float,
        x_max: float,
    ):
        number_line = NumberLine(
            x_range=[x_min, x_max, 1],
            length=8.5,
            include_numbers=True,
            include_tip=False,
            decimal_number_config={"num_decimal_places": 0, "font_size": 22},
        )

        zero_anchor = number_line.n2p(0)
        zero_line = DashedLine(
            zero_anchor + UP * 0.7,
            zero_anchor + DOWN * 0.7,
            color=self.ZERO_COLOR,
            dash_length=0.08,
        )
        zero_label = Text("0", font_size=24, color=self.ZERO_COLOR).next_to(zero_line, UP, buff=0.08)

        interval = Line(
            number_line.n2p(ci_lo_pct),
            number_line.n2p(ci_hi_pct),
            color=self.DELTA_COLOR,
            stroke_width=12,
        )
        lo_dot = Dot(number_line.n2p(ci_lo_pct), radius=0.05, color=self.DELTA_COLOR)
        hi_dot = Dot(number_line.n2p(ci_hi_pct), radius=0.05, color=self.DELTA_COLOR)
        center_dot = Dot(number_line.n2p(delta_pct), radius=0.09, color=self.DELTA_COLOR)

        delta_label = Text(
            pct(delta_pct, 1, signed=True),
            font_size=24,
            color=self.DELTA_COLOR,
        ).next_to(center_dot, UP, buff=0.18)

        ci_label = Text(
            f"95% CI of the gap: [{pct(ci_lo_pct, 2, signed=True)} ; {pct(ci_hi_pct, 2, signed=True)}]",
            font_size=22,
            color=self.DELTA_COLOR,
        ).next_to(number_line, DOWN, buff=0.24)

        crosses_zero = ci_lo_pct <= 0 <= ci_hi_pct

        if crosses_zero:
            status_text = Text(
                "CI crosses zero  →  not statistically significant",
                font_size=24,
                color=RED_B,
                weight=BOLD,
            )
            status_box = SurroundingRectangle(
                status_text,
                buff=0.2,
                color=RED_B,
                corner_radius=0.15,
            )
        else:
            status_text = Text(
                "CI does not cross zero  →  statistically significant",
                font_size=24,
                color=GREEN_B,
                weight=BOLD,
            )
            status_box = SurroundingRectangle(
                status_text,
                buff=0.2,
                color=GREEN_B,
                corner_radius=0.15,
            )

        diff_visual = VGroup(
            number_line,
            zero_line,
            zero_label,
            interval,
            lo_dot,
            hi_dot,
            center_dot,
            delta_label,
            ci_label,
        )
        status_group = VGroup(status_box, status_text)

        return diff_visual, status_group