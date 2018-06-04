import React, { Component } from 'react';

function precisionRound(number, precision) {
  var factor = Math.pow(10, precision);
  return Math.round(number * factor) / factor;
}

function playerRankEntry(player) {
  return <li key={player.PlayerName}>{player.PlayerName}: {precisionRound(player.mu, 1)} mmr</li>;
}

class Ranking extends Component {
  constructor(props) {
    super(props);
    this.state = {};

    // Get player data
    fetch('https://api.foosweb.test.kounta.com/player')
      .then(function(response) {
        return response.json();
      })
      // Sort top to bottom
      .then(function(data) {
        return data.sort((a, b) => {
          return b.mu - a.mu;
        });
      })
      // Add to state
      .then(function(players) {
        this.setState({
          "players": players
        });
      }.bind(this));
  }

  render() {
    let players = []
    if (this.state.players !== undefined) {
      players = this.state.players;
    }
    const newPlayers = players.map(playerRankEntry);
    return (
      <div className="Ranking">
        <p>Current player ranking:</p>
        <ol>
          {newPlayers}
        </ol>

      </div>
    );
  }
}

export default Ranking;
