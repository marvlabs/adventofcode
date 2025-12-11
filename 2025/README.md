![Advent of Code](./aoc.png)
# Advent of Code 2025
Progress and quick overview of completed puzzles (auto-extracted CONFIG.name / CONFIG.learned or top docstring / comments).
Run `python3 generate_readme.py` to refresh this file.
## Completed Puzzles
| Day | File | Title / Name | Short summary / Learned |
|-----|------|---------------|-------------------------|
| 0 | `2025_00.py` | title |  |
| 1 | `2025_01.py` | Day 1: Secret Entrance - turn that dial | ...so many special cases to err on... |
| 2 | `2025_02.py` | Day 2: Gift Shop - find patterns in numbers | math vs string manipulation? |
| 3 | `2025_03.py` | Day 3: Lobby - find joltage maxen | pos <> pos-1 |
| 4 | `2025_04.py` | Day 4: Printing Department - remove paper rolls | Which char to compare again??? |
| 4 | `2025_04_anim.py` | Day 4: Printing Department - remove paper rolls | which char to compare??? |
| 5 | `2025_05.py` | Day 5: Cafeteria - food ranges | ranges - again; and list comprehension - again |
| 6 | `2025_06.py` | Day 6: Trash Compactor - cephalopod maths | zipit - comprehendit |
| 7 | `2025_07.py` | Day 7: Laboratories - tachyons and quantum tachyons | WTF? No bruteforce??? Iterative beats recursion. |
| 8 | `2025_08.py` | Day 8: Playground - wire up them boxes | Why not just do it right the first time? Kruskal's algorithm |
| 9 | `2025_09_anim.py` | Day 9: Movie Theater - is your square in shape? | Details, lines, boundaries... aaarghhh |
| 9 | `2025_09.py` | Day 9: Movie Theater - is your square in shape? | Details, lines, boundaries... aaarghhh |
| 10 | `2025_10.py` | Day 10: Factory - random button hitting ALWAYS starts the machine | LP: scipy optimize for linear programming |
| 11 | `2025_11.py` | Day 11: Reactor - pass fft dac on the way out | recursing in AoC always needs a cache |

## Notes
- Animated solutions: `2025_04_anim.py`, `2025_09_anim.py`
- Alternative implementations are in `alternatives/`
- Inputs in `input/` and stats in `2025_stat.json`


        Advent of Code 2025                               Tests [run time]  Puzzle [Difficulty, work time, run time]      lessons learned
        ---------------------------------------------------------------------------------------------------------------------------------------
        2025-01 Day 1: Secret Entrance - turn that dial                   0.000s   D1  0:30    0.002s   ...so many special cases to err on...
        2025-02 Day 2: Gift Shop - find patterns in numbers               0.000s   D2  0:30    0.000s   math vs string manipulation?
        2025-03 Day 3: Lobby - find joltage maxen                         0.000s   D1  0:20    0.004s   pos <> pos-1
        2025-04 Day 4: Printing Department - remove paper rolls           0.001s   D2  0:25    0.635s   Which char to compare again???
        2025-05 Day 5: Cafeteria - food ranges                            0.000s   D2  0:15    0.004s   ranges - again; and list comprehension - again
        2025-06 Day 6: Trash Compactor - cephalopod maths                 0.000s   D2  0:30    0.002s   zipit - comprehendit
        2025-07 Day 7: Laboratories - tachyons and quantum tachyons       0.000s   D2  0:30    0.003s   WTF? No bruteforce??? Iterative beats recursion.
        2025-08 Day 8: Playground - wire up them boxes                    0.000s   D2  1:00    0.692s   Why not just do it right the first time? Kruskal's algorithm
        2025-09 Day 9: Movie Theater - is your square in shape?           0.000s   D3  2:00    4.331s   Details, lines, boundaries... aaarghhh
        2025-10 Day 10: Factory                                           0.006s   D3  2:00    0.176s   LP: scipy optimize for linear programming
        2025-11 Day 11: Reactor                                           0.000s   D2  0:10    0.001s   recursing in AoC always needs a cache
        ---------------------------------------------------------------------------------------------------------------------------------------
