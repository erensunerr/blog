import React from 'react'
import "./SmallView.css"

export default function SmallView(props) {
    let index = props.index;
    let col_start = (2 * (index % 3) + 1) + 1;
    let row_start = index - (index % 3) === 0 ? 0 : 2*((index - (index % 3)) / 3);

    console.log(index, row_start, col_start);
    let style = {
      gridColumnStart: col_start,
      gridColumnEnd: col_start + 1,
      gridRowStart: row_start,
      gridRowEnd: row_start + 1,
    };
    return (
      <button name={props.name} className="small-view-button" style={style} onClick={props.onClickHandler}>
        {props.title}
      </button>
  );
}
