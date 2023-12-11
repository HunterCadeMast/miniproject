# miniproject
---------- READ ME ----------

**Introduction:**
Welcome to the wonderful world of Othello. This repository should contain a working model of a game of Othello. From WebGME, it should run as expected. However, the visualizer is set up with some issues making it not work correctly in WebGME. Any questions feel free to reach out!

**Issues:**
There were a couple of issues that I ran into and I think were very close to being fixed, but I never was fully able to. One was getting the visualizer to fully work. It shows on WebGME but does not run at all. Seems to show an issue with the logger and tried to fix it, but was not successful. Most of the logic for it is change. There were a few that I was not able to implement fully as I did not have the ability to see what I was changing.

The second issue was with the AUTO function and the UNDO function. Those both should fully be implemented, as is highlighting and all the other additions, but I could not figure out how to change the current game state while the plugin is running. I attempted to, but it did not fully fix that though. If this is added, then the rest should work correctly.

**Installation and Usage:**
  - Download the repository locally.
  - Locate the repository (/myminiproject) in the command line and run 'node app.js'
  - Create a new project with the seed 'Othello'.
  - Inside WebGME, attach the 'myPlugin' plugin to the 'Tile' of the META-model.
  - Additionally, attach the 'ReactOthello' visualizer to the 'Tile' of the META-model.
  - From the designated tile of your choice inside of any game state, run 'myPlugin' for WebGME use or use 'ReactOthello' for the visualizer.

**Implementation:**
Inside of our plugin, we have 6 functions
  - main(self)
    - Inside of this function, we run all of our other functions. It starts by instantiating the board and setting up the overall structure.
  - show_states(self)
    - This function formats the states for printing purposes. It is not currently being implemented.
  - next_move_viable(self)
    - Here we search the current move's selection to make sure that the move is valid. It will send back a bool letting us know if we can move there by searching all of the tiles around itself to see if it can move.
  - highlight_move(self, row, column)
    - This is similar to next_move_viable, except it gives every tile through a row and column to know which tiles the current player can currently pick from.
  - make_new_state(self)
    - This will check again if the move is valid and if so, it will flip all of the necessary pieces while also creating a new state.
  - undo_last_move(self)
    - Here we will delete the current game state to return to the previous. It is not currently being implemented.
  - ai_move(self)
    - This should simulate a random move for selecting a valid spot the next player can take.

**Directory Structure:**
Currently, the main directory with information that may be changed is the '/src' directory. It contains the plugins, seeds, and visualizer.
  - plugins
    - Here, our plugin is run by '__init__.py'. The rest of the files add the plugin to the repository.
  - seeds
    - This will create a new META-model for Othello when run.
  - visualizers
    - This contains files for the 'ReactOthello' visualizer. The panel controls which selections are made, the widget controls what will occur with each command, and then 'Visualizers.json' sets our visualizer to run in WebGME.
