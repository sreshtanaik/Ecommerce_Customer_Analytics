import pandas as pd

# -----------------------------------
# 1. LOAD DATA
# -----------------------------------

file_path = "data/raw/online_retail_II.xlsx"

df_2009_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

df_2010_2011 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

# Combine both years
df = pd.concat(
    [df_2009_2010, df_2010_2011],
    ignore_index=True
)

print("Rows before cleaning:", len(df))


# -----------------------------------
# 2. CLEAN DATA
# -----------------------------------

clean_df = df.copy()

# Remove exact duplicates
clean_df = clean_df.drop_duplicates()

# Remove transactions without Customer ID
clean_df = clean_df.dropna(subset=["Customer ID"])

# Remove cancelled invoices
clean_df = clean_df[
    ~clean_df["Invoice"].astype(str).str.startswith("C")
]

# Keep positive quantities only
clean_df = clean_df[
    clean_df["Quantity"] > 0
]

# Keep positive prices only
clean_df = clean_df[
    clean_df["Price"] > 0
]

# Convert Customer ID to integer
clean_df["Customer ID"] = clean_df["Customer ID"].astype(int)

# Calculate revenue
clean_df["Revenue"] = (
    clean_df["Quantity"] * clean_df["Price"]
)


# -----------------------------------
# 3. VALIDATE CLEANING
# -----------------------------------

print("\nRows after cleaning:", len(clean_df))

print("\nMissing values after cleaning:")
print(clean_df.isnull().sum())

print("\nDuplicate rows after cleaning:")
print(clean_df.duplicated().sum())

print("\nCancelled invoices remaining:")
print(
    clean_df["Invoice"]
    .astype(str)
    .str.startswith("C")
    .sum()
)

print("\nCleaned data preview:")
print(clean_df.head())

# -----------------------------------
# 4. EXPORT CLEANED DATA
# -----------------------------------

output_path = "data/cleaned/online_retail_cleaned.csv"

clean_df.to_csv(
    output_path,
    index=False
)

print("\nCleaned dataset saved to:")
print(output_path)