"""compute_periods.py - Deterministic period engine for the kick-off data request.

The kick-off data request asks the borrower for a fixed look-back of audited
financials, an LTM income statement, quarterly internal statements, a current
budget, and a long-range forecast. The exact period labels depend only on the
system date, the borrower's fiscal-year-end, and two look-back/horizon knobs.
Computing them by hand is error-prone (off-by-one on completed quarters,
calendar vs. fiscal quarter labeling), so this script owns that math. Claude
never derives these dates itself - it runs this script and consumes the output.

USAGE
-----
    python scripts/compute_periods.py --system-date YYYY-MM-DD \
        [--fiscal-year-end MM-DD] [--history-years N] [--forecast-years N]

Writes a JSON object to stdout with the period fragment strings the
populate_kickoff.py script substitutes into the template:

    {
      "audited_range":   "FY'23-'25",   # last <history_years> completed FYs
      "ltm_anchor":      "3/26",        # M/YY of the most recent completed FQE
      "quarter_label":   "Q1'26",       # fiscal quarter of the LTM anchor
      "quarterly_range": "FY'24 - Q1'26",
      "budget_fy":       "FY'26",       # current in-progress FY
      "forecast_range":  "FY'26-'30",   # budget FY through +forecast_years
      "last_completed_fy_end": "2025-12-31",
      "ltm_anchor_date":      "2026-03-31"
    }

DESIGN CONSTANTS (justified, not voodoo)
----------------------------------------
CLOSE_BUFFER_DAYS = 30
    A kick-off list is sent ~30 days before the borrower can realistically
    close its most recent quarter's books. Anchoring the LTM to the most recent
    quarter end on or before (system_date - 30d) avoids requesting a quarter the
    borrower has not yet closed. This matches the screening-templates kick-off
    convention.

DEFAULT_HISTORY_YEARS = 3
    The standard kick-off audited look-back is three fiscal years
    (per wiki/deal-templates/screening-templates.md).

DEFAULT_FORECAST_YEARS = 5
    A typical long-range model horizon is five fiscal years. forecast_years is
    a *count of years*: the forecast range runs from the budget FY through
    budget_year + forecast_years - 1 (so the default 5 yields FY'26-'30, five
    fiscal years inclusive). Configurable per deal.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, timedelta

CLOSE_BUFFER_DAYS = 30
DEFAULT_HISTORY_YEARS = 3
DEFAULT_FORECAST_YEARS = 5


def _yy(year: int) -> str:
    """Two-digit year string, zero-padded ('2026' -> '26', '2007' -> '07')."""
    return f"{year % 100:02d}"


def _add_months(d: date, months: int) -> date:
    """Shift a date by a signed number of months, clamping the day to the
    last valid day of the target month (so 3-31 minus 3 months -> 12-31)."""
    total = (d.year * 12 + (d.month - 1)) + months
    year, month = divmod(total, 12)
    month += 1
    # Clamp day to the last day of the target month.
    if month == 12:
        next_month_first = date(year + 1, 1, 1)
    else:
        next_month_first = date(year, month + 1, 1)
    last_day = (next_month_first - timedelta(days=1)).day
    return date(year, month, min(d.day, last_day))


def _fye_for_year(fiscal_year: int, fye_month: int, fye_day: int) -> date:
    """The fiscal-year-end date for the FY labeled `fiscal_year`.

    Convention: a fiscal year is labeled by the calendar year in which it ends.
    FY2025 with FYE 12-31 ends 2025-12-31; FY2025 with FYE 3-31 ends
    2025-03-31 (covering Apr-2024 .. Mar-2025).
    """
    # Clamp Feb-29 FYEs to Feb-28 in non-leap years.
    try:
        return date(fiscal_year, fye_month, fye_day)
    except ValueError:
        return _add_months(date(fiscal_year, fye_month, 1), 1) - timedelta(days=1)


def _quarter_ends(fiscal_year: int, fye_month: int, fye_day: int) -> list[date]:
    """The four fiscal-quarter-end dates of FY `fiscal_year`, ascending.
    Q4 == the FYE; Q3 = FYE-3mo; Q2 = FYE-6mo; Q1 = FYE-9mo."""
    fye = _fye_for_year(fiscal_year, fye_month, fye_day)
    return [
        _add_months(fye, -9),  # Q1
        _add_months(fye, -6),  # Q2
        _add_months(fye, -3),  # Q3
        fye,                   # Q4
    ]


@dataclass
class Periods:
    audited_range: str
    ltm_anchor: str
    quarter_label: str
    quarterly_range: str
    budget_fy: str
    forecast_range: str
    last_completed_fy_end: str
    ltm_anchor_date: str

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)


def compute_periods(
    system_date: date,
    fiscal_year_end: str = "12-31",
    history_years: int = DEFAULT_HISTORY_YEARS,
    forecast_years: int = DEFAULT_FORECAST_YEARS,
) -> Periods:
    """Compute the kick-off period fragment strings. Pure function; no I/O."""
    if history_years < 1:
        raise ValueError(f"history_years must be >= 1, got {history_years}")
    if forecast_years < 1:
        raise ValueError(f"forecast_years must be >= 1, got {forecast_years}")
    try:
        fye_month, fye_day = (int(x) for x in fiscal_year_end.split("-"))
        # Validate by constructing a date in a leap year (accepts 02-29).
        date(2000, fye_month, fye_day)
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"fiscal_year_end must be 'MM-DD' (e.g. '12-31'), got "
            f"{fiscal_year_end!r}: {exc}"
        ) from exc

    # 1. Most recent *completed* fiscal quarter end on/before the buffered date.
    buffered = system_date - timedelta(days=CLOSE_BUFFER_DAYS)
    anchor_qe: date | None = None
    anchor_fy: int = system_date.year
    anchor_q: int = 4
    # Scan the FY containing/around the buffered date and the year on either
    # side; the buffered date is always within +/-1 fiscal year of one of them.
    for fy in range(system_date.year + 1, system_date.year - 3, -1):
        for q_idx, qe in enumerate(_quarter_ends(fy, fye_month, fye_day), start=1):
            if qe <= buffered and (anchor_qe is None or qe > anchor_qe):
                anchor_qe, anchor_fy, anchor_q = qe, fy, q_idx
    if anchor_qe is None:
        raise ValueError(
            f"could not resolve a completed fiscal quarter on/before "
            f"{buffered.isoformat()} (system_date={system_date.isoformat()}, "
            f"fiscal_year_end={fiscal_year_end})"
        )

    # 2. Last completed FY = the FY whose FYE precedes the LTM anchor.
    fye_of_anchor_fy = _fye_for_year(anchor_fy, fye_month, fye_day)
    last_completed_fy = anchor_fy if anchor_qe >= fye_of_anchor_fy else anchor_fy - 1
    audited_start = last_completed_fy - history_years + 1
    if history_years == 1:
        audited_range = f"FY'{_yy(last_completed_fy)}"
    else:
        audited_range = f"FY'{_yy(audited_start)}-'{_yy(last_completed_fy)}"

    # 3. LTM anchor + quarter labels.
    ltm_anchor = f"{anchor_qe.month}/{_yy(anchor_qe.year)}"
    quarter_label = f"Q{anchor_q}'{_yy(anchor_fy)}"

    # 4. Quarterly internal / compliance range: FY'(anchor_fy - 2) -> anchor Q.
    quarterly_range = f"FY'{_yy(anchor_fy - 2)} - {quarter_label}"

    # 5. Budget FY = current in-progress FY (the FY after the last completed FY).
    budget_year = last_completed_fy + 1
    budget_fy = f"FY'{_yy(budget_year)}"
    forecast_end = budget_year + forecast_years - 1
    forecast_range = f"FY'{_yy(budget_year)}-'{_yy(forecast_end)}"

    return Periods(
        audited_range=audited_range,
        ltm_anchor=ltm_anchor,
        quarter_label=quarter_label,
        quarterly_range=quarterly_range,
        budget_fy=budget_fy,
        forecast_range=forecast_range,
        last_completed_fy_end=_fye_for_year(
            last_completed_fy, fye_month, fye_day
        ).isoformat(),
        ltm_anchor_date=anchor_qe.isoformat(),
    )


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Kick-off data request period engine.")
    p.add_argument("--system-date", required=True, help="System date, YYYY-MM-DD.")
    p.add_argument(
        "--fiscal-year-end",
        default="12-31",
        help="Borrower fiscal-year-end as MM-DD (default 12-31).",
    )
    p.add_argument(
        "--history-years",
        type=int,
        default=DEFAULT_HISTORY_YEARS,
        help=f"Audited look-back in FYs (default {DEFAULT_HISTORY_YEARS}).",
    )
    p.add_argument(
        "--forecast-years",
        type=int,
        default=DEFAULT_FORECAST_YEARS,
        help=f"Forecast horizon in FYs (default {DEFAULT_FORECAST_YEARS}).",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> None:
    args = _parse_args(argv)
    try:
        sys_date = date.fromisoformat(args.system_date)
    except ValueError as exc:
        sys.stderr.write(f"ERROR: --system-date must be YYYY-MM-DD: {exc}\n")
        sys.exit(2)
    try:
        periods = compute_periods(
            sys_date,
            fiscal_year_end=args.fiscal_year_end,
            history_years=args.history_years,
            forecast_years=args.forecast_years,
        )
    except ValueError as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        sys.exit(2)
    print(periods.to_json())


if __name__ == "__main__":
    main(sys.argv[1:])
