import pandas as pd

# -----------------------------------
# 1. LOAD CLEANED DATA
# -----------------------------------

file_path = "data/cleaned/online_retail_cleaned.csv"

df = pd.read_csv(
    file_path,
    parse_dates=["InvoiceDate"]
)

print("Rows loaded:", len(df))


# -----------------------------------
# 2. SET ANALYSIS DATE
# -----------------------------------

analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

print("Analysis date:", analysis_date)


# -----------------------------------
# 3. CALCULATE RFM METRICS
# -----------------------------------

rfm = df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

print("\nRFM preview:")
print(rfm.head())

print("\nNumber of customers:")
print(len(rfm))

# -----------------------------------
# 4. CREATE RFM SCORES
# -----------------------------------

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print("\nRFM scores preview:")
print(rfm.head(10))

# -----------------------------------
# 5. CREATE CUSTOMER SEGMENTS
# -----------------------------------

def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "New Customers"

    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"

    elif r <= 2 and f <= 2:
        return "Hibernating"

    else:
        return "Potential Loyalists"


rfm["Segment"] = rfm.apply(
    assign_segment,
    axis=1
)

print("\nCustomer segments:")
print(rfm["Segment"].value_counts())

print("\nSegment preview:")
print(
    rfm[
        [
            "Customer ID",
            "Recency",
            "Frequency",
            "Monetary",
            "R_Score",
            "F_Score",
            "M_Score",
            "RFM_Score",
            "Segment"
        ]
    ].head(15)
)

# -----------------------------------
# 6. ANALYZE SEGMENT PERFORMANCE
# -----------------------------------

segment_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("Customer ID", "count"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Customer_Value=("Monetary", "mean")
    )
    .reset_index()
)

segment_summary["Revenue_Share_Pct"] = (
    segment_summary["Total_Revenue"]
    / segment_summary["Total_Revenue"].sum()
    * 100
)

segment_summary = segment_summary.sort_values(
    "Total_Revenue",
    ascending=False
)

print("\nSegment performance:")
print(
    segment_summary.round(
        {
            "Avg_Recency": 1,
            "Avg_Frequency": 1,
            "Total_Revenue": 2,
            "Avg_Customer_Value": 2,
            "Revenue_Share_Pct": 2
        }
    )
)

# -----------------------------------
# 7. EXPORT RFM RESULTS
# -----------------------------------

rfm.to_csv(
    "data/cleaned/rfm_customer_segments.csv",
    index=False
)

segment_summary.to_csv(
    "data/cleaned/rfm_segment_summary.csv",
    index=False
)

print("\nRFM files exported successfully.")