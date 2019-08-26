import  React from 'react'
import web_address from './WebAddress'
import "./ReadPostView.css"
export default class ReadPostView extends React.Component {
  constructor(){
    super();
    this.state = {
      body: [],
    }
  }

  componentDidMount(){
    fetch(web_address + "/api/get_post/" + this.props.title)
    .then(response => response.json())
    .then(response => {
      console.log(response)
      this.setState({
        body: response.sections
        })
    })
  }


  render() {
    return (
      <div id="read-post-view">
      <button onClick={this.props.isReadingHandler} name="go_back">Go Back</button>
      <h1>{this.props.title}</h1>
      {
        this.state.body.map(
          (bodyComp) => {
            if (bodyComp.src){
              return (<img src={bodyComp.src} alt={bodyComp.alt} key={this.state.body.indexOf(bodyComp)}/>);
            } else{
              return (<p key={this.state.body.indexOf(bodyComp)} dangerouslySetInnerHTML={{ __html: bodyComp }}></p>)
            }
          }
        )
      }
      </div>
    )
  }
}
