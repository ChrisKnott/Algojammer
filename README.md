# Algojammer

**Algojammer** is an experimental, proof-of-concept code editor for writing algorithms in Python. It was mainly written to assist with solving the kind of algorithm problems that feature in competitions like [Google Code Jam](https://code.google.com/codejam/), [Topcoder](https://tco18.topcoder.com/algorithm/) and [HackerRank](https://www.hackerrank.com/domains/algorithms).

![Editor](https://github.com/ChrisKnott/Algojammer/raw/master/README/Algojammer.gif)  
<sup>Writing code for a Bubble Sort algorithm (sorting array of 10 numbers, then changing code to 100 numbers)</sup>

Algojammer is heavily inspired by <sub><sup>(stolen from)</sup></sub> the work of [Bret Victor](http://worrydream.com/), particularly [Learnable Programming](http://worrydream.com/LearnableProgramming/) (2012) and [Inventing On Principle](https://vimeo.com/36579366) (2012), although it only incorporates some of the ideas presented. A longer list of other influences and similar projects is given in [Inspiration](https://github.com/ChrisKnott/Algojammer#inspiration). 

The project is not finished, but I am not in a position to work on it at the moment, so I am putting it out there in the hope of inspiring others to contribute, or at least provoke some interesting discussion.

## Overview

### Editor
The left hand side of the main window is a text editor where you should write your algorithm. We refer to the contents of the Editor as "Maincode".

![Editor](https://github.com/ChrisKnott/Algojammer/raw/master/README/Editor.png)

This editor uses [Ace](https://ace.c9.io/). See [this page](https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts) for keybindings.

### Execution
By default your code is re-run immediately on any changes. Algojammer is a "time-travelling" or "omniscient" debugger, where steps of execution can be arbitrarily jumped to. There is not really any concept of "debugging" in the sense of controlling the execution of the code via breakpoints or "stepping through". The Execution of your code should be thought of as just a physical *fact* about the lines of text you have written. In the same way we might consider the *"Number Of 'e' Characters"* in the code, or the *"Average Line Length"* of the code, the *"Execution"* of the code, is just a **static fact that is entirely determined by the code**.

Of course, while the *"Number Of 'e' Characters"* is a fairly simple fact - just a single integer - the Execution is quite a complicated fact. The Execution is so complicated, actually, that reasoning about and moulding the Execution into what you want is essentially the entire art and craft of programming. The features of Algojammer are designed to help you understand the Execution of your code *visually*, so it can be **intentionally crafted**, bit-by-bit, into the algorithm you want.

The Execution consists of two elements;
- The **Steps** taken through the code, as each line executes in turn
- The **State** of any variables at any of one of these Steps.

### Timeline
To the right of your code editor is the Timeline, the first tool to help understand the Execution. Each Step is representated by a small square on the Timeline. These squares proceed from left to right, and line up with the corresponding line of code that was executed. The Timeline can be zoomed and scrolled with the mouse, and the Current Step is highlighted. Hold shift to set the Current Step.

![Timeline](https://github.com/ChrisKnott/Algojammer/raw/master/README/Timeline.png)  
<sup>The Timeline with Step #32 highlighted as the Current Step</sup>

The Timeline can give an immediate "feel" or "shape" to an algorithm by giving you some idea of how Execution is distributed across the lines. Notice in the following screenshot of a Bubble Sort algorithm, we can see that with each pass of the algorithm, the bottom two lines are executed less and less frequently. This gives us some hints that this particular sorting algorithm performs well on nearly-sorted data. Other sorting algorithms have a different "shape".

![Bubble Sort](https://github.com/ChrisKnott/Algojammer/raw/master/README/Bubble.png)

### Metacode
In Algojammer, we can interogate and investigate the Execution by writing Metacode. Metacode is **code that we write about the Maincode's Execution**.

A lot of programmers will have, as a final attempt at tracking down a tricky bug, done something like this;
1. Give up on "debugging" (stepping through + watch variables)
2. Add logging EVERYWHERE
3. Run the program
4. Write a script to parse this massive log file
5. Using new superpowers, start investigating the problem

Metacode can be thought of as a reification of this sort of process. The basic idea is... we are programmers, we have chosen Python to describe our algorithm, we might as well use Python to describe the queries we have about that algorithm as well. *"When is x less than y?"*, *"Is p ever twice as big as q at the same time that r is negative?"* etc. - these types of questions are natural answered by writing code.

The following screenshot is from [Chronon](http://chrononsystems.com/), which is an omniscient debugger for Java. The user is adding a filter to find places where a certain condition is true (kind of like a conditional breakpoint).

![Chronon dialog](https://github.com/ChrisKnott/Algojammer/raw/master/README/Chronon.png)  
<sup>Specifying a simple condition via GUI dialog (?!)</sup>

Things like this make me wonder if designers have lost their minds. People have got so used to interacting with computers through dialogs that they struggle to imagine anything else - even if those people *are programmers*, and they ***are programming at the time!*** To be clear, Chronon is an *absolutely phenomenal* product (way better than this project!), but this dialog genuinely reminded me of those [intentionally terrible UIs for entering phone numbers](https://imgur.com/a/4f3XB) that were a meme a while ago. Metacode neatly replaces this kind of clumsiness.

In normal programming environments, the distinction between Maincode and Metacode is not explicit. Usually, Metacode, such as print statements or logging, is mixed directly in with Maincode. For some queries we might have, this is not too bad, but for more advanced queries that incorporate questions about, say, *how data mutates across time*, you might have to actually refactor your code to log the data you want. Explicitly separate Metacode - with an omniscient view of the entire Execution - avoids this issue entirely.

### Sheets
The output of Metacode generally goes on Sheets. Conceptually, Sheets should be thought of like scraps of paper - messy, temporary aids to help with comprehension. They are not part of your algorithm and would normally be discarded as soon as they have achieved their goal, which is greater understanding.

Sheets perform the role that is covered in normal IDEs by watch windows and the debug console, but with the added advantage of being able to output both text and pictures.

![Sheet](https://github.com/ChrisKnott/Algojammer/raw/master/README/Sheet%201.png)  
<sup>The equivalent of a watch variable</sup>
  
![Sheet](https://github.com/ChrisKnott/Algojammer/raw/master/README/Sheet%202.png)  
<sup>Printing an array on multiple lines, with indexes</sup>

![Sheet](https://github.com/ChrisKnott/Algojammer/raw/master/README/Sheet%203.png)  
<sup>Drawing the contents of an array as a bar chart</sup>

![Sheet](https://github.com/ChrisKnott/Algojammer/raw/master/README/Metacode.gif)  
<sup>Editing the Metacode for an output to change it's appearance</sup>

To add an output to a Sheet, right click the Sheet and select 'Add'. To edit that output's Metacode, right click *it* and select 'Edit'.

### State
In a Metacode editor, **any variables that are in scope in Maincode at the Current Step will automatically be in scope**, with their values set to whatever they were on that Step. This is why in the above examples, the Metacode can just refer to `X`, a Maincode variable, and also why the picture changes as we scrub through.

There's nothing to stop you overriding these values but it won't have any effect outside of that code snippet (remember - *Execution is just a static fact!*).

On top of this, **Metacode is completely omniscient**. You also have access to a special variable `jam`, that can be thought of like a Swiss army knife for interrogating the Execution. For example `jam.state(100)` will return a state object for Step #100. So, we can calculate things like `jam.state(1000).x - jam.state(2000).x` - the change in the value of `x` between Step #1000 and Step #2000.

We can also query things like `jam.visits(6)` - an array that tells us every Step that executed Line #6, or `jam.line(250)` - the Line that was executed on Step #250. 

Eventually more 'tools' will be added to the `jam` object such as the ability to query the callstack.

### Markers
(not finished)\
~~Apart from Sheets, the only other place that Metacode can output information is to the Timeline in the form of Markers. Markers are basically the closest Algojammer equivalent to breakpoints. Markers appear on the Timeline as vertical coloured lines, and should be used to show **where in the Execution certain conditions are true**.~~

~~Markers are stored in the dictionary `jam.markers`, which can be read from any Metacode editor, but only written to from the special Marker Editor. You can open the Marker Editor by right clicking the Timeline.~~

~~Only 100 Markers can be set at one time (this is for performance reasons, it's not a design choice).~~

## Demo
A quick demo is available on [YouTube](https://www.youtube.com/watch?v=9XPE4uT0AdE).

![Video](https://github.com/ChrisKnott/Algojammer/raw/master/README/vid.png)

## Running Algojammer
```diff
- The current implementation of Algojammer is extremely hacky and brittle. 
- It *will* crash, do weird things and leak memory like a sieve
- I want to rewrite it from scratch to be more stable, but I'm struggling
- If you are experienced with contributing to CPython and want to help, let me know
```

Install and run Algojammer like this;
```bash
git clone https://github.com/ChrisKnott/Algojammer.git
pip3 install eel
cd Algojammer/c_ext
python3 setup.py build install
cd ..
python3 algojammer.py
```

Currently Algojammer uses [Eel](https://github.com/ChrisKnott/Eel) for the GUI, which means you need Chrome or Chromium installed. The Execution is recorded using a C++ extension that requires a C++11 compiler to build.

Algojammer is only tested on Python 3.5, and due to the very hacky nature in which it is currently implemented, probably doesn't work on many other versions.

## Plans
A critiscism that is sometimes levelled at Bret Victor's (or Chris Grainger's) work is that the demos feel revolutionary but essentially solve "toy problems", and start to creak when you think how they might scale to "real programming".

Algojammer is definitely still within the "toy" sphere. However, I think it moves forward in a couple of important ways. Firstly, it is designed to solve toy problems (questions from algorithm competitions) that are;
1. Outside of my control
2. Genuinely hard
3. Measurable

I think this is important because it attaches a certain degree of **falsifiability** to some of the navel-gazing, pretentious nonsense I've written above. Ultimately, when the clock's ticking in Code Jam, and I just *really need to solve this problem*, do I reach for a tool like Algojammer? This test can't be faked. An actual "bicycle for the mind", is not something that feels revolutionary in a conference talk. An actual bicycle is something that let's me **easily beat people who are better than me in a race**.

So, this is the current goal for the project: **to build a tool that has a provably positive effect on people's performace in Code Jam**.

Unfortunately I have reached the limits of my enthusiasm, ability and ideas at the moment, so I am putting it out slightly early in the hopes that other people can help, or at least to stimulate some interesting discussion.

Please use the [Issues](https://github.com/ChrisKnott/Algojammer/issues) for starting discussions on ideas you might have for either design, or engineering. It doesn't have to be related to Python or Algorithms. I am not interested in actual issues in this actual codebase - this is a demo/prototype.

## Inspiration

If you like things like this, you should check out this stuff...
- [JIVE](https://cse.buffalo.edu/jive/) - an omniscient debugger for Java with visualisations and query based debugging, seems to be a research project of University of Buffalo.
- [Light Table](http://lighttable.com/) - "next generation code editor" by Chris Grainger. See also [What Does Programming Look Like In 10 Years?](https://www.youtube.com/watch?v=zQo4jUVWI_I) and [Toward a better programming](http://www.chris-granger.com/2014/03/27/toward-a-better-programming/) for more advanced ideas.
- [ldb](http://scholar.sun.ac.za/handle/10019.1/96853) - A reverse debugger written as part of Abraham Coetzee's Masters thesis *"Combining reverse debugging and live programming towards visual thinking in computer programming"*. The thesis is full of great insights and gives a great summary of other work.
- [Observable](https://beta.observablehq.com/) - a new type of interactive/explorative coding from Mike Bostock, creator of the D3 visualisation library
- [Seymour](https://harc.github.io/seymour-live2017/) - a Javascript like programming language and associated coding environment, with live diagrams of execution. A Y-Combinator research project by Saketh Kasibatla and Alex Warth.
- [Chronon](http://chrononsystems.com/) - a very professional omniscient debugger for Java ("a DVR for Java").
- [ODB](http://omniscientdebugger.github.io/) - Omniscient Debugger, for Java from 2007, by Bil Lewis. I think this coined the term "omniscient debugger".
- [Chronomancer](https://robert.ocallahan.org/2007/08/announcing-chronomancer_21.html) - An omniscient debugger for C++ from 2007 by Robert O'Callahan
- [rr](https://rr-project.org/) - Also by Robert O'Callahan, a low level reversible debugger - basically an omniscient version of gdb

There are many other projects out there such as [RevPDB](https://morepypy.blogspot.com/2016/07/reverse-debugging-for-python.html) (a reversable debugger for Python from the Pypy team) and [Undo](https://undo.io/) (reversable debugger for C++), but I haven't looked into them in detail.

