import re
import pandas as pd
from pathlib import Path

# =========================================================
# INPUT AND OUTPUT FILES
# =========================================================

input_file = Path("all_apps_wide-2026-10-29.csv") #keep same if csv in same folder as .py file
                                                  #change path to csv file
output_file = Path("public_goods_cleaned.csv")             # wide: one row per participant
output_file_long = Path("public_goods_cleaned_long.csv")   # long: one row per participant per round


# =========================================================
# OPTIONS
# =========================================================

# Name of the app folder in the oTree project. oTree uses it as the prefix of
# every app column in the CSV (e.g. "public_goods.3.player.contribution").
# If your folder has a different name, change it here.
APP_NAME = "public_goods"

# If True, the player_name column (chosen display name) is removed from both
# outputs. Participant identity is then only available through participant.code.
DROP_PLAYER_NAMES = True

# The game defines 99 punishment columns per round (punish_p1 ... punish_p99),
# one for every possible recipient. Only as many as there are participants in a
# session are ever used. If True, the unused ones are removed from both outputs.
DROP_UNUSED_PUNISH_COLUMNS = True

# Game constants used for the derived measures. These must match the values in
# C (the constants class) in the app's __init__.py.
ENDOWMENT = 10
PUNISHMENT_ENDOWMENT = 2
PUNISHMENT_REDUCTION = 3


# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv(input_file)


# =========================================================
# IDENTIFIERS TO KEEP
# =========================================================

identifier_columns = [
    "participant.code",           # Unique participant identifier
    "participant.id_in_session",  # Participant number within the session
    "session.code",               # Session identifier
    f"{APP_NAME}.1.group.id_in_subsession",  # Group ID (always 1: one group per session)
]


# =========================================================
# KEEP ALL APP-SPECIFIC VARIABLES
# =========================================================

app_prefixes = (f"{APP_NAME}.",)

app_columns = [
    col for col in df.columns
    if col.startswith(app_prefixes)
]

if not app_columns:
    raise SystemExit(
        f"No columns starting with '{APP_NAME}.' were found in {input_file}.\n"
        f"Check APP_NAME at the top of the script (it must match the app folder name)."
    )

# Optionally remove the participant's chosen name
if DROP_PLAYER_NAMES:
    app_columns = [col for col in app_columns if not col.endswith(".player_name")]

# Optionally remove punishment columns for recipients that do not exist.
# The largest possible group is the largest session (one group per session).
punish_column_pattern = re.compile(rf"^{re.escape(APP_NAME)}\.\d+\.player\.punish_p(\d+)$")

if "session.code" in df.columns:
    max_group_size = int(df.groupby("session.code").size().max())
else:
    max_group_size = len(df)

if DROP_UNUSED_PUNISH_COLUMNS:
    kept = []
    for col in app_columns:
        match = punish_column_pattern.match(col)
        if match and int(match.group(1)) > max_group_size:
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
# Wide columns look like:  public_goods.3.player.contribution
#                          public_goods.3.group.individual_share
# In the long file, player variables keep their name (e.g. "contribution") and
# group variables get a "group_" prefix (e.g. "group_individual_share").

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

# Only identifiers that are not round-specific go in the long file
long_id_columns = [col for col in id_columns if not col.startswith(f"{APP_NAME}.")]

round_frames = []
for round_number in sorted(round_columns):
    frame = df[long_id_columns].copy()
    frame["round"] = round_number
    for new_name, original_col in round_columns[round_number].items():
        frame[new_name] = df[original_col]
    round_frames.append(frame)

long_df = pd.concat(round_frames, ignore_index=True)

# Make sure the numeric columns used below really are numeric
for col in ("contribution", "payoff", "punishment_sent", "punishment_received",
            "group_total_contribution", "group_average_contribution",
            "group_individual_share"):
    if col in long_df.columns:
        long_df[col] = pd.to_numeric(long_df[col], errors="coerce")


# =========================================================
# DERIVED MEASURES (LONG FORMAT ONLY)
# =========================================================

# One-group-per-session keys (every participant in a session shares a group)
group_keys = [col for col in ("session.code", "round") if col in long_df.columns]

# Treatment flag: punishment variables only make sense in the PG_P treatment
is_pg_p = (long_df["treatment"] == "PG_P") if "treatment" in long_df.columns else None

if "contribution" in long_df.columns:
    # Contribution as a share of the endowment (0 to 1)
    long_df["contribution_rate"] = long_df["contribution"] / ENDOWMENT

    # Profit from the contribution stage only: endowment - contribution + share.
    # (Does not include the point reductions of the PG_P treatment.)
    if "group_individual_share" in long_df.columns:
        long_df["base_profit"] = (
            ENDOWMENT - long_df["contribution"] + long_df["group_individual_share"]
        )

    # Average contribution of the OTHER group members, and how far the
    # participant's own contribution is from it (negative = gave less than others)
    if "group_total_contribution" in long_df.columns and group_keys:
        group_size = long_df.groupby(group_keys)["participant.code"].transform("size")
        others_total = long_df["group_total_contribution"] - long_df["contribution"]
        long_df["others_avg_contribution"] = (others_total / (group_size - 1)).where(group_size > 1)
        long_df["deviation_from_others"] = long_df["contribution"] - long_df["others_avg_contribution"]

# Punishment measures (PG_P only; left blank for the PG treatment)
if is_pg_p is not None:
    # Units of reduction handed out: sum of the punish_p<k> columns. Each unit
    # costs the sender 1 point and removes PUNISHMENT_REDUCTION points from the target.
    punish_cols = [col for col in long_df.columns if re.fullmatch(r"punish_p\d+", col)]
    if punish_cols:
        long_df["punishment_units_sent"] = long_df[punish_cols].sum(axis=1).where(is_pg_p)

    # Units of reduction received (points received / points removed per unit)
    if "punishment_received" in long_df.columns:
        long_df["punishment_units_received"] = (
            long_df["punishment_received"] / PUNISHMENT_REDUCTION
        ).where(is_pg_p)

    # Net effect of the punishment stage on the round payoff:
    # +2 extra points - points paid - points received
    if {"punishment_sent", "punishment_received"}.issubset(long_df.columns):
        long_df["punishment_net"] = (
            PUNISHMENT_ENDOWMENT - long_df["punishment_sent"] - long_df["punishment_received"]
        ).where(is_pg_p)

# Order rows by participant, then round
sort_columns = [col for col in ("session.code", "participant.code", "round") if col in long_df.columns]
long_df = long_df.sort_values(sort_columns).reset_index(drop=True)

# Running total of payoff over rounds (this is the leaderboard number after each round)
if "payoff" in long_df.columns:
    long_df["cumulative_payoff"] = long_df.groupby("participant.code")["payoff"].cumsum()

long_df.to_csv(output_file_long, index=False)


# =========================================================
# CONSISTENCY CHECKS
# =========================================================

print_checks = []

# 1. Group total should equal the sum of the individual contributions
if {"contribution", "group_total_contribution"}.issubset(long_df.columns) and group_keys:
    summed = long_df.groupby(group_keys)["contribution"].transform("sum")
    bad = ((summed - long_df["group_total_contribution"]).abs() > 1e-6) & long_df["group_total_contribution"].notna()
    n_bad = long_df.loc[bad, group_keys].drop_duplicates().shape[0]
    print_checks.append(("Group total = sum of contributions", n_bad, "session-round(s) differ"))

# 2. Payoff should equal base profit (+ punishment net effect in PG_P)
if {"payoff", "base_profit"}.issubset(long_df.columns):
    expected = long_df["base_profit"]
    if "punishment_net" in long_df.columns:
        expected = expected + long_df["punishment_net"].fillna(0)
    n_bad = int(((long_df["payoff"] - expected).abs() > 0.01).sum())
    print_checks.append(("Payoff = base profit + punishment effect", n_bad, "row(s) differ"))


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

# Report the consistency checks (0 problems is what you want to see)
print("\nConsistency checks (0 = OK):")
for label, n_bad, unit in print_checks:
    print(f"  {label}: {n_bad} {unit}")
