import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data of gurugram real Estate.csv')
print(df.head())
print(df.columns.tolist())

# data cleaning
# columns 
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.columns = df.columns.str.replace('socity', 'society')

# numeric columns
df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)
df['area'] = df['area'].astype(str).str.replace(',', '').astype(int)
df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(int)

# categrical columns
df['status'] = df['status'].astype(str).str.strip().str.lower()
df['rera_approval'] = df['rera_approval'].astype(str).str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False})
df['flat_type'] = df['flat_type'].astype(str).str.strip().str.lower()

# remove duplicates
df = df.drop_duplicates()
# print(df)

#exploratory data analysis of gurugram real estate dataset

# Q1 Which is the costliest flat in the dataset?
costliest_flat = df.loc[df['price'].idxmax()]
print(f"1. The costliest flat is located in {costliest_flat['locality']} with a price of {costliest_flat['price']/10000000:.2f} Crores.")

# Q2 Which locality has the highest average price?
locality_avg_price = df.groupby('locality')['price'].mean().idxmax()
print(f"2. The locality with the highest average price is {locality_avg_price}.")

# Which locality has the highest rate per square foot?
locality_avg_rate =  df.groupby('locality')['rate_per_sqft'].mean().sort_values(ascending=False).idxmax()
print(f"3. The locality with the highest average rate per square foot is {locality_avg_rate}.")

# Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()
if ready_to_move_avg_price > under_construction_avg_price:
    print("4. Ready-to-move properties cost more on average.")
else:
    print("4.Under-construction properties cost more on average.")

#5 Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price > rera_not_approved_avg_price:
    print("5. RERA-approved properties command a price premium on average.")
else:
    print("5.RERA-approved properties do not command a price premium on average.")    

#6 How does area (sqft) impact property price?
sns.scatterplot(data=df, x='area', y='price')
print("6.No the area (sqft) does not always impact property price. There are many other factors that can influence the price of a property, such as location, amenities, and market conditions.")
plt.show()

#7 Which BHK configuration is the most expensive on average?
most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
print(f"7. The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

#8 Which property type (Apartment, Floor, Plot) is the costliest?
most_expensive_property_type = df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"8.The costliest property type on average is {most_expensive_property_type}.")

#9 Do certain builders or companies consistently price higher?
print("9. top 5 builder that have high price are:", end=" ")
top_5_builder = df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)
for builder in top_5_builder.index:
    print(builder, end=", ")
    
#10 Are larger homes always more expensive per square foot?
sns.scatterplot(data=df, x='area', y='rate_per_sqft')
plt.show()
print("\n10.No, larger homes are not always more expensive per square foot. The price per square foot can vary based on factors such as location, amenities, and market demand.")