# Portfolio audit — 22 September 2026

Scope: the public portfolio, GitHub profile, and all five linked application repositories. Reviewed repository health, browser demo journeys, and desktop/mobile rendering. Fixes were saved to each affected repository's main branch.

## Fixes

| Project | Changes |
| --- | --- |
| Student Toolkit OS | Theme-aware chart labels; navigation from Analytics and Targets; scrollable Settings; working browser alerts and JSON backup download/restore; validate backups before replacing demo state; browser deadline input; rehydrate theme after restore/reset; explicitly disable native-only reminder controls on web. |
| PredictMyGrade | Prevent overlapping settings controls; two-column desktop settings and single-column mobile layout; regression assertions for control bounds and overlap. |
| Guardian | Keep simulated downloads available for subsequent scans and quarantine restoration; export the filtered history; reset filters; wrap long paths and mobile toolbars; fit navigation at 320px. |
| Academic Performance Calculator | Give module names readable column widths; allow horizontal table scrolling in the compact browser view. |
| Portfolio website | Make the Java runtime audit fail on launch errors instead of accepting an error status as a successful screenshot. |

PC Part Picker and the GitHub profile were reviewed without needing source changes in this pass.

## Verification

- PredictMyGrade: 115 backend tests and 130 browser tests passed. Inspected the corrected live Settings page and mobile dark-theme screenshot.
- Student Toolkit: lint, TypeScript and 19 unit tests passed. Browser journey checks cover backup validation, download/restore, deadline persistence, navigation, mobile overflow, settings scrolling and chart theme colours.
- Guardian: 39 native tests passed with Qt offscreen. Expanded browser checks passed, including restored download redetection, disabled-monitor manual scanning, filtered CSV export and 320px history layout. Inspected final mobile screenshot.
- Academic calculator: Java CI and desktop/mobile browser launch checks passed. Inspected final mobile screenshot with readable names and internal table scrolling.
- PC Part Picker: existing Java and browser checks were green; manually opened the live Java inventory interface.
- Portfolio: local link/site checks passed for all seven HTML pages. Live smoke and desktop/mobile runtime audit passed.

## Scope limits

These are portfolio demonstrations. Guardian's web demo uses simulated files; real ClamAV integration, desktop tray behavior and host permissions require native Linux validation. Student Toolkit scheduled notifications require Android/iOS. The academic calculator's Access database persistence remains desktop-only. PredictMyGrade uses disposable demo accounts and mock billing; deployment can reset demo sessions.

Automated tests and the inspected screenshots cover representative journeys, not every possible input or native environment. No LinkedIn post was published by this audit.
