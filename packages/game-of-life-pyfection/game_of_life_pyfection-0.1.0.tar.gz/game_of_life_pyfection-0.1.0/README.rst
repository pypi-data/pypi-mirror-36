Game of life: Pyfection
=======================

An OO implementation of Conway's Game of life with a apocalyptic twist

.. image:: resources/worksonmymachine.png
   :width: 150pt

Main Features
-------------

* Free software: MIT license
* Dependency free
* Winner of the "Works on my machine" certificate
* Game functions as supposed to
* Most likely all cells will die if enough generations are provided
* Some cells might come back as zombies

Usage
-----

Download from pip
   ::

      pip install -U game_of_life_pyfection

Run from source

   1) Fetch repo

      ::


         git pull https://github.com/Michaelliv/game_of_life_pyfection.git

   2) Move to game directory

      ::

         cd game_of_life_pyfection
   3) run tests

      ::

         python -m unittest discover -s tests -p "test_*"
   4) run game

      ::

         python main.py [width] [height] [infect_after] [max_generations] [seed...]

         -w width              width of the board
         -h height             height of the board
         -i infect_after       generation after which cells are infected
         -m max_generations    maximal amount of generations
         -s seed               initial seed of the board

         example:

             python main.py 2 3 3 6 1 0 0 1 1 1
