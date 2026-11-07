"""Small-sample guardrailed comparison for two-variant conversion tests."""
import math


def analyze_two_variant(control_visitors, control_conversions, variant_visitors, variant_conversions, alpha=0.05):
    """Compare two binomial conversion rates with a pooled two-sided z test.

    The normal approximation is withheld when expected successes or failures
    in either group are below five. This is a descriptive estimate and does
    not account for sequential peeking or multiple comparisons.
    """
    values = (control_visitors, control_conversions, variant_visitors, variant_conversions)
    if any(int(value) != value for value in values):
        raise ValueError("Visitor and conversion counts must be whole numbers.")
    nc, xc, nv, xv = map(int, values)
    if nc < 1 or nv < 1:
        raise ValueError("Each variant needs at least one visitor.")
    if xc < 0 or xv < 0 or xc > nc or xv > nv:
        raise ValueError("Conversions must be between zero and the visitor count.")
    if not 0 < alpha < 1:
        raise ValueError("Alpha must be between zero and one.")

    pc = xc / nc
    pv = xv / nv
    pooled = (xc + xv) / (nc + nv)
    expected = [nc * pooled, nc * (1 - pooled), nv * pooled, nv * (1 - pooled)]
    adequate = min(expected) >= 5
    se = math.sqrt(pooled * (1 - pooled) * (1 / nc + 1 / nv)) if 0 < pooled < 1 else 0
    z_score = (pv - pc) / se if adequate and se else None
    p_value = math.erfc(abs(z_score) / math.sqrt(2)) if z_score is not None else None
    absolute_lift = pv - pc
    relative_lift = absolute_lift / pc if pc else None
    significant = p_value is not None and p_value < alpha
    if not adequate:
        interpretation = "insufficient sample for the normal-approximation significance estimate"
    elif significant and absolute_lift > 0:
        interpretation = "variant conversion rate is higher at the selected significance threshold"
    elif significant and absolute_lift < 0:
        interpretation = "variant conversion rate is lower at the selected significance threshold"
    else:
        interpretation = "no statistically detectable difference at the selected significance threshold"

    return {
        "control_rate": pc,
        "variant_rate": pv,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "z_score": z_score,
        "p_value": p_value,
        "alpha": alpha,
        "significant": significant,
        "sample_adequate": adequate,
        "interpretation": interpretation,
    }
