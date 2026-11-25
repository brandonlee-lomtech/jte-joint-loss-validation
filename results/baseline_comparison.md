| Scenario | Target | Exact (qjlb) | This solver: rel. error | MC | Sobol | Strat. | IS |
|---|---|---:|---:|---:|---:|---:|---:|
| adb-base | E[L] | 10.064m | 2e-14 | 0.9% | 0.4% | 0.7% | 1.4% ✗ |
| adb-base | P(joint attach) | 4.4138% | 3e-14 | 5.0% | 2.7% | 2.7% | 2.5% |
| adb-base | P(L>80m) | 1.2047% | 1e-13 | 7.3% ✗ | 6.4% ✗ | 2.4% | 3.5% |
| adb-base | Stop-loss | 0.282m | 4e-13 | 7.8% ✗ | 12.1% ✗ | 3.7% | 4.6% |
| adb-base | P(both exhausted) | 3.163e-05 | 2e-12 | 177.5% ✗ | 177.5% ✗ | 95.6% ✗ | 48.9% ✗ |
| adb-independent | E[L] | 10.064m | 1e-15 | 0.8% | 0.5% | 0.9% | 1.4% ✗ |
| adb-independent | P(joint attach) | 2.7156% | 9e-15 | 6.9% ✗ | 5.9% ✗ | 4.3% | 3.1% |
| adb-independent | P(L>80m) | 0.7186% | 2e-15 | 8.5% ✗ | 11.6% ✗ | 4.6% | 3.4% |
| adb-independent | Stop-loss | 0.171m | 2e-15 | 15.7% ✗ | 21.9% ✗ | 6.3% ✗ | 4.4% |
| adb-independent | P(both exhausted) | 3.924e-06 | 6e-14 | 956.9% ✗ | 956.9% ✗ | 100.0% ✗ | 58.6% ✗ |
| adb-common-shock | E[L] | 10.064m | 4e-14 | 1.1% ✗ | 0.4% | 0.5% | 1.4% ✗ |
| adb-common-shock | P(joint attach) | 5.0526% | 5e-14 | 4.9% | 3.0% | 2.3% | 2.1% |
| adb-common-shock | P(L>80m) | 1.6066% | 1e-13 | 8.1% ✗ | 6.4% ✗ | 3.0% | 2.7% |
| adb-common-shock | Stop-loss | 0.385m | 5e-13 | 7.9% ✗ | 9.3% ✗ | 2.1% | 4.0% |
| adb-common-shock | P(both exhausted) | 4.400e-05 | 2e-12 | 128.2% ✗ | 128.2% ✗ | 63.6% ✗ | 37.3% ✗ |
| adb-rain-stress | E[L] | 11.171m | 6e-15 | 0.9% | 0.4% | 1.1% ✗ | 1.5% ✗ |
| adb-rain-stress | P(joint attach) | 7.0464% | 1e-14 | 3.7% | 2.6% | 2.7% | 3.7% |
| adb-rain-stress | P(L>80m) | 1.3215% | 2e-14 | 6.6% ✗ | 6.3% ✗ | 3.5% | 2.8% |
| adb-rain-stress | Stop-loss | 0.306m | 8e-14 | 7.2% ✗ | 11.2% ✗ | 5.7% ✗ | 4.5% |
| adb-rain-stress | P(both exhausted) | 6.925e-05 | 1e-13 | 120.6% ✗ | 88.9% ✗ | 86.0% ✗ | 25.7% ✗ |
| adb-rain-cover | E[L] | 9.970m | 2e-14 | 0.9% | 0.4% | 0.6% | 1.5% ✗ |
| adb-rain-cover | P(joint attach) | 4.4138% | 3e-14 | 5.0% | 2.7% | 2.7% | 3.3% |
| adb-rain-cover | P(L>80m) | 0.6997% | 2e-13 | 10.5% ✗ | 13.5% ✗ | 5.4% ✗ | 4.7% |
| adb-rain-cover | Stop-loss | 0.171m | 7e-13 | 12.3% ✗ | 13.6% ✗ | 4.6% | 4.1% |
| adb-rain-cover | P(both exhausted) | 3.163e-05 | 2e-12 | 177.5% ✗ | 177.5% ✗ | 95.6% ✗ | 69.1% ✗ |

Sampler cells: relative RMSE over 10 repeats x 8,192 samples (seed 0); ✗ = outside the official evaluation-v1 tolerance. This solver is deterministic; its cell is the relative error vs the official exact value.
