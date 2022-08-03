
#Question 1: Read the .csv file and show the general information about the dataset.
import pandas as pd
df=pd.read_csv("datasets/persona.csv") #dataset can not be shared because it is private.
df.head()
df.info()
df.isnull().sum()

# Question 2: How many unique SOURCE are there? What are their frequencies?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Question 3: How many unique PRICE are there?
df["PRICE"].nunique()

# Question 4: How many sales were made from which PRICE?
df["PRICE"].value_counts()

# Question 5: How many sales were made from which country?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

# Question 6: How much was earned in total from sales by country?
df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# Question 7: What are the sales numbers according to SOURCE types?
df["SOURCE"].value_counts()

# Question 8: What are the PRICE averages by country?
df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})

# Question 9: What are the PRICE averages according to SOURCE?
df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})

# Question 10: What are the PRICE averages in the COUNTRY-SOURCE breakdown?
df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})



#############################################
# TASK 2: What are the average earnings in breakdown of COUNTRY, SOURCE, SEX, AGE?
#############################################
df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()


#############################################
# TASK 3: Sort the output by PRICE.
#############################################
# To better see the output from the previous question, apply the sort_values method to PRICE in descending order.
# Save the output as agg_df.
agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()


#############################################
# TASK 4: Convert the names in the index to variable names.
#############################################
# All variables except PRICE in the output of the third question are index names.
# Convert these names to variable names.

agg_df = agg_df.reset_index()
agg_df.head()


#############################################
# TASK 5: Convert AGE variable to categorical variable and add it to agg_df.
#############################################
# Convert the numeric variable age to a categorical variable.

# Let's specify where the AGE variable will be divided:
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Let's express what the nomenclature will be for the dividing points:
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# Let's divide age:
agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
agg_df.head()


#############################################
# TASK 6: Identify new level based customers and add them as variables to the dataset.
#############################################
# Define a variable named customers_level_based and add this variable to the dataset.
# Attention!
# After creating customers_level_based values with list comp, these values need to be deduplicated.
# For example, it could be more than one of the following expressions: USA_ANDROID_MALE_0_18
# It is necessary to take them to groupby and get the price averages.


# variable names:
agg_df.columns

# gözlem değerlerine nasıl erişiriz?
for row in agg_df.values:
    print(row)

# We want to put the VALUES of the COUNTRY, SOURCE, SEX and age_cat variables next to each other and concatenate them with an underscore.
# We can do this with list comprehension.
# Let's perform the operation in such a way that we select the observation values in the above loop:
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Let's add it to the dataset:
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

# Let's remove the unnecessary variables:
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))


agg_df["customers_level_based"].value_counts()

# For this reason, after groupby according to the segments, we should take the price averages and deduplicate the segments.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})

# It is in the customers_level_based index. Let's turn that into a variable.
agg_df = agg_df.reset_index()
agg_df.head()

# Let's check. we expect each persona to be one:
agg_df["customers_level_based"].value_counts()
agg_df.head()


#############################################
# TASK 7: Segment new customers (USA_ANDROID_MALE_0_18).
#############################################
# Segment by PRICE,
# add segments to agg_df with "SEGMENT" naming,
# describe the segments,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})



#############################################
# TASK 8: Classify the new customers and estimate how much income they can bring.
#############################################
# What segment does a 33-year-old Turkish woman using ANDROID belong to and how much income is expected to earn on average?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# In which segment and on average how much income would a 35-year-old French woman using IOS expect to earn?
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

