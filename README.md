# A Star Search

A small UI visualization for the A* (star) search algorithm. The User Interface was created using wxGlade.

## Requirements

- Python 3.6.3
  - Numpy
  - wxPython

## Usage

### 1. Input

The program accepts `.txt` files to facilitate the labyrinth input. The file should follow some rules.

1. The first line of the file should contain 04 space-separated values, which corresponds to **number of lines**, **number of columns**, **horizontal** and **vertical move cost**.
2. The following lines should illustrate a labyrinth-like pattern. In these lines could exist 4 differents values, each with one different meaning.
   - **0**: Viable positions
   - **1**: Obstacles
   - **2**: Initial position
   - **3**: Final position.

For exemple, here is an input `.txt`.
```
05 09 01 02
0 0 0 0 0 1 0 0 0
2 0 0 1 0 0 0 1 0
0 0 1 1 0 0 1 0 0
0 0 0 0 0 1 0 0 0
0 1 0 0 0 1 0 0 3
```

### 2. Output

The program output is show in the *Labirinto* tab. Here the semi-optimal path can be seen and the considered search positions.
The remaining options and illustrated and commented in the program UI.

## Gallery
![](https://github.com/Fernandohf/A_Star/blob/master/media/python_2018-10-08_22-17-09.png)
![](https://github.com/Fernandohf/A_Star/blob/master/media/python_2018-10-08_22-17-24.png)
![](https://github.com/Fernandohf/A_Star/blob/master/media/python_2018-10-08_22-17-29.png)
