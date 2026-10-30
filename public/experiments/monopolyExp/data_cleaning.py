import re
import pandas as pd
from pathlib import Path

# =========================================================
# INPUT AND OUTPUT FILES
# =========================================================

input_file = Path("all_apps_wide-2026-10-30.csv")  # keep same if csv in same folder as .py file
                                                   # change path to csv file
output_file = Path("monopoly_cleaned.csv")              # wide: one row per participant
output_file_long = Path("monopoly_cleaned_long.csv")    # long: one row per participant per round


# =========================================================
# OPTIONS
# =========================================================

# Name of the app folder in the oTree project. oTree uses it as the prefix of
# every app column in the CSV (e.g. "monopoly.3.player.choice").
# If your folder has a different name, change it here. (If the name below is not
# found, the script tries to detect it from the CSV automatically.)
APP_NAME = "monopoly"

# If True, the player_name column (chosen display name) is removed from both
# outputs. Participant identity is then only available through participant.code.
DROP_PLAYER_NAMES = True

# The game is built with room for up to 50 rounds of Part 2, but Part 2 usually
# stops much earlier (10% chance of stopping after every round). Rounds that
# were never played are empty. If True, they are removed from both outputs.
DROP_UNPLAYED_ROUNDS = True

# Game constants used for the derived measures. These must match the values in
# C (the constants class) in the app's __init__.py.
NUM_ROUNDS_P1 = 10        # rounds 1-10 = Part 1; later rounds = Part 2
PLAYERS_PER_GROUP = 5
PAYOFF_MATRIX = {         # [your choice][number of OTHER participants choosing Low]
    "Low":  {4: 10, 3: 8, 2: 6, 1: 4, 0: 2},
    "High": {4: 12, 3: 11, 2: 9, 1: 7, 0: 5},
}

P2_START = NUM_ROUNDS_P1 + 1
# Highest possible total profit of a group in one round (everybody chooses Low)
MAX_GROUP_PROFIT = PLAYERS_PER_GROUP * PAYOFF_MATRIX["Low"][PLAYERS_PER_GROUP - 1]


# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv(input_file)

# If APP_NAME does not match, try to find it from the "<app>.<round>.player.choice" columns
if not any(col.startswith(f"{APP_NAME}.") for col in df.columns):
    choice_pattern = re.compile(r"^(.+)\.\d+\.player\.choice$")
    candidates = sorted({m.group(1) for m in map(choice_pattern.match, df.columns) if m})
    if len(candidates) == 1:
        print(f"APP_NAME '{APP_NAME}' not found; using '{candidates[0]}' instead.\n")
        APP_NAME = candidates[0]
    else:
        raise SystemExit(
            f"No columns starting with '{APP_NAME}.' were found in {input_file}.\n"
            f"Check APP_NAME at the top of the script (it must match the app folder name)."
        )


# =========================================================
# IDENTIFIERS TO KEEP
# =========================================================

# Note: in Part 1 groups are re-formed every round, so the group ID is
# round-specific and is kept inside the app columns (group.id_in_subsession),
# not as a single participant-level identifier.
identifier_columns = [
    "participant.code",           # Unique participant identifier
    "participant.id_in_session",  # Participant number within the session
    "session.code",               # Session identifier
]


# =========================================================
# KEEP ALL APP-SPECIFIC VARIABLES
# =========================================================

app_prefixes = (f"{APP_NAME}.",)

app_columns = [
    col for col in df.columns
    if col.startswith(app_prefixes)
]

# Optionally remove the participant's chosen name
if DROP_PLAYER_NAMES:
    app_columns = [col for col in app_columns if not col.endswith(".player_name")]

# The role column is always empty in this game
app_columns = [col for col in app_columns if not col.endswith(".player.role")]

column_pattern = re.compile(rf"^{re.escape(APP_NAME)}\.(\d+)\.(player|group|subsession)\.(.+)$")

# Work out which rounds were actually played (at least one choice was recorded)
all_rounds = sorted({int(m.group(1)) for m in map(column_pattern.match, app_columns) if m})
played_rounds = [
    r for r in all_rounds
    if f"{APP_NAME}.{r}.player.choice" in df.columns
    and df[f"{APP_NAME}.{r}.player.choice"].notna().any()
]
last_played_round = max(played_rounds) if played_rounds else 0

# Optionally remove the columns of rounds that were never played
if DROP_UNPLAYED_ROUNDS:
    kept = []
    for col in app_columns:
        match = column_pattern.match(col)
        if match and int(match.group(1)) > last_played_round:
            continue
        kept.append(col)
    app_columns = kept


# =========================================================
# SELECT COLUMNS
# =========================================================

# Keep identifiers that exist in the CSV
id_columns = [
    col for col in identifier_columns
    if col in df.columns
]

# Combine identifiers and app variables, without duplicates
columns_to_keep = list(dict.fromkeys(id_columns + app_columns))

# Create cleaned dataset
cleaned_df = df[columns_to_keep].copy()


# =========================================================
# EXPORT CLEANED DATASET (WIDE)
# =========================================================

cleaned_df.to_csv(output_file, index=False)


# =========================================================
# BUILD LONG-FORMAT DATASET (ONE ROW PER PARTICIPANT PER ROUND)
# =========================================================
# Wide columns look like:  monopoly.3.player.choice
#                          monopoly.3.group.total_low
# In the long file, player variables keep their name (e.g. "choice") and
# group variables get a "group_" prefix (e.g. "group_total_low").

# round number -> {new column name: original column name}
round_columns = {}
for col in app_columns:
    match = column_pattern.match(col)
    if not match:
        continue
    round_number = int(match.group(1))
    level = match.group(2)
    field = match.group(3)
    if level == "subsession":
        continue  # the round number is already in the "round" column
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

# Make sure the numeric columns used below really are numeric
numeric_columns = ("others_low", "others_high", "payoff", "id_in_group",
                   "group_total_low", "group_total_high", "group_id_in_subsession")
for col in numeric_columns:
    if col in long_df.columns:
        long_df[col] = pd.to_numeric(long_df[col], errors="coerce")

# Keep only rounds that were played in that session (a participant who dropped
# out keeps a row with blank values; rounds nobody played are removed)
if DROP_UNPLAYED_ROUNDS and "choice" in long_df.columns:
    played = long_df.groupby(["session.code", "round"])["choice"].transform(lambda s: s.notna().any())
    long_df = long_df[played].reset_index(drop=True)


# =========================================================
# DERIVED MEASURES (LONG FORMAT ONLY)
# =========================================================

# Part 1 = rounds 1-10 (random groups every round), Part 2 = later rounds (fixed group, chat)
long_df["part"] = long_df["round"].apply(lambda r: 1 if r <= NUM_ROUNDS_P1 else 2)
long_df["round_in_part"] = long_df["round"].where(long_df["part"] == 1, long_df["round"] - NUM_ROUNDS_P1)

# Length of Part 2 in each session (it is drawn at random) and a flag for its last round
long_df["session_part2_rounds"] = (
    long_df.groupby("session.code")["round"].transform("max") - NUM_ROUNDS_P1
).clip(lower=0)
long_df["is_final_round"] = (long_df["round"] == long_df.groupby("session.code")["round"].transform("max"))

# One group of PLAYERS_PER_GROUP per (session, round, group id)
group_keys = [col for col in ("session.code", "round", "group_id_in_subsession") if col in long_df.columns]

if "choice" in long_df.columns:
    # 1 = Low quantity, 0 = High quantity (blank if no choice recorded)
    long_df["chose_low"] = (long_df["choice"] == "Low").astype(float).where(long_df["choice"].notna())

    if "others_low" in long_df.columns:
        # Share of the other group members who chose Low (0 to 1)
        long_df["others_low_share"] = long_df["others_low"] / (PLAYERS_PER_GROUP - 1)

        # What the payoff should be according to the payoff table, and what the
        # participant would have earned with the other choice (others held fixed)
        def table_payoff(choice, others_low, switch=False):
            if pd.isna(choice) or pd.isna(others_low):
                return float("nan")
            if switch:
                choice = "High" if choice == "Low" else "Low"
            return PAYOFF_MATRIX.get(choice, {}).get(int(others_low), float("nan"))

        long_df["table_payoff"] = [
            table_payoff(c, o) for c, o in zip(long_df["choice"], long_df["others_low"])
        ]
        long_df["payoff_if_other_choice"] = [
            table_payoff(c, o, switch=True) for c, o in zip(long_df["choice"], long_df["others_low"])
        ]
        # Gain from switching to the other option (negative = current choice was better)
        if "payoff" in long_df.columns:
            long_df["gain_from_switching"] = long_df["payoff_if_other_choice"] - long_df["payoff"]

    # Group-level outcome: total profit of the group in the round and its
    # efficiency (1 = everybody chose Low, the highest possible group profit)
    if "payoff" in long_df.columns and group_keys:
        n_valid = long_df.groupby(group_keys)["payoff"].transform("count")
        long_df["group_total_profit"] = (
            long_df.groupby(group_keys)["payoff"].transform("sum").where(n_valid == PLAYERS_PER_GROUP)
        )
        long_df["group_efficiency"] = long_df["group_total_profit"] / MAX_GROUP_PROFIT

# Part 2 group identifier: the group the participant was in at the start of Part 2.
# part2_chat_channel is the same string oTree uses for the chat channel, so it
# can be used to match the participant to the chat log.
if "group_id_in_subsession" in long_df.columns:
    p2_group = (
        long_df[long_df["round"] == P2_START]
        .set_index("participant.code")["group_id_in_subsession"]
    )
    long_df["part2_group_id"] = long_df["participant.code"].map(p2_group).where(long_df["part"] == 2)
    long_df["part2_chat_channel"] = (
        long_df["session.code"] + "_part2_group_" + long_df["part2_group_id"].astype("Int64").astype(str)
    ).where(long_df["part2_group_id"].notna())

# Order rows by participant, then round
sort_columns = [col for col in ("session.code", "participant.code", "round") if col in long_df.columns]
long_df = long_df.sort_values(sort_columns).reset_index(drop=True)

# Behavior over time: previous choice and whether the participant changed it (within a part)
if "choice" in long_df.columns:
    by_part = long_df.groupby(["participant.code", "part"])
    long_df["prev_choice"] = by_part["choice"].shift(1)
    long_df["switched_choice"] = (
        (long_df["choice"] != long_df["prev_choice"])
        .astype(float)
        .where(long_df["choice"].notna() & long_df["prev_choice"].notna())
    )
    if "others_low" in long_df.columns:
        long_df["prev_others_low"] = by_part["others_low"].shift(1)

# Running totals of payoff: within the part, and over all rounds
if "payoff" in long_df.columns:
    long_df["cumulative_payoff_part"] = long_df.groupby(["participant.code", "part"])["payoff"].cumsum()
    long_df["cumulative_payoff_total"] = long_df.groupby("participant.code")["payoff"].cumsum()

long_df.to_csv(output_file_long, index=False)


# =========================================================
# CONSISTENCY CHECKS
# =========================================================

print_checks = []

# 1. Every group-round should have exactly PLAYERS_PER_GROUP members
if group_keys:
    sizes = long_df.groupby(group_keys)["participant.code"].transform("size")
    n_bad = long_df.loc[sizes != PLAYERS_PER_GROUP, group_keys].drop_duplicates().shape[0]
    print_checks.append((f"Group size = {PLAYERS_PER_GROUP}", n_bad, "group-round(s) differ"))

# 2. Others' Low + others' High should equal group size - 1
if {"others_low", "others_high"}.issubset(long_df.columns):
    total = long_df["others_low"] + long_df["others_high"]
    n_bad = int(((total != PLAYERS_PER_GROUP - 1) & total.notna()).sum())
    print_checks.append(("others_low + others_high = group size - 1", n_bad, "row(s) differ"))

# 3. Group total of Low choices should equal the number of Low choices in the group
if {"chose_low", "group_total_low"}.issubset(long_df.columns) and group_keys:
    summed = long_df.groupby(group_keys)["chose_low"].transform("sum")
    bad = ((summed - long_df["group_total_low"]).abs() > 1e-6) & long_df["group_total_low"].notna()
    n_bad = long_df.loc[bad, group_keys].drop_duplicates().shape[0]
    print_checks.append(("Group total_low = number of Low choices", n_bad, "group-round(s) differ"))

# 4. Payoff should equal the payoff table value
if {"payoff", "table_payoff"}.issubset(long_df.columns):
    n_bad = int(((long_df["payoff"] - long_df["table_payoff"]).abs() > 0.01).sum())
    print_checks.append(("Payoff = payoff table value", n_bad, "row(s) differ"))

# 5. Played rounds with a missing choice (a participant who dropped out)
if "choice" in long_df.columns:
    print_checks.append(("Missing choice in a played round", int(long_df["choice"].isna().sum()), "row(s)"))


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
print(f"Long format: {len(long_df)} rows ({long_df['round'].nunique()} rounds)")

# Part 2 length per session (it is random, so it differs between sessions)
print("\nRounds played per session (Part 1 + Part 2):")
for session_code, n_rounds in long_df.groupby("session.code")["round"].max().items():
    print(f"  {session_code}: {NUM_ROUNDS_P1} + {max(n_rounds - NUM_ROUNDS_P1, 0)}")

print("\nRetained columns:")
for col in columns_to_keep:
    print(f"  {col}")

# Check that the expected identifiers are present
print("\nIdentifier check:")
for col in identifier_columns:
    status = "FOUND" if col in cleaned_df.columns else "NOT FOUND"
    print(f"  {col}: {status}")

# Report the consistency checks (0 problems is what you want to see)
print("\nConsistency checks (0 = OK):")
for label, n_bad, unit in print_checks:
    print(f"  {label}: {n_bad} {unit}")
