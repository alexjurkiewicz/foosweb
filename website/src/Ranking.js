import React, { Component } from 'react';

function precisionRound(number, precision) {
  var factor = Math.pow(10, precision);
  return Math.round(number * factor) / factor;
}

function playerRankEntry(player) {
  return <li>{player.PlayerName}: {precisionRound(player.mu, 2)} mmr</li>;
}

class Ranking extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    fetch('https://api.foosweb.jurkiewi.cz/player')
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        console.log(data);
        data = data.sort((a, b) => {
          return b.mu - a.mu;
        });
        this.setState({
          "players": data
        });
      }.bind(this));
  }

  render() {
    let players = []
    if (this.state.players !== undefined) {
      players = this.state.players;
    }
    const newPlayers = players.map(playerRankEntry);
    console.log(players);
    console.log(newPlayers);
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
