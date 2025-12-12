![Advent of Code](./aoc.png)
# Advent of Code 2025
Progress and quick overview of completed puzzles  
_Run `python3 2025.py readme` to refresh this file._  

Run `python3 2025.py all stat` to run the puzzles and print the below statistics.

## Notes
- Animated solutions: `2025_04_anim.py`, `2025_09_anim.py`
- Inputs in `input/<day>.txt` and stats are kept in `2025_stat.json` by the framework
- Day 10 uses linprog from scipy.optimize
  The animations use pygame  
  install if necessary  
  ```
  python -m venv .venv   
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## Puzzle statistics

       Advent of Code 2025                               Tests [run time]  Puzzle [Difficulty, work time, run time]      lessons learned
       ---------------------------------------------------------------------------------------------------------------------------------------
       2025-01 Day 1: Secret Entrance - turn that dial                   0.000s   D1  0:30    0.002s   ...so many special cases to err on...
       2025-02 Day 2: Gift Shop - find patterns in numbers               0.000s   D2  0:30    0.000s   math vs string manipulation?
       2025-03 Day 3: Lobby - find joltage maxen                         0.000s   D1  0:20    0.005s   pos <> pos-1
       2025-04 Day 4: Printing Department - remove paper rolls           0.001s   D2  0:25    0.621s   Which char to compare again???
       2025-05 Day 5: Cafeteria - food ranges                            0.000s   D2  0:15    0.004s   ranges - again; and list comprehension - again
       2025-06 Day 6: Trash Compactor - cephalopod maths                 0.000s   D2  0:30    0.002s   zipit - comprehendit
       2025-07 Day 7: Laboratories - tachyons and quantum tachyons       0.000s   D2  0:30    0.003s   WTF? No bruteforce??? Iterative beats recursion.
       2025-08 Day 8: Playground - wire up them boxes                    0.000s   D2  1:00    0.687s   Why not just do it right the first time? Kruskal's algorithm
       2025-09 Day 9: Movie Theater - is your square in shape?           0.000s   D3  2:00    4.358s   Details, lines, boundaries... aaarghhh
       2025-10 Day 10: Factory - random bashing ALWAYS fixes things      0.007s   D3  2:00    0.114s   LP: scipy optimize for linear programming
       2025-11 Day 11: Reactor - pass fft dac on the way out             0.000s   D2  0:10    0.001s   recursing in AoC always needs a cache
       2025-12 Day 12: Christmas Tree Farm                               0.000s   D2  0:15    0.002s   Sometimes, easy wins.
       ---------------------------------------------------------------------------------------------------------------------------------------
       Advent of Code 2025 Total:   work 8h25m,   runtime 4 seconds
