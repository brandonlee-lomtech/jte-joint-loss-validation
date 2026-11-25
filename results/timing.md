| Scenario | This solver | Official exact | MC | IS |
|---|---:|---:|---:|---:|
| adb-base | 1.6 ms | 2.7 ms | 4.5 ms | 5.3 ms |
| adb-independent | 7.5 ms | 4.3 ms | 6.2 ms | 7.0 ms |
| adb-common-shock | 1.7 ms | 3.0 ms | 5.0 ms | 5.7 ms |
| adb-rain-stress | 1.7 ms | 7.4 ms | 9.3 ms | 10.0 ms |
| adb-rain-cover | 1.6 ms | 8.6 ms | 10.4 ms | 11.1 ms |

Median wall time including model load (this solver: 10 in-process runs; others: `qjlb run` median_one_off_seconds). Parity with the official exact solver; no speed-up is claimed.
