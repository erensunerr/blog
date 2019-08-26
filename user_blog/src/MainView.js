import React from 'react'
import SmallView from "./SmallView"
import "./MainView.css"

export default function MainView(props) {

    let style = {
        display: "grid",
        gridTemplateColumns: "40px 300px 40px 300px 40px 300px 40px",
        gridTemplateRows: "40px 300px ".repeat(
          props.postTitles.length - (props.postTitles.length % 3) === 0 ? 0 : ((props.postTitles.length - (props.postTitles.length % 3)) / 3) - 1
        )
    }
    return (
      <div id="main-view" style={style}>
      {
      props.postTitles.map((title) => {
        return (
        <SmallView index={props.postTitles.indexOf(title)} title={title} name={title} onClickHandler={props.isReadingHandler} key={title}/>
      );
      })
      }
      </div>
  );

}
