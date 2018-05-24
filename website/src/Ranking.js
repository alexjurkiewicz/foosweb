import React, { Component } from 'react';

class Ranking extends Component {
  constructor(props) {
    super(props);
    this.state = {rankingData: {}};
    fetch('https://api.foosweb.jurkiewi.cz/player')
      .then(function(response) {
        console.log(response);
        this.state.rankingData = response.body;
      })
  }
  render() {
    return (
      <div className="Ranking">
        Here is the player ranking:
      </div>
    );
  }
}

export default Ranking;
