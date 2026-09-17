import pandas as pd

# 1. Data acquisition
df = pd.read_csv("input.csv")

# 2. Import/export
# df = pd.read_excel("input.xlsx")
# df.to_csv("output.csv", index=False)

# 3. Data cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.dropna(how="all")

# 4. Missing values
numeric_columns = df.select_dtypes(include="number").columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
df = df.dropna(subset=["id"]) if "id" in df.columns else df

# 5. Duplicate records
df = df.drop_duplicates()

# 6. Inconsistent data
if "status" in df.columns:
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    df["status"] = df["status"].replace({"active ": "active", "yes": "active", "no": "inactive"})

# 7. Data formatting
if "name" in df.columns:
    df["name"] = df["name"].astype(str).str.strip().str.title()
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 8. Data transformation
if "price" in df.columns and "quantity" in df.columns:
    df["total"] = df["price"] * df["quantity"]

df.to_csv("cleaned_output.csv", index=False)