# Description

This resository constains the code for solving a [Three Circles Puzzle](https://machinarium.fandom.com/wiki/Prison_Safe_Puzzle) from a Machinarium game, also known as a triangle or Prison Safe puzzle. You can access the tool at [triangle-puzzle-solver.web.app](https://triangle-puzzle-solver.web.app) or by using this repository.

There are three tools in this repository: a python script that allows you to interact with a puzzle and find a solution to any configuration (`main.py`), a script that calculates solutions to all possible puzzles and stores it as a JSON file (`calculate_all_puzzles.py`), and a web app that allows to access these pre-calculated solutions (`website` folder).

Python script:

![Example of a main python script](/images/puzzle_code.png "Main app")

Web app:

![Example of a web app](/images/puzzle_website.png "Wev app")

# Installation and Usage

You need a Python 3.6+ interpreter to run the script. You can install the required packages by running `pip install -r requirements.txt`. Then you can run the main script by executing 
`python main.py` in the terminal.

Executing `python calculate_all_puzzles.py` will store the solutions to all possible configurations in a `solutions.json` file.

Finally, in order to access the web app, just open `index.html` from the `website` folder with any relatively modern browser. This is equivalent to accessing the web app at [triangle-puzzle-solver.web.app](https://triangle-puzzle-solver.web.app).