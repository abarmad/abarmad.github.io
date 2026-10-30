README

EXPERIMENT DESCRIPTION
======================
This experiment is a computerized market game (the "Monopoly Experiment" or
"Monopoly Quantity Game"). It is designed to illustrate the tension between
individual incentives and joint profit: each participant acts as a firm that
chooses between a LOW and a HIGH production quantity. Producing the high
quantity always earns more for the firm, whatever the others do, but the group
earns the most when everybody produces the low quantity. The game also lets
you study what changes when participants can talk to each other.

In each round, every participant privately chooses one option:

    Low Quantity (L)   or   High Quantity (H)

A participant's profit in the round depends on their own choice and on the
number of OTHER participants in the group (out of 4) who chose Low:

    Other players choosing Low   Payoff if Low   Payoff if High
                4                     10              12
                3                      8              11
                2                      6               9
                1                      4               7
                0                      2               5

High pays more than Low in every row (12 > 10, 11 > 8, 9 > 6, 7 > 4, 5 > 2),
so choosing High is always individually best. But if all 5 group members
choose High, each earns 5 (25 in total), while if all 5 choose Low, each earns
10 (50 in total). This is a prisoner's dilemma / collusion game.

The experiment has two parts, played one after the other in the same session:

  PART 1  10 rounds. Groups of 5 are re-formed at random EVERY round, so
          participants never keep the same group. No communication. After each
          round participants see their own choice, their profit for the round
          and their cumulative profit. (They do not see how many others chose
          Low or High; see "Important notes on the design" if you want to
          change that.)

  PART 2  A random number of rounds. Participants are placed in a group of 5
          at random and stay in that group for all rounds of Part 2. After
          every round there is a 10% chance that the round was the last and a
          90% chance that the game continues (on average Part 2 lasts about 10
          rounds). A real-time group chat is available on the decision screen
          before each choice. After each round participants see their own
          choice, the number of other participants who chose Low and High,
          their profit and their cumulative profit.

At the end, a summary page shows the final ranking (Part 1 profit, Part 2
profit and total profit for the members of the Part 2 group), the participant's
round-by-round history for both parts and a chart of the group's total profit
in each round of Part 2.

An instruction handout (PDF, "instructions.pdf", titled "Monopoly Experiment")
accompanies the game. It has one page-set for Part 1 and one for Part 2. The
same text is shown on screen (Instructions page before Part 1, Part2Instructions
page before Part 2). Hand out Part 2 only after Part 1 is finished, if you
want participants to read it at that point.

Groups are formed of exactly 5 participants (PLAYERS_PER_GROUP = 5), so the
number of participants in a session must be a multiple of 5.


VARIABLES
=========

CONSTANTS (C)
-------------
NAME_IN_URL        Value: 'Monopoly_Quantity_Game'
                   Name used in the participant URL

PLAYERS_PER_GROUP  Value: 5
                   Participants per group (the session size must be a multiple
                   of 5)

NUM_ROUNDS_P1      Value: 10
                   Rounds in Part 1 (rounds 1-10)

CONTINUE_PROB      Value: 0.9
                   Probability that Part 2 continues after a round (10% chance
                   that a round is the last)

MAX_ROUNDS_P2      Value: 50
                   Safety cap on the length of Part 2. oTree needs a fixed
                   maximum number of rounds, so rounds that are not needed are
                   skipped. The chance of reaching the cap is about 0.6%

NUM_ROUNDS         Value: 60 (= NUM_ROUNDS_P1 + MAX_ROUNDS_P2)
                   Total number of rounds oTree creates. Rounds 11 and above
                   are Part 2

TIMEOUT_P1         Value: 120
                   Seconds to submit a choice in Part 1

TIMEOUT_P2         Value: 180
                   Seconds to submit a choice in Part 2 (longer because
                   participants can chat)

SHOW_OTHERS_IN_PART1
                   Value: False
                   If True, the Part 1 results page (and the Part 1 history on
                   the summary page) also show how many other participants
                   chose Low and High. Part 2 always shows them

PAYOFF_MATRIX      The payoff table above, [your choice][number of other
                   participants choosing Low]


GROUP VARIABLES
---------------
(One value per round. In Part 1 the groups are different every round; in Part
2 they are fixed.)

total_low          Type: IntegerField
                   Number of participants in the group who chose Low

total_high         Type: IntegerField
                   Number of participants in the group who chose High


PLAYER VARIABLES
----------------
(One value per round per participant.)

player_name        Type: StringField
                   The participant's chosen display name, entered once on the
                   first page in round 1. Used on the final ranking. Letters
                   and numbers only, cannot be empty

choice             Type: StringField ('Low' or 'High')
                   The participant's quantity choice. If a participant does not
                   submit before the timer runs out, a random choice (Low or
                   High) is assigned automatically and is stored here exactly
                   like a real choice (see "Important notes on the design")

others_low         Type: IntegerField
                   Number of OTHER group members (0 to 4) who chose Low

others_high        Type: IntegerField
                   Number of OTHER group members (0 to 4) who chose High
                   (always 4 - others_low)

justification      Type: LongStringField
                   Free-text answer to "Reflective Reasoning: Based on the
                   outcome of this first round, please provide your thoughts on
                   your strategy." Collected only in round 1, on the Results
                   page. Cannot be empty

payoff             Type: built-in oTree currency/points field
                   Profit in the round, taken from the payoff table. Summed
                   over all rounds, it is the participant's total profit


GAME FLOW (PAGE SEQUENCE)
=========================
1. Instructions        Round 1 only. Shows the Part 1 rules and asks the
                       participant for a player name.

2. Part2Instructions   First round of Part 2 (round 11) only. Shows the Part 2
                       rules.

3. Submission          Each round played. The participant chooses Low or High.
                       There is a countdown timer. In Part 2 the group chat is
                       shown on this page.

4. ResultsWaitPage     Each round played. Waits until all 5 group members have
                       decided (or timed out), then tallies the choices and
                       calculates the payoffs.

5. Results             Each round played. Shows the choice, the profit and the
                       cumulative profit (within the current part). In Part 2
                       it also shows how many others chose Low and High. In
                       round 1 only, participants also type their reflective
                       reasoning.

6. Summary             Last round of the session only (the last round of Part
                       2). Shows the ranking, the round-by-round history for
                       both parts and the chart of group profit in Part 2.

Participants cannot tell which Part 2 round is the last one: the Results button
only says "Continue", and the Summary page appears only after the last round.


WORKED EXAMPLE
==============
Five participants (A, B, C, D, E) choose L, L, H, L, H. Three of them chose Low.

  A (Low):   2 OTHERS chose Low  ->  profit 6
  B (Low):   2 OTHERS chose Low  ->  profit 6
  C (High):  3 OTHERS chose Low  ->  profit 11
  D (Low):   2 OTHERS chose Low  ->  profit 6
  E (High):  3 OTHERS chose Low  ->  profit 11

Group total profit = 6 + 6 + 11 + 6 + 11 = 40.
If everybody had chosen Low the total would be 50 (10 each); if everybody had
chosen High it would be 25 (5 each).

In the cleaned data: others_low = (number of Low choices in the group) minus 1
for a Low chooser, and the number of Low choices for a High chooser. Here
group_total_low = 3 for everyone, and others_low is 2 for A, B and D and 3 for
C and E.


IMPORTANT NOTES ON THE DESIGN
=============================
- The session size must be a multiple of 5. Otherwise some participants cannot
  be placed in a group.

- The wait pages require ALL 5 members of the group. If one participant leaves
  or disconnects, the others cannot proceed. See "Participants cannot proceed"
  under Troubleshooting. In Part 2 this is more serious, because the group
  stays together for all rounds.

- Part 1 matching: groups are formed at random in every round. Therefore
  group.id_in_subsession and player.id_in_group change from round to round in
  Part 1 (they identify a group or a position in THAT round only). In Part 2
  the groups and the id_in_group stay the same in every round.

- The number of Part 2 rounds is drawn once, when the session is created: Part
  2 always has at least 1 round, and after each round there is a 10% chance of
  stopping. The drawn length is not stored in the CSV; it can be read off the
  data as (number of rounds with choices) - 10. To fix the length for testing,
  add part2_num_rounds=N to the session configuration (see below).

- Rounds that are not played (after the random stop) exist in the raw CSV but
  have no choices (payoff shows 0 or blank). The cleaning script removes them.

- Timeouts are not flagged. If a participant does not submit in time, the
  game assigns a random choice and the data look the same as a real choice. If
  you need to find such cases, use the "Page times" download (a very long time
  on the Submission page, or no submit time). You could also add a field such
  as timed_out to the code.

- Part 1 results show only choice, profit and cumulative profit, as in the
  instructions. Set SHOW_OTHERS_IN_PART1 = True to show the Low/High counts in
  Part 1 too (and update the instructions to match).

- The chat is shown on the decision screen of Part 2 only (not on the results
  page and not on the wait page). Chat messages are NOT in the main CSV. oTree
  stores them separately; look for a chat log download in the "Data" tab of
  the admin page (the name depends on the oTree version). Participants appear
  in the chat as "Player N" (N = id_in_group), not with their chosen names, but
  they can write anything in the chat, so the chat text may identify people.
  The chat channel of a group is "<session.code>_part2_group_<group id>", which
  is the value of the part2_chat_channel column in the cleaned long file.

- The round 1 reasoning question is not mentioned in the instructions handout.
  Remove it (the justification field, get_form_fields and the block in
  Results.html) if you do not want to collect it.

- Participants' chosen names are only used on the final ranking, which shows
  the names of all 5 members of the Part 2 group. Tell participants not to use
  their real full name if you want to keep results anonymous.

- The Instructions page shows the logo "images/ssel_logo.png" from the static
  folder. If the file is missing from your project, the logo appears as a
  broken image; add the file to the _static/images folder or remove the image
  from Instructions.html.


SETTINGS.PY CONFIGURATION
=========================
The project needs a session configuration for the experiment. Example:

    SESSION_CONFIGS = [
        dict(
            name='monopoly',
            display_name='Monopoly Quantity Game',
            app_sequence=['monopoly'],
            num_demo_participants=5,
        ),
    ]

The app folder name is the prefix of all data columns. The files in the folder
must be: __init__.py, Instructions.html, Part2Instructions.html,
Submission.html, Results.html and Summary.html. If your folder is called
something else, change APP_NAME in the cleaning script (or let the script
detect it). num_demo_participants (and the number of participants you enter
when creating a real session) must be a multiple of 5.

Optional: to run a session with a fixed Part 2 length (for example for testing
the Summary page), add part2_num_rounds=3 (or any number from 1 to 50) to the
session configuration. Leave it out in real sessions, so the length is random.


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
   "monopoly" app and the "settings.py" file).
2. If it arrived as a .zip file, unzip it.
3. Save it somewhere easy to find, such as your Desktop or Documents.


STEP 4: OPEN THE PROJECT FOLDER IN YOUR TERMINAL
------------------------------------------------
In the terminal, use the "cd" command to move into the project folder. For
example:

    cd your/path/to/monopoly_project

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
3. Choose "Monopoly Quantity Game" from the list of session configurations.
4. Enter the number of participants. It must be a multiple of 5 (5, 10, 15,
   ...). The groups are formed automatically: random groups every round in Part
   1, and random groups that stay fixed in Part 2.
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
  members of a group must be present for every round to be completed.

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


STEP 8: MONITOR THE SESSION
---------------------------
- Use the "Monitor" tab in the admin page to see each participant's progress
  in real time.
- Each round, participants submit a choice and then wait on the results wait
  page until all 5 members of their group have submitted (or the timer has run
  out). This is normal. If the wait is long, check the Monitor tab to see who
  is holding things up.
- After Part 1 (10 rounds), participants see the Part 2 instructions and
  continue. Part 2 ends at a random round, and participants then see the final
  summary page.
- Make sure the instruction handout is given to participants before the
  session starts (Part 1) and before Part 2.


STEP 9: COLLECT THE RESULTS
---------------------------
1. When all participants have finished, go to the "Data" tab in the admin
   page.
2. Click the download button to export the data as a CSV file, which opens in
   Excel or Google Sheets.
3. The file includes, for each participant and each round played, their
   choice, the number of other participants who chose Low and High, their
   group's totals, their payoff and, for round 1, the written reasoning.
4. Also download the chat log (if your oTree version offers it) and the "Page
   times" file, if you want to analyze the Part 2 chat or timeouts.


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

Participants cannot proceed past a wait page
    The wait pages continue only when every member of the group has finished
    the previous page. If one person disconnected, closed their browser or is
    idle, the rest of the group waits (the timer will assign that person a
    random choice only if the page is open in their browser). Ask the person
    to reopen their link, or use the Monitor tab to find them. If someone has
    permanently left, the session may need to be restarted with the remaining
    participants.

Error about groups or players per group when creating the session
    The number of participants is not a multiple of 5. Create the session with
    5, 10, 15, ... participants.

The chat does not appear in Part 2
    The chat is shown only on the decision (Submission) page of Part 2, and
    needs the oTree version that supports the chat tag. Check that
    Submission.html is the Part 2 version of the file.

Part 2 ends too early or too late
    The length of Part 2 is random (10% chance of stopping after each round).
    For a fixed length (testing only) add part2_num_rounds to the session
    configuration.

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
- There is one row per participant (player). Because this game has up to 60
  rounds, each round has its own set of columns in the same row. Group-level
  columns (such as total_low) have identical values for all members of the same
  group in a given round.
- Column names are long and use dots. For this game, the app columns follow
  the pattern:

      monopoly.3.player.choice
      monopoly.3.group.total_low

  The "3" is the round number. "player" and "group" tell you which level the
  variable belongs to. So the choice in round 4 is monopoly.4.player.choice.
  Rounds 1-10 are Part 1; rounds 11 and above are Part 2.
- If you download the file for just this app (instead of "all apps"), the
  prefix is shorter, for example: 3.player.choice
- Participants who did not finish will have blank cells. Some blanks are
  normal by design:
    player_name is filled only in round 1
    justification is filled only in round 1 (blank in all other rounds)
    rounds after the random end of Part 2 are blank (no choices at all)
- Every session has its own Part 2 length, so the number of rounds with data
  differs between sessions.
- In Part 1, group.id_in_subsession and player.id_in_group change every
  round, so they cannot be used to follow a group across rounds. In Part 2
  they are the same in every round.


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
                                 sums the per-round payoffs of all rounds
                                 played (Part 1 and Part 2)
  session.code                   Unique ID for the session
  session.label, session.comment Blank unless you set them
  session.is_demo                True if the session was a demo session
  session.config.*               Many columns copying the session settings
                                 (the same value in every row)
  session.mturk_HITId, etc.      Only used for MTurk; blank here
  monopoly.N.subsession.round_number
                                 The round number
  monopoly.N.player.id_in_group  Position of the player within the group
                                 (random every round in Part 1; fixed in Part 2)
  monopoly.N.player.role         Blank unless roles are defined
  monopoly.N.group.id_in_subsession
                                 Group number within the session in that round
                                 (changes between rounds in Part 1)


COLUMNS YOU PROBABLY WANT TO KEEP
(Replace N with each round number played.)
  participant.code
  participant.id_in_session
  session.code
  monopoly.N.player.player_name        (round 1 only)
  monopoly.N.player.id_in_group
  monopoly.N.player.choice
  monopoly.N.player.others_low
  monopoly.N.player.others_high
  monopoly.N.player.payoff
  monopoly.N.player.justification      (round 1 only)
  monopoly.N.group.id_in_subsession
  monopoly.N.group.total_low
  monopoly.N.group.total_high


SUGGESTED CLEANING STEPS (in Excel, Google Sheets, or Python)
1. Save a copy of the original download and never edit it. Do all cleaning in
   a second copy.
2. Delete the columns you do not need (all session.config.*, the participant._
   columns, the MTurk columns) and the columns of rounds that were never
   played.
3. Rename the long column headers to short ones. For example, rename
   "monopoly.3.player.choice" to "choice_r3".
4. Reshape from wide to long. For most analyses (for example, the share of Low
   choices by round, or the effect of chat in Part 2) it is easiest to have one
   row per participant per round, with a "round" column.
5. Remove test data. If you ran practice or demo sessions, delete those rows.
   Check session.code or session.is_demo to tell sessions apart.
6. Check for incomplete sessions. If a participant dropped out, the group
   could not continue, so the remaining rounds will be blank for that group.
   Decide in advance how you will treat these sessions and note it in your
   records.
7. Check that group-level values match. Within a session, round and group, all
   members should show the same total_low and total_high, and total_low
   should equal the number of Low choices in the group. If not, something went
   wrong.
8. If you combine several sessions into one file, keep session.code so you can
   tell them apart, and do not rely on id_in_session alone because it restarts
   at 1 in every session. Remember that every session has its own Part 2
   length.


DATA CLEANING PYTHON FILE
If you don't want to manually select which columns you want to keep, you can
run the provided "data_cleaning.py" python script to generate cleaned up
versions of the csv file. It needs the pandas package ("pip install pandas").
Before running it, first make sure that you update the path to where you have
the raw csv file located (and APP_NAME, if your app folder is not called
"monopoly"; the script also tries to detect the name by itself), and then you
can run it with "python3 data_cleaning.py". It produces two files:

  monopoly_cleaned.csv
      Wide format, one row per participant. Keeps the identifiers and every
      monopoly column for all rounds that were played (rounds that were never
      played are removed).

  monopoly_cleaned_long.csv
      Long format, one row per participant per round played, with a "round"
      column. Player variables keep their names (choice, others_low, payoff,
      ...) and group variables get a "group_" prefix (group_total_low,
      group_id_in_subsession, ...). It also adds these derived columns:

        part                      1 (rounds 1-10) or 2 (later rounds)
        round_in_part             round number within the part (1, 2, ...)
        session_part2_rounds      number of rounds Part 2 lasted in that
                                  session
        is_final_round            True in the last round of the session
        chose_low                 1 if choice is Low, 0 if High
        others_low_share          others_low / 4 (0 to 1)
        table_payoff              payoff according to the payoff table
                                  (used for the consistency check)
        payoff_if_other_choice    what the participant would have earned with
                                  the other option, if the others had done the
                                  same
        gain_from_switching       payoff_if_other_choice - payoff (negative =
                                  the participant's choice was the better one)
        group_total_profit        total profit of the group in the round
        group_efficiency          group_total_profit / 50 (1 = everybody
                                  chose Low, the highest possible)
        part2_group_id            group the participant was in at the start of
                                  Part 2 (Part 2 rows only)
        part2_chat_channel        "<session.code>_part2_group_<group id>", the
                                  chat channel of that group (Part 2 rows
                                  only); use it to match chat logs
        prev_choice               choice in the previous round of the same part
                                  (blank in the first round of each part)
        switched_choice           1 if the choice differs from prev_choice
        prev_others_low           others_low in the previous round of the same
                                  part
        cumulative_payoff_part    running total of payoff within the part (this
                                  is the cumulative profit shown on the results
                                  page)
        cumulative_payoff_total   running total of payoff over all rounds

When it finishes, the script prints how many rounds each session played
("10 + n") and a few consistency checks. All should show 0:
every group has 5 members, others_low + others_high = 4, the group's total_low
equals the number of Low choices, the payoff equals the payoff table value, and
no choice is missing in a played round. A non-zero number usually means a
participant dropped out or the constants at the top of the script do not match
the game (NUM_ROUNDS_P1, PLAYERS_PER_GROUP, PAYOFF_MATRIX).

By default the script drops the player_name column from both outputs. Set
DROP_PLAYER_NAMES = False at the top of the script to keep it. The justification
text is kept, so review it before sharing the data. Set DROP_UNPLAYED_ROUNDS =
False to keep all 60 rounds (the unplayed ones are empty).


USEFUL DERIVED MEASURES
- Share of Low choices by round: the mean of chose_low per round (or per
  round_in_part within each part). Collusion (everybody choosing Low) is
  against each participant's own interest in every round, so a high share of
  Low is a sign of cooperation or collusion.
- Group efficiency: group_efficiency is 1 if everybody chose Low and 0.5 if
  everybody chose High. Compare it across rounds and between Part 1 and Part
  2.
- Part 1 vs Part 2 (the effect of repeated play with a fixed group plus chat):
  compare chose_low and group_efficiency between part == 1 and part == 2. Part
  2 differs from Part 1 in three ways at once (fixed group, chat, random end),
  so the comparison cannot separate them.
- Learning and conditional behavior: use prev_choice, prev_others_low and
  switched_choice to see whether participants react to what the others did
  in the previous round (Part 2; in Part 1 the data show others_low only
  if SHOW_OTHERS_IN_PART1 was True, and the group changes every round).
- Cost of choosing Low: in a single round, High always pays more, so
  gain_from_switching is positive for every Low choice (and negative for every
  High choice). For Low choices it measures how much the participant gave up
  in that round by not choosing High.
- End-game effects: compare the last round of the session (is_final_round)
  with the rounds before. Participants did not know which round would be the
  last, so a large change in the last round would be notable.
- Group-level analysis in Part 2: use session.code + part2_group_id as the
  group identifier (observations within a group are not independent).
  Cluster standard errors at that level. In Part 1, groups are different every
  round, so cluster at the participant level instead.
- Chat content: match the chat log to the data via part2_chat_channel.
  Compare groups that agreed to choose Low in the chat with their later
  choices.


PRIVACY
- The data includes participants' chosen player names and their free-text
  answers (justification), which may contain identifying information. Treat
  both as potentially identifying.
- The chat log contains free text written by participants and can contain
  identifying information, too.
- For analysis or sharing, replace names with participant.code and delete the
  player_name column. Review the free-text answers and the chat before sharing.
- In small sessions (one group of 5) the group members can be identified from
  the ranking. Keep that in mind before sharing data.
- Store the original file somewhere secure (not a shared or public drive), and
  follow your institution's rules on data handling.


OPTIONAL: PAGE TIMES AND OTHER EXPORTS
- The "Data" tab also offers a "Page times" download, which shows how long
  each participant spent on each page. This is useful for checking how long
  participants took to decide, for spotting participants who timed out (and
  were given a random choice) and for finding participants who held up their
  group.
- Some versions also offer an "Excel-friendly" version of the CSV, and a
  download of the chat messages.
