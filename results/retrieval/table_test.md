| Config | Strategy | Hit@1 | Evidence Hit@3 | MRR@10 | Context Evidence Rate | Avg context chars | Median ms/query |
|---|---|---|---|---|---|---|---|
| dense | dense[B] | 5/8 (62.5%) | 6/8 (75.0%) | 0.744 | 6/8 (75.0%) | 2533.2 | 66.6 |
| chosen | rrf(dense[B]+bm25) | 4/8 (50.0%) | 7/8 (87.5%) | 0.688 | 7/8 (87.5%) | 2503.2 | 68.0 |
