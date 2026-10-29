
import pandas as pd
from pathlib import Path

# =========================================================
# INPUT AND OUTPUT FILES
# =========================================================

input_file = Path("all_apps_wide-2026-10-28.csv") #keep same if csv in same folder as .py file
                                                  #change path to csv file
output_file = Path("tradeDealGame_cleaned.csv")


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
    "tradeDealGame.1.group.id_in_subsession",  # Group ID
]


# =========================================================
# KEEP ALL APP-SPECIFIC VARIABLES
# =========================================================

app_prefixes = ("tradeDealGame.",)

app_columns = [
    col for col in df.columns
    if col.startswith(app_prefixes)
]


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
# EXPORT CLEANED DATASET
# =========================================================

cleaned_df.to_csv(output_file, index=False)


# =========================================================
# SUMMARY
# =========================================================

print("CSV cleaning complete!")
print(f"Original columns: {len(df.columns)}")
print(f"Retained columns: {len(cleaned_df.columns)}")
print(f"Removed columns: {len(df.columns) - len(cleaned_df.columns)}")
print(f"Rows retained: {len(cleaned_df)}")
print(f"\nOutput file: {output_file.resolve()}")

print("\nRetained columns:")
for col in columns_to_keep:
    print(f"  {col}")

# Check that the expected identifiers are present
print("\nIdentifier check:")
for col in identifier_columns:
    status = "FOUND" if col in cleaned_df.columns else "NOT FOUND"
    print(f"  {col}: {status}")
