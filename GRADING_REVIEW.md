# COMP1110 Project Grading Review

Review date: 2026-05-01  
Reviewer role: simulated grader / requirements checker  
Target topic: Topic C, Restaurant Queue Simulation  
Guideline source: `D:\ylj\HKU\2025-2026\COMP1110\Project\COMP1110 Project Guidelines.pdf` and the adjacent extracted Markdown copy  
Repository reviewed: `D:\ylj\HKU\2025-2026\COMP1110\Project\github\COMP1110_Project_2026`

This review is advisory, not an official TA grade. It only grades evidence visible in the local repository and the provided handbook. Moodle submission status, tutorial attendance, individual report submissions, and any off-repo video file cannot be confirmed from this repository unless explicitly present.

## Executive Summary

The project is a strong match for Topic C. The repository contains a working Python restaurant queue simulator, a complete README, planning/research/final-report materials, sample data, generated figures, and automated tests. The strongest areas are final code completeness, input validation, reproducibility instructions, and research/report depth.

Main risks:

- The demo video is not present; `Final_report/final_report.md` says "Demo Video: To be added".
- No individual final reports are present in the repository, so AI-use documentation and individual contribution consistency cannot be verified.
- The handbook suggests 5-6 paired Topic C case studies; the report has several implemented baseline-centered comparisons, but part of the 5-6 pair coverage is explicitly listed as proposed future work rather than completed experiment output.
- Some evaluation outputs are not standardized across every scenario, which the README/report also acknowledge.

Suggested score range for repo-verifiable group components:

| Component | Handbook weight | Suggested range | Rationale |
|---|---:|---:|---|
| Project Plan | 15 | 13-14 | Plan PDF has topic, roles, tool summary, task breakdown, and Gantt-style timeline. |
| Final Code | 25 | 22-24 | Working implementation, validation, README, tests, and sample outputs. Minor deductions for rigid A/B/C model and script-oriented structure. |
| Group Final Report | 35 | 29-32 | Detailed research, modeling, implementation explanation, case studies, limitations. Deductions for missing demo link and partially proposed case-pair coverage. |
| Individual Final Report | 10 | Not verifiable | No individual reports found in repo. |
| Tutorial participation | 15 | Not verifiable | Attendance is outside repository evidence. |
| Video demo | 0 | Required but missing in repo | Not graded by weight, but required for TA reproduction support. |

Approximate verifiable subtotal: **64-70 / 75** for the group plan/code/report components visible in this repository.

## Evidence Inventory

| Evidence area | Repository evidence | Status | Notes / improvement needed |
|---|---|---|---|
| README and run instructions | `README.md`, `requirements.txt` | Strong | README explains environment, install commands, input schema, validation rules, testing, case studies, and limitations. |
| Public GitHub evidence | `git remote -v` points to `https://github.com/bobownYAO/COMP1110_Project_2026` | Mostly satisfied | Local remote exists. Public accessibility was not web-verified in this local review. |
| Project plan | `Plan/COMP1110 Project Plan.pdf`, `Plan/index.md` | Satisfied | PDF has topic C, 4 members, task breakdown, app summary, and timeline. |
| Research notes | Four member research Markdown files in `Research/` | Strong | Covers VIP, size-based queues, single snake, table sharing, THE GULU, Meituan/KeeTa, Haidilao, and Meiwei Bu Yong Deng. |
| Group final report | `Final_report/final_report.md` plus images | Strong with caveats | Detailed report exists; demo link remains missing. |
| Individual reports | None found by filename search | Not verifiable | Add/submit individual reports separately; include AI-use documentation if AI was used. |
| Video demo | No video files found; report says "To be added" | Missing | Add video link/file before submission. |
| Source code | 12 Python files in `Modeling&Coding/` | Strong | Main entry point, I/O, queue state, strategies, output analysis, and plotting modules are present. |
| Tests and data | 5 Python files in `Testing/`, 57 CSV files, 74 PNG files, 12 TXT files | Strong | Includes validation tests, strategy tests, end-to-end tests, generated datasets, and output figures. |

## Requirements Checklist

| Requirement | Evidence checked | Status | Suggested level | Needed improvement |
|---|---|---|---|---|
| Choose one handbook topic | README and final report identify Restaurant Queue Simulation | Met | Excellent | None. |
| Topic C research survey of queue approaches | Final report Section 2; `Research/*.md` | Met | Excellent | Keep citations consistent; avoid overclaiming real-world operational numbers unless sourced. |
| Compare queue approaches across wait time, utilization, fairness, peak-hour performance, complexity | Final report comparison table | Met | Excellent | None substantial. |
| Document modeling assumptions | Final report modeling approach and limitations; README limitations | Met | Good | Make the assumptions list easier to find as a standalone subsection. |
| Customer data model: group size, arrival time, dining duration | `io_file.py`, README input schema, tests | Met | Excellent | None. |
| Restaurant/table/queue model | `queue_structure.py`, strategy modules, restaurant CSV schema | Met | Good | Current A/B/C categories are fixed; configurable ranges would improve flexibility. |
| File input/output | `io_file.read_file`, output summary CSV, generated charts | Met | Excellent | None. |
| Basic input validation | `io_file.py`, `Testing/test_input_validation.py` | Met | Excellent | Validation is stronger than the minimum requirement. |
| Core simulation: arrivals, queues, table release, seating decisions | `strategy_single_snake.py`, `strategy_size_base.py`, `strategy_vip.py` | Met | Good | Consider reducing duplicated strategy logic and documenting exact fairness policy per strategy. |
| Metrics: average wait, max queue length, table utilization / occupation, served counts | `output_file.py`, README, tests | Met | Excellent | Standardize summary exports across every scenario folder. |
| Text-based interaction | `main.py` interactive mode and CLI mode | Met | Good | CLI mode is strong; interactive prompts have minor spelling issues such as "Dinning". |
| Case studies with exact inputs and outputs | `Testing/Baseline`, `Testing/MoreVIP`, `Testing/Testdata-MoreA`, `Testing/Testdate-longshort`, final report Section 6 | Partially met | Good | Handbook suggests 5-6 paired scenarios. Implemented comparisons are useful, but several additional pairs are only proposed. |
| Side-by-side evaluation of scenario pairs | Final report tables and existing summary CSVs | Mostly met | Good | Ensure every pair has the same metric table and output CSV, not only figures. |
| README completeness | README sections 3-10 | Met | Excellent | Add demo video link once available. |
| GitHub repository completeness | 183 tracked files; key folders and source included | Met | Good | Confirm public repo access before submission. |

## Code Review Findings

Strengths:

- `main.py` supports both interactive and non-interactive CSV execution, which helps TA reproducibility.
- `io_file.py` validates required columns, empty files, malformed CSVs, invalid strategies, invalid table categories, invalid VIP values, negative values, group sizes, and unknown restaurants.
- `queue_structure.py` uses deques for waiting queues and min-heaps for occupied tables, which is appropriate for a basic queue simulation.
- All three implemented strategies produce common result columns: `final_wait_time`, `start_service_time`, `leave_time`, and `assigned_table_type`.
- `output_file.py` exports summary metrics and computes queue length and occupation rate.
- Automated tests check input validation, strategy behavior, and end-to-end outputs.

Limitations / risks:

- Table categories are hard-coded as `A`, `B`, and `C`, with fixed group-size interpretation. This is acceptable for a course project but less flexible than the handbook's general "group size range" language.
- The implementation is script-oriented and has some repeated logic across strategy modules.
- `single_snake` intentionally permits small groups to use larger available tables, while `size_base` and `vip` use stricter category matching. This is a valid modeling choice, but the report should keep emphasizing that comparisons depend on this policy difference.
- Some strategy modules print previews directly, which can make batch output verbose.

## Verification Commands

Commands were run from:

```text
D:\ylj\HKU\2025-2026\COMP1110\Project\github\COMP1110_Project_2026
```

Environment:

```text
Python 3.13.9
pandas/numpy/matplotlib/pytest import check: passed
```

Automated tests:

```bash
python -m pytest Testing
```

Result:

```text
22 passed in 5.92s
```

README sample CLI run:

```bash
python "Modeling&Coding\main.py" --dining fixed --restaurant-csv "Testing\sample_cases\valid_restaurant.csv" --customer-csv "Testing\sample_cases\valid_customer.csv" --output-dir "Testing\grading_review_sample_output"
```

Result:

```text
Exit code 0
Summary metrics: R1, size_base, 3 customers, 3 served, 0 unserved,
avg_wait_time 0.0, max_wait_time 0.0, avg_occupation_rate_pct 62.9699,
avg_queue_length 0.0, max_queue_length 0, total_tables 4, total_seats 14.
```

The generated sample output directory was removed after recording the result so that this review leaves only the grading document as a new project file.

The full final case batch script was not rerun because existing case-output evidence already exists under `Testing/Testdate-longshort/restaurant_run_outputs_latest_long_short_fast/`, including `summary_metrics_by_dataset.csv`, `summary_metrics_by_restaurant.csv`, and `COMPACT_SUMMARY.txt`. Rerunning the full batch would create many large output artifacts without materially changing the grading judgment.

## Suggested Grading by Section

### Project Plan: 13-14 / 15

Evidence:

- `Plan/COMP1110 Project Plan.pdf` has team members, Topic C, task breakdown by member, research assignments, modeling/coding/report responsibilities, app/tool summary, and a week-by-week timeline.
- The plan covers the required elements: role assignment, existing tool/app summary, and milestones.

Improvement:

- The Markdown `Plan/index.md` is only a final summary. If TAs inspect the repo rather than the PDF, a fuller Markdown copy of the original plan would be easier to grade.

### Final Code: 22-24 / 25

Evidence:

- Code runs from CLI and tests pass.
- Implements CSV loading, validation, dining-time preprocessing, three strategies, seating decisions, result columns, metrics, charts, and generated test data.
- README is unusually complete for reproduction.

Improvement:

- Make table categories and group-size thresholds configurable.
- Reduce duplicated code across strategies.
- Standardize outputs for every final-report case.

### Group Final Report: 29-32 / 35

Evidence:

- Report includes problem significance, research background, modeling, role breakdown, implementation explanation, case studies, metrics, limitations, and Topic C checklist.
- Research depth is strong and compares several queue approaches.
- Case-study discussion is analytical and includes realistic limitations.

Improvement:

- Add the missing demo video link.
- Convert proposed case pairs into completed, rerunnable experiments if time allows.
- Make each implemented scenario pair use the same side-by-side metric format.

### Topic C Specific Compliance: Good to Excellent, with one case-study caveat

The implementation clearly satisfies the core Topic C modeling and coding requirements: restaurant settings, customer arrivals, queues, table release, seating, waiting-time metrics, queue length, utilization, file I/O, and validation. The main caveat is the suggested 5-6 paired case studies. The project has strong implemented comparisons, but its own report separates additional case pairs as future work, so a strict grader may mark this as partially complete.

### Individual and Attendance Components: Not Verifiable

No individual final reports or attendance records are included in the repository. If AI tools were used, each individual report must document the tool name/version, prompts, and how outputs were modified or verified, according to the handbook.

## Prioritized Improvement Actions

High priority:

1. Add the video demo link/file before final submission. Even though it is 0%, the handbook requires it for reproduction support.
2. Ensure individual final reports are submitted separately and include AI-use documentation if applicable.
3. If possible, complete at least one or two of the proposed case pairs as actual rerunnable CSV inputs plus output summaries, so the 5-6 paired scenario expectation is safer.

Medium priority:

1. Standardize final scenario outputs so every case has the same summary CSV fields and comparable side-by-side table.
2. Add a concise "Modeling assumptions" subsection in the README or report.
3. Confirm the GitHub repository is public and the final report link is correct.

Low priority:

1. Refactor repeated strategy code into shared helper functions.
2. Make A/B/C table categories configurable.
3. Reduce verbose preview printing during batch runs, or add a quiet flag.

## Final Judgment

This is a strong and mostly compliant Topic C submission. A grader would likely find the implementation credible and reproducible: tests pass, sample execution works, and the final report connects the code to meaningful restaurant-queue trade-offs. The most important submission risks are outside the core code: missing demo evidence, unverifiable individual reports, and partially proposed rather than fully executed case-study pairs.
