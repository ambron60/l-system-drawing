<img src="/venv/tree.png" alt="">

# L-System Graphical Modeling

An L-system or Lindenmayer system is a parallel rewriting system and a type of formal grammar. An L-system consists of an alphabet of symbols that can be used to make strings, a collection of production rules that expand each symbol into some larger string of symbols, an initial "axiom" string from which to begin construction, and a mechanism for translating the generated strings into geometric structures [[LINK]](https://en.wikipedia.org/wiki/L-system)

This project is a Python-based rendering or interpretation of L-systems as per the title **The Algorithmic Beauty
of Plants** by Przemyslaw Prusinkiewicz and Aristid Lindenmayer [[Book]](http://algorithmicbotany.org/papers/abop/abop.pdf).

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Curves](#curves)
- [Support](#support)
- [License](#license)

## Installation

All the code required to get started is in the file (*lsystem.py*). Only a working installation of Python 3 is necessary [[LINK]](https://www.python.org/).

## Features

L-systems lie at the heart of this project; however, the rewriting and geometric interpretation of such L-systems is accomplished via the [Turtle](https://docs.python.org/3.3/library/turtle.html?highlight=turtle#module-turtle) library in Python 3. The basic idea of turtle interpretation is given below. A state of the Turtle turtle is defined as a triplet (x, y, α), where the Cartesian coordinates (x, y) represent the turtle’s position, and the angle α, called the heading, is interpreted as the direction in which the turtle is facing. Given the step size d and the angle increment δ, the turtle can respond to commands represented by a given set of symbols (i.e., "F" meaning "move forward").

Following the same rewriting rules, this project is capable of creating [[Fractals]](http://mathworld.wolfram.com/Fractal.html) of different forms via a recursive given set of rules input by the user (see [Usage](#usage) section).

## Usage

Here's an example of a plant-like generated L-system (Axial Tree) using the bracketed sequence X->F-[[X]+X]+F[+FX]-X F->FF. The rest of the parameters, such as the number of iterations (n), is described below.

![Axial Tree](https://s7.gifyu.com/images/ezgif.com-cropcc2d2a5cd782a90b.gif)

For example, to create a [Dragon Curve](http://mathworld.wolfram.com/DragonCurve.html) enter the following:

```
Enter rule[1]:rewrite term (0 when done): L->L+R+
Enter rule[2]:rewrite term (0 when done): R->-L-R
Enter rule[3]:rewrite term (0 when done): 0
Enter axiom (initial string): L
Enter number of iterations (n): 10
Enter step size (segment length): 5
Enter initial heading (alpha-0): 90
Enter angle: 90
```

> **Note**: Step size (segment length) is highly dependent on screen size, etc. Adjust as needed, but a good rule of thumb is a value between 5 and 10.

## Axial Trees and Curves

Figure | Derivation
| --- | --- |
Koch Island | F->F-F+F+FF-F-F+F w=F-F-F-F n=2 alpha0=90 angle(i)=90
Koch (1st variation) | F->FF-F-F-F-F-F+F w=F-F-F-F n=3 alpha0=90 angle(i)=90
Koch Islands and Lakes | F->F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF f->ffffff w=F+F+F+F n=2 alpha0=90 angle(i)=90                          
Cuadratic Snowflake | F->F+F-F-F+F w=-F n=4 alpha0=90 angle(i)=90
Hexagonal Gosper curve | L->L+R++R-L--LL-R+ R->-L+RR++R+L--L-R w=L n=4 alpha0=60 angle(i)=60
Axial Tree (node-rewriting) | X->F-[[X]+X]+F[+FX]-X F->FF w=X n=5 alpha0=90 angle(i)=22.5

## Support

For questions or comments:

- Author: **Gianni Perez** @ [skylabus.com](https://www.skylabus.com) or at gianni.perez@us.ibm.com
- [![](http://www.linkedin.com/img/webpromo/btn_liprofile_blue_80x15.png)](http://uk.linkedin.com/in/gianni-perez)


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ambron60/l-system-drawing/blob/master/LICENSE.md)
