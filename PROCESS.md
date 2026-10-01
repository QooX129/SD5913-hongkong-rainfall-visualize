# Process

<!-- Same as assignment 1, same honesty. Which tools you used and for what; one
thing you kept and why it was good; one thing you rejected and why it was wrong.
"I did not use any" is fine if it is true.

If a model wrote most of plot.py, which is likely and allowed, the interesting part
is what you had to correct: did it invent a column name, use pandas where a list
would do, silently drop the rows it could not parse? -->

Step 1: decide which phenomenon and time range I want to show, and further communicate with Copilot to confirm that the data I want is possible to get. 

Step 2: ask the Coplito to change the data fetching path and update the graph ploting logic.

## Tools

Gituhub Copilot within Visual Studio Code
## Kept

After confirming the topic is daily total rainfall data over a month, I asked Copilot to update the fetch data path, which receives user input for the year and month, then store the data in the \data folder and plot the graph.
## Rejected

Initially, I would like to obtain all rainfall data over 18 districts in Hong Kong, however, after further research, rainfall data for the 18 districts only provide the latest 1-hour. If I want a full record over the year, it only provides the daily total rainfall recorded in the Hong Kong Observatory Station not the 18 districts. 