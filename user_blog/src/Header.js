import React from 'react'
import web_address from "./WebAddress"
import './Header.css'
export default class Header extends React.Component {
  constructor(){
    super();
    this.state = {
      title: null,
      author: null
    }
  }
  componentDidMount() {
       fetch(web_address + "/api/get_info")
           .then(response => response.json())
           .then(response => {
               let {title, author} = response
               this.setState({
                 title: title,
                 author: author
               })
           })
   }
  render(){
  return (
    <div id="header">
      {this.state.title ? <h1>{this.state.title}</h1> : null}
      {this.state.author ? <h2>by {this.state.author}</h2> : null}
    </div>
  );
}
}
