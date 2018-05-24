import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Ranking from './Ranking';
import NewGame from './NewGame';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Kounta Foosball Tracker</h1>
        </header>
        <NewGame/>
        <hr/>
        <Ranking/>
      </div>
    );
  }
}

export default App;
