import React from 'react';
import './App.css';
import Header from './Header'
import Footer from './Footer'
import MainView from './MainView'
import ReadPostView from './ReadPostView'
import web_address from './WebAddress'
import Loading from './Loading'
class App extends React.Component {
  constructor(){
    super();
    this.state = {
      isReading: false,
      title: null,
      post_titles: []
    }
    this.isReadingHandler = this.isReadingHandler.bind(this);
  }

  isReadingHandler(e) {
    let {name} = e.target;
    if (name === "go_back"){this.setState({
      isReading: false,
      title: null
    })} else {
      this.setState({
        isReading: true,
        title: name
      })
    }
  }

  componentDidMount(){
    fetch(web_address + "/api/get_post_list")
    .then((response) => {
      return response.json()
    }).then((response) => {
      console.log(response)
      this.setState({
        post_titles: response
      })
    })
  }

  render(){
  return (
    <div id="app">
      <Header />
      { this.state.post_titles.length !== 0 ?
        (this.state.isReading
        ? <ReadPostView isReadingHandler={this.isReadingHandler} title={this.state.title}/>
        : <MainView postTitles={this.state.post_titles} isReadingHandler={this.isReadingHandler}/>)
        : <Loading />}
      <Footer />
    </div>
  );
}
}

export default App;
