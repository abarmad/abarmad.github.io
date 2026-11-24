README

EXPERIMENT DESCRIPTION
======================
This experiment is a computerized sequence of four classic 2x2 games (also
called matrix games or normal-form games). It is designed to let participants
experience strategic interaction first-hand: how the structure of the payoffs
shapes behavior, when people cooperate and when they do not, how groups
coordinate on one of several possible outcomes, and why some games have no
predictable pure-strategy outcome at all.

Participants play in pairs. In each round, both members of a pair choose
between two actions, Action A and Action B, at the same time and without
communicating. The combination of the two choices determines the points each
person earns, according to a payoff matrix that is shown on screen before the
choice. One member of the pair plays the "Row" role and the other plays the
"Column" role. In the matrix, every cell shows two numbers: the Row player's
points first, then the Column player's points.

The experiment has four games, played one after the other, with 5 rounds each
(20 rounds in total). Participants are randomly re-matched with a new partner
in EVERY round, so nobody builds a relationship with a particular opponent (a
"strangers" design). The Row and Column roles are also re-assigned at random in
every round, so a participant will usually play both roles within a game.

After each game (rounds 5, 10, 15 and 20) everyone is held on a feedback page
until the experimenter moves the class on. This page shows the participant's
total points in the game just played, the percentage of the whole class that
chose A and B in each of the 5 rounds, and how often each cell of the matrix
occurred. The pause is meant to be used for a short class discussion before
the next game starts.

At the end, the participant sees a global leaderboard (total points over all 20
rounds), an overview of every game (cell frequencies and a chart of how the
class's choices evolved), and answers a short feedback survey about how useful
the experiments were.

One instruction handout (PDF) accompanies the game. It explains the structure
of the sequence and how to read a payoff matrix, but it does not show the four
real matrices, because those are displayed on screen at the start of every
round.


THE FOUR GAMES
==============
In the tables below, each cell is (Row payoff, Column payoff). The textbook
names are given for the instructor's convenience only. Participants see the
games as "Game 1" to "Game 4" and are not told what type of game they are
playing.

GAME 1  (Prisoner's Dilemma)

                    Column: A     Column: B
        Row: A        3, 3          0, 4
        Row: B        4, 0          1, 1

    B is a dominant strategy for both players, so (B, B) is the only Nash
    equilibrium, even though both players would earn more at (A, A). Action A
    can be thought of as cooperating and Action B as defecting.

GAME 2  (Coordination game)

                    Column: A     Column: B
        Row: A        4, 4          0, 0
        Row: B        0, 0          2, 2

    Two pure Nash equilibria: (A, A) and (B, B). Both players prefer (A, A),
    but each player's best choice depends on what the other does, so a pair
    can get stuck at the inferior (B, B).

GAME 3  (Battle of the Sexes)

                    Column: A     Column: B
        Row: A        4, 2          0, 0
        Row: B        0, 0          2, 4

    Two pure Nash equilibria: (A, A) and (B, B). Players want to coordinate but
    disagree on which equilibrium is best: the Row player prefers (A, A) and
    the Column player prefers (B, B). Miscoordination pays zero to both.

GAME 4  (Matching Pennies)

                    Column: A     Column: B
        Row: A        2, -2        -2, 2
        Row: B       -2, 2          2, -2

    A zero-sum game: the Row player wants to MATCH the Column player's action
    and the Column player wants to MISMATCH. There is no pure-strategy Nash
    equilibrium. The unique equilibrium is mixed, with each player choosing A
    and B with probability 1/2. Payoffs can be negative in this game.


VARIABLES
=========

CONSTANTS (C)
-------------
NAME_IN_URL        Value: 'matrix_games_sequence'
                   Name of game folder in the participant links

PLAYERS_PER_GROUP  Value: 2
                   Participants are matched in pairs. The number of
                   participants in a session must therefore be even

ROUNDS_PER_GAME    Value: 5
                   Number of rounds of each of the four games

NUM_GAMES          Value: 4
                   Number of different games in the sequence

NUM_ROUNDS         Value: 20 (ROUNDS_PER_GAME x NUM_GAMES)
                   Total number of rounds. Rounds 1-5 are Game 1, rounds 6-10
                   are Game 2, rounds 11-15 are Game 3 and rounds 16-20 are
                   Game 4

TIMEOUT_SECONDS    Value: 60
                   Time limit, in seconds, for the decision page of each
                   round. If it expires, a random choice is made for the
                   participant (see "Important notes on the design")

GAMES              A list of the four games. Each has a name ('Game 1' ...
                   'Game 4') and a payoff matrix written as
                   {(Row choice, Column choice): (Row payoff, Column payoff)}.
                   To change a game, edit the numbers in this list. To change
                   the order of the games, reorder the list


GROUP VARIABLES
---------------
This app defines no group variables of its own. The only group-level column in
the export is oTree's built-in group.id_in_subsession, which identifies the
pair a participant was matched with in a given round. Matching is re-done in
every round, so the same number in different rounds means different people.


PLAYER VARIABLES
----------------
(One value per round per participant.)

player_name        Type: StringField
                   The participant's chosen display name, entered once on the
                   first page in round 1. Used on the final leaderboard

choice             Type: StringField (choices 'A' or 'B')
                   The participant's action in the round. If the participant
                   did not choose in time, the game fills it in with a random
                   'A' or 'B' (equal probability)

is_row             Type: BooleanField
                   True if the participant is the Row player in this round,
                   False if the Column player. Re-assigned at random in every
                   round (the player with id_in_group 1 is the Row player)

opponent_choice    Type: StringField
                   The partner's final choice in this round ('A' or 'B')

opponent_payoff    Type: IntegerField
                   The points the partner earned in this round

payoff             Type: built-in oTree currency/points field
                   The points the participant earned in this round, read from
                   the payoff matrix of the current game. Summed over all 20
                   rounds for the leaderboard. Can be negative in Game 4

q1                 Type: IntegerField (1 to 5)
                   Survey: "From 1 to 5, how useful were the experiments for
                   you to understand economics concepts?" Collected only in
                   the last round. The slider starts at 3

q2                 Type: StringField (choices 'class', 'lab', 'never')
                   Survey: "Have you participated before in experiments on
                   decision making?" Answers: yes in class, yes in a lab, no
                   never. Collected only in the last round

q3                 Type: LongStringField
                   Survey: free-text answer about how the experiments helped
                   the participant learn. Collected only in the last round.
                   Cannot be left empty


GAME FLOW (PAGE SEQUENCE)
=========================
1. Instructions            Round 1 only. Describes the sequence of games and the
                           rules, and asks the participant for a player name
                           in a pop-up window when they click "Start".

2. Submission              Each round. Shows the participant's role (Row or
                           Column), the payoff matrix of the current game and
                           the choice between Action A and Action B. 60-second
                           time limit.

3. ResultsWaitPage         Each round. Waits for the partner, fills in any
                           missing choice at random, and calculates the
                           payoffs of both players.

4. RoundResults            Each round. Shows the participant's choice, the
                           partner's choice, and the points each earned.

5. ExperimenterPauseWaitPage
                           After rounds 5, 10, 15 and 20. Holds every
                           participant until ALL pairs in the session have
                           finished the game.

6. GameFeedback            After rounds 5, 10, 15 and 20. Shows the points
                           earned in the game, the percentage of the class
                           choosing A and B in each round of the game, and
                           the frequency of each matrix cell. This page has no
                           "Next" button: the experimenter has to move the
                           class on (see Step 8).

7. FinalSummary            Round 20 only. Shows the global leaderboard, a
                           summary of each of the four games (cell frequencies
                           and a chart of the percentage choosing A and B in
                           each round), and the feedback survey (q1, q2, q3).

8. ThankYou                Round 20 only. Final thank-you page.


WORKED EXAMPLE
==============
Game 3 (Battle of the Sexes), one round. Matrix cells are
(Row payoff, Column payoff).

                    Column: A     Column: B
        Row: A        4, 2          0, 0
        Row: B        0, 0          2, 4

  Row chooses A and Column chooses A: outcome (A, A), cell 4, 2. The Row
  player earns 4 and the Column player earns 2.

  Row chooses A and Column chooses B: outcome (A, B), cell 0, 0. Both earn 0.

Game 4 (Matching Pennies), one round.

  Row chooses B and Column chooses A: outcome (B, A), cell -2, 2. The Row
  player loses 2 points and the Column player earns 2 points.

If a participant does not choose within 60 seconds, the game picks A or B at
random, so the round is still played and the payoffs are calculated normally.


IMPORTANT NOTES ON THE DESIGN
=============================
- Use an EVEN number of participants. Participants are matched in pairs
  (PLAYERS_PER_GROUP = 2), and oTree will not create a session whose number of
  participants is not a multiple of 2.

- Matching is random across the whole session in every round. In a small
  session the same two people can be paired again by chance. A session of 10 or
  more participants makes repeated pairings uncommon. The minimum is 2.

- Roles (Row or Column) are also random in every round, so within one game a
  participant can be the Row player in some rounds and the Column player in
  others. The role is shown at the top of the decision page.

- The games are always played in the same order (Game 1, 2, 3, 4), so the
  effect of a particular game cannot be separated from the effect of its
  position in the sequence. To change the order, reorder the GAMES list in the
  app's __init__.py.

- Time limit and random choices. If a participant does not choose within the
  60-second limit, a random choice is recorded in the "choice" variable. There
  is NO column marking that a choice was random, so these rounds look like any
  other in the data. The "Page times" download (see the last section) lets you
  find rounds where the decision page took about 60 seconds.

- The experimenter must advance participants after every game. The feedback
  page shown after rounds 5, 10, 15 and 20 has no "Next" button, and
  participants see the message "Please wait for the experimenter to move you
  to the next page". See Step 8 for how to do this.

- The charts on the final summary page need an internet connection, because
  they load the Chart.js library from a public server. Without internet access
  the tables and leaderboard still appear but the charts will be empty.

- The SSEL logo shown at the top of some pages is loaded from the project's
  static files as images/ssel_logo.png. If the file is missing from the
  project's _static folder, the pages still work but the logo does not appear.

- Participants' chosen names are displayed to everyone in the session on the
  final leaderboard. The game does not check that names are unique. Tell
  participants not to use their real full name if you want to keep results
  anonymous.

- The slider for question q1 in the survey starts at 3, and the question is
  required. A recorded 3 therefore cannot be told apart from a participant who
  never moved the slider.

- In Game 4 payoffs can be negative, so a participant's total over the 20
  rounds can be negative too. The leaderboard shows negative totals as they
  are.

- The wait page after rounds 5, 10, 15 and 20 requires ALL participants in the
  session. If one participant leaves or disconnects, nobody can move on from
  that point. See "Participants cannot proceed" under Troubleshooting.


SETTINGS.PY CONFIGURATION
=========================
The project needs a session configuration for the experiment. Example:

    SESSION_CONFIGS = [
        dict(
            name='matrix_games',
            display_name='Strategic Interaction (2x2 Games)',
            app_sequence=['matrix_games_sequence'],
            num_demo_participants=4,
        ),
    ]

The name in app_sequence must be exactly the name of the app's folder. The same
folder name is used as the prefix of the app's columns in the data export. This
app does not need any PARTICIPANT_FIELDS.


RUNNING EXPERIMENT
==================

STEP 1: INSTALL PYTHON
----------------------
oTree runs on Python, so Python must be installed first.

1. Go to https://www.python.org/downloads/ and download the latest Python 3
   installer for your operating system.
2. Run the installer.
   - Windows: on the first screen, CHECK the box "Add Python to PATH" before
     clicking Install. This is the most common source of problems.
   - Mac: follow the default prompts.
3. Confirm Python installed correctly. Open a terminal:
   - Windows: press the Windows key, type "cmd", and press Enter.
   - Mac: press Cmd + Space, type "Terminal", and press Enter.
   Then type the following and press Enter:

       python --version

   (On a Mac, use "python3 --version" if the first command fails.) You should
   see something like "Python 3.12.x". If you see an error, close the
   terminal, reopen it, and try again.


STEP 2: INSTALL oTree
---------------------
In the same terminal, type:

    pip install -U otree

(On a Mac, use "pip3 install -U otree" if "pip" is not found.)

Wait for the installation to finish. To confirm it worked, type:

    otree --version

You should see a version number printed.


STEP 3: DOWNLOAD THE EXPERIMENT FILES
-------------------------------------
1. Download the experiment project folder (the folder containing the
   "matrix_games_sequence" app and the "settings.py" file).
2. If it arrived as a .zip file, unzip it.
3. Save it somewhere easy to find, such as your Desktop or Documents.
   Example: Documents/matrix_games_project


STEP 4: OPEN THE PROJECT FOLDER IN YOUR TERMINAL
------------------------------------------------
In the terminal, use the "cd" command to move into the project folder. For
example:

    cd Documents/matrix_games_project

Check that you are in the right place. The folder should contain a file called
settings.py. To list files, type "dir" (Windows) or "ls" (Mac).


STEP 5: START THE oTree SERVER
------------------------------
Type:

    otree devserver

Leave this terminal window open for the entire session. Closing it will stop
the experiment. When the server is ready you will see a message saying it is
running at http://localhost:8000.

To stop the server later, click on the terminal and press Ctrl + C.


STEP 6: OPEN THE ADMIN PAGE AND CREATE A SESSION
------------------------------------------------
1. Open a web browser (Chrome is recommended) and go to:

       http://localhost:8000

2. Click "Sessions" in the top menu, then "Create new session".
3. Choose "Strategic Interaction (2x2 Games)" from the list of session
   configurations.
4. Enter the number of participants. Use an EVEN number (see "Important notes
   on the design"). They are paired automatically by the game.
5. Click "Create".


STEP 7: GET PARTICIPANTS INTO THE GAME
--------------------------------------
After creating the session, open the "Links" tab. There are two kinds of
links, and you can choose either one.

Option A: Session-wide link (one link for everyone)
- Share the single "Session-wide link" with all participants (on a projector,
  by email, or through your course site). Each participant opens it in their
  own browser and is assigned a spot automatically, in the order they arrive.
- This is the fastest option for a classroom or lab where everyone is present
  at the same time, and is the recommended option for this game, since all
  participants must be present to finish each game.

Option B: Individual participant links (one link per person)
- The "Links" tab also lists a separate link for each participant slot (P1,
  P2, P3, and so on). Copy each link and send one to each person by email,
  text message, or any messaging app.
- Each link is tied to a specific spot in the session. If a participant closes
  their browser or loses their connection, they can reopen their same link and
  return to where they left off. Make sure each person uses only their own
  link, and that no link is shared between two people.
- This is the best option for remote participants who will all join at the
  same agreed time.

Network requirements for Options A and B (running from your own computer)
- Participants must be able to reach your computer over the network. Find your
  computer's local IP address (Windows: type "ipconfig"; Mac: type "ifconfig"
  or check Wi-Fi settings) and replace "localhost" in the link with that
  address, e.g. http://192.168.1.25:8000/...
- You may need to start the server with the following command so that other
  devices can connect:

      otree devserver 0.0.0.0:8000

- Everyone must be on the same network (for example, the same classroom
  Wi-Fi). Links sent by email or message will only work for people on that
  network while your server is running.

Option C: Online / remote participants (outside your network)
- A local server cannot be reached from outside your network. If your
  participants are not on the same network as you, host the project online
  (for example through oTree Hub or Heroku). Once it is hosted, both the
  session-wide link and the individual links will work from anywhere. See the
  official oTree documentation for hosting instructions:
  https://otree.readthedocs.io

Note: you do not need to pair participants manually. The game puts them into
pairs at random, and re-pairs them in every round.

Give participants the instruction handout (PDF) before the session starts, or
display it on a screen.


STEP 8: MONITOR THE SESSION AND MOVE THE CLASS ON
-------------------------------------------------
- Use the "Monitor" tab in the admin page to see each participant's progress
  in real time.
- In each round, participants choose A or B, wait briefly for their partner,
  and see the results of the round. A short wait is normal. If it is long,
  check the Monitor tab to see whose partner has not chosen yet.
- After rounds 5, 10, 15 and 20, participants wait for everyone to finish the
  game and then see the game feedback page. This page has no "Next" button.
  Use the time to discuss the game with the class. When you are ready, move
  everyone on from the Monitor tab (use the "Advance slowest users" button;
  since all participants are on the same page at that point, this moves all of
  them on. The name of the button can differ slightly between oTree versions).
- After round 20, participants see the final summary and fill in the feedback
  survey, then see the thank-you page.


STEP 9: COLLECT THE RESULTS
---------------------------
1. When all participants have finished, go to the "Data" tab in the admin
   page.
2. Click the download button to export the data as a CSV file, which opens in
   Excel or Google Sheets.
3. The file includes, for each participant and each of the 20 rounds, their
   choice, role, partner's choice and payoffs, and the answers to the survey
   questions (in the last round).


TROUBLESHOOTING
---------------

"python is not recognized" (Windows)
    Python was not added to PATH. Re-run the Python installer and check "Add
    Python to PATH".

"otree is not recognized" or "command not found"
    Close and reopen the terminal. If it still fails, try:
    python -m otree devserver

"Address already in use" or port error
    Another program is using port 8000. Close other oTree windows, or start
    the server on a different port:
    otree devserver 8001

Participants cannot connect
    Check that everyone is on the same network, that you used your IP address
    instead of "localhost", and that your firewall allows connections to
    Python.

Session cannot be created / error about the number of participants
    The number of participants must be a multiple of 2. Create the session
    again with an even number.

Participants cannot proceed past a wait page
    The results wait page needs both members of a pair, and the wait page after
    rounds 5, 10, 15 and 20 needs every participant in the session. If one
    person disconnected, closed their browser or is idle, others wait. Ask the
    person to reopen their link, or use the Monitor tab to find them. If
    someone has permanently left, the session may need to be restarted with the
    remaining even number of participants.

Participants are stuck on the game feedback page
    This is expected. The page has no "Next" button, so the experimenter has to
    move the class on (see Step 8).

The charts on the final page are empty
    The computer or network has no internet access to the Chart.js library. The
    leaderboard and the tables still work.

The logo does not appear
    Add the SSEL logo file to the project's _static folder as
    images/ssel_logo.png.

Changes to the code do not appear
    The devserver reloads automatically in most cases. If not, stop it with
    Ctrl + C and start it again.


MORE HELP
---------
Official oTree documentation: https://otree.readthedocs.io
oTree discussion group: https://groups.google.com/g/otree


STEP 10: HANDLING YOUR DATA
---------------------------
oTree exports a lot of extra columns that you do not need for analysis. This
section explains what the file looks like and how to clean it up.


DOWNLOAD THE DATA BEFORE YOU STOP THE SERVER
- When you run "otree devserver", the data is not permanently saved. It may be
  erased when you stop or restart the server, or when you change the code.
  Always download the CSV BEFORE closing the terminal.
- Download it from the "Data" tab of the admin page. Download it again after
  any late participants finish.


WHAT THE FILE LOOKS LIKE
- There is one row per participant (player). Because this game has 20 rounds,
  each round has its own set of columns in the same row.
- Column names are long and use dots. For this game, the app columns follow
  the pattern:

      matrix_games_sequence.3.player.choice
      matrix_games_sequence.3.group.id_in_subsession

  The "3" is the round number (1 to 20). "player" and "group" tell you which
  level the variable belongs to. So the choice in round 12 is
  matrix_games_sequence.12.player.choice. The first part of the name is the
  name of the app's folder.
- If you download the file for just this app (instead of "all apps"), the
  prefix is shorter, for example: 3.player.choice
- Participants who did not finish will have blank cells. Some blanks are
  normal by design:
    player_name is filled only in round 1
    q1, q2 and q3 are filled only in round 20
    role is always blank (the game does not use oTree roles; use is_row)


EXTRA COLUMNS ADDED BY oTree
These are added automatically and are usually safe to delete. Exact names can
vary slightly by oTree version.

  participant.code               Unique ID for the participant (useful as
                                 an anonymous ID; KEEP)
  participant.id_in_session      Participant number in the session (KEEP)
  participant.label              Blank unless you set one
  participant._is_bot            Whether the participant was a bot
  participant._index_in_pages    Internal page tracker
  participant._max_page_index    Internal page tracker
  participant._current_app_name  Internal page tracker
  participant._current_page_name Internal page tracker
  participant.time_started_utc   When the participant first opened the game
  participant.visited            Whether the participant opened their link
  participant.mturk_worker_id    Only used for MTurk; blank here
  participant.mturk_assignment_id Only used for MTurk; blank here
  participant.payoff             oTree's built-in participant payoff, which
                                 sums the per-round payoffs (this equals the
                                 total shown on the leaderboard)
  session.code                   Unique ID for the session
  session.label, session.comment Blank unless you set them
  session.is_demo                True if the session was a demo session
  session.config.*               Many columns copying the session settings
                                 (the same value in every row)
  session.mturk_HITId, etc.      Only used for MTurk; blank here
  matrix_games_sequence.N.subsession.round_number
                                 The round number, 1 to 20
  matrix_games_sequence.N.player.id_in_group
                                 1 or 2: the participant's position in the pair
                                 in that round (1 is the Row player)
  matrix_games_sequence.N.player.role
                                 Always blank here


COLUMNS YOU PROBABLY WANT TO KEEP
(Replace N with each round number, 1 to 20.)
  participant.code
  participant.id_in_session
  session.code
  matrix_games_sequence.N.player.player_name   (round 1 only)
  matrix_games_sequence.N.player.is_row
  matrix_games_sequence.N.player.choice
  matrix_games_sequence.N.player.opponent_choice
  matrix_games_sequence.N.player.payoff
  matrix_games_sequence.N.player.opponent_payoff
  matrix_games_sequence.N.player.q1             (round 20 only)
  matrix_games_sequence.N.player.q2             (round 20 only)
  matrix_games_sequence.N.player.q3             (round 20 only)
  matrix_games_sequence.N.group.id_in_subsession


SUGGESTED CLEANING STEPS (in Excel, Google Sheets, or Python)
1. Save a copy of the original download and never edit it. Do all cleaning in
   a second copy.
2. Delete the columns you do not need (all session.config.*, the participant._
   columns, and the MTurk columns).
3. Rename the long column headers to short ones. For example, rename
   "matrix_games_sequence.3.player.choice" to "choice_r3".
4. Reshape from wide to long. For most analyses (for example, the share of A
   choices by round, cooperation over time in Game 1, or equilibrium selection
   in Games 2 and 3) it is easiest to have one row per participant per round,
   with a "round" column. In Python with pandas this can be done by stripping
   the prefix and using pandas.wide_to_long, or by melting each variable and
   merging.
5. Add the game number. Rounds 1-5 are Game 1, rounds 6-10 are Game 2, rounds
   11-15 are Game 3 and rounds 16-20 are Game 4.
6. Remove test data. If you ran practice or demo sessions, delete those rows.
   Check session.code or session.is_demo to tell sessions apart.
7. Check for incomplete sessions. If a participant dropped out, their later
   rounds will be blank and their partners in those rounds may be affected.
   Decide in advance how you will treat these sessions and note it in your
   records.
8. Check that pairs match. Within a session and round, the two members of a
   pair (same group.id_in_subsession) should show each other's choice as
   opponent_choice and each other's payoff as opponent_payoff.
9. If you combine several sessions into one file, keep session.code so you can
   tell them apart, and do not rely on id_in_session alone because it restarts
   at 1 in every session.


DATA CLEANING PYTHON FILE
If you don't want to manually select which columns you want to keep, you can
run the provided "data_cleaner.py" python script to generate cleaned up
versions of the csv file. It needs the pandas package ("pip install pandas").
Before running it, first make sure that you update the name or path of the raw
csv file at the top of the script, and then you can run it with "python3
data_cleaner.py". The script finds the name of the app in the csv by itself (set
APP_NAME at the top if your csv contains several apps). It produces two files:

  matrix_games_cleaned.csv
      Wide format, one row per participant. Keeps the identifiers and every
      app column for all 20 rounds.

  matrix_games_cleaned_long.csv
      Long format, one row per participant per round, with a "round" column.
      Player variables keep their names (choice, payoff, ...) and group
      variables get a "group_" prefix (group_id_in_subsession). It also adds
      these derived columns:

        game_number            1 to 4: which game the round belongs to
        round_in_game          1 to 5: the round within that game
        pair_id                identifies the pair in a round (both partners
                               have the same value)
        role                   "Row" or "Column" in that round
        row_choice             the Row player's action (A or B)
        column_choice          the Column player's action (A or B)
        outcome                the cell played, e.g. "AB" means Row chose A
                               and Column chose B
        choice_A               1 if the participant chose A, 0 if B
        points_in_game_so_far  running total of points within the current game
        total_points_so_far    running total of points since round 1

By default the script drops the player_name column from both outputs. Set
DROP_PLAYER_NAMES = False at the top of the script to keep it. The free-text
answers to question q3 are kept, so review them before sharing the data. The
script assumes 5 rounds per game; if you change ROUNDS_PER_GAME in the app,
change it in the script too.

USEFUL DERIVED MEASURES
- Share of Action A, by game and round: the average of choice_A for each
  game_number and round_in_game. This shows learning and convergence over the
  5 rounds of a game.
- Game 1 (Prisoner's Dilemma): the cooperation rate is the share of A, and the
  rate of mutual cooperation is the share of pairs with outcome "AA". Look at
  whether cooperation falls over the rounds.
- Games 2 and 3: the coordination rate is the share of pairs with outcome "AA"
  or "BB". In Game 2, check how often pairs reach the better equilibrium (AA)
  and how often they get stuck at (BB). In Game 3, check which equilibrium
  pairs pick, and whether the Row player's favorite outcome (AA) is more common
  than the Column player's (BB).
- Game 4 (Matching Pennies): the share of A for Row players and for Column
  players, and how far they are from 50 percent.
- Role effects: compare payoffs and choices of Row and Column players within a
  game, using the role column.
- Total score: total_points_so_far in round 20, which equals the leaderboard
  value.
- Survey: summarize q1 (usefulness, 1 to 5), q2 (earlier experience) and read
  the q3 answers. Remember that q1 starts at 3.


PRIVACY
- The data includes participants' chosen player names and their free-text
  answers to q3, which may contain identifying information. Treat both as
  potentially identifying.
- For analysis or sharing, replace names with participant.code and delete the
  player_name column. Review the q3 text before sharing.
- Store the original file somewhere secure (not a shared or public drive), and
  follow your institution's rules on data handling.


OPTIONAL: PAGE TIMES AND OTHER EXPORTS
- The "Data" tab also offers a "Page times" download, which shows how long
  each participant spent on each page. This is useful for finding rounds where
  the decision page lasted about 60 seconds (a sign that the time limit ran
  out and a random choice was recorded), and for spotting participants who
  were idle or who held up the class.
- Some versions also offer an "Excel-friendly" version of the CSV and a
  separate download for any extra data your app records.
