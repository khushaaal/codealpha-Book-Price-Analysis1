import os
import re
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

# Website URL
url = "https://books.toscrape.com/"

# Send HTTP Request
response = requests.get(url)

# Check if request is successful
if response.status_code != 200:
    print("Failed to fetch the website.")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all book containers
books = soup.find_all("article", class_="product_pod")

# Lists to store data
book_names = []
prices = []
ratings = []
availability = []

# Extract data from each book
for book in books:

    # Book Name
    name = book.h3.a["title"]

    # Price (Extract only the number)
    price_text = book.find("p", class_="price_color").text
    price = re.search(r"\d+\.\d+", price_text).group()

    # Rating
    rating = book.p["class"][1]

    # Availability
    stock = book.find("p", class_="instock availability").text.strip()

    # Append data to lists
    book_names.append(name)
    prices.append(float(price))
    ratings.append(rating)
    availability.append(stock)

# Create DataFrame
df = pd.DataFrame({
    "Book Name": book_names,
    "Price (£)": prices,
    "Rating": ratings,
    "Availability": availability
})

# Save CSV
df.to_csv("books.csv", index=False)

print("✅ books.csv created successfully!")

# Display first 5 rows
print("\nFirst 5 Books:\n")
print(df.head())

# Statistics
print("\nStatistics")
print(df.describe())

print("\nAverage Price:", round(df["Price (£)"].mean(), 2))
print("Highest Price:", df["Price (£)"].max())
print("Lowest Price:", df["Price (£)"].min())

# Create graphs folder
os.makedirs("graphs", exist_ok=True)

# -----------------------------
# Price Distribution Graph
# -----------------------------
plt.figure(figsize=(8, 5))

sns.histplot(df["Price (£)"], bins=10, kde=True)

plt.title("Book Price Distribution")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig("graphs/price_distribution.png")

plt.show()

# -----------------------------
# Rating Graph
# -----------------------------
rating_order = ["One", "Two", "Three", "Four", "Five"]

plt.figure(figsize=(7, 5))

sns.countplot(data=df, x="Rating", order=rating_order)

plt.title("Book Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig("graphs/ratings.png")

plt.show()

print("\n✅ Graphs saved successfully!")
print("🎉 Project Completed Successfully!")