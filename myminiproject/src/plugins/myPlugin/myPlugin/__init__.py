"""
This is where the implementation of the plugin code goes.
The myPlugin-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import random
from webgme_bindings import PluginBase

logger = logging.getLogger('myPlugin')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class myPlugin(PluginBase):
  def main(self):
    active_node = self.active_node
    core = self.core
    logger = self.logger
    self.namespace = None
    META = self.META
    logger.debug('path: {0}'.format(core.get_path(active_node)))
    logger.info('name: {0}'.format(core.get_attribute(active_node, 'name')))
    logger.warn('pos : {0}'.format(core.get_registry(active_node, 'position')))
    logger.error('guid: {0}'.format(core.get_guid(active_node)))

    states = []
    def set_board(self):
      nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
      nodes = {}
      for node in nodesList:
        nodes[core.get_path(node)] = node
      self.nodes = nodes
      for path in nodes:
        node = nodes[path]
        name = core.get_attribute(node, 'name')
        if (core.is_instance_of(node, META['GameState'])):
          currentMove= nodes[core.get_pointer_path(node, "currentMove")]
          currentMoveColor = core.get_attribute(currentMove,'color')
          currentMoveTile = core.get_parent(currentMove)
          currentMoveTileRow = core.get_attribute(currentMoveTile, 'row')
          currentMoveTileColumn = core.get_attribute(currentMoveTile, 'column')
          currentPlayer = core.get_attribute(nodes[core.get_pointer_path(node, "currentPlayer")], 'name')
          states.append({"path": path, "name": name, "board": [[None for x in range(8)] for x  in range(8)], "currentPlayer" : currentPlayer,
          "currentMoveColor": currentMoveColor, "currentMoveTileRow": currentMoveTileRow, "currentMoveTileColumn": currentMoveTileColumn}) 
        if (core.is_instance_of(node, META['Tile'])):
          for state in states:
            if state["path"][:4] == path[:4]:
              row = core.get_attribute(node, 'row')
              column = core.get_attribute(node, 'column')
              children = core.get_children_paths(node)
              flips = []
              childColor = None
              childPath = None
              if len(children) > 0:
                childPath = children[0]
                childColor = core.get_attribute(nodes[childPath], 'color')
                for path2 in nodes:
                  node2 = nodes[path2]
                  if (core.is_instance_of(node2, META['mightFlip'])):
                    srcTile = core.get_parent(nodes[core.get_pointer_path(node2, 'src')])
                    dstTile = core.get_parent(nodes[core.get_pointer_path(node2, 'dst')])
                    srcInfo = {'column': core.get_attribute(srcTile, 'column'), 'row':core.get_attribute(srcTile,'row')}
                    dstInfo = {'column': core.get_attribute(dstTile, 'column'), 'row':core.get_attribute(dstTile,'row')}
                    if node == srcTile:
                      flips.append(dstInfo)                           
              state["board"][row][column] = {"color": childColor, "flips": flips}

    def show_states(self):
      for state in self.states:
        stateString = """[
        name: {}
        currentPlayer: {}
        currentMove: color:{}, row{}, column{}
        """.format(state["name"], state["currentPlayer"], state["currentMoveColor"], state["currentMoveTileRow"], state["currentMoveTileColumn"])
        boardString = "board:\n["
        for row in state["board"]:
          rowstring = "["
          for tile in row:
            rowstring += "[color: {}, flips{}]".format(tile["color"], tile["flips"])
          rowstring += "]"
          boardString += rowstring
          boardString += "\n"
        boardString +="]\n]"
        stateString += boardString

    def next_move_viable(self):
      self.valid = False
      self.to_flip = []
      self.next_moves = {"black":"white", "white": "black"}
      flip_directions = [(0,1), (1,0), (1,1), (-1,-1), (1,-1), (-1,1), (-1,0), (0,-1)]
      logger = self.logger
      core = self.core
      nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
      nodes = {}
      for node in nodesList:
        nodes[core.get_path(node)] = node
      self.nodes = nodes
      current_node = self.active_node
      board = core.get_parent(current_node)
      gamestate = core.get_parent(board)
      current_move = self.nodes[core.get_pointer_path(gamestate, "currentMove")]
      current_move_color = core.get_attribute(current_move, 'color')
      next_move_color = self.next_moves[current_move_color]
      self.next_move_color = next_move_color
      state_path = gamestate["nodePath"]
      for state in self.states:
        if state_path == state['path']:
          board_ref = state['board']
          column = core.get_attribute(current_node, 'column')
          row = core.get_attribute(current_node, 'row')
          if board_ref[row][column]['color'] == None:
            for direction in flip_directions:
              to_flip = []
              if board_ref[row + direction[0]][column + direction[1]]['color'] == current_move_color:
                to_flip = [(row + direction[0], column + direction[1])]
                multiplier = 2
                while (row + (direction[0]*multiplier) > 0 and row + (direction[0]*multiplier) < 8) and (column + (direction[1]*multiplier) > 0 and column + (direction[1]*multiplier) < 8):
                  if board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]['color'] == next_move_color:
                    end_position = (row + direction[0]*multiplier, column + (direction[1]*multiplier))
                    for position in to_flip:
                      self.to_flip.append(position)
                    self.valid = True
                  to_flip.append((row + direction[0]*multiplier, column + (direction[1]*multiplier)))
                  multiplier +=1
      return

    # Highlights moves.
    def highlight_move(self, row, column):
      self.valid = False
      self.to_flip = []
      self.next_moves = {"black": "white", "white": "black"}
      flip_directions = [(0,1), (1,0), (1,1), (-1,-1), (1,-1), (-1,1), (-1,0), (0,-1)]
      logger = self.logger
      core = self.core
      nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
      nodes = {}
      for node in nodesList:
        nodes[core.get_path(node)] = node
      current_node = self.active_node
      board = core.get_parent(current_node)
      gamestate = core.get_parent(board)
      current_player = nodes[core.get_pointer_path(gamestate, "currentPlayer")]
      current_move_color = core.get_attribute(current_player, 'color')
      next_move_color = self.next_moves[current_move_color]
      self.next_move_color = next_move_color
      state_path = gamestate["nodePath"]
      for state in self.states:
        if state_path == state['path']:
          board_ref = state['board']
          if board_ref[row][column]['color'] == None:
            for direction in flip_directions:
              to_flip = []
              if board_ref[row + direction[0]][column + direction[1]]['color'] == current_move_color:
                to_flip = [(row + direction[0], column + direction[1])]
                multiplier = 2
                while (row + (direction[0]*multiplier) > 0 and row + (direction[0]*multiplier) < 8) and (column + (direction[1]*multiplier) > 0 and column + (direction[1]*multiplier) < 8):
                  if board_ref[row + direction[0]*multiplier][column + (direction[1]*multiplier)]['color'] == next_move_color:
                    end_position = (row + direction[0]*multiplier, column + (direction[1]*multiplier))
                    for position in to_flip:
                      self.to_flip.append(position)
                    self.valid = True
                  to_flip.append((row + direction[0]*multiplier, column + (direction[1]*multiplier)))
                  multiplier +=1
      return

    def make_new_state(self):
      import re
      if not self.valid:
        self.logger.error("THIS IS AN INVALID MOVE")
        self.create_message(self.active_node, "THIS IS AN INVALID MOVE")
        return
      active_node = self.active_node
      core = self.core
      logger = self.logger
      META = self.META
      nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
      nodes = {}
      for node in nodesList:
        nodes[core.get_path(node)] = node
      self.nodes = nodes
      logger.info(self.to_flip)
      parent_state = core.get_parent(core.get_parent(active_node))
      game_folder = core.get_parent(parent_state)
      self.row = core.get_attribute(active_node, 'row')
      self.column = core.get_attribute(active_node, 'column')
      black_count = 0
      white_count = 0
      parent_name = core.get_attribute(parent_state, 'name')
      new_name = parent_name + "_1"
      try:
        for i, c in enumerate(parent_name):
          if c.isdigit():
            number_index = i
            break
        state_number = int(parent_name[number_index:]) + 1
        new_name = parent_name[:number_index] + f"{state_number}"
      except:
        pass
      copied_node = core.copy_node(parent_state, game_folder)
      core.set_attribute(copied_node, 'name', new_name)
      child_paths = core.get_children_paths(copied_node)
      old_player = core.get_pointer_path(copied_node, "currentPlayer")
      for child_path in child_paths:
        child = core.load_by_path(self.root_node, child_path)
        if core.is_instance_of(child, META["Player"]):
          if not child_path == old_player:
            core.set_pointer(copied_node, "currentPlayer", child)
        if core.is_instance_of(child, META["Board"]):
          board = child
          tile_paths = core.get_children_paths(board)
          for tile_path in tile_paths:
            tile = core.load_by_path(self.root_node, tile_path)
            if core.get_children_paths(tile):
              piece_path = core.get_children_paths(tile)[0]
              piece_color = core.get_attribute(core.load_by_path(self.root_node, piece_path), 'color')
              if (core.get_attribute(tile, 'row'), core.get_attribute(tile, 'column')) in self.to_flip:
                core.set_attribute(core.load_by_path(self.root_node, piece_path), 'color', self.next_move_color)
                piece_flip_color = core.get_attribute(core.load_by_path(self.root_node, piece_path), 'color')
                if piece_flip_color == "black":
                    black_count += 1
                elif piece_flip_color == "white":
                    white_count += 1
              else:
                if piece_color == "black":
                    black_count += 1
                elif piece_color == "white":
                    white_count += 1
            elif core.get_attribute(tile, 'row') ==self.row and core.get_attribute(tile, 'column') ==self.column:
                created_piece = core.create_node({'parent':tile, 'base': META["Piece"]})
                core.set_pointer(copied_node, "currentMove", created_piece)
                core.set_attribute(created_piece, 'color', self.next_move_color)
                new_piece_color = core.get_attribute(created_piece, 'color')
                if new_piece_color == "black":
                    black_count += 1
                elif new_piece_color == "white":
                    white_count += 1
      logger.warning("Black Pieces:")
      logger.warning(black_count)
      logger.warning("White Pieces:")
      logger.warning(white_count)
      copied_board_paths = core.get_children_paths(copied_node)
      for board_child in copied_board_paths:
          copied_board = core.load_by_path(self.root_node, board_child)
          if core.is_instance_of(copied_board, META["Board"]):
            copied_tile_paths = core.get_children_paths(copied_board)
            for tile_child in copied_tile_paths:
              copied_tile = core.load_by_path(self.root_node, tile_child)
              if core.is_instance_of(copied_tile, META["Tile"]):
                self.active_node = copied_tile
      self.util.save(self.root_node, self.commit_hash, self.branch_name)

    # Undo last action (Is not currently being called)
    def undo_last_move(self):
      core = self.core
      logger = self.logger
      parent_state = core.get_parent(core.get_parent(self.active_node))
      last_state_name = core.get_attribute(parent_state, 'name')
      try:
          index = last_state_name.rindex('_')
          last_state_number = int(last_state_name[index + 1:])
      except ValueError:
          last_state_number = 0
      if last_state_number == 0:
        logger.info(f"Currently at oldest game state")
      else:
        core.delete_node(parent_state)
        logger.info(f"Undo: Reverted to previous game state")
      # SHOULD CHANGE GAMESTATE BACK TO PREVIOUS INSTEAD OF JUST DELETING, BUT WAS NOT ABLE TO FIGURE OUT LOGIC TO IT
      self.util.save(self.root_node, self.commit_hash, self.branch_name)
      
    # Have the computer make a move
    def ai_move(self):
      import re
      nodesList = core.load_sub_tree(core.get_parent(core.get_parent(core.get_parent(active_node))))
      nodes = {}
      for node in nodesList:
        nodes[core.get_path(node)] = node
      self.nodes = nodes
      self.states = states
      self.highlight = []
      for row in range(7):
        for column in range(7):
          highlight_move(self, row, column)
          if self.valid:
            self.highlight.append({'row': row, "column": column})                  
      logger.warning("AI HIGHLIGHTS:")
      logger.warning(self.highlight)
      if not self.highlight:
          self.logger.info("AI has no valid moves.")
          return
      move = random.choice(self.highlight)
      row = move['row']
      column = move['column']
      current_node = self.active_node
      board = core.get_parent(current_node)
      gamestate = core.get_parent(board)
      current_move = nodes[core.get_pointer_path(gamestate, "currentMove")]
      current_move_color = core.get_attribute(current_move, 'color')
      next_move_color = self.next_moves[current_move_color]
      self.next_move_color = next_move_color
      logger.warning(current_move)
      core.set_attribute(current_move, 'row', row)
      core.set_attribute(current_move, 'column', column)
      # SHOULD WORK IF LOGIC IS ADDED TO CHANGE GAME STATE TO THE NEW ONE

    set_board(self)
    self.states = states
    self.highlight = []
    for row in range(7):
      for column in range(7):
        highlight_move(self, row, column)
        if self.valid:
          self.highlight.append({'row': row, "column": column})                  
    logger.warning("Here are the highlighted/valid moves the current player can make:")
    logger.warning(self.highlight)
    next_move_viable(self)
    make_new_state(self)
    set_board(self)
    self.states = states
    ai_move(self)
    make_new_state(self)