## Models

Match:
```json
{
  "timestamp": 0,
  "team1_before": "<team>",
  "team2_before": "<team>",
  "score": [0, 0],
  "team1_after": "<team>",
  "team2_after": "<team>"
}
```

* The "win value" will be shared proportionately between teams based on the scores. Example: score [0, 10] will give more MMR to the winners than [5, 10].

Team:
```json
["<player>", "<player>"]
```

Player:
```json
{
  "name": "string",
  "mu": 0.0,
  "sigma": 0.0
}
```

* **Mu** Represents the player's MMR. Higher is better.
* **Sigma** Represents the uncertainty (standard deviation) about the player's Mu rating. Higher means more uncertainty.

## Tables

* match
  * Contains `match` object
  * Primary key: `[timestamp]`
  * Full record of all matches and the before/after snapshot of player MMR so we can track it over time
* player
  * Contains `player` object
  * Primary key: `[name]`
  * Up to date record of every player to show current scores

## API Endpoints:

* `/match`
  * POST only
  * Submit data:
    ```json
    {
      "team1": ["alex", "elliot"],
      "team2": ["jamie", "brendan"],
      "score": [10, 0]
    }
    ```
  * Returns 200 OK with match record
  * No server-side validation (should be done client-side)
  * Internal process
    1. Get current records for players
    2. Run MMR calculation
    3. Create new player objects
    4. Create match object
    5. Push player objects to player table
    6. Push match object to match table
    7. Return HTTP 200 {match}
* `/player`
  * GET only
  * Returned data:
    ```json
    {
      "players": ["<player>", ...]
    }
    ```
  * Internal process
    1. Scan & return player table
* `/match`
  * GET only
  * Returned data:
    ```json
    {
      "matches": ["<match>", ...]
    }
    ```
  * Internal process
    1. Scan & return match table
