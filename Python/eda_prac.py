import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "date": ["2026-05-20", "2026-05-20", "2026-05-20", "2026-05-21", "2026-05-21", "2026-05-21"],
    "category": ["Electronics", "Clothing", "Groceries", "Electronics", "Clothing", "Groceries"],
    "units_sold": [15, 40, 120, 18, 35, 140],
    "revenue": [75000, 20000, 12000, 90000, 17500, 14000],
    "discount_pct": [10, 20, 5, 15, 25, 5]
})

print(df)


# --- Plot 1: Histogram of units_sold (overall) ---
def plot_units_histogram(df):
    plt.figure(figsize=(8, 5))
    
    sns.histplot(data=df, x='units_sold', bins=20)
    
    plt.title('Distribution of Units Sold')
    plt.xlabel('Units Sold')
    plt.ylabel('Frequency')

    plt.show()

# --- Plot 2: Histogram of units_sold by category ---
def plot_units_histogram_hue(df):
    # Your implementation here
    plt.figure(figsize=(8,5))

    sns.histplot(data=df, x='units_sold', bins=20, hue='category')

    plt.title('Distribution of Units Sold')
    plt.xlabel('Units Sold')
    plt.ylabel('Frequency')

    plt.show()

# --- Plot 3: Box plot of revenue by category ---
def plot_revenue_boxplot(df):
    # Your implementation here
    plt.figure(figsize=(8,5))

    sns.boxplot(data=df, y='revenue', hue='category')

    plt.title('A box plot of revenue grouped by category')
    plt.xlabel('category')
    plt.show()

# --- Plot 4: Scatter plot of units_sold vs revenue ---
def plot_scatter(df):
    # Your implementation here

    sns.scatterplot(data=df, x='category', y='revenue', hue='category')
    plt.show()

    # for category, data in df.groupby("category"):
    #     print(category, data)

# --- Outlier bounds ---
def compute_outlier_bounds(df):
    Q1 = df["revenue"].quantile(0.25)
    Q3 = df["revenue"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)

    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Lower Bound:", lower)
    print("Upper Bound:", upper)

    outliers = df[
        (df["revenue"] < lower) |
        (df["revenue"] > upper)
    ]

    print("\nOutliers:")
    print(outliers if not outliers.empty else "No Outliers")


if __name__ == "__main__":
    plot_units_histogram(df)
    plot_units_histogram_hue(df)
    plot_revenue_boxplot(df)
    plot_scatter(df)
    compute_outlier_bounds(df)