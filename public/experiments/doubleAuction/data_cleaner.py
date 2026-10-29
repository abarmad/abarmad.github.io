
import re
import pandas as pd
from pathlib import Path

# =========================================================
# INPUT AND OUTPUT FILES
# =========================================================

input_file = Path("all_apps_wide-2026-10-28.csv") #keep same if csv in same folder as .py file
                                                  #change path to csv file
output_file = Path("uniform_double_auction_cleaned.csv")             # wide: one row per participant
output_file_long = Path("uniform_double_auction_cleaned_long.csv")   # long: one row per participant per round


# =========================================================
# OPTIONS
# =========================================================

# If True, the player_name column (chosen display name) is removed from both
# outputs. Participant identity is then only available through participant.code.
DROP_PLAYER_NAMES = True


# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv(input_file)


# =========================================================
# IDENTIFIERS TO KEEP
# =========================================================

identifier_columns = [
    "participant.code",  # Unique participant identifier
    "session.code",      # Session identifier
    "uniform_double_auction.1.group.id_in_subsession",  # Group ID (always 1: one market per session)
]


# =========================================================
# KEEP ALL APP-SPECIFIC VARIABLES
# =========================================================

app_prefixes = ("uniform_double_auction.",)

app_columns = [
    col for col in df.columns
    if col.startswith(app_prefixes)
]

# Optionally remove the participant's chosen name
if DROP_PLAYER_NAMES:
    app_columns = [col for col in app_columns if not col.endswith(".player_name")]


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
# Wide columns look like:  uniform_double_auction.3.player.bid
#                          uniform_double_auction.3.group.market_price
# In the long file, player variables keep their name (e.g. "bid") and group
# variables get a "group_" prefix (e.g. "group_market_price"), because some
# names (like "treatment") exist at both levels.

column_pattern = re.compile(r"^uniform_double_auction\.(\d+)\.(player|group)\.(.+)$")

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
long_id_columns = [col for col in id_columns if not col.startswith("uniform_double_auction.")]

round_frames = []
for round_number in sorted(round_columns):
    frame = df[long_id_columns].copy()
    frame["round"] = round_number
    for new_name, original_col in round_columns[round_number].items():
        frame[new_name] = df[original_col]
    round_frames.append(frame)

long_df = pd.concat(round_frames, ignore_index=True)


# =========================================================
# DERIVED MEASURES (LONG FORMAT ONLY)
# =========================================================

# Buyer flag (oTree usually exports booleans as 1/0, sometimes True/False)
if "is_buyer" in long_df.columns:
    is_buyer = long_df["is_buyer"].isin([1, 1.0, True, "1", "True"])

    # Bid shading (buyers): value - bid. Positive = bid below value.
    if {"value", "bid"}.issubset(long_df.columns):
        long_df["bid_shading"] = (long_df["value"] - long_df["bid"]).where(is_buyer)

    # Ask markup (sellers): ask - cost. Positive = ask above cost.
    if {"cost", "ask"}.issubset(long_df.columns):
        long_df["ask_markup"] = (long_df["ask"] - long_df["cost"]).where(~is_buyer)

# Efficiency: actual surplus divided by the theoretical maximum surplus
if {"group_actual_total_surplus", "group_theo_max_surplus"}.issubset(long_df.columns):
    max_surplus = long_df["group_theo_max_surplus"].where(long_df["group_theo_max_surplus"] != 0)
    long_df["efficiency"] = long_df["group_actual_total_surplus"] / max_surplus

# Order rows by participant, then round
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
