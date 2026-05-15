## Contents

- STEP 13 — POPULATE THE TEMPLATE
  - Content dict schema (top-level keys)
  - Run snippet (write JSON, invoke `scripts/populate_memo.py`)
  - Bullet-format conventions (`"Header: detail"` split; exact prefix labels)
  - Out of scope (analyst-populated charts; the `su_note` exception)

---

## STEP 13 — POPULATE THE TEMPLATE

After drafting all section content, build a single content dict, write it to a
JSON file, and run `scripts/populate_memo.py`. The script edits the bundled
template at `assets/posting-memo-template.docx` in-place (preserving Word
auto-numbering, bold-prefix run formatting, and italic+underline-prefix run
formatting in multi-paragraph cells) and saves a populated copy.

**Schema:** see the docstring at the top of `scripts/populate_memo.py` for the
complete content dict schema. Top-level keys: `header`, `situation_overview`,
`company_overview` (with `opening` + `bullets`), `financial_headline`,
`discussion_analysis`, `su_note`, `risk_flags`, `strengths`, `considerations`,
`recommendation`, `designated_criteria`, `posting_rating`, `final_rating`.

**Run:**

```python
import json, subprocess
from pathlib import Path

Path("/tmp/posting_memo_content.json").write_text(json.dumps(content, indent=2))
output_path = "/mnt/user-data/outputs/<DealName>_-_Overland_Posting_Memo_<MM-DD-YY>_vS.docx"
subprocess.run(
    ["python", "scripts/populate_memo.py", "/tmp/posting_memo_content.json", output_path],
    check=True,
)
```

Then return the output via `present_files`.

**Bullet-format conventions** — Strengths, Considerations, Discussion & Analysis,
and Company Overview bullets all use the `"Header: detail"` convention. The
script splits at the first `": "` and routes the prefix into the formatted
header run (bold for Strengths/Considerations; italic+underline for D&A and
Company Overview bullets) and the remainder into the regular body run.

Use the exact prefix labels:
- **D&A**: `M&A / Organic Results`, `Revenue`, `Gross Profit`,
  `CA EBITDA & Adjustments`, `Capex`, `NWC`
- **Company Overview**: `TAM & Market Share`, `Products / Services`, `Customers`,
  `Suppliers`, `Labor / Raw Materials`, `Operations / Facilities`

**Out of scope** (analyst populates manually after running this skill):
- Historical Financial Summary chart cell (left column of D&A row)
- Sources & Uses chart and Pro Forma Capitalization chart
- Appendix chart placeholders (Sellside QoE, Customer/Supplier/Employee Overviews)

The `Note: [X]` annotation directly below the S&U chart IS populated from
`su_note` (only the first occurrence — appendix `Note: [X]` placeholders are
intentionally left untouched).
