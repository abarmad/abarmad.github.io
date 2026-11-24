import re
import pandas as pd
from pathlib import Path

# =========================================================
# INPUT AND OUTPUT FILES
# =========================================================

input_file = Path("all_apps_wide-2026-11-23.csv")  # keep same if csv in same folder as .py file
                                                   # change path/name to your csv file
output_file = Path("matrix_games_cleaned.csv")            # wide: one row per participant
output_file_long = Path("matrix_games_cleaned_long.csv")  # long: one row per participant per round


# =========================================================
# OPTIONS
# =========================================================

# If True, the player_name column (chosen display name) is removed from both
# outputs. Participant identity is then only available through participant.code.
DROP_PLAYER_NAMES = True

# Name of the oTree app (the name of its folder). Leave as None to detect it
# automatically from the csv. Set it by hand (for example "matrix_games_sequence")
# if the csv contains several apps with a "choice" variable.
APP_NAME = None

# Must match ROUNDS_PER_GAME in the app's __init__.py
ROUNDS_PER_GAME = 5


# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv(input_file)


# =========================================================
# FIND THE APP PREFIX
# =========================================================
# App columns look like:  matrix_games_sequence.3.player.choice

if APP_NAME is None:
    candidates = sorted({
        m.group(1)
        for col in df.columns
        if (m := re.match(r"^([^.]+)\.\d+\.player\.choice$", col))
    })
    if len(candidates) != 1:
        raise SystemExit(
            f"Could not tell which app to use (found: {candidates}). "
            "Set APP_NAME at the top of this script."
        )
    APP_NAME = candidates[0]

print(f"Using app: {APP_NAME}")


# =========================================================
# IDENTIFIERS TO KEEP
# =========================================================

identifier_columns = [
    "participant.code",           # Unique participant identifier
    "participant.id_in_session",  # Participant number in the session
    "session.code",               # Session identifier
]


# =========================================================
# KEEP ALL APP-SPECIFIC VARIABLES
# =========================================================

app_columns = [col for col in df.columns if col.startswith(f"{APP_NAME}.")]

# Optionally remove the participant's chosen name
if DROP_PLAYER_NAMES:
    app_columns = [col for col in app_columns if not col.endswith(".player_name")]


# =========================================================
# SELECT COLUMNS
# =========================================================

id_columns = [col for col in identifier_columns if col in df.columns]
columns_to_keep = list(dict.fromkeys(id_columns + app_columns))
cleaned_df = df[columns_to_keep].copy()


# =========================================================
# EXPORT CLEANED DATASET (WIDE)
# =========================================================

cleaned_df.to_csv(output_file, index=False)


# =========================================================
# BUILD LONG-FORMAT DATASET (ONE ROW PER PARTICIPANT PER ROUND)
# =========================================================
# Player variables keep their name (e.g. "choice"); group variables get a
# "group_" prefix (e.g. "group_id_in_subsession").

column_pattern = re.compile(rf"^{re.escape(APP_NAME)}\.(\d+)\.(player|group)\.(.+)$")

# round number -> {new column name: original column name}
round_columns = {}
for col in app_columns:
    match = column_pattern.match(col)
    if not match:
        continue
    round_number = int(match.group(1))
    level = match.group(2)
    field = match.group(3)
    new_name = field if level == "player" else f"group_{field}"
    round_columns.setdefault(round_number, {})[new_name] = col

round_frames = []
for round_number in sorted(round_columns):
    frame = df[id_columns].copy()
    frame["round"] = round_number
    for new_name, original_col in round_columns[round_number].items():
        frame[new_name] = df[original_col]
    round_frames.append(frame)

long_df = pd.concat(round_frames, ignore_index=True)

# oTree leaves "role" empty in this app
if "role" in long_df.columns and long_df["role"].isna().all():
    long_df = long_df.drop(columns="role")


# =========================================================
# DERIVED MEASURES (LONG FORMAT ONLY)
# =========================================================

# Which game and which round of the game
long_df["game_number"] = (long_df["round"] - 1) // ROUNDS_PER_GAME + 1
long_df["round_in_game"] = (long_df["round"] - 1) % ROUNDS_PER_GAME + 1

# Identifies the pair a participant was matched with in a round: both members of
# the pair share the same pair_id (session + round + group number)
if {"session.code", "group_id_in_subsession"}.issubset(long_df.columns):
    long_df["pair_id"] = (
        long_df["session.code"].astype(str)
        + "_r" + long_df["round"].astype(str)
        + "_g" + long_df["group_id_in_subsession"].astype(str)
    )

# Row / Column role (oTree usually exports booleans as 1/0, sometimes True/False)
truthy = {1, 1.0, True, "1", "True", "true"}
falsy = {0, 0.0, False, "0", "False", "false"}

def to_bool(value):
    if value in truthy:
        return True
    if value in falsy:
        return False
    return pd.NA

if "is_row" in long_df.columns:
    is_row = long_df["is_row"].map(to_bool)
    known = is_row.notna()
    row_mask = is_row.fillna(False).astype(bool)

    long_df["role"] = is_row.map({True: "Row", False: "Column"})

    if {"choice", "opponent_choice"}.issubset(long_df.columns):
        # Both players' actions, from the Row and Column point of view
        long_df["row_choice"] = long_df["choice"].where(row_mask, long_df["opponent_choice"]).where(known)
        long_df["column_choice"] = long_df["opponent_choice"].where(row_mask, long_df["choice"]).where(known)
        # Cell of the payoff matrix that was played, e.g. "AB" = Row chose A, Column chose B
        long_df["outcome"] = (long_df["row_choice"] + long_df["column_choice"]).where(known)

# 1 if the participant chose Action A, 0 if Action B
if "choice" in long_df.columns:
    long_df["choice_A"] = (long_df["choice"] == "A").astype(int).where(long_df["choice"].isin(["A", "B"]))

# Running totals of points
if "payoff" in long_df.columns:
    long_df = long_df.sort_values(["session.code", "participant.code", "round"]).reset_index(drop=True)
    long_df["points_in_game_so_far"] = long_df.groupby(["participant.code", "game_number"])["payoff"].cumsum()
    long_df["total_points_so_far"] = long_df.groupby("participant.code")["payoff"].cumsum()

# Order rows by session, participant, then round
sort_columns = [col for col in ("session.code", "participant.code", "round") if col in long_df.columns]
long_df = long_df.sort_values(sort_columns).reset_index(drop=True)

long_df.to_csv(output_file_long, index=False)


# =========================================================
# SUMMARY
# =========================================================

print("CSV cleaning complete!")
print(f"Original columns: {len(df.columns)}")
print(f"Retained columns: {len(cleaned_df.columns)}")
print(f"Removed columns: {len(df.columns) - len(cleaned_df.columns)}")
print(f"Rows retained: {len(cleaned_df)}")
print(f"\nOutput file (wide): {output_file.resolve()}")
print(f"Output file (long): {output_file_long.resolve()}")
print(f"Long format: {len(long_df)} rows ({len(round_columns)} rounds)")

print("\nRetained columns:")
for col in columns_to_keep:
    print(f"  {col}")

# Check that the expected identifiers are present
print("\nIdentifier check:")
for col in identifier_columns:
    status = "FOUND" if col in cleaned_df.columns else "NOT FOUND"
    print(f"  {col}: {status}")
