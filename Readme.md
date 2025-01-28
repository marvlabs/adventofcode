# Advent Of Code
https://adventofcode.com/

### Prerequisites
```
export AOC=$HOME/dev/aoc
```

## 2022 some tests

### Trying some easy Perl solutions as intro
```
cd $AOC/2022
./01.pl input/01.input
./02.pl input/02.input
```

## 2023 Perl

```
export PERL5LIB=$AOC/aoclibs/lib
cd $AOC
2023/01.pl
2023/02.pl
2023/17.pl GUI

for i in {01..25}; do 2023/$i NODEBUG; done
2023/getStat2023.pl
```

### Perl helper libs

```
prove $AOC/aoclibs/t/XY.t
```

### Perl module stuff
Try ```h2xs -X -n XY::Board``` to create lib structure next time


## 2015 Python

```
cd $AOC/2015
python 2015_01.py

python 2015.py 01
python 2015.py all
python 2015.py stat
```


## 2024 Python
```
cd $AOC/2024
python 2024_01.py

python 2024.py 01 02 03
python 2024.py all stat
```

# Puzzles
The AOC puzzle inputs are personalized and copyrighted: Don't publish them. That's why they're encrypted here.

To encrypt:
```
cd $AOC
PPW=somepassword
for d in 20??
do
zip  -x "*/.gitempty" -r --encrypt --password $PPW  puzzles/input_$d.zip $d/input
done
```

Decrypt:
```
cd $AOC
PPW=somepassword
for f in puzzles/*.zip
do
unzip  -P $PPW  $f
done
```

# Github
Adding second repo:
- create personal access token on Github
- create aoc repo on github -> adentofcode.git
- add remote, use token as password when asked (gets saved somewhere in MacOs)
```
git config http.postBuffer 524288000 # some side-band connection break otherwise

git remote add gh https://marvlabs@github.com/marvlabs/adventofcode.git 
git remote -v

# Necessary? should not on empty repo
# git pull gh main --allow-unrelated-histories

git ... add ... commit
git push origin
git push gh
```
