import React, { Component } from 'react';

import { KountaPlayers } from './kounta-data';

function optionise(name) {
  return <option key={name} value={name}>{name}</option>;
}

class Ranking extends Component {
  constructor() {
    super();
    this.state = {
      team1score: 0,
      team2score: 0,
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    this.setState({
      [target.name]: target.value
    });
  }

  handleSubmit(event) {
    let match = {
      'team1': [this.state.player1, this.state.player2],
      'team2': [this.state.player3, this.state.player4],
      'score': [this.state.team1score, this.state.team2score],
    }
    // Basic sanity checking
    const players = new Set([this.state.player1, this.state.player2, this.state.player3, this.state.player4]);
    if (players.size !== 4) {
      alert("You have the same player in two spots!");
      event.preventDefault(); return;
    }
    if ((this.state.team1score === "10") === (this.state.team2score === "10")) {
      alert("One score must be 10.");
      event.preventDefault(); return;
    }

    fetch('https://api.foosweb.jurkiewi.cz/match', {
      body: JSON.stringify(match),
      headers: {
        'content-type': 'application/json'
      },
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
    })
    .then(response => response.json())
    .then(responseData => console.log(responseData));

    event.preventDefault();
  }

  render() {
    const nameOptions = KountaPlayers.map(optionise);

    return (
      <div action="/match">
        <p>Submit a new match:</p>
        <form onSubmit={this.handleSubmit}>
          <p>
            Team 1: Player 1:
            <select name="player1" value={this.state.player1} onChange={this.handleChange}>
              {nameOptions}
            </select>
            Player 2:
            <select name="player2" value={this.state.player2} onChange={this.handleChange}>
              {nameOptions}
            </select>
            Score:
            <input type="number" min="0" max="10" name="team1score" value={this.state.team1score} onChange={this.handleChange}>
            </input>
          </p>
          <p>
            Team 2: Player 1:
            <select name="player3" value={this.state.player3} onChange={this.handleChange}>
              {nameOptions}
            </select>
            Player 2:
            <select name="player4" value={this.state.player4} onChange={this.handleChange}>
              {nameOptions}
            </select>
            Score:
            <input type="number" min="0" max="10" name="team2score" value={this.state.team2score} onChange={this.handleChange}>
            </input>
          </p>
          <input type="submit" value="Submit Match" />
        </form>
      </div>
    );
  }
}

export default Ranking;
