# Komi [link](https://forums.online-go.com/t/komi-needs-correction-on-9-x-9/2013/7)

This is actually a hot area of contention. Yilun Yang 7p thought 2.5 was the right komi for 9x9. (See commented game #1 20.) This seems common-sense because the board is so small. But he’s in the minority. Virtually all professional 9x9 33 games have used 5.5 komi. That’s TV games, formal tournaments, everything. The RICOH Pair Go cup 4 even used 6.5 for 9x9 decision games. Say what?

It may be helpful to discuss methods of deriving komi. Similar to 19x19, there’s basically two schools of thought: ideal komi and result-based komi. Ideal komi is the komi value that would result in a draw after perfect play from both. We don’t have that for 9x9, unfortunately. However, I’ve been conducting extensive research on 9x9 19 lately using a bot for an evaluation function. Having traced professional games backwards selecting moves with a high evaluation output score, my research currently suggests a value of 6 komi to be ideal. Therefore, the OGS 5.5 should be agreeable for black.

The second school is result-based komi. This method appeals to actual game results, looking to set komi at an equal win rate for black and white. This is probably the majority view, and my research also suggests 5.5 komi here. My collection of 267 pro games (linked above) contains a 47.3% win rate for black opening on tengen and 60% opening at 5-4 and 65.8% opening at 4-4. Over 200 of these games had 5.5 komi and 28 had 6.5. Therefore, OGS komi both conforms to the standard komi and statistical win rates. If anything, more is needed for white.

For these reasons, I believe the initial loss for black is kind of illusory and the advantage of going first will show its worth upon closer inspection.
