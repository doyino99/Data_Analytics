#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas --upgrade --quiet')
import pandas as pd
data= pd.read_csv("C:/Users/adedo/Desktop/Data_analytics/data/inventory.csv")
pd.options.display.float_format = "{:,.2f}".format
df = data.fillna(0)
print(df)


# In[2]:


#Create an amount column and total quantity column
df['amount'] = (df['RECEIVED'] - df['ISSUED']) * df["UNIT COST"]
df['TotalQty'] = df.groupby("CLASS").cumsum().eval("RECEIVED - ISSUED")
print(df)


# In[3]:


def get_WAC(df):
    # Set the first average price (We need an inception)
    df.loc[df.index[0], "WAC"] = df.loc[df.index[0], "UNIT COST"]

    # loop over the remaining rows.
    for i in range(1, len(df)):
        # if nothing was received, take the previous value
        if df.loc[df.index[i], "RECEIVED"] == 0:
            df.loc[df.index[i], "WAC"] = df.loc[df.index[i - 1], "WAC"]
        # if something was received
        elif df.loc[df.index[i], "RECEIVED"] > 0:
            df.loc[df.index[i], "WAC"] = (
                df.loc[df.index[i], "amount"]
                + ((df.loc[df.index[i - 1], "WAC"]) * (df.loc[df.index[i - 1], "TotalQty"]))
            ) / (df.loc[df.index[i], "TotalQty"])
        elif df.loc[df.index[i], "RECEIVED"] < 0:
            df.loc[df.index[i], "WAC"] = df.loc[df.index[i - 1], "WAC"]
        else:
            df.loc[df.index[i], "WAC"] = 0

    df["WAC"] = df["WAC"].round(1)

    return df


df = df.groupby("CLASS", group_keys=False).apply(get_WAC)
print(df)


# In[4]:


print(df.loc[df["CLASS"] == "FD"])


# In[ ]:




