import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { icon } from '@fortawesome/fontawesome-svg-core/import.macro';
import { useState } from 'react';
import CONSTANTS from 'constants.js';

export default function Tile({player, piece, position, win}) {

    const [hasMouse, setMouse, onHasMouseChange] = useState(false);

    const onTileClick = () => {
        if (piece === CONSTANTS.PIECE.EMPTY) {
            WEBGME_CONTROL.playerMoves(player, position);
        }
    }

    const onMouseEnter = () => {
        setMouse(true);
    }

    const onMouseLeave = () => {
        setMouse(false);
    }

    const getPiece = () => {
        console.log('GP:',player,piece,position,win);
        const styleO = {fontSize:'90px', paddingLeft:'8px',paddingTop:'2px'};
        const styleX = {fontSize:'90px', paddingLeft:'13px',paddingTop:'2px'};
        const dStyle = player === CONSTANTS.PLAYER.O ? 
            JSON.parse(JSON.stringify(styleO)) : 
            JSON.parse(JSON.stringify(styleX));
        dStyle.opacity = 0.5;

        let style = dStyle;
        let myIcon = null;
        switch (piece) {
            case CONSTANTS.PIECE.O:
                style = styleO;
                myIcon = <FontAwesomeIcon icon={faCircle} style={{ color: 'black' }} />;
                break;
            case CONSTANTS.PIECE.X:
                style = styleX;
                myIcon = <FontAwesomeIcon icon={faCircle} style={{ color: 'white', border: '1px solid black' }} />;
                break;
            default:
                if(hasMouse) {
                    if(player === CONSTANTS.PLAYER.O) {
                        myIcon = <FontAwesomeIcon icon={faCircle} style={{ color: 'black' }} />;
                    } else {
                        myIcon = <FontAwesomeIcon icon={faCircle} style={{ color: 'white', border: '1px solid black' }} />;
                    }
                }
        }
        if (isValidMove(position)) {
            style.border = '2px solid yellow';
          }
        if(myIcon !== null) {
            return (<FontAwesomeIcon style={style} icon={myIcon} size='xl'/>); 
        }

        return null;
    }

    const getTile = () => {
        const style = {
            width:'100px', 
            height:'100px', 
            borderColor:'black',
            borderWidth:'2px',
            border:'solid'};

            if (win && win.positions.indexOf(position) !== -1) {
                style.backgroundColor = '#EE2E31';
            } else if(hasMouse) {
                if(piece === CONSTANTS.PIECE.EMPTY) {
                    style.backgroundColor = '#F4C095';
                } else {
                    style.backgroundColor = '#1D7874';
                    style.opacity = 0.75;
                }
            }
            if (isValidMove(position)) {
                style.backgroundColor = '#76c7c0'; // Change the background color for valid moves
              }
            return (<div onClick={onTileClick} 
                style={style}
                onMouseEnter={onMouseEnter}
                onMouseLeave={onMouseLeave}>{getPiece()}</div>);
    }

    return getTile();
}