# COMP1110 Project Grading Review

Review date: 2026-04-29  
Repository reviewed: `D:\ylj\HKU\2025-2026\COMP1110\Project\github\COMP1110_Project_2026`  
Guideline reviewed: `D:\ylj\HKU\2025-2026\COMP1110\Project\COMP1110 Project Guidelines.pdf`, Version 1.2, Feb 27, 2026  
Chosen topic: Topic C, Restaurant Queue Simulation

This review is a grader-style evidence check against the course guideline. The scores below are evidence-based estimates from the local repository, not official TA marks. Items that cannot be checked from repository files are marked as "unable to verify from repository evidence" instead of being guessed.

## 1. Overall Verdict

The project is broadly aligned with Topic C and has a substantial amount of usable evidence: a plan, research notes, Python simulation code, README instructions, input-validation tests, generated datasets, figures, and a long final report. The strongest parts are the implementation of three queue strategies, the clear README, and the detailed long/short arrival analysis.

The main weaknesses are assessment-risk rather than project-collapse issues: the case studies do not fully match the guideline's "5-6 paired scenarios where each pair varies exactly one factor" wording, automated tests mainly cover input validation rather than simulation correctness, there is no dependency-management file, and some evaluation outputs are not standardized across all case groups.

### Estimated Score From Repository Evidence

| Component | Guideline weight | Evidence-based estimate | Status |
|---|---:|---:|---|
| Project Plan | 15 | 12.0 | Good, but problem scope is brief |
| Final Code | 25 | 20.5 | Working and relevant, with testing/packaging gaps |
| Group Final Report | 35 | 29.0 | Strong analysis, but Topic C case-design fit is partial |
| Individual Final Report | 10 | Unable to verify | No individual reports found in repository |
| Group Discussion Participation | 15 | Unable to verify | Attendance cannot be verified from repository |
| Video Demo | 0 | Unable to verify | No video file found in repository |

Estimated subtotal for verifiable group deliverables: **61.5 / 75**.

## 2. Evidence Index

| Area | Repository evidence |
|---|---|
| README and run instructions | `README.md`, sections 3-10 |
| Project plan | `Plan/COMP1110 Project Plan.pdf`, `Plan/index.md` |
| Research notes | `Research/Research_*.md` for VIP, size-based, single snake, table sharing, and app/platform research |
| Final report | `Final_report/final_report.md` plus 8 referenced figures; 23 image references checked, 0 missing |
| Core code | `Modeling&Coding/main.py`, `io_file.py`, `queue_structure.py`, `strategy_single_snake.py`, `strategy_size_base.py`, `strategy_vip.py`, `output_file.py`, plotting modules |
| Tests and data | `Testing/test_input_validation.py`, `Testing/sample_cases/`, `Testing/Baseline/`, `Testing/MoreVIP/`, `Testing/Testdata-MoreA/`, `Testing/Testdate-longshort/` |
| Generated outputs | PNG charts, processed CSV outputs, long/short summary metrics in `Testing/Testdate-longshort/restaurant_run_outputs_latest_long_short_fast/` |
| Missing or external evidence | Individual final reports, tutorial attendance records, video demo, public GitHub URL submission proof |

## 3. Project Plan Review

Estimate: **12.0 / 15**

| Requirement | Evidence | Judgment |
|---|---|---|
| Daily-life problem and scope | Plan identifies Topic C and queue-management apps/platforms; final repository clarifies restaurant queue simulation | Partially satisfied in the plan itself; clearer in README/final report |
| Task breakdown and role assignment | Plan PDF assigns research, modeling, coding, case-study, and report duties to Yao Lijia, Yu Wei, Jiang Hongyi, Zhang Zhanhao | Satisfied |
| Brief summary of existing tools/apps | Plan summarizes Meituan, Meiwei Bu Yong Deng, THE GULU, and Haidilao | Satisfied |
| Timeline/milestones/Gantt chart | Plan includes a 6-week Gantt-style timeline from research to final improvement | Satisfied |
| Consistency with final report/README | Member roles in README and final report broadly match the plan | Mostly satisfied |

Main issues:

- The plan is useful but compact. It does not clearly define the final simulation scope, exact input/output format, or case-study design at the level expected for later implementation.
- The plan references "Algorithm 1,2,3,4", while the final code implements three named strategies: `single_snake`, `size_base`, and `vip`. This is not fatal, but the naming is not fully consistent.

Improvements:

- Add a short explicit scope paragraph: no GUI, no table sharing in code, CSV-based restaurant/customer inputs, three strategy comparison, fixed/random dining time.
- Add a small planned-output list: wait time, queue length, groups served, table utilization, occupation rate, and figures.

## 4. Final Code Review

Estimate: **20.5 / 25**

| Requirement | Evidence | Judgment |
|---|---|---|
| Language/environment documented | README states Python 3, pandas, numpy, matplotlib, pytest | Satisfied |
| Setup/run instructions | README gives install commands, `python main.py`, CSV/manual input workflow, and pytest command | Mostly satisfied |
| File I/O | `io_file.py` loads restaurant/customer CSVs and supports console input | Satisfied |
| Data model | CSV schemas documented; `State` stores occupied tables and waiting queues | Satisfied |
| Core simulation | Three strategy modules implement step-by-step table release, arrivals, queues, seating, and leave times | Satisfied |
| Metrics | `output_file.py` reports wait-time stats and occupation rate; plotting modules cover queue length, utilization, waiting-time density | Mostly satisfied |
| Error handling | `io_file.py` checks missing columns, empty data, invalid strategies/table sizes, numeric/non-negative values, VIP values, unknown restaurants | Strong |
| Sample tests | `Testing/test_input_validation.py` plus fixtures in `Testing/sample_cases/` | Satisfied for input validation, limited for strategy correctness |
| Documentation/readability | README is detailed; code is split by responsibility | Good, with style/packaging weaknesses |

Verified run results:

- `python -m pytest Testing -q` returned `10 passed in 1.13s`.
- A safe reproduction was run in a temporary directory using `valid_restaurant.csv` and `valid_customer.csv`. The main program loaded CSV input, served all sample customers, printed wait-time and occupation-rate analysis, and generated five charts: occupation rate, table utilization line, table utilization bar, waiting-time density, and queue length over time.

Main issues:

- There is no `requirements.txt`, `pyproject.toml`, or environment file. README gives manual install commands, which is acceptable but less reproducible.
- Automated tests only cover input validation. They do not assert seating order, VIP priority behavior, size-based behavior, single-snake fallback behavior, queue-length metrics, or chart/summary correctness.
- `main.py` calls `__main__()` unconditionally, so importing the module would immediately start the interactive program. A standard `if __name__ == "__main__":` guard would be safer.
- Output paths are inconsistent: occupation rate is saved under `outputs/occupation_rate.png`, while other charts are saved in the current directory.
- `plot_table_utilization_bar.py` infers table type from customer group size. For `single_snake`, small groups can be seated at larger table types, so table-type utilization can be inaccurate unless the actual table type used is stored by the strategy.
- Console output includes some Unicode box/arrow symbols that displayed as mojibake in the current terminal during reproduction. This is a presentation issue, not a core logic failure.

Improvements:

- Add `requirements.txt` with `pandas`, `numpy`, `matplotlib`, and `pytest`.
- Add tests for each strategy using small deterministic datasets with expected `start_service_time`, `leave_time`, and `final_wait_time`.
- Store actual assigned table type in the simulation result so table-type utilization charts reflect real seating decisions.
- Standardize all generated outputs under one output directory and document that directory in README.

## 5. Group Final Report Review

Estimate: **29.0 / 35**

| Requirement | Evidence | Judgment |
|---|---|---|
| Problem significance/challenges | Final report introduction explains restaurant waiting, limited tables, service order, utilization | Satisfied |
| Research survey | Sections 2.1-2.4 cover single snake, VIP, size-based queues, table sharing, and real platforms | Strong |
| Comparison of existing approaches | Report discusses pros/cons and trade-offs across strategies; research files support platform comparisons | Mostly satisfied, but no single compact comparison table across all Topic C criteria |
| Modeling explanation | Sections 3 and 5 explain datasets, assumptions, `State`, strategy scope, code flow | Satisfied |
| System design/key functions | Sections 5.1-5.8 describe input, preprocessing, strategy dispatch, outputs, plots, tests | Satisfied |
| Case studies | Section 6 covers baseline, MoreVIP, MoreA, and long/short intervals with charts and metrics | Good, but not fully aligned with required 5-6 paired-scenario design |
| Evaluation/limitations/future work | Section 6.6 and README limitations table discuss synthetic data, fixed dining time, no walkaways, no table sharing, output standardization | Satisfied |
| Consistency with code | Report matches the three implemented strategies and acknowledges table sharing is conceptual only | Mostly satisfied |

Main issues:

- Topic C.1 asks for **5-6 paired scenarios**, each pair varying exactly one factor while keeping the customer arrival pattern fixed within the pair. The repository has rich scenario groups, but the final report presents four main groups rather than 5-6 clearly labeled pairs.
- Some case groups are better supported than others. Long/short has strong summary CSV evidence; MoreA has processed CSVs and figures; Baseline and MoreVIP rely more on generated charts and narrative.
- The report is long and detailed, but some analysis is repetitive. A grading reader may prefer a concise comparison table mapping each case to factor varied, fixed controls, metrics, and conclusion.
- The final report references real-world platforms and sources, but some research claims are ambitious. A TA may expect clearer separation between sourced facts, modeling assumptions, and simulation results.

Improvements:

- Add a case-study control table with columns: pair ID, factor varied, fixed customer arrival file, restaurant setting variation, strategy, metrics, conclusion.
- Reframe existing material into at least five explicit pairs, or state why the selected four scenario groups are sufficient if the group intentionally deviated.
- Export the same summary metrics for Baseline, MoreVIP, MoreA, and long/short so every case has comparable numerical support.

## 6. Topic C Specific Checklist

| Topic C requirement | Evidence | Status | Improvement needed |
|---|---|---|---|
| Survey real-world queue-management strategies | Research notes and final report cover single snake, size-based, VIP, table sharing, THE GULU, Meituan/KeeTa, Meiwei Bu Yong Deng, Haidilao | Satisfied | Add a concise comparison table if space allows |
| Compare approaches by wait time, utilization, fairness, peak performance, complexity | Discussed in prose and some tables | Mostly satisfied | Make one explicit comparison table across all criteria |
| Document assumptions | Final report states fixed/random dining time, table categories A/B/C, no full table-sharing implementation, simplified behavior | Mostly satisfied | Add one assumption list near the model section |
| Customer data model | Customer CSV includes index, restaurant, VIP, group size, arrival time, calculated dining time | Satisfied | Consider documenting dining-time units and random seed behavior |
| Table/queue data model | Restaurant CSV uses name, strategy, open time, table size, table number; `State` stores queues and occupied heaps | Satisfied | Store actual assigned table type in results |
| File I/O | CSV reading and console input implemented | Satisfied | Add command-line noninteractive mode for easier reproducibility |
| Missing/empty/malformed input handling | Input validation tests cover many invalid CSV cases | Strong | Add missing-file test and malformed CSV/parser test |
| Core simulation | Step-by-step simulation implemented in three strategy modules | Satisfied | Add deterministic unit tests for seating decisions |
| Seat earliest suitable group when table frees | Implemented per strategy, though rules differ by strategy | Mostly satisfied | Explain that `vip` intentionally prioritizes VIPs within table category |
| Track dining durations | `dinning_time`, `start_service_time`, and `leave_time` tracked | Satisfied | Correct spelling to `dining_time` in future refactor if possible |
| Average/max wait time | Printed by `output_file.py`; summary CSVs exist for long/short | Satisfied | Export automatically for every run |
| Max queue length | Plotted and present in long/short summary CSV | Mostly satisfied | Main program does not print/export max queue length by default |
| Groups served | Served/unserved inferable; long/short summary CSV includes served/unserved | Mostly satisfied | Print/export served count in main report |
| Table utilization | Plots and summary CSVs exist | Mostly satisfied | Fix table-type utilization inference for single-snake actual assignments |
| Service level within X minutes | Mentioned in guideline as example metric; not clearly implemented | Optional/weak | Add if aiming for stronger metrics coverage |
| 5-6 paired scenarios | Baseline, MoreVIP, MoreA, long/short exist; long/short has 6 datasets and summary metrics | Partially satisfied | Reorganize into 5-6 explicit paired comparisons |
| Same arrival pattern within pair | Baseline/MoreVIP/MoreA/long-short datasets use controlled distributions; exact fixed-pair explanation is not always explicit | Mostly/partially satisfied | State controls and changed factor for each pair |
| Present outputs and seating decisions | Outputs, charts, processed CSVs, and narrative exist | Mostly satisfied | Include sample seating decisions or processed output excerpts in report |
| Discuss trade-offs, failures, real practices | Final report and README discuss limitations and real-world practices | Satisfied | Condense and tie each trade-off directly to a metric |

## 7. Testing and Reproduction Evidence

### Automated Tests

Command run:

```powershell
python -m pytest Testing -q
```

Result:

```text
10 passed in 1.13s
```

Coverage interpretation:

- Good coverage of CSV input validation.
- No direct automated coverage of queue strategy correctness, seating order, metric calculations, plotting output, or report-data consistency.

### Safe Reproduction

The main workflow was reproduced in a temporary directory, not inside the repository, to avoid overwriting existing outputs. Inputs used:

- `Testing/sample_cases/valid_restaurant.csv`
- `Testing/sample_cases/valid_customer.csv`

Result:

- Program accepted fixed dining time and CSV loading.
- All 3 sample customers were served with `final_wait_time = 0`.
- Analysis output included max/min/average waiting time and average occupation rate.
- Generated `occupation_rate.png`, `table_utilization_line.png`, `table_utilization_bar.png`, `waiting_time_density.png`, and `queue_length_over_time.png`.

### Scenario Data Observations

| Scenario folder | Evidence observed | Notes |
|---|---|---|
| `Testing/Baseline/` | 3 customer files, 3 restaurant files, charts for single/size_base/vip | Same group distribution across strategies; VIP file has baseline VIP rate |
| `Testing/MoreVIP/` | VIP customer/restaurant files and charts | Tests increased VIP rate; useful priority-pressure case |
| `Testing/Testdata-MoreA/` | 3 strategy datasets and processed outputs | Tests many small groups; stronger output evidence than Baseline |
| `Testing/Testdate-longshort/` | 6 long/short datasets plus summary metrics CSVs | Strongest case-study evidence; includes wait, utilization, queue length, served/unserved |

## 8. Missing or Unverifiable Items

| Item | Repository evidence | Grading implication |
|---|---|---|
| Individual Final Reports | No individual report files found | Cannot verify 10% individual assessment or AI-use disclosure |
| AI-use documentation | Not visible in repository individual reports | If AI was used, each student must document tool/version/prompts/verification in their own report |
| Tutorial attendance | No attendance record in repository | Cannot verify 15% participation |
| Video demo | No `.mp4`, `.mov`, `.avi`, or video-like file found | 0% weight, but required for TA reproduction |
| Public GitHub submission proof | Local git repo exists, but no public URL proof in checked files | Ensure final group report or Moodle submission includes public repository link |

## 9. Priority Improvement List

### Must Fix Before Submission

1. Ensure the final submission includes individual final reports outside or alongside the repository. Each must include contribution details, personal evaluation/reflection, and AI-use documentation if applicable.
2. Ensure the video demo is submitted, even though it has 0% weight.
3. Add or clearly include the public GitHub repository link in the Group Final Report/Moodle submission.
4. Reframe the case-study section into explicit paired scenarios, or add a short table explaining how the existing scenarios satisfy the 5-6 paired-scenario requirement.

### Strongly Recommended

1. Add `requirements.txt`.
2. Add deterministic strategy tests for `single_snake`, `size_base`, and `vip`.
3. Export standardized summary metrics for every scenario group, not only long/short.
4. Fix table-type utilization calculation by recording actual assigned table type during simulation.
5. Standardize all chart outputs under one documented output directory.

### Optional Enhancements

1. Add a service-level metric, such as percentage of groups seated within 10 or 20 minutes.
2. Add command-line arguments for noninteractive batch execution.
3. Replace terminal box-drawing symbols with plain ASCII for safer display across Windows terminals.
4. Add a concise assumptions table in the final report.

## 10. Repository State Note

Before creating this review file, `git status --short` already showed modified Python bytecode cache files under `Modeling&Coding/__pycache__/` and an untracked `Testing/__pycache__/` directory. These appear to be runtime/cache artifacts, not source/report changes. This review did not intentionally modify existing project source, report, test data, or figures.

