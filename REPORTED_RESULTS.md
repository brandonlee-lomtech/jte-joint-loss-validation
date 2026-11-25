# Results reported in the Technical Proposal — produced by the full engine (NOT included in this repository)

> **Read this first.** The numbers on this page were produced by our full joint-tail engine, which is **not** part of this public repository and therefore **cannot be reproduced from this repository**. They are copied verbatim from the full engine's result tables and run logs (snapshot 2026-11-25) so that the panel can match them to the Technical Proposal. No number here is new. Everything that *this* repository reproduces is in [`results/`](results/) and listed in the README. The full engine will be made available to the evaluation panel on request, under confidentiality, in Phase 2.

Labels: all engine runs are classical CPU (`classical_cpu`). The QAE rows are **resource estimates only**; no quantum circuit was executed on hardware. Synthetic n-country portfolios use the official ADB marginals; they are not official benchmarks.

### R1. Scaling: chain of n countries (ADB marginals, 3-year term, T = USD 40m x n)  [source: full-engine table T3]

| n | annual states | MPS time | max bond | dense exact time | check |
|---:|---:|---:|---:|---:|---|
| 2 | 10^2 | 3 ms | 9 | 4 ms | dense diff 1e-11; MC 2M paths: max abs z = 1.25 (5/5 targets observable) |
| 3 | 10^3 | 28 ms | 9 | 99 ms | dense diff 8e-12 |
| 4 | 10^4 | 173 ms | 9 | 6492 ms | dense diff 1e-11 |
| 5 | 10^5 | 216 ms | 9 | not run (10^n memory/time) | MC 2M paths: max abs z = 1.27 (4/5 targets observable) |
| 6 | 10^6 | 240 ms | 9 | not run (10^n memory/time) |  |
| 8 | 10^8 | 305 ms | 9 | not run (10^n memory/time) |  |
| 10 | 10^10 | 324 ms | 9 | not run (10^n memory/time) | MC 2M paths: max abs z = 0.94 (3/5 targets observable) |
| 15 | 10^15 | 484 ms | 9 | not run (10^n memory/time) |  |
| 20 | 10^20 | 680 ms | 9 | not run (10^n memory/time) | MC 2M paths: max abs z = 0.36 (1/5 targets observable) |
| 30 | 10^30 | 1111 ms | 9 | not run (10^n memory/time) |  |
| 50 | 10^50 | 1891 ms | 9 | not run (10^n memory/time) |  |
| 100 | 10^100 | 4186 ms | 9 | not run (10^n memory/time) |  |

### R2. Decision quantities (exact)  [source: full-engine table T7]

| Decision quantity (3-year term) | adb-base | adb-independent | adb-common-shock | Ignoring dependence |
|---|---:|---:|---:|---:|
| Stop-loss pure premium above USD 80m | USD 282,355 | USD 171,266 | USD 385,043 | -39% |
| VaR 99.5% of combined loss | USD 105.0m | USD 87.5m | USD 105.0m | -17.5m |
| ES 99.5% of combined loss | USD 124.0m | USD 111.0m | USD 131.4m | -13.0m |
| Diversification benefit (ES 99.5%) | 16.2% | 25.0% | 11.2% | overstated by 8.8% pts |
| P(both countries pay) — joint trigger | 4.41% | 2.72% | 5.05% | -38% |
| P(both bonds exhausted) | 3.16e-05 | 3.92e-06 | 4.40e-05 | ÷8.1 |
| P(TJK exhausted given KGZ exhausted) | 1.49% | 0.19% | 2.08% | |

| Copula calibrated to the same marginals and P(both pay) | implied P(both exhausted) | ratio to model |
|---|---:|---:|
| Independent | 3.92e-06 | 0.12× |
| Gaussian | 3.04e-05 | 0.96× |
| Student-t (ν = 4) | 2.44e-04 | 7.70× |

| 5-country pool (ADB marginals, T = USD 200m) | chain dependence | independent |
|---|---:|---:|
| ES 99.5% of pool loss | USD 180.6m | USD 168.6m |
| Diversification benefit (ES 99.5%) | 51.2% | 54.5% |
| Stop-loss premium above USD 200m | USD 18,923 | USD 9,014 |



### R3. Resources for the hardest official target, incl. QAE resource estimate (not executed)  [source: full-engine table T8]

| Method | Samples / oracle calls | Notes |
|---|---:|---|
| Plain Monte Carlo | 3,161,151 paths | (1-p)/(p * 0.1^2) |
| Official importance sampling | 120,754 paths | from exact IS variance |
| Ideal amplitude estimation (k = 1 to 2) | 5,586 to 11,171 oracle calls | noiseless, error-corrected assumption |
| Tensor-network contraction (this work) | 1 contraction | ~ms on a laptop CPU, rel. error 1e-11 |

| QAE circuit resource (Qiskit 2.6.2 transpile to {cx, u}) | Value |
|---|---:|
| Logical qubits (3x7 path + objective + ~20 ancillas) | 42 |
| State preparation, one year (7 qubits) | 120 CNOT, depth 241 |
| 21-control Z (Grover diffusion) | 1,682 CNOT |
| Payout oracle (stated estimate, not built) | 480 CNOT |
| One Grover iterate | 5,044 CNOT |
| Longest coherent circuit (M/2 iterates, k = 1) | 14.1 million CNOT |
| CNOT budget for 50 % success at 2-qubit error 1e-3 | 693 CNOT |

### R4. Budget to meet each official tolerance on adb-base  [source: full-engine table T13]

| Target | MC paths | Official IS paths | QAE oracle calls k = 1 | k = 2 | x4 confidence convention |
|---|---:|---:|---:|---:|---:|
| E[L] | 46,004 | 11,092 | 1,213 | 2,425 | 4,851 |
| P(joint attach) | 8,663 | 4,245 | 292 | 585 | 1,170 |
| P(L>80m) | 32,804 | 4,500 | 569 | 1,138 | 2,276 |
| Stop-loss | 57,253 | 5,676 | 1,056 | 2,111 | 4,223 |
| P(both exhausted) | 3,161,151 | 120,754 | 5,586 | 11,171 | 22,343 |

QAE: M = k * pi * sqrt(a(1-a)) / eps. Variances are exact (full enumeration of the 100^3 paths), not extrapolated.


### R5. Largest portfolio within the official tolerances and the official 60 s per-run limit  [source: full-engine table T11; one internal tuning column omitted]

| Dependence graph | n | processes | rtol 1e-12: time / chi / 1-Z / pass | rtol 1e-16: time / chi / 1-Z / pass | max abs z vs reference (paths) |
|---|---:|---:|---|---|---:|
| allpairs | 5 | 24 | 0.2 s / 10 / 5e-13 / pass | 0.1 s / 13 / 4e-14 / pass | 1.5 (1,000,000) |
| allpairs | 10 | 74 | 0.8 s / 10 / 3e-11 / pass | 1.2 s / 14 / 2e-12 / pass | 1.0 (1,000,000) |
| allpairs | 15 | 149 | 2.2 s / 10 / 3e-09 / pass | 5.9 s / 16 / 6e-12 / pass | 1.1 (400,000) |
| allpairs | 20 | 249 | 6.9 s / 11 / 2e-08 / pass | 17.1 s / 18 / 2e-11 / pass | 1.3 (400,000) |
| chain | 5 | 18 | 0.0 s / 9 / 4e-14 / pass | 0.0 s / 10 / 1e-15 / pass | 2.6 (1,000,000) |
| chain | 10 | 38 | 0.0 s / 9 / 9e-14 / pass | 0.0 s / 10 / 4e-15 / pass | 1.1 (1,000,000) |
| chain | 20 | 78 | 0.1 s / 9 / 2e-13 / pass | 0.1 s / 10 / 1e-14 / pass | 1.7 (400,000) |
| chain | 50 | 198 | 0.7 s / 9 / 4e-13 / pass | 0.8 s / 10 / 8e-14 / pass | 1.8 (100,000) |
| chain | 100 | 398 | 2.7 s / 9 / 6e-13 / pass | 3.0 s / 10 / 3e-13 / pass | 1.3 (100,000) |
| chain | 200 | 798 | 11.2 s / 9 / 3e-12 / pass | 11.9 s / 10 / 1e-12 / pass | 1.3 (100,000) |
| longrange | 5 | 20 | 0.0 s / 27 / 3e-13 / pass | 0.0 s / 38 / 2e-14 / pass | 1.3 (1,000,000) |
| longrange | 10 | 43 | 0.3 s / 69 / 3e-12 / pass | 0.8 s / 121 / 9e-14 / pass | 2.8 (1,000,000) |
| longrange | 15 | 65 | 7.4 s / 156 / 2e-11 / pass | 29.9 s / 322 / 5e-13 / pass | 1.0 (400,000) |
| regional | 5 | 19 | 0.2 s / 23 / 6e-13 / pass | 0.1 s / 36 / 2e-15 / pass | 1.8 (1,000,000) |
| regional | 10 | 39 | 0.3 s / 23 / 2e-10 / pass | 0.3 s / 40 / 2e-13 / pass | 1.0 (1,000,000) |
| regional | 20 | 79 | 0.6 s / 18 / 1e-07 / pass | 0.8 s / 37 / 2e-10 / pass | 1.8 (400,000) |
| regional | 50 | 199 | 2.0 s / 9 / 2e-02 / FAIL acc | 2.2 s / 14 / 2e-04 / pass | 32.8 (100,000) |
| regional | 100 | 399 | 5.0 s / 9 / 2e-02 / FAIL acc | 6.2 s / 10 / 2e-02 / FAIL acc | 34.4 (100,000) |
| regional | 200 | 799 | 15.7 s / 9 / 2e-02 / FAIL acc | 16.8 s / 10 / 2e-02 / FAIL acc | 37.4 (100,000) |

Largest n passing (any setting): allpairs n = 20, chain n = 200, longrange n = 15, regional n = 50. Targets: E[L], P(>=2 pay), P(L > USD 160m), E[(L - 160m)+], P(>=2 exhausted), P(>=3 exhausted); official relative tolerances with official absolute floors (money floors scaled to USD 80m x n). Pass = run <= 60 s and every target within tol + 3 se of an independent MC (bulk) / tilted-IS (exhaustion) reference. Times are single-process wall clock measured with 4 experiments running in parallel on 8 cores.

### R6. Re-timing of the largest passing sizes  [source: full-engine run logs e13b, verbatim]

First block: wall clock with other experiments running in parallel on 8 cores. Blocks `e13b_threads1*`: single-threaded BLAS, no other load. A size is within the official limit only if its time is <= 60 s.

```text
# e13b
chain     n=400 rtol=1e-12:   49.3s chi=9 rc=0
chain     n=450 rtol=1e-12:   59.9s chi=9 rc=0
chain     n=500 rtol=1e-12:   73.9s chi=9 rc=0
regional  n= 50 rtol=1e-16:    2.9s chi=14 rc=0
longrange n= 20 rtol=1e-12:   29.9s chi=258 rc=0
longrange n= 21 rtol=1e-12:   66.1s chi=445 rc=0
longrange n= 22 rtol=1e-12:  138.3s chi=508 rc=0
longrange n= 25 rtol=1e-12:  107.2s chi=486 rc=0
allpairs  n= 25 rtol=1e-12:   41.5s chi=14 rc=0
allpairs  n= 28 rtol=1e-12:   62.4s chi=14 rc=0
allpairs  n= 30 rtol=1e-12:   66.2s chi=15 rc=0
# e13b_threads1
allpairs  n= 25 rtol=1e-12:   14.6s chi=14 rc=0
allpairs  n= 28 rtol=1e-12:   18.2s chi=14 rc=0
longrange n= 20 rtol=1e-12:   21.3s chi=258 rc=0
longrange n= 21 rtol=1e-12:   62.7s chi=445 rc=0
chain     n=450 rtol=1e-12:   56.2s chi=9 rc=0
# e13b_threads1_b
allpairs  n= 30 rtol=1e-12:   21.9s chi=15 rc=0
allpairs  n= 35 rtol=1e-12:   36.9s chi=17 rc=0
allpairs  n= 40 rtol=1e-12:   58.2s chi=17 rc=0
longrange n= 22 rtol=1e-12:  122.1s chi=507 rc=0
chain     n=500 rtol=1e-12:   69.9s chi=9 rc=0
regional  n= 50 rtol=1e-16:    2.2s chi=14 rc=0
```

### Withheld-method results not reproduced here

Dependence-stress tests (independent / Gaussian / Student-t / shared-event), non-chain dependence (regional, long-range, all-pairs) and automatic bond-dimension selection are described in the Technical Proposal. Their code is withheld; see README, section "What is withheld and why".
