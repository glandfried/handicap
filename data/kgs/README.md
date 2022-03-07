All public game results are in a gzipped csv file available at https://downloads.gokgs.com/public-games.csv.gz

## Columns:

- Date - Date game started.
- white, black - Self-explanatory.
- Revision - Used only to ensure each game has a unique file name. File name for a file with revision 0 is "http://www.gokgs.com/games/year/month/day/white-black.sgf". With nonzero revision, the end is "white-black-<revision+1>.sgf".
- game_type, board_size, handicap, komi - self explanatory.
- approx_time - Heuristic used in estimating clock speed. Low numbers are fast
  games, high numbers are slow ones.
- score - final score. Negative means White won, positive black won. Some magic numbers:
  -  +/-8192.5 - Win by time.
  -  +/-8193.0 - Win by resign.
  -  8193.5 - No result.
  -  8194.0 - Unfinished.
  -  +/-8194.5 - Forfeit