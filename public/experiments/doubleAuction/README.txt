README

EXPERIMENT DESCRIPTION
======================
This experiment is a computerized uniform-price double auction designed to
illustrate how competitive markets set a single price, how private values and
costs translate into trading profits, and how close a market can get to the
efficient (surplus-maximizing) outcome. Participants are placed in one market
and take the role of either a buyer or a seller. Buyers are given a private
value (their maximum willingness to pay) and sellers are given a private cost
(their minimum acceptable price). Neither side sees anyone else's value or
cost.

In each round, every buyer submits one bid and every seller submits one ask.
Bids are ranked from highest to lowest and asks from lowest to highest. The
highest bid is matched with the lowest ask, the second-highest bid with the
second-lowest ask, and so on, for as long as the bid is greater than or equal
to the ask. All matched traders trade at one single market price: the average
of the bid and the ask in the LAST successful match. A matched buyer earns
(value - market price) and a matched seller earns (market price - cost).
Unmatched participants earn zero trading profit.

The game is played for 10 rounds. Roles are randomly assigned in round 1, kept
for the first 5 rounds, and switched for the last 5 rounds, so every
participant experiences both sides of the market. Values and costs are
redrawn every round. At the end, profits are summed across all rounds and a
ranking (leaderboard) is shown, along with a round-by-round comparison of the
actual market outcome and the theoretical competitive outcome.

There are two treatments, set in the session configuration:

  default      Standard double auction. Payoff = trading profit.

  competitive  Same auction, plus a group bonus. If EVERY buyer in the market
               trades in a round, every participant (buyers and sellers, 
               traders or not) receives an additional 10 points that round.
               Payoff = trading profit + 10 (if everyone buys). This creates
               a tension between individual profit and group success, since a
               buyer may want to bid higher to guarantee that all buyers trade.

Two instruction handouts (PDF) accompany the game, one per treatment: the
"competitive" handout includes Step 5 (Final Profits, with the 10-point
bonus) and the "default" handout does not. Hand out or display the one that
matches the treatment you are running.

All participants in a session are placed in ONE group (one market), because
PLAYERS_PER_GROUP is set to None. The market size is therefore the number of
participants in the session. Half of the participants become buyers and the
other half become sellers.


VARIABLES
=========

CONSTANTS (C)
-------------
NAME_IN_URL        Value: 'uniform_double_auction'
                   Name of game folder

PLAYERS_PER_GROUP  Value: None
                   Set to None so that all participants in the session form
                   one single market (one group)

NUM_ROUNDS         Value: 10
                   Participants play 10 rounds. Roles are kept for rounds 1-5
                   and switched for rounds 6-10 (NUM_ROUNDS // 2 rounds per
                   role)

BUYER_VAL_RANGE    Value: [30, 80]
                   Buyer private values are drawn as random integers between
                   30 and 80 (before the balancing adjustments described
                   below)

SELLER_COST_RANGE  Value: [10, 50]
                   Seller private costs are drawn as random integers between
                   10 and 50 (before the balancing adjustments described
                   below)

BONUS_POINTS       Value: 10
                   The bonus every participant receives in the "competitive"
                   treatment when every buyer trades in that round


GROUP VARIABLES
---------------
(One value per round. In this game there is one group per round, so these
describe the whole market.)

market_price       Type: FloatField
                   The single price at which all trades occur: the average of
                   the bid and ask in the last successful match. Set to 0 if
                   no trades occurred

quantity           Type: IntegerField
                   Number of trades (matched buyer-seller pairs) in the round

treatment          Type: StringField
                   'default' or 'competitive', taken from the session config

all_bought         Type: BooleanField
                   True if every buyer traded (quantity equals the number of
                   buyers, and there is at least one buyer). Triggers the
                   bonus in the competitive treatment

theo_total_surplus Type: FloatField
                   Theoretical efficient surplus: buyer values sorted from
                   high to low are paired with seller costs sorted from low
                   to high, and (value - cost) is summed over pairs where
                   value >= cost. This is the maximum surplus from trade
                   alone, ignoring the bonus

theo_max_surplus   Type: FloatField
                   The maximum surplus attainable in the treatment. Default:
                   equal to theo_total_surplus. Competitive: the sum of
                   (value - cost) over ALL sorted pairs (including negative
                   ones, as the bonus requires every buyer to trade) plus the
                   full bonus pool (number of players x 10)

actual_total_surplus
                   Type: FloatField
                   The surplus actually realized: the sum of (value - cost)
                   over the matched pairs, plus the bonus received by all
                   players if it was triggered


PLAYER VARIABLES
----------------
(One value per round per participant.)

player_name        Type: StringField
                   The participant's chosen display name, entered once on the
                   first page in round 1. Used on the final leaderboard. Only
                   letters, numbers and spaces are allowed

treatment          Type: StringField
                   The treatment the participant is in (copied from group)

is_buyer           Type: BooleanField
                   True if the participant is a buyer in this round, False if
                   a seller. Assigned randomly in round 1 (half buyers, half
                   sellers) and flipped after round 5

value              Type: IntegerField
                   Buyer's private value (maximum willingness to pay) for this
                   round. Blank for sellers

cost               Type: IntegerField
                   Seller's private cost (minimum acceptable price) for this
                   round. Blank for buyers

bid                Type: FloatField (min = 0)
                   The price a buyer submits. Set to 0 for sellers

ask                Type: FloatField (min = 0)
                   The price a seller submits. Set to 0 for buyers

is_trader          Type: BooleanField (initial = False)
                   True if the participant was matched and traded this round

trading_profit     Type: FloatField (initial = 0)
                   Buyer: value - market price, if matched. Seller: market
                   price - cost, if matched. Zero if the participant did not
                   trade. This can be negative if a participant bids above
                   their value or asks below their cost and still trades

payoff             Type: built-in oTree currency/points field
                   trading_profit + bonus (the bonus is 10 in the competitive
                   treatment when every buyer trades, otherwise 0). Summed over
                   all rounds for the leaderboard

justification      Type: LongStringField
                   Free-text explanation of the participant's bid or ask and
                   how they might have changed it. Collected only in round 1
                   on the Results page. Cannot be left empty


HOW THE VALUES AND COSTS ARE GENERATED
======================================
Each round, every buyer draws a value from 30-80 and every seller draws a cost
from 10-50. Because purely random draws can produce degenerate markets (for
example, no possible trades), the code then applies "parameter balancing":

1. Interior equilibrium. If the highest buyer value is lower than the lowest
   seller cost, the highest buyer value is reset to (lowest cost + 5), so at
   least one trade is always possible. If the lowest buyer value is higher than
   the highest seller cost, the highest seller cost is reset to (lowest buyer
   value + 5), so that not every possible pair trades.

2. Competitive treatment only. The total "negative surplus" (the sum of
   (cost - value) over sorted pairs where the cost exceeds the value) must stay
   below (number of players x 10 - 5). If it does not, the weakest buyer's
   value is raised by 2 and the weakest seller's cost is lowered by 2,
   repeatedly, until the condition holds. This guarantees that the bonus pool
   is large enough to make it worthwhile for the group to get every buyer to
   trade.

Note that the realized values and costs can therefore fall slightly outside
the ranges listed in the constants.


GAME FLOW (PAGE SEQUENCE)
=========================
1. Instructions     Round 1 only. Shows the rules and asks the participant for
                    a player name.

2. RoleSwitch       Shown only at the start of round 6 (the first round after
                    the switch). Tells participants that their role has
                    changed.

3. Submission       Each round. Buyers submit a bid and sellers submit an ask.
                    The participant sees their own private value or cost.

4. ResultsWaitPage  Each round. Waits until all participants have submitted,
                    then clears the market and calculates prices, quantities,
                    profits, and surplus.

5. Results          Each round. Shows the ranked bids and asks (the
                    participant's own is highlighted, with private values
                    shown), the market price, whether they traded, their
                    trading profit, and the bonus if applicable. In round 1
                    only, participants also type a justification for their
                    bid or ask.

6. Summary          Last round only. Shows the leaderboard (total profit per
                    participant over all rounds) and a round-by-round history
                    comparing the theoretical equilibrium price, quantity and
                    surplus with the actual outcomes.


WORKED EXAMPLE
==============
Bids: 100, 90, 80, 70      Asks: 20, 40, 60, 85

  100 >= 20  match
   90 >= 40  match
   80 >= 60  match
   70 <  85  stop

Three trades occur. The last successful match is bid 80 and ask 60, so the
market price is (80 + 60) / 2 = 70. All three matched buyers pay 70 and all
three matched sellers receive 70. A matched buyer with value 95 earns 95 - 70
= 25. A matched seller with cost 45 earns 70 - 45 = 25.

Competitive treatment: if all four buyers had traded, each of the participants
would also have received +10 that round.


IMPORTANT NOTES ON THE DESIGN
=============================
- Use an EVEN number of participants. Buyers are the first half of a random
  shuffle (i < N/2), so with an odd N there is one more buyer than seller.
  In the competitive treatment this makes the bonus impossible to earn, since
  every buyer cannot trade when buyers outnumber sellers.

- A larger market (for example 8 to 20 participants) gives a more meaningful
  price formation process than a very small one. The minimum is 2
  (one buyer, one seller).

- The wait page requires ALL participants in the session. If one participant
  leaves or disconnects, the market cannot clear and everyone waits. See
  "Participants cannot proceed" under Troubleshooting.

- Participants' chosen names are displayed to everyone in the market on the
  final leaderboard. Tell participants not to use their real full name if you
  want to keep results anonymous.

- Ties in bids or asks are broken arbitrarily by the sort order.

- A participant who bids above their value, or asks below their cost, and is
  matched can earn negative trading profit. This is allowed by the game and
  is flagged on the Results page.


SETTINGS.PY CONFIGURATION
=========================
The project needs a session configuration for each treatment, and the
participant field used to remember each person's starting role. Example:

    SESSION_CONFIGS = [
        dict(
            name='double_auction_default',
            display_name='Double Auction (Default)',
            app_sequence=['uniform_double_auction'],
            num_demo_participants=8,
            treatment='default',
        ),
        dict(
            name='double_auction_competitive',
            display_name='Double Auction (Competitive)',
            app_sequence=['uniform_double_auction'],
            num_demo_participants=8,
            treatment='competitive',
        ),
    ]

    PARTICIPANT_FIELDS = ['is_buyer']

The app stores the participant's round 1 role in participant.is_buyer, so
"is_buyer" must be listed in PARTICIPANT_FIELDS in recent oTree versions or
the session will fail to start. If the "treatment" key is missing from the
session configuration, the game defaults to the 'default' treatment.


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
   "uniform_double_auction" app and the "settings.py" file).
2. If it arrived as a .zip file, unzip it.
3. Save it somewhere easy to find, such as your Desktop or Documents.
   Example: Documents/double_auction_project


STEP 4: OPEN THE PROJECT FOLDER IN YOUR TERMINAL
------------------------------------------------
In the terminal, use the "cd" command to move into the project folder. For
example:

    cd your/path/to/doubleAuction/Double_Auction

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
   configurations: "Double Auction (Default)" or "Double Auction
   (Competitive)". Each session runs ONE treatment, so create a separate
   session for each treatment.
4. Enter the number of participants. Use an EVEN number (see "Important notes
   on the design"). All of them will be placed in a single market.
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
  participants must be present for the market to clear in every round.

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

Note: because the game puts everyone into one group (PLAYERS_PER_GROUP =
None), you do not need to pair participants manually. Roles (buyer or seller)
are assigned randomly by the game in round 1.


STEP 8: MONITOR THE SESSION
---------------------------
- Use the "Monitor" tab in the admin page to see each participant's progress
  in real time.
- Each round, participants submit one bid or ask and then wait on the
  results wait page until EVERY participant has submitted. This is normal.
  If the wait is long, check the Monitor tab to see who has not yet
  submitted.
- Roles switch automatically at the start of round 6, and participants see a
  notice page explaining the change.
- After round 10, participants see the final leaderboard and round history.
- Make sure the instructions handout matching your treatment (competitive or
  default) is given to participants before the session starts.


STEP 9: COLLECT THE RESULTS
---------------------------
1. When all participants have finished, go to the "Data" tab in the admin
   page.
2. Click the download button to export the data as a CSV file, which opens in
   Excel or Google Sheets.
3. The file includes, for each participant and each of the 10 rounds, their
   role, private value or cost, bid or ask, whether they traded, trading
   profit, payoff, and the group-level market price, quantity and surplus
   measures. The round 1 justification text is also included.


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

Participants cannot proceed past the results wait page
    The market clears only when every participant in the session has
    submitted a bid or ask. If one person disconnected, closed their browser
    or is idle, everyone else waits. Ask the person to reopen their link, or
    use the Monitor tab to find them. If someone has permanently left, the
    session may need to be restarted with the remaining even number of
    participants.

Session fails to start with an error about "is_buyer"
    Add PARTICIPANT_FIELDS = ['is_buyer'] to settings.py (see the settings.py
    configuration section above).

Wrong treatment is running
    The treatment comes from the "treatment" key of the chosen session
    configuration in settings.py, not from anything participants do. Check
    that you selected the right configuration in Step 6.

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
- There is one row per participant (player). Because this game has 10 rounds,
  each round has its own set of columns in the same row. Group-level columns
  (such as market price) have identical values for everyone in the session
  in a given round.
- Column names are long and use dots. For this game, the app columns follow
  the pattern:

      uniform_double_auction.3.player.bid
      uniform_double_auction.3.group.market_price

  The "3" is the round number (1 to 10). "player" and "group" tell you which
  level the variable belongs to. So the bid in round 7 is
  uniform_double_auction.7.player.bid.
- If you download the file for just this app (instead of "all apps"), the
  prefix is shorter, for example: 3.player.bid
- Participants who did not finish will have blank cells. Some blanks are
  normal by design:
    value is blank in rounds where the participant was a seller
    cost is blank in rounds where the participant was a buyer
    justification is blank in rounds 2 to 10 (it is collected only in
    round 1)
    player_name is filled only in round 1


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
  participant.is_buyer           The participant's role in round 1 (the role
                                 for rounds 1-5; flipped for rounds 6-10)
  session.code                   Unique ID for the session
  session.label, session.comment Blank unless you set them
  session.is_demo                True if the session was a demo session
  session.config.*               Many columns copying the session settings
                                 (the same value in every row)
  session.mturk_HITId, etc.      Only used for MTurk; blank here
  uniform_double_auction.N.subsession.round_number
                                 The round number, 1 to 10
  uniform_double_auction.N.player.id_in_group
                                 Position of the player within the market
                                 (the whole session is one group)
  uniform_double_auction.N.player.role
                                 Blank unless roles are defined
  uniform_double_auction.N.group.id_in_subsession
                                 Group number within the session (always 1
                                 here, since there is one market per session)


COLUMNS YOU PROBABLY WANT TO KEEP
(Replace N with each round number, 1 to 10.)
  participant.code
  participant.id_in_session
  session.code
  uniform_double_auction.N.player.player_name   (round 1 only)
  uniform_double_auction.N.player.treatment
  uniform_double_auction.N.player.is_buyer
  uniform_double_auction.N.player.value
  uniform_double_auction.N.player.cost
  uniform_double_auction.N.player.bid
  uniform_double_auction.N.player.ask
  uniform_double_auction.N.player.is_trader
  uniform_double_auction.N.player.trading_profit
  uniform_double_auction.N.player.payoff
  uniform_double_auction.N.player.justification (round 1 only)
  uniform_double_auction.N.group.market_price
  uniform_double_auction.N.group.quantity
  uniform_double_auction.N.group.all_bought
  uniform_double_auction.N.group.theo_total_surplus
  uniform_double_auction.N.group.theo_max_surplus
  uniform_double_auction.N.group.actual_total_surplus


SUGGESTED CLEANING STEPS (in Excel, Google Sheets, or Python)
1. Save a copy of the original download and never edit it. Do all cleaning in
   a second copy.
2. Delete the columns you do not need (all session.config.*, the participant._
   columns, and the MTurk columns).
3. Rename the long column headers to short ones. For example, rename
   "uniform_double_auction.3.player.bid" to "bid_r3".
4. Reshape from wide to long. For most analyses (for example, average
   efficiency by round, bid shading by role, or learning over rounds) it is
   easiest to have one row per participant per round, with a "round" column.
   In Python with pandas this can be done by stripping the prefix and using
   pandas.wide_to_long, or by melting each variable and merging.
5. Remove test data. If you ran practice or demo sessions, delete those rows.
   Check session.code or session.is_demo to tell sessions apart.
6. Check for incomplete sessions. If a participant dropped out, the market
   could not clear in later rounds, so the remaining rounds will be blank for
   everyone. Decide in advance how you will treat these sessions and note it
   in your records.
7. Check that group-level values match. Within a session and round, all
   participants should show the same market_price, quantity, and surplus
   values. If they do not, something went wrong.
8. If you combine several sessions into one file, keep session.code and the
   treatment column so you can tell them apart, and do not rely on
   id_in_session alone because it restarts at 1 in every session.

DATA CLEANING PYTHON FILE
If you don't want to manually select which columns you want to keep, you can
run the provided "data_cleaner.py" python script to generate cleaned up
versions of the csv file. It needs the pandas package ("pip install pandas").
Before running it, first make sure that you update the path to where you have
the raw csv file located, and then you can run it with "python3
data_cleaner.py". It produces two files:

  uniform_double_auction_cleaned.csv
      Wide format, one row per participant. Keeps the identifiers and every
      uniform_double_auction column for all 10 rounds.

  uniform_double_auction_cleaned_long.csv
      Long format, one row per participant per round, with a "round" column.
      Player variables keep their names (bid, ask, value, ...) and group
      variables get a "group_" prefix (group_market_price, ...). It also adds
      three derived columns: bid_shading (buyers: value - bid), ask_markup
      (sellers: ask - cost) and efficiency (actual_total_surplus divided by
      theo_max_surplus).

By default the script drops the player_name column from both outputs. Set
DROP_PLAYER_NAMES = False at the top of the script to keep it. The
justification text is kept, so review it before sharing the data.

USEFUL DERIVED MEASURES
- Efficiency in a round: actual_total_surplus / theo_max_surplus. In the
  default treatment this compares realized gains from trade with the maximum
  possible. In the competitive treatment, theo_max_surplus includes the full
  bonus pool, so interpret efficiency accordingly.
- Bid shading (buyers): value - bid. Ask markup (sellers): ask - cost.
- Deviation from competitive equilibrium: compare market_price and quantity
  with the theoretical price and quantity. The theoretical price is the
  average of the last pair (value, cost) with value >= cost when sorted, and
  the theoretical quantity is the number of such pairs. The Summary page
  computes these for display but they are not stored as columns, so
  calculate them from the value and cost columns if needed.
- Treatment effect: compare market_price, quantity, all_bought and efficiency
  between sessions run with 'default' and 'competitive'.
- Learning and role-switch effects: compare behavior in rounds 1-5 with
  rounds 6-10, and rounds 5 vs 6 for the effect of switching sides.


PRIVACY
- The data includes participants' chosen player names and their free-text
  justification, which may contain identifying information. Treat both as
  potentially identifying.
- For analysis or sharing, replace names with participant.code and delete the
  player_name column. Review the justification text before sharing.
- Store the original file somewhere secure (not a shared or public drive), and
  follow your institution's rules on data handling.


OPTIONAL: PAGE TIMES AND OTHER EXPORTS
- The "Data" tab also offers a "Page times" download, which shows how long
  each participant spent on each page. This is useful for checking how long
  participants took to decide on each bid or ask, and for spotting
  participants who were idle or who held up the market.
- Some versions also offer an "Excel-friendly" version of the CSV and a
  separate download for any extra data your app records.
