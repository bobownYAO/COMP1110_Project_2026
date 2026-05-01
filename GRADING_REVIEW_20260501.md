# COMP1110 Project Grading Review

Review date: 2026-05-01  
Repository reviewed: `D:\ylj\HKU\2025-2026\COMP1110\Project\github\COMP1110_Project_2026`  
Guideline reviewed: `D:\ylj\HKU\2025-2026\COMP1110\Project\COMP1110 Project Guidelines.pdf`, Version 1.2, Feb 27, 2026  
Chosen topic: Topic C, Restaurant Queue Simulation  
Output policy: this file was added as a new review document. Existing project files were not edited by this review.

Baseline git status before writing this file:

```text
 M Final_report/final_report.md
 M README.md
```

These two modified files were already dirty at the start of this review. They were treated as current project evidence and were not reverted or modified.

## 1. Overall Verdict

The project is substantially aligned with Topic C. It contains a Python restaurant queue simulation, three implemented queue strategies, CSV file input, validation tests, generated data, visual outputs, research notes, a project plan, a detailed README, and a long final report with case-study analysis.

The strongest evidence is in the final code and final report: the repository clearly models restaurants, customer groups, table categories, queues, seating decisions, wait times, queue length, and utilization. The automated tests now cover both input validation and selected strategy behavior, and they pass locally.

The main grading risks are not project-breaking, but they matter against the guideline wording:

- The Topic C suggested case-study design asks for 5-6 paired scenarios where each pair varies exactly one factor. The project has several useful scenarios, but they are not consistently presented as 5-6 controlled pairs.
- The final report is rich, but some claims would be stronger if every case study had a uniform table of input files, changed variable, metrics, result interpretation, and real-world comparison.
- Individual final reports, attendance records, public GitHub submission evidence, and video demo are not visible in this repository, so they cannot be verified from local files.
- The README is strong, but reproducibility would improve with a single scripted command for rerunning all documented case studies without interactive input.

## 2. Estimated Score From Repository Evidence

These are grader-style evidence estimates, not official TA marks.

| Component | Guideline weight | Evidence-based estimate | Status |
|---|---:|---:|---|
| Project Plan | 15 | 12.0 | Good, but scope and final case design are compact |
| Final Code | 25 | 21.5 | Working, documented, tested; reproducibility and packaging can improve |
| Group Final Report | 35 | 29.0 | Strong research and analysis; Topic C paired-scenario fit is partial |
| Individual Final Report | 10 | Unable to verify | No individual reports found in repository |
| Group Discussion Participation | 15 | Unable to verify | Tutorial attendance cannot be verified from repository evidence |
| Video Demo | 0 | Unable to verify | No video file found in repository |

Estimated subtotal for verifiable group deliverables: **62.5 / 75**.

## 3. Evidence Index

| Area | Repository evidence |
|---|---|
| README and run instructions | `README.md`, including overview, roles, environment, dependencies, run commands, CSV schemas, validation rules, testing, and case-study summary |
| Project plan | `Plan/COMP1110 Project Plan.pdf`, `Plan/index.md` |
| Research notes | `Research/Research_JiangHongyi.md`, `Research/Research_Yaolijia.md`, `Research/Research_YuWei.md`, `Research/Research_ZhangZhaohao.md` |
| Final report | `Final_report/final_report.md` and figures in `Final_report/` |
| Core code | `Modeling&Coding/main.py`, `io_file.py`, `queue_structure.py`, `strategy_single_snake.py`, `strategy_size_base.py`, `strategy_vip.py`, `output_file.py`, plotting modules |
| Dependencies | `requirements.txt` lists `pandas`, `numpy`, `matplotlib`, `pytest` |
| Automated tests | `Testing/test_input_validation.py`, `Testing/test_strategy_behavior.py`, `Testing/sample_cases/` |
| Generated datasets and outputs | `Testing/Baseline/`, `Testing/MoreVIP/`, `Testing/Testdata-MoreA/`, `Testing/Testdate-longshort/`, `Modeling&Coding/outputs/` |
| Missing or external evidence | Individual final reports, tutorial attendance records, video demo, Moodle submission proof, public GitHub URL proof |

Additional evidence checks:

- `python -m pytest Testing -q` passed with 19 tests.
- `Final_report/final_report.md` has 23 image references; 0 were missing in local file checks.
- No repository video files were found with common extensions such as `.mp4`, `.mov`, `.avi`, `.mkv`, or `.webm`.
- No individual report files were found in the repository scan.

## 4. Guideline Requirement Matrix

| Guideline area | Requirement | Evidence | Judgment | Improvement needed |
|---|---|---|---|---|
| Section 2.1 Project Plan | Describe daily-life problem and scope | Plan identifies Topic C and queue-management platforms; README and final report clarify restaurant queue simulation | Mostly satisfied | Make the plan itself more explicit about exact simulation scope, excluded features, inputs, and outputs |
| Section 2.1 Project Plan | Task breakdown and roles for all members | Plan PDF assigns research, modeling, coding, testing, case-study, and report roles to four members | Satisfied | Align plan algorithm labels with final strategy names |
| Section 2.1 Project Plan | Brief summary of existing tools/apps | Plan summarizes Meituan/KeeTa, Meiwei Bu Yong Deng, THE GULU, and Haidilao | Satisfied | Add short comparison criteria in the plan, not only descriptions |
| Section 2.1 Project Plan | Timeline with milestones | Plan includes a 6-week Gantt-style timeline | Satisfied | Tie milestones to concrete deliverables and test checkpoints |
| Section 2.2 Final Code | README specifies language, environment, setup | README states Python 3 and dependencies; `requirements.txt` exists | Satisfied | Add exact tested Python version and one setup command including pytest |
| Section 2.2 Final Code | Text-based interaction and simple file I/O | `main.py` uses console prompts; `io_file.py` reads CSV and console rows | Satisfied | Provide a non-interactive demo command or script for reproduction |
| Section 2.2 Final Code | Readable and documented source code | Code is split by data input, queue state, strategies, analysis, plotting | Mostly satisfied | Add docstrings or comments for core strategy decisions and table matching rules |
| Section 2.2 Final Code | Sample test cases | `Testing/sample_cases/`, generated datasets, baseline and long/short outputs | Satisfied | Add a short README explaining the purpose of each dataset folder |
| Section 2.3 Group Final Report | Updated task breakdown and role assignment | Final report Section 4 and README roles table | Satisfied | Ensure wording exactly matches any individual reports submitted outside the repo |
| Section 2.3 Group Final Report | Problem significance and modeling | Final report Sections 1 and 3 | Satisfied | Add a concise model diagram or state-transition summary |
| Section 2.3 Group Final Report | Detailed survey and comparison | Final report Section 2 compares single snake, size-based, VIP, and table sharing | Strong | Strengthen source quality by distinguishing measured facts from conceptual claims |
| Section 2.3 Group Final Report | System design and key functions | Final report Section 5 maps program flow, input, state, strategies, metrics, plots | Satisfied | Reference exact files/functions more consistently |
| Section 2.3 Group Final Report | Case studies and evaluation | Final report Section 6, generated outputs, summary CSVs and figures | Mostly satisfied | Reframe cases as controlled pairs with one variable changed per pair |
| Section 2.3 Group Final Report | Limitations and improvements | Final report Section 6.6 and recommendations | Satisfied | Add direct links between each limitation and a future implementation change |
| Section 2.4 Individual Reports | Individual contribution, reflection, AI use if applicable | No individual reports in repository | Unable to verify | Confirm individual reports were submitted separately and include required AI-use disclosure if relevant |
| Section 2.5 Participation | Attendance in final four tutorials | Not stored in repository | Unable to verify | No repository action possible |
| Section 2.6 Video Demo | Short demo showing workflow for at least one case | No video file found | Unable to verify | Add or submit demo externally if not already done |
| Section 3 Source Code | Alignment with Topic C features | Three restaurant queue strategies implement core Topic C behavior | Satisfied | Add full-case regression tests for end-to-end metrics |
| Section 4 AI Use | AI use must be documented in individual report if used | No individual reports visible | Unable to verify | If AI was used, each individual report should name tool/version, prompts, and verification/modification process |
| Section 5 Submission | Final code public GitHub repo with link in Group Final Report | Local git repository exists; public URL proof not visible in checked files | Partially verifiable | Include the public GitHub URL in final report or README if required by submission |

## 5. Project Plan Review

Estimate: **12.0 / 15**

The plan satisfies the main structural requirements: it identifies Topic C, lists four members, assigns research/coding/testing/report duties, summarizes related real-world queue systems, and gives a week-by-week timeline.

| Requirement | Evidence | Judgment |
|---|---|---|
| Daily-life problem and scope | Topic C appears in the plan; related app summaries focus on restaurant queueing | Mostly satisfied |
| Role assignment | Yao Lijia, Yu Wei, Jiang Hongyi, and Zhang Zhanhao are assigned distinct research and implementation roles | Satisfied |
| Existing tools/apps | Meituan/KeeTa, Meiwei Bu Yong Deng, THE GULU, Haidilao are summarized | Satisfied |
| Timeline | 6-week Gantt-style plan from research to final improvement | Satisfied |
| Consistency with final work | Final repository implements `single_snake`, `size_base`, and `vip`; plan refers to Algorithm 1-4 | Mostly satisfied |

Main issues:

- The plan is brief on final implementation scope. It does not clearly state the final CSV schema, exact metrics, excluded features, or case-study design.
- The plan mentions Algorithm 1-4, but the final code has three named strategies. The mismatch is understandable but should be explained.
- The plan does not explicitly say table sharing will remain conceptual only, while the final project does not implement it.

Recommended improvements:

- Add a scope paragraph: CSV inputs only, text interface, no GUI/database, no table sharing implementation, three strategies, fixed/random dining time.
- Add planned outputs: average/max wait time, queue length, groups served, occupation/table utilization, plots, and processed output CSVs.
- Align algorithm labels with final strategy names.

## 6. Final Code Review

Estimate: **21.5 / 25**

The code is clearly relevant to Topic C and has a working simulation structure. The strongest parts are the CSV validation, separation of strategy modules, shared queue state, metrics, visual outputs, and automated tests.

| Requirement | Evidence | Judgment |
|---|---|---|
| Language and environment | README states Python 3; `requirements.txt` lists dependencies | Satisfied |
| Setup/run instructions | README gives install commands, `python main.py`, CSV/manual input workflow, and pytest command | Satisfied |
| File I/O | `io_file.read_file()` loads restaurant/customer CSV; `read_console()` supports manual rows | Satisfied |
| Input validation | `io_file.py` checks missing columns, empty data, invalid strategy/table size, numeric values, negative values, invalid VIP, unknown restaurants | Strong |
| Data model | Restaurant/customer CSV schemas documented; `State` stores occupied tables and VIP/non-VIP queues by table category | Satisfied |
| Core simulation | Strategy modules implement seating decisions for `single_snake`, `size_base`, and `vip` | Satisfied |
| Metrics | `output_file.py` computes wait time, served/unserved, queue length, occupation rate; generated summaries include table utilization metrics in output datasets | Mostly satisfied |
| Visualization | Plot modules and many PNG outputs exist | Satisfied |
| Tests | 19 pytest tests cover validation and selected strategy behavior | Good |
| Documentation/readability | Modular structure and README explain purpose and usage | Good |

Main issues:

- The main workflow is interactive, so a TA cannot rerun the main case studies with one command.
- Strategy correctness tests are useful but still small; they do not verify full end-to-end metrics on realistic datasets.
- The code uses the misspelled column name `dinning_time`; this is consistent internally but looks unprofessional in a final submission.
- Some metric naming differs between modules and outputs, for example occupation rate versus table utilization. This can confuse readers unless carefully defined.
- There are generated caches such as `__pycache__` and `.pytest_cache`; they do not affect functionality but are not ideal for repository cleanliness.

Recommended improvements:

- Add a non-interactive runner script or documented command that executes all final case studies and writes outputs to a known folder.
- Add regression tests for one complete small restaurant scenario per strategy, checking exact wait times, served count, max queue length, and table assignment.
- Standardize metric names in README, final report, and output CSV columns.
- Add a `.gitignore` cleanup policy for cache files if not already handled outside this visible tree.

## 7. Test and Reproducibility Review

Command run from repository root:

```text
python -m pytest Testing -q
```

Observed result:

```text
...................                                                      [100%]
19 passed in 1.13s
```

Collected test coverage:

- `Testing/test_input_validation.py`: 13 validation-oriented checks, including valid CSV loading, missing columns, invalid strategy, invalid table size, missing table type, invalid numeric values, invalid VIP values, unknown restaurants, negative values, missing file, empty file, and malformed CSV.
- `Testing/test_strategy_behavior.py`: 6 strategy-behavior checks, including shared output columns, size-based matching and FIFO waiting, VIP priority within a table type, and single-snake seating a small group at a larger available table.

Additional test assets:

- `Testing/sample_cases/` contains focused validation fixtures.
- `Testing/Baseline/`, `Testing/MoreVIP/`, `Testing/Testdata-MoreA/`, and `Testing/Testdate-longshort/` contain scenario data, generated outputs, charts, and summaries.
- `Testing/Testdate-longshort/restaurant_run_outputs_latest_long_short_fast/summary_metrics_by_dataset.csv` records 6 datasets with 1000 customers each and 0 unserved customers.

Coverage gaps:

- No one-command full reproduction of all final report figures was found.
- No automated assertion checks the final report's exact case-study metrics against current code output.
- No tests for missing/empty restaurant settings beyond input validation, and no tests for all generated case-study folders.

## 8. Group Final Report Review

Estimate: **29.0 / 35**

The final report is detailed and broadly meets the Group Final Report requirements. It explains the problem, research background, modeling assumptions, core entities, queue state, implemented strategies, code logic, case studies, metrics, limitations, and references.

| Requirement | Evidence | Judgment |
|---|---|---|
| Daily-life problem and significance | Section 1 frames restaurant queue management and operational trade-offs | Satisfied |
| Modeling as computing/data-science problem | Section 3 describes entities, assumptions, time, queue state, and strategy scope | Satisfied |
| Detailed survey and comparison | Section 2 surveys single snake, VIP, size-based, and table sharing approaches with real platforms | Strong |
| Updated task breakdown | Section 4 lists planned roles and contributions | Satisfied |
| System design and functions | Section 5 explains main program, data input, queue structure, strategies, outputs, plots, and testing assets | Satisfied |
| Case studies | Section 6 covers baseline, More VIP, More Small Groups, Long vs Short Intervals, and limitations | Mostly satisfied |
| Evaluation and limitations | Section 6 includes metrics, analysis, final recommendations, and limitations | Satisfied |
| Figures | 23 image references checked; 0 missing | Satisfied |

Main issues:

- Topic C.1 specifically suggests 5-6 paired scenarios where each pair varies exactly one factor. The report has several strong scenarios, but the pairing structure is not fully explicit or consistently applied.
- The report is long and sometimes blends research claims, platform facts, and conceptual modeling assumptions. A grader may prefer clearer separation of evidence, assumptions, and project results.
- Some case sections have richer numerical comparison than others. Uniform case-study formatting would make the evidence easier to grade.
- Public GitHub URL evidence was not found in the checked README/final report search.

Recommended improvements:

- Reorganize Section 6 around a table with columns: pair ID, controlled variable, unchanged inputs, changed inputs, files used, metrics, result, interpretation.
- Add a concise "Topic C requirements checklist" at the end of the final report.
- Include the public GitHub link and demo video location if they exist externally.

## 9. Topic C Specific Review

| Topic C requirement | Evidence | Judgment | Needed improvement |
|---|---|---|---|
| Define customer arrival scenarios with group size, arrival time, dining duration | Customer CSV has `number` and `arrival_time`; code computes `dinning_time` | Satisfied | Explain computed dining time more visibly in report and README |
| Define restaurant settings with tables and queue strategies | Restaurant CSV has `name`, `strategy`, `open_time`, `table_size`, `table_number` | Satisfied | Clarify table capacities A/B/C wherever metrics are discussed |
| Multiple queues serving group size ranges | `State` has queues by A/B/C; size-based and VIP strategies use table categories | Satisfied | State exact group-to-table mapping in final report checklist |
| FCFS behavior within queue | Tests check FIFO for size-based waiting; final report states FCFS assumptions | Mostly satisfied | Add more tests for FCFS across all strategies |
| Assign arriving groups to matching queues | Strategy modules and tests support this | Satisfied | Add an end-to-end trace example |
| Seat earliest-waiting suitable group when table frees | Implemented in strategy behavior; tested partly | Mostly satisfied | Add tests for table release ordering and competing queues |
| Track dining durations | `dinning_time`, `start_service_time`, and `leave_time` are computed | Satisfied | Correct spelling if possible in future cleanup |
| Output average wait time | `output_file.py` and summary CSVs include `avg_wait_time` | Satisfied | None |
| Output max queue length | `output_file.py` and summary CSVs include `max_queue_length` | Satisfied | None |
| Output table utilization | Plot/output files include utilization; `output_file.py` primarily names occupation rate | Mostly satisfied | Standardize occupation versus utilization definitions |
| Include basic input validation | Strong validation in `io_file.py`; 13 validation tests | Strong | None |
| Include 5-6 paired scenarios varying one factor | Baseline, MoreVIP, MoreA, long/short datasets exist; long/short has clear paired outputs | Partially satisfied | Reframe or add 5-6 explicit controlled pairs |
| Present metrics side-by-side | Long/short summaries and report tables do this; other cases are less uniform | Mostly satisfied | Use a consistent side-by-side table for every pair |
| Discuss limitations and real-world comparison | Final report includes limitations and platform research | Satisfied | Tie each case to a specific real-world practice |

## 10. Individual, Attendance, Video, and AI Evidence

| Item | Repository evidence | Judgment |
|---|---|---|
| Individual final reports | No individual report files found | Unable to verify |
| AI use disclosure in individual reports | No individual reports found | Unable to verify |
| Tutorial attendance | Not represented in repository | Unable to verify |
| Video demo | No common video file found | Unable to verify |
| Public GitHub link | Local repository exists; no public URL proof found in checked README/final report search | Partially verifiable |

Important note: the guideline requires AI-use documentation in the Individual Final Report if AI tools were used. Because individual reports are not present in this repository, this review cannot determine whether that requirement was satisfied.

## 11. Priority Improvements

High priority:

1. Make Topic C case-study compliance explicit. Add or reorganize into 5-6 paired scenarios where each pair varies exactly one factor.
2. Add a one-command, non-interactive reproduction workflow for all final report outputs.
3. Ensure individual reports, if submitted separately, include contribution details, reflection, and AI-use disclosure where applicable.
4. Add the public GitHub URL and video demo location to the final report or README if submission rules require it.

Medium priority:

1. Add end-to-end regression tests for exact metrics on small deterministic datasets.
2. Standardize metric names: occupation rate, table utilization, average wait, max wait, average queue length, max queue length.
3. Add a short dataset manifest explaining each test folder, what variable changes, and what output files prove.
4. Improve report concision by separating platform research, assumptions, implemented behavior, and measured results.

Low priority:

1. Rename `dinning_time` to `dining_time` in a future cleanup if compatibility allows.
2. Remove generated cache files from submitted repository if permitted.
3. Add more docstrings to strategy modules and plotting modules.

## 12. Final Assessment

The project would likely be viewed as a solid Topic C submission from the repository evidence alone. It demonstrates meaningful modeling, real implementation, relevant research, working tests, generated case-study data, and a detailed final report.

The biggest opportunity is presentation discipline: the work already contains much of the required substance, but the final grading evidence should be arranged more directly around the manual's wording, especially the Topic C.1 paired-scenario requirement and reproducibility of case-study outputs.

Recommended final action before submission: create a concise compliance appendix in the final report or README that maps every Topic C requirement to a file, command, output, and figure.
