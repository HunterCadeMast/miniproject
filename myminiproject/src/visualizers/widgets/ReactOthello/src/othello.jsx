import React, {useCallback, useState} from 'react';
import Board from './board';
import CONSTANTS from 'constants.js';

export default function Othello({player, win, board}) {
    const getLabel = () => {
        if(!win) {
            let finished = true;
            board.forEach(piece => {
                if(piece === CONSTANTS.PIECE.EMPTY) {
                    finished = false;
                }
            });
            if(finished) {
                return 'Game ended in tie.';
            }
            
            if(player === CONSTANTS.PLAYER.O) {
                return 'Player Black moves...';
            } else {
                return 'Player White moves...';
            }
        } else {
            if(win.player === CONSTANTS.PLAYER.O) {
                return 'Player Black won!';
            } else {
                return 'Player White won!';
            }
        }
    }
    const countPieces = (color) => {
        return board.reduce((count, piece) => {
          return piece === color ? count + 1 : count;
        }, 0);
      }
      const onUndo = () => {
        if (step > 0) {
          setStep(step - 1);
        }
      };    
      return (
        <div style={{ width: '100%', height: '100%', fontFamily: 'fantasy', fontSize: '36px', fontWeight: 'bold' }}>
          {getLabel()}
          <Board player={player} board={board} win={win} />
          <div>
            Black Pieces: {countPieces(CONSTANTS.PIECE.BLACK)} | White Pieces: {countPieces(CONSTANTS.PIECE.WHITE)}
          </div>
          <button onClick={onUndo}>Undo</button>
        </div>
      );
}