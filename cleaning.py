import pandas as pd
import numpy as np
import re

# this piece of code will make sure you cann see the data clearly.

pd.set_option("display.max_columns", None)   # show all columns
pd.set_option("display.max_rows", 100)       # or None for unlimited
pd.set_option("display.width", 1000)         # prevent wrapping
pd.set_option("display.max_colwidth", None)  # show full column text

# from IPython.display import display as ds

df=pd.read_csv('aus_ccx_21.csv')

# print(df.head())
# print("**********************************************")
# print(df.shape)
# print("*********************")
# print(df.info())

#********************************************************************************************************
# will check is there any trailing spaces here in the data
#********************************************************************************************************

df['first_name']=df['first_name'].str.strip()
df['last_name']=df['last_name'].str.strip()
df['email']=df['email'].str.strip()
df['remarks']=df['remarks'].str.strip()

# from the aboves piece of code we can see that all the columns given to us is in object form(string) so we need to remove leading or trailing spaces
# but writing manually is difficult

df[df.select_dtypes(include='object').columns]=df[df.select_dtypes(include='object').columns].astype('string').map(str.strip,na_action='ignore')

# Step 1: df.select_dtypes(include='object')
# This selects all columns with dtype = object (usually text columns).

# Step 2: .columns
# Extracts just the column names of those object columns.

# .astype('string')
# Converts those columns from object dtype → Pandas’ dedicated string dtype.
# Difference:
# object = generic Python objects (less optimized).
# string = new optimized pandas type with better string ops & null handling.

# .map(str.strip, na_action='ignore')
# Applies str.strip() to each cell → removes leading/trailing spaces.
# na_action='ignore': ensures NaN values are not modified (otherwise str.strip(NaN) would error out).

# print(df.head(7))
# print(df.info())

#********************************************************************************************************
# validating email, error emails to nan and formatting the email correctly
#********************************************************************************************************

df['email']=df['email'].str.lower()
a=df['email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',na = False)
df.loc[~a, 'email'] = np.nan



#********************************************************************************************************
# date time cleaning
#********************************************************************************************************

df['join_date'] = df['join_date'].replace('Not Available',np.nan)
df['join_date'] = pd.to_datetime(df['join_date'],errors='coerce',dayfirst = True)
# Without dayfirst, Pandas assumes MM/DD/YYYY.
# With dayfirst=True, it assumes DD/MM/YYYY.




#********************************************************************************************************
# salary (remove usd and symbol just numbers) chnage to numeric
#********************************************************************************************************

df['salary'] = df['salary'].str.replace(r'[\$,USD\s]','',regex=True)
df['salary'] = pd.to_numeric(df['salary'],errors = 'coerce')

# print(df.info())


#********************************************************************************************************
# remarks trailing and leading spaces (double spaces present in the remarks make it to single)
#********************************************************************************************************

df['remarks'] = df['remarks'].str.strip()
df['remarks'] = df['remarks'].str.replace("  "," ")
df.loc[df['remarks'].isnull(),"remarks"] = np.nan

# print(df['remarks'])

#********************************************************************************************************
# sales (remove usd and symbol just numbers) chnage to numeric
#********************************************************************************************************

df['sales']=df['sales'].str.replace("$",'').str.strip()
df['sales'] = pd.to_numeric(df['sales'],errors = 'coerce')

# print(df.head(20))

#********************************************************************************************************
# time_productive change to numeric
#********************************************************************************************************
df['time_productive']=df['time_productive'].str.replace("hrs",'').str.strip()
df['time_productive'] = pd.to_numeric(df['time_productive'],errors = 'coerce')
df.loc[df['time_productive'].isnull(),"time_productive"] = np.nan
# print(df.info())


#********************************************************************************************************
# replace missing values in email to "unknown@no_mail.com"
#********************************************************************************************************

df.loc[df['email'].isnull(),'email'] = "unknown@no_mail.com"
# print(df.head(10))


#********************************************************************************************************
# replace missing values in remarks to "unknown"
#********************************************************************************************************
df.loc[df['remarks'].isnull(),'remarks'] = "unknown"
# print(df.head(20))
# print(df.info())


#********************************************************************************************************
# drop duplicates based on first_name,last_name,email
#********************************************************************************************************

df=df.drop_duplicates(subset=['first_name','last_name','email'])
# print(df.head(40))


#********************************************************************************************************
# Highest recorded sales
#teh central average
#the middle point of distribution
#the most frequent observed value
#********************************************************************************************************

# print("Highest recorded sales :- ",df['sales'].max())
# print("Central average :- ", round(df['sales'].mean(),2))
# print("The middle point of distribution :- ", df['sales'].median())
# print("Thhe most frequent observed value :- ", df['sales'].mode()[0])


#********************************************************************************************************
# add new column (increment)
# above 4000 sales -> 12% 
# 2000 - 4400 sales -> 10% 
# 1000-2000 sales -> 8% 
# outside these ranges ->none
#********************************************************************************************************

df['increment_percentage'] = None
df.loc[df['sales'] >= 4000,"increment_percentage"] = 12
df.loc[(df['sales'] >= 2000) & (df['sales'] < 4000),"increment_percentage"] = 10
df.loc[(df['sales'] >= 1000) & (df['sales'] < 2000),"increment_percentage"] = 8
# print(df.head(20))


#********************************************************************************************************
# who do not fall in bracket give 3 percent
# make new updated salary column.
#********************************************************************************************************
df.loc[df['increment_percentage'].isnull(),'increment_percentage'] = 3
df['Updated_salary'] =df['salary'] + (df['salary']*(df['increment_percentage']*0.01))


# fill the salary with values    
df['salary']=df['salary'].apply(lambda x:np.random.randint(43571,60809) if pd.isnull(x) else x)
df['Updated_salary'] =df['salary'] + (df['salary']*(df['increment_percentage']*0.01))
df['Updated_salary']=pd.to_numeric(df['Updated_salary'],errors='coerce')
# print(df.info())


#********************************************************************************************************
# flag employees with
# sales data missing
# time productivity is below 80
# final incremented salary in top 40%
#********************************************************************************************************

df['termination_flag'] = None
a=np.percentile(df['Updated_salary'],60)
df.loc[(df['sales'].isnull()) & (df['time_productive'] < 80)& (df['Updated_salary'] > a),'termination_flag'] = "Yes"
df.loc[df['termination_flag'].isnull(),'termination_flag'] = "No"

# print(df[df["termination_flag"] == "Yes"])
# print(df.info())


#********************************************************************************************************
# work experience in tearms of years and days
#emp with 4+ years of exp and increment percentage > 10 in promoton pipeline.
#********************************************************************************************************
a=pd.to_datetime("today").normalize()
df['experience'] = a - df['join_date']
df['remaining'] = df['experience'].dt.days%365
df['abc']= df['experience'].dt.days//365
df['experience'] = df['experience'].dt.days//365
df['experience'] = df['experience'].astype(str) + " Years " + df['remaining'].astype(str) + " Days"
df.loc[df['experience'].str.contains('nan'),'experience'] = np.nan
df.drop(columns='remaining',inplace = True)

df['Promotion'] = "Not in pipline"
df.loc[(df['abc'] >= 4) & (df['increment_percentage'] >=  10),'Promotion'] = "In Pipieline"
df.drop(columns='abc',inplace = True)

# print(df['Promotion'].head(40))

print(df[df['Promotion'] == 'In Pipieline'])


