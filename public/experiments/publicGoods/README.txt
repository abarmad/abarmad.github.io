README

EXPERIMENT DESCRIPTION
======================
This experiment is a computerized public goods game (the "Common Fund
Experiment"). It is designed to illustrate the tension between individual
incentives and group welfare, how much people contribute to a shared pool when
free-riding pays, and whether the opportunity to reduce other people's points
changes contribution behavior. Participants are placed in one group. Nobody
sees what any individual contributes while deciding.

In each round, every participant starts with 10 points and privately chooses
how many of them (0 to 10) to contribute to a common fund. All contributions
are added together, multiplied by a fixed multiplier, and the resulting
"common prize" is split equally among ALL participants, whether or not they
contributed. A participant's profit from this stage is:

    10 - own contribution + own share of the prize

Because each point contributed returns only (multiplier / group size) points
to the contributor, contributing is individually costly whenever the group is
larger than the multiplier, even though the group as a whole is best off when
everyone contributes everything.

The game is played for 5 rounds with the same group. Group members keep their
group, but the ID numbers shown to participants are re-shuffled every round, so
"Player 3" in one round is not necessarily the same person in the next round.
At the end, profits are summed across all rounds and a ranking (leaderboard)
is shown, together with a chart of the average contribution in each round.

There are two treatments, set in the session configuration:

  PG     Standard public goods game. Payoff = 10 - contribution + share of
         the prize.

  PG_P   Public goods game with point reductions (punishment). After seeing
         everyone's contribution in a round, each participant receives 2
         additional points that they may use to reduce other participants'
         profits. Paying 1 point reduces another participant's profit by 3
         points, and a participant can reduce at most 6 points from any single
         other participant (that is, at most 2 paid units per target). Payoff
         = 10 - contribution + share of the prize + 2 - points paid for
         reductions - points reduced by others. This creates a tension
         between keeping the 2 extra points and spending them to punish
         low contributors.

Two instruction handouts (PDF) accompany the game, one per treatment:
"instructions.pdf" (titled "Common Fund Experiment") is for the PG treatment,
and "instructions_variant2.pdf" (titled "Common Fund Experiment Modified") is
for the PG_P treatment. The PG_P handout adds a "Point Reductions" section,
the extended "Final Profits" formula and a note that ID numbers are shuffled.
Hand out or display the one that matches the treatment you are running.

All participants in a session are placed in ONE group, because
PLAYERS_PER_GROUP is set to None. The group size is therefore the number of
participants in the session.


VARIABLES
=========

CONSTANTS (C)
-------------
NAME_IN_URL        Value: 'public_goods'
                   Name of game folder

PLAYERS_PER_GROUP  Value: None
                   Set to None so that all participants in the session form
                   one single group

NUM_ROUNDS         Value: 5
                   Participants play 5 rounds in the same group

ENDOWMENT          Value: 10
                   Points every participant starts each round with, and the
                   maximum contribution

MULTIPLIER         Value: 3
                   The total contribution is multiplied by this number to
                   form the common prize (see "Important notes on the design"
                   about the handouts, which say "doubled")

PUNISHMENT_ENDOWMENT
                   Value: 2
                   Extra points given to each participant per round in the
                   PG_P treatment, to spend on reducing others' profits

PUNISHMENT_COST    Value: 1
                   Points paid for one unit of reduction

PUNISHMENT_REDUCTION
                   Value: 3
                   Points removed from the target for each unit of reduction

MAX_REDUCTION_PER_PLAYER
                   Value: 6
                   Maximum points one participant can remove from another
                   participant in a round. This equals
                   MAX_REDUCTION_PER_PLAYER / PUNISHMENT_REDUCTION = 2 units
                   per target


GROUP VARIABLES
---------------
(One value per round. In this game there is one group per session, so these
describe the whole group.)

total_contribution Type: IntegerField
                   Sum of all participants' contributions in the round

average_contribution
                   Type: FloatField
                   total_contribution divided by the number of participants,
                   rounded to 2 decimals

individual_share   Type: FloatField
                   Each participant's share of the common prize:
                   total_contribution x MULTIPLIER / number of participants,
                   rounded to 2 decimals


PLAYER VARIABLES
----------------
(One value per round per participant.)

treatment          Type: StringField
                   'PG' or 'PG_P', taken from the session config. If the
                   session config has no 'treatment' key, the game defaults to
                   'PG' for this field

player_name        Type: StringField
                   The participant's chosen display name, entered once on the
                   first page in round 1. Used on the final leaderboard. Cannot
                   be empty or only spaces

shuffled_id        Type: IntegerField
                   Random ID (1 to group size) used to display participants to
                   each other in the round. Reshuffled every round. This is
                   NOT the same as id_in_group (see "Punishment columns"
                   below)

contribution       Type: IntegerField (min = 0, max = 10)
                   Points the participant contributed to the common fund

punishment_sent    Type: IntegerField (initial = 0)
                   Points the participant PAID for reductions in this round
                   (units assigned x PUNISHMENT_COST). Always 0 in the PG
                   treatment

punishment_received
                   Type: IntegerField (initial = 0)
                   Points REMOVED from the participant by others in this round
                   (units received x PUNISHMENT_REDUCTION). Always 0 in the PG
                   treatment

punish_p1 ... punish_p99
                   Type: IntegerField (min = 0, max = 2, initial = 0)
                   One field per possible recipient. punish_pK is the number
                   of reduction UNITS the participant assigned to the group
                   member whose id_in_group is K in that round. The total
                   across all K cannot exceed PUNISHMENT_ENDOWMENT (2 units).
                   The participant's own column and the columns for
                   non-existent group members are always 0. All 0 in the PG
                   treatment. The game supports at most 99 participants per
                   session

justification      Type: LongStringField
                   Free-text answer to "Can you explain your reasoning behind
                   your first contribution decision?" Collected only in round 1
                   on the Results page. Cannot be left empty

nextContribution   Type: LongStringField
                   Free-text answer to "Will you change your contribution for
                   the next round? If so, why?" Collected only in round 1 on
                   the Results page. Cannot be left empty

payoff             Type: built-in oTree currency/points field
                   PG: (10 - contribution) + individual_share.
                   PG_P: the same, plus 2 - punishment_sent -
                   punishment_received. Summed over all rounds for the
                   leaderboard. In PG_P a round payoff can be negative if a
                   participant is punished heavily


GAME FLOW (PAGE SEQUENCE)
=========================
1. Instructions        Round 1 only. Shows the rules and asks the participant
                       for a player name.

2. Submission          Each round. The participant chooses a contribution
                       from 0 to 10 points.

3. ResultsWaitPage     Each round. Waits until all participants have
                       submitted, then calculates the total contribution,
                       the average contribution, each participant's share, and
                       the round payoffs.

4. Results             Each round. Shows the group's contributions (listed by
                       shuffled ID) and the participant's profit. In PG_P, the
                       participant also chooses how to spend the 2 extra
                       points on reductions here. In round 1 only,
                       participants also type a justification and their plan
                       for the next round.

5. PunishmentWaitPage  PG_P only. Each round. Waits for everyone to finish the
                       Results page, then applies the reductions to every
                       participant's payoff.

6. FinalResults        PG_P only. Each round. Shows the breakdown of the final
                       profit: base profit, the 2 extra points, points paid,
                       and points reduced by others.

7. Summary             Last round only. Shows the leaderboard (total profit
                       per participant over all rounds) and a chart of the
                       average contribution in each round.


WORKED EXAMPLE
==============
Four participants (A, B, C, D) contribute 10, 5, 0 and 5 points. With
MULTIPLIER = 3:

  Total contribution = 20
  Common prize       = 20 x 3 = 60
  Individual share   = 60 / 4 = 15 for everyone

PG treatment. Profit = 10 - contribution + 15:

  A: 10 - 10 + 15 = 15
  B: 10 -  5 + 15 = 20
  C: 10 -  0 + 15 = 25   (the free-rider earns the most)
  D: 10 -  5 + 15 = 20

PG_P treatment. Suppose A assigns 2 units to C, B assigns 1 unit to C, and C
and D assign none:

  A pays 2 x 1 = 2 points. B pays 1 point.
  C loses (2 + 1) x 3 = 9 points.

  A: 15 + 2 - 2 - 0 = 15
  B: 20 + 2 - 1 - 0 = 21
  C: 25 + 2 - 0 - 9 = 18
  D: 20 + 2 - 0 - 0 = 22

The free-rider C now earns less than D, but A and B each paid something to
bring that about.


IMPORTANT NOTES ON THE DESIGN
=============================
- Use a group larger than the multiplier. Contributing only becomes costly for
  the individual when the multiplier is smaller than the number of
  participants (the return per contributed point is MULTIPLIER / group size).
  With MULTIPLIER = 3, use at least 4 participants. A larger group (for
  example 6 to 20) gives a more meaningful punishment decision.

- The wait pages require ALL participants in the session. If one participant
  leaves or disconnects, the group cannot proceed and everyone waits. See
  "Participants cannot proceed" under Troubleshooting.

- Participants' chosen names are displayed on the final leaderboard. The code
  also passes each other participant's chosen name ("nickname") to the Results
  page template. Check your Results template to see whether it is displayed;
  if it is, participants can identify each other, which weakens the anonymity
  that the ID shuffling is meant to provide. Tell participants not to use
  their real full name if you want to keep results anonymous.

- The ID shuffle is assigned in both treatments, but only the PG_P handout
  mentions it.

- The punishment columns use id_in_group, not shuffled_id. punish_pK refers to
  the participant whose id_in_group is K. Participants see the shuffled ID,
  which differs from id_in_group and changes every round. To find out who a
  participant punished, look up the participant with id_in_group = K in the
  same session and round.

- The game supports at most 99 participants because punishment fields exist
  only for punish_p1 ... punish_p99.

- The round 1 questions are shown on the Results page, so in PG_P they appear
  together with the punishment decision.

- The leaderboard total shown on the Results page does not yet include the
  current round's reductions in PG_P, since they are applied after that page.


SETTINGS.PY CONFIGURATION
=========================
The project needs a session configuration for each treatment, and the
participant field used to store the chosen name. Example:

    SESSION_CONFIGS = [
        dict(
            name='public_goods_PG',
            display_name='Public Goods (No Point Reductions)',
            app_sequence=['public_goods'],
            num_demo_participants=4,
            treatment='PG',
        ),
        dict(
            name='public_goods_PG_P',
            display_name='Public Goods (With Point Reductions)',
            app_sequence=['public_goods'],
            num_demo_participants=4,
            treatment='PG_P',
        ),
    ]

    PARTICIPANT_FIELDS = ['name']

The app stores the chosen name in participant.name, so "name" must be listed
in PARTICIPANT_FIELDS in recent oTree versions or the first page may fail. The
app folder must be called "public_goods" (the folder name is the prefix of all
the data columns) and must contain the page templates (.html files) as well as
__init__.py. If the "treatment" key is missing from the session configuration,
the game defaults to 'PG' and no point reductions are applied.


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
   "public_goods" app and the "settings.py" file).
2. If it arrived as a .zip file, unzip it.
3. Save it somewhere easy to find, such as your Desktop or Documents.
   Example: Documents/public_goods_project


STEP 4: OPEN THE PROJECT FOLDER IN YOUR TERMINAL
------------------------------------------------
In the terminal, use the "cd" command to move into the project folder. For
example:

    cd your/path/to/publicGoods/Public_Goods

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
3. Choose the treatment you want to run from the list of session
   configurations: "Public Goods (No Point Reductions)" or "Public Goods (With
   Point Reductions)". Each session runs ONE treatment, so create a separate
   session for each treatment.
4. Enter the number of participants (see "Important notes on the design").
   All of them will be placed in a single group.
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
  participants must be present for every round to be completed.

Option B: Individual participant links (one link per person)
- The "Links" tab also lists a separate link for each participant slot (P1,
  P2, P3, and so on). Copy each link and send one to each person by email,
  text message, or any messaging app.
- Each link is tied to a specific spot in the session. If a participant closes
  their browser or loses their connection, they can reopen their same link and
  return to where they left off. Make sure each person uses only their own
  link, and that no link is shared between two people.
- This is the best option for remote participants who will all join at the
  same agreed time. (The handouts ask participants to click the provided link
  only once.)

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

Note: because the game puts everyone into one group (PLAYERS_PER_GROUP =
None), you do not need to pair participants manually.


STEP 8: MONITOR THE SESSION
---------------------------
- Use the "Monitor" tab in the admin page to see each participant's progress
  in real time.
- Each round, participants submit a contribution and then wait on the results
  wait page until EVERY participant has submitted. In the PG_P treatment they
  wait a second time after the Results page, until everyone has decided how to
  spend their 2 extra points. This is normal. If the wait is long, check the
  Monitor tab to see who is holding things up.
- After round 5, participants see the final leaderboard and the chart of
  average contributions.
- Make sure the instructions handout matching your treatment (PG or PG_P) is
  given to participants before the session starts.


STEP 9: COLLECT THE RESULTS
---------------------------
1. When all participants have finished, go to the "Data" tab in the admin
   page.
2. Click the download button to export the data as a CSV file, which opens in
   Excel or Google Sheets.
3. The file includes, for each participant and each of the 5 rounds, their
   contribution, the group's total, average and share, their punishment
   decisions and payoff. The round 1 free-text answers are also included.


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
    The wait pages continue only when every participant in the session has
    finished the previous page. If one person disconnected, closed their
    browser or is idle, everyone else waits. Ask the person to reopen their
    link, or use the Monitor tab to find them. If someone has permanently
    left, the session may need to be restarted with the remaining
    participants.

Error mentioning "name" on the first page or when starting the session
    Add PARTICIPANT_FIELDS = ['name'] to settings.py (see the settings.py
    configuration section above).

No point reductions appear in the PG_P session
    The treatment comes from the "treatment" key of the chosen session
    configuration in settings.py, not from anything participants do. Check
    that the key is spelled exactly 'PG_P' and that you selected the right
    configuration in Step 6.

Wrong treatment is running
    Check that you selected the right configuration in Step 6.

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
- There is one row per participant (player). Because this game has 5 rounds,
  each round has its own set of columns in the same row. Group-level columns
  (such as the individual share) have identical values for everyone in the
  session in a given round.
- Column names are long and use dots. For this game, the app columns follow
  the pattern:

      public_goods.3.player.contribution
      public_goods.3.group.individual_share

  The "3" is the round number (1 to 5). "player" and "group" tell you which
  level the variable belongs to. So the contribution in round 4 is
  public_goods.4.player.contribution.
- If you download the file for just this app (instead of "all apps"), the
  prefix is shorter, for example: 3.player.contribution
- Participants who did not finish will have blank cells. Some blanks are
  normal by design:
    player_name is filled only in round 1
    justification and nextContribution are filled only in round 1 (blank in
    rounds 2 to 5)
- The punish_p1 ... punish_p99 columns exist for all 5 rounds, so a raw export
  has 495 punishment columns, almost all of them 0. In the PG treatment all of
  them are 0 (no reductions are possible). Only as many as there are
  participants in the session are ever used.


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
                                 total profit shown on the leaderboard)
  participant.name               The chosen player name (copy of
                                 player_name; only present if listed in
                                 PARTICIPANT_FIELDS)
  session.code                   Unique ID for the session
  session.label, session.comment Blank unless you set them
  session.is_demo                True if the session was a demo session
  session.config.*               Many columns copying the session settings
                                 (the same value in every row)
  session.mturk_HITId, etc.      Only used for MTurk; blank here
  public_goods.N.subsession.round_number
                                 The round number, 1 to 5
  public_goods.N.player.id_in_group
                                 Position of the player within the group
                                 (the whole session is one group). This stays
                                 the same in every round
  public_goods.N.player.role     Blank unless roles are defined
  public_goods.N.group.id_in_subsession
                                 Group number within the session (always 1
                                 here, since there is one group per session)


COLUMNS YOU PROBABLY WANT TO KEEP
(Replace N with each round number, 1 to 5.)
  participant.code
  participant.id_in_session
  session.code
  public_goods.N.player.player_name      (round 1 only)
  public_goods.N.player.treatment
  public_goods.N.player.id_in_group
  public_goods.N.player.shuffled_id
  public_goods.N.player.contribution
  public_goods.N.player.punishment_sent
  public_goods.N.player.punishment_received
  public_goods.N.player.punish_p1 ... punish_pG   (G = group size)
  public_goods.N.player.payoff
  public_goods.N.player.justification    (round 1 only)
  public_goods.N.player.nextContribution (round 1 only)
  public_goods.N.group.total_contribution
  public_goods.N.group.average_contribution
  public_goods.N.group.individual_share


SUGGESTED CLEANING STEPS (in Excel, Google Sheets, or Python)
1. Save a copy of the original download and never edit it. Do all cleaning in
   a second copy.
2. Delete the columns you do not need (all session.config.*, the participant._
   columns, the MTurk columns, and the unused punish_p columns).
3. Rename the long column headers to short ones. For example, rename
   "public_goods.3.player.contribution" to "contribution_r3".
4. Reshape from wide to long. For most analyses (for example, average
   contribution by round, the effect of punishment over time, or end-game
   behavior) it is easiest to have one row per participant per round, with a
   "round" column. In Python with pandas this can be done by stripping the
   prefix and using pandas.wide_to_long, or by melting each variable and
   merging.
5. Remove test data. If you ran practice or demo sessions, delete those rows.
   Check session.code or session.is_demo to tell sessions apart.
6. Check for incomplete sessions. If a participant dropped out, the group
   could not continue, so the remaining rounds will be blank for everyone.
   Decide in advance how you will treat these sessions and note it in your
   records.
7. Check that group-level values match. Within a session and round, all
   participants should show the same total_contribution, average_contribution
   and individual_share. If they do not, something went wrong.
8. If you combine several sessions into one file, keep session.code and the
   treatment column so you can tell them apart, and do not rely on
   id_in_session alone because it restarts at 1 in every session.


DATA CLEANING PYTHON FILE
If you don't want to manually select which columns you want to keep, you can
run the provided "data_cleaner.py" python script to generate cleaned up
versions of the csv file. It needs the pandas package ("pip install pandas").
Before running it, first make sure that you update the path to where you have
the raw csv file located (and APP_NAME, if your app folder is not called
"public_goods"), and then you can run it with "python3 data_cleaner.py". It
produces two files:

  public_goods_cleaned.csv
      Wide format, one row per participant. Keeps the identifiers and every
      public_goods column for all 5 rounds (except the unused punish_p
      columns).

  public_goods_cleaned_long.csv
      Long format, one row per participant per round, with a "round" column.
      Player variables keep their names (contribution, payoff, ...) and group
      variables get a "group_" prefix (group_total_contribution, ...). It also
      adds these derived columns:

        contribution_rate         contribution / 10 (0 to 1)
        base_profit               10 - contribution + group_individual_share
                                  (profit from the contribution stage only)
        others_avg_contribution   average contribution of the OTHER group
                                  members in that round
        deviation_from_others     contribution - others_avg_contribution
                                  (negative = gave less than the others)
        punishment_units_sent     sum of the punish_p columns: units of
                                  reduction handed out (PG_P only)
        punishment_units_received punishment_received / 3: units of reduction
                                  received (PG_P only)
        punishment_net            2 - punishment_sent - punishment_received:
                                  net effect of the punishment stage on the
                                  round payoff (PG_P only)
        cumulative_payoff         running total of payoff over the rounds

      The three punishment columns are left blank in the PG treatment, so
      that "no punishment available" is not confused with "chose not to
      punish".

When it finishes, the script prints two consistency checks. Both should show 0:
the group total must equal the sum of the individual contributions, and the
payoff must equal base_profit plus punishment_net. A non-zero number usually
means a participant dropped out or the constants at the top of the script do
not match the game (ENDOWMENT, PUNISHMENT_ENDOWMENT, PUNISHMENT_REDUCTION).

By default the script drops the player_name column from both outputs. Set
DROP_PLAYER_NAMES = False at the top of the script to keep it. The
justification and nextContribution text is kept, so review it before sharing
the data. Set DROP_UNUSED_PUNISH_COLUMNS = False to keep all 99 punish_p
columns per round.


USEFUL DERIVED MEASURES
- Average contribution rate by round: contribution / 10, or
  group_average_contribution / 10. The standard outcome in public goods games
  is that this starts at around 40-60% in round 1 and declines over rounds
  without punishment.
- Group efficiency: the average base profit equals
  10 + average_contribution x (multiplier - 1), so average contribution
  already measures how much of the possible gain from cooperation the group
  achieved. Full cooperation gives every participant 10 x multiplier points
  (30 with a multiplier of 3); universal free-riding gives 10.
- Free-riding: contribution below others_avg_contribution
  (deviation_from_others < 0), or contribution = 0.
- Punishment targeting: in PG_P, compare punishment_units_received with
  deviation_from_others. Typical findings are that punishment is mostly aimed
  at participants who contributed less than the others, and that
  punishment_units_received falls as the contributions rise. To see who
  punished whom, match punish_pK with the participant whose id_in_group = K in
  the same session and round.
- Cost of punishment: sum of punishment_sent over participants is what was paid
  and sum of punishment_received is what was destroyed. The difference
  (destroyed - paid) is the net loss of group welfare. Punishment does not
  create points; it only moves points to the common loss.
- Treatment effect: compare contribution, group_average_contribution and the
  final payoff between sessions run with 'PG' and 'PG_P'. Compare base_profit
  (not payoff) if you want to isolate the contribution stage from the extra
  points and reductions.
- Learning and end-game effects: compare round 1 with later rounds, and
  round 5 with round 4. Use the round 1 justification and nextContribution
  text to see what participants intended to do.


PRIVACY
- The data includes participants' chosen player names and their free-text
  answers (justification and nextContribution), which may contain identifying
  information. Treat both as potentially identifying.
- For analysis or sharing, replace names with participant.code and delete the
  player_name column. Review the free-text answers before sharing.
- The punish_p columns reveal who punished whom (by id_in_group). Keep that in
  mind before sharing data from small sessions.
- Store the original file somewhere secure (not a shared or public drive), and
  follow your institution's rules on data handling.


OPTIONAL: PAGE TIMES AND OTHER EXPORTS
- The "Data" tab also offers a "Page times" download, which shows how long
  each participant spent on each page. This is useful for checking how long
  participants took to decide on each contribution, and for spotting
  participants who were idle or who held up the group.
- Some versions also offer an "Excel-friendly" version of the CSV and a
  separate download for any extra data your app records.
