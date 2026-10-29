README

EXPERIMENT DESCRIPTION
======================
This experiment is a computerized trade  game designed to illustrate the gains
from trade and  comparative advantage. Participants are paired  and each takes
the role of a country that produces two goods, clothes and food, with the pair
having different production possibilities that  only each participant can see.
Each country first picks its best production plan under autarky, where utility
is 5 x min(clothes,  food), which gives a benchmark of  15 for both countries.
The pair then  has five minutes to  negotiate a binding trade  deal specifying
how many units  of one good each country  will sell and how many  units of the
other it will receive in return, without revealing its production table. After
the deal is set, each country privately chooses a production plan that lets it
honor the agreement, and its final utility is calculated from what it consumes
after trade. Pairs  whose deal leaves both countries strictly  better off than
under autarky  earn a participation point.  The game shows  how specialization
according to comparative advantage and  mutually beneficial exchange can raise
welfare for  both parties, even when  each side has limited  information about
the other's costs.

Participants will be assigned to groups of  2 upon joining the server link. If
an odd number of  participants join the link, the last  participant that joins
will wait 90 seconds  for another person to join the server.  If no one joins,
they are  taken to  a page  that informs  them that  they cannot  continue the
experiment.


VARIABLES
=========

CONSTANTS (C)
-------------
NAME_IN_URL        Value: 'tradeDealGame'
                   Name of game folder

PLAYERS_PER_GROUP  Value: None
                   Set to none for manual grouping

NUM_ROUNDS         Value: 1
                   Participants play only 1 round of the game

AUTARKY_UTILITY    Value: 15
                   The maximum utility both parties can achieve without trade


GROUP VARIABLES
---------------
c1_clothes_export  Type: IntegerField
                   Value Range: x > 0
                   The number of  units of clothes country 1  agrees to export
                   to country 2

c1_food_export     Type: IntegerField
                   Value Range: x > 0
                   The number of  units of food country 1 agrees  to export to
                   country 2

c2_clothes_export  Type: IntegerField
                   Value Range: x > 0
                   The number of  units of clothes country 2  agrees to export
                   to country 1

c2_food_export     Type: IntegerField
                   Value Range: x > 0
                   The number of  units of food country 2 agrees  to export to
                   country 1

p1_benefits        Type: IntegerField
                   Value Range: x > 0
                   The total  utility the  participant representing  country 1
                   obtains after trade

p2_benefits        Type: IntegerField
                   Value Range: x > 0
                   The total utility the  participant representing  country 2
                   obtains after trade

negotiation_start_time
                   Type: FloatField (initial = 0)
                   Value Range: [0, 300] (0 seconds to 300 seconds)
                   The timer to count down the time the group has to negotiate
                   (maximum of 5 minutes negotiation time).


PLAYER VARIABLES
----------------
player_name        Type: StringField
                   The participant's name

email_address      Type: StringField (optional)
                   The participant's email address

country            Type: IntegerField
                   Value Range: [1,2]
                   Which country the  participant is assigned to  represent in
                   the group

participation_point
                   Type: IntegerField (initial = 0)
                   Value Range: x >= 0
                   If  both   countries  reach  higher  utility   under  trade
                   (compared to autarky), then they both get a "point"

autarky_plan       Type: IntegerField (1-6)
                   The  production  plan  the participant  selected  as  their
                   autarky plan

selected_plan      Type: IntegerField (1-6)
                   The  production plan  the participant  selected during  the
                   negotiation phase

clothes_import     Type: IntegerField (initial = 0)
                   Track how  many units of  clothes the participant  plans to
                   import from the other country

clothes_export     Type: IntegerField (initial = 0)
                   Track how  many units of  clothes the participant  plans to
                   export to the other country

food_import        Type: IntegerField (initial = 0)
                   Track  how many  units  of food  the  participant plans  to
                   import from the other country

food_export        Type: IntegerField (initial = 0)
                   Track  how many  units  of food  the  participant plans  to
                   export to the other country

total_clothes      Type: IntegerField
                   Clothes export +  clothes import for the  participant after
                   negotiation

total_food         Type: IntegerField
                   Food  export  +  food  import  for  the  participant  after
                   negotiation

timed_out          Type: BooleanField (initial = False)
                   Flags  when the  negotiation  timer  is finished;  initiate
                   warning to let participants know  they need to submit their
                   plans + exports



RUNNING EXPERIMENT
==================

STEP 1: INSTALL PYTHON
----------------------
oTree runs on Python, so Python must be installed first.

1. Go  to https://www.python.org/downloads/ and  download the latest  Python 3
   installer for your operating system.
2. Run the installer.
   - Windows: on the  first screen, CHECK the box "Add  Python to PATH" before
     clicking Install. This is the most common source of problems.
   - Mac: follow the default prompts.
3. Confirm Python installed correctly. Open a terminal:
   - Windows: press the Windows key, type "cmd", and press Enter.
   - Mac: press Cmd + Space, type "Terminal", and press Enter.
   Then type the following and press Enter:

       python --version

   (On a Mac, use "python3 --version" if  the first command fails.) You should
   see  something  like "Python  3.12.x".  If  you  see  an error,  close  the
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
1.  Download  the  experiment  project   folder  (the  folder  containing  the
   "tradeDealGame" app and the "settings.py" file).
2. If it arrived as a .zip file, unzip it.
3. Save it somewhere easy to find, such as your Desktop or Documents. Example:
   Documents/trade_game_project


STEP 4: OPEN THE PROJECT FOLDER IN YOUR TERMINAL
------------------------------------------------
In the  terminal, use the  "cd" command to move  into the project  folder. For
example:

    cd Documents/trade_game_project

Check that you are in the right place. The folder should contain a file called
settings.py. To list files, type "dir" (Windows) or "ls" (Mac).


STEP 5: START THE oTree SERVER
------------------------------
Type:

    otree devserver

Leave this terminal window  open for the entire session. Closing  it will stop
the experiment. When the  server is ready you will see a  message saying it is
running at http://localhost:8000.

To stop the server later, click on the terminal and press Ctrl + C.


STEP 6: OPEN THE ADMIN PAGE AND CREATE A SESSION
------------------------------------------------
1. Open a web browser (Chrome is recommended) and go to:

       http://localhost:8000

2. Click "Sessions" in the top menu, then "Create new session".
3. Choose the trade deal game from the list of session configurations.
4. Enter  the number  of participants.  Because participants  are paired  into
   two-country groups, use an EVEN number; if odd, the last player to join the
   session will not be able to continue the experiment.
5. Click "Create".


STEP 7: GET PARTICIPANTS INTO THE GAME
--------------------------------------
After creating  the session,  open the  "Links" tab.  There are  two kinds  of
links, and you can choose either one.

Option A: Session-wide link (one link for everyone)
- Share the single "Session-wide link"  with all participants (on a projector,
  by email, or through  your course site). Each participant opens  it in their
  own browser and is assigned a spot automatically, in the order they arrive.
- This is the fastest option for a  classroom or lab where everyone is present
  at the same time.

Option B: Individual participant links (one link per person)
- The "Links"  tab also lists a  separate link for each  participant slot (P1,
  P2, P3,  and so on). Copy  each link and send  one to each person  by email,
  text message, or any messaging app.
- Each link  is tied to a specific  spot in the session. Because  of this, you
  control exactly who is in which spot, which makes it easier to decide who is
  paired with whom.
- If a  participant closes their browser  or loses their connection,  they can
  reopen their  same link and  return to where they  left off. Make  sure each
  person uses  only their  own link, and  that no link  is shared  between two
  people.
- This is the best option for remote participants, for pairing specific people
  together, or when participants will not all join at the same time.

Network requirements for Options A and B (running from your own computer)
- Participants must be able to reach your computer over the network. Find your
  computer's local IP address (Windows:  type "ipconfig"; Mac: type "ifconfig"
  or  check Wi-Fi  settings) and  replace "localhost"  in the  link with  that
  address, e.g. http://192.168.1.25:8000/...
- You may  need to start the server  with the following command  so that other
  devices can connect:

      otree devserver 0.0.0.0:8000

-  Everyone must  be on  the same  network  (for example,  the same  classroom
  Wi-Fi). Links  sent by email  or message will only  work for people  on that
  network while your server is running.

Option C: Online / remote participants (outside your network)
-  A local  server  cannot  be reached  from  outside  your network.  If  your
  participants are  not on the  same network as  you, host the  project online
  (for example  through oTree  Hub or  Heroku). Once  it is  hosted, both  the
  session-wide link and the individual links  will work from anywhere. See the
  official     oTree      documentation     for      hosting     instructions:
  https://otree.readthedocs.io

Note: the game  uses manual grouping (PLAYERS_PER_GROUP = None),  so make sure
participants are paired into groups of two,  one assigned as Country 1 and the
other as Country 2, before the negotiation phase begins.


STEP 8: MONITOR THE SESSION
---------------------------
- Use the "Monitor"  tab in the admin page to  see each participant's progress
  in real time.
- The  negotiation phase has a  five-minute timer. When it  ends, participants
  are warned to submit their production plans and trade amounts.
-  Participants cannot  proceed  past  a wait  page  until  their partner  has
  finished the same stage. This is normal.


STEP 9: COLLECT THE RESULTS
---------------------------
1. When  all participants  have finished, go  to the "Data"  tab in  the admin
   page.
2. Click the download button to export the  data as a CSV file, which opens in
   Excel or Google Sheets.
3. The file  includes each participant's selected plans,  trade amounts, total
   clothes and food, participation point, and survey responses.


TROUBLESHOOTING
---------------
"python is not recognized" (Windows)
    Python was not added  to PATH. Re-run the Python installer  and check "Add
    Python to PATH".

"otree is not recognized" or "command not found"
    Close and reopen the terminal. If it still fails, try:
    python -m otree devserver

"Address already in use" or port error
    Another program  is using port 8000.  Close other oTree windows,  or start
    the server on a different port:
    otree devserver 8001

Participants cannot connect
    Check that everyone is on the same  network, that you used your IP address
    instead  of "localhost",  and  that your  firewall  allows connections  to
    Python.

Changes to the code do not appear
    The devserver  reloads automatically in most  cases. If not, stop  it with
    Ctrl + C and start it again.


MORE HELP
---------
Official oTree documentation: https://otree.readthedocs.io
oTree discussion group: https://groups.google.com/g/otree


STEP 10: HANDLING YOUR DATA
---------------------------
oTree exports a lot  of extra columns that you do not  need for analysis. This
section explains what the file looks like and how to clean it up.


DOWNLOAD THE DATA BEFORE YOU STOP THE SERVER
- When you run "otree devserver", the data is not permanently saved. It may be
  erased when  you stop or  restart the server, or  when you change  the code.
  Always download the CSV BEFORE closing the terminal.
- Download it from  the "Data" tab of the admin page.  Download it again after
  any late participants finish.


WHAT THE FILE LOOKS LIKE
- There is one row per  participant (player). Because participants are paired,
  the two players in  a group will have identical values  in the group columns
  (for example, the trade amounts).
- Column names  are long and use dots.  For this game, the  app columns follow
  the pattern:

      tradeDealGame.1.player.selected_plan
      tradeDealGame.1.group.c1_clothes_export

  The "1"  is the  round number  (this game  has only  1 round).  "player" and
  "group" tell you which level the variable belongs to.
- If  you download the  file for just  this app  (instead of "all  apps"), the
  prefix is shorter, for example: player.selected_plan
- Participants who  did not finish will  have blank cells. Blank  cells in the
  optional fields (email_address, survey_q1 to survey_q3) are normal.


EXTRA COLUMNS ADDED BY oTree
These are added automatically and are usually  safe to delete. Exact names can
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
  participant.payoff             oTree's built-in payoff (this game does
                                 not use it; utility is calculated from the
                                 plan variables)
  session.code                   Unique ID for the session
  session.label, session.comment Blank unless you set them
  session.is_demo                True if the session was a demo session
  session.config.*               Many columns copying the session settings
                                 (the same value in every row)
  session.mturk_HITId, etc.      Only used for MTurk; blank here
  tradeDealGame.1.subsession.round_number
                                 Always 1 in this game
  tradeDealGame.1.player.id_in_group
                                 1 or 2 position within the pair
  tradeDealGame.1.player.role    Blank unless roles are defined
  tradeDealGame.1.player.payoff  Built-in payoff; not used
  tradeDealGame.1.group.id_in_subsession
                                 Group number within the session (KEEP; use
                                 this to match partners)


COLUMNS YOU PROBABLY WANT TO KEEP
  participant.code
  participant.id_in_session
  tradeDealGame.1.group.id_in_subsession
  tradeDealGame.1.player.country
  tradeDealGame.1.player.autarky_plan
  tradeDealGame.1.player.selected_plan
  tradeDealGame.1.player.clothes_import / clothes_export
  tradeDealGame.1.player.food_import / food_export
  tradeDealGame.1.player.total_clothes / total_food
  tradeDealGame.1.player.participation_point
  tradeDealGame.1.player.timed_out
  tradeDealGame.1.group.c1_clothes_export / c1_food_export
  tradeDealGame.1.group.c2_clothes_export / c2_food_export
  tradeDealGame.1.player.survey_q1 / survey_q2 / survey_q3


SUGGESTED CLEANING STEPS (in Excel or Google Sheets)
1. Save a copy of the original download  and never edit it. Do all cleaning in
   a second copy.
2. Delete the columns you do not need (all session.config.*, the participant._
   columns, and the MTurk columns).
3.  Rename  the  long  column  headers to  short  ones.  For  example,  rename
   "tradeDealGame.1.player.selected_plan" to "selected_plan".
4. Remove test data. If you ran  practice or demo sessions, delete those rows.
   Check session.code or session.is_demo to tell sessions apart.
5. Check  for incomplete  pairs. If  one person  dropped out,  their partner's
   results may be incomplete. Decide in advance how you will treat these cases
   and note it in your records.
6. Check  that partners match.  Both players in a  group should have  the same
   group-level trade amounts. If they do not, something went wrong.
7. If you combine several sessions into one file, keep session.code so you can
   tell them apart, and do not rely on id_in_session alone because it restarts
   at 1 in every session.

DATA CLEANING PYTHON FILE
If you don't want to manually select which columns you want to keep, you can 
run the provided "data_cleaner.py" python script to generate a cleaned up ver
sion of the csv file. Before running it, first make sure that you update the 
path to where you have the raw csv file located, and then you can run it with 
"python3 data_cleaner.py".  


PRIVACY
- The data includes participants' names. These are personally identifying.
- For analysis or sharing, replace  names and emails with participant.code and
  delete the name and email columns.
- Store the original file somewhere secure (not a shared or public drive), and
  follow your institution's rules on data handling.


OPTIONAL: PAGE TIMES AND OTHER EXPORTS
- The  "Data" tab also  offers a "Page times"  download, which shows  how long
  each participant  spent on each  page. This  is useful for  checking whether
  participants reached the end of the five-minute negotiation.
-  Some versions  also offer  an "Excel-friendly"  version  of the  CSV and  a
  separate download for any extra data your app records.