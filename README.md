<img src="http://www.sidefx.com/docs/houdini/nodes/images/lsystems/roll5.png" alt="">

# Py-L-Sys

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

- All the code required to get started is in the file (*lsystem.py*). Only a working installation of Python 3 is necessary [[LINK]](https://www.python.org/).

## Features

L-systems lie at the heart of this project; however, the rewriting and geometric interpretation of such L-systems is accomplished via the [Turtle](https://docs.python.org/3.3/library/turtle.html?highlight=turtle#module-turtle) library in Python 3. The basic idea of turtle interpretation is given below. A state of the Turtle turtle is defined as a triplet (x, y, α), where the Cartesian coordinates (x, y) represent the turtle’s position, and the angle α, called the heading, is interpreted as the direction in which the turtle is facing. Given the step size d and the angle increment δ, the turtle can respond to commands represented by a given set of symbols (i.e., "F" meaning "move forward").

Following the same rewriting rules, this project is capable of creating [[Fractals]](http://mathworld.wolfram.com/Fractal.html) of different forms via a recursive given set of rules input by the user (see [Usage](#usage) section).

## Usage

Here's an example of a plant-like generated OL-system using the bracketed sequence F->F[+F]F[-F]F. The rest of the parameters, such as the number of iterations (n), is shown in the below screengrab.

![Alt Text](https://media.giphy.com/media/443krfSzd7qRq6Q8pb/giphy.gif)

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

## Curves

Curve                   | Derivation 
------------------------| --------------------------------------------------------
Koch Island             | F->F-F+F+FF-F-F+F w=F-F-F-F n=2 alpha0=90 angle(i)=90
Koch (1st variation)    | F->FF-F-F-F-F-F+F w=F-F-F-F n=3 alpha0=90 angle(i)=90
Koch Islands and Lakes  | F->F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF
                        | f->ffffff
                          
Cuadratic Snowflake     | F->F+F-F-F+F w=-F n=4 alpha0=90 angle(i)=90

## Support

For questions or comments:

- Author: **Gianni Perez** @ [SKYLABUS.COM](https://www.skylabus.com) or at gianni.perez@us.ibm.com

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ambron60/l-system-drawing/blob/master/LICENSE.md)
