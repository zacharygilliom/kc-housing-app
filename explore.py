import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math as math
df = pd.read_csv('data/kc_house_data.csv')


# print(df.head())

def change_datetime(df, col):
    df[col] = df[col].apply(lambda x:x[:-7]).astype(int)
    df[col] = df[col].apply(lambda x:pd.to_datetime(x, format='%Y%m%d'))
    return df[col]

df['date'] = change_datetime(df, 'date')

print(df.head())

print(df.columns)
# We can see from this graph that the square footage of the living area has a big impact on price
# sns.scatterplot(data=df, x='sqft_living', y='price')
# plt.savefig('image.png')

# Surprisingly, the square footage of the lot does not have an impact on pricing. It seems logical as
# most of the lots are probably the same size so the location/structure is more important.
# sns.scatterplot(data=df, x='sqft_lot', y='price')
# plt.savefig('image2.png')


# trying to just plot the raw data gets messy. 
# sns.barplot(data=df, x='date', y='price', hue='bedrooms', ci=None)
# plt.savefig('image3.png')


# lets try to clean up the data a little bit.
# let's see how the average price of a how is impacted by the number of bedrooms.
df_room_grouped = df.groupby(['bedrooms'], as_index=False).mean()
# sns.barplot(data=df_room_grouped, x='bedrooms', y='price')
# plt.savefig('image4.png')
# The data shows that the price of a house increases as the number of bedrooms increases up until about 8 room.
# from there, the average price of the house starts to fall.  Most likely due to families not needing that many 
# rooms in the house.

# How about the number of floors in a house.
df_floors_grouped = df.groupby(['floors'], as_index=False).mean()
# sns.barplot(data=df_floors_grouped, x='floors', y='price')
# plt.savefig('image5.png')
# as expected also, the price of the house increases as the # of floors increases.

print(df['waterfront'].unique())
# Having the waterfront value as either a yes or no value will allow us to create some more
# insightful plots, like a violin plot.  Lets see how the price is impacted by # of bedrooms and
# whether the apartment is waterfront or not.

# we want to group it like we did before for our bedrooms, but we also want to group it by whether it's 
# waterfront or not.

df_wat_bed_grouped = df.groupby(['bedrooms', 'waterfront'], as_index=False).mean()
print(df_wat_bed_grouped.head())

# now that we have our data structed and aggregated we can plot it using a violinplot in seaborn

# sns.violinplot(data=df_wat_bed_grouped, x='bedrooms', y='price', hue='waterfront')
# plt.savefig('image6.png')

# That plot didn't turn out like we wanted it to --- let's take out some not useful data here.
# let's remove any house that has the number of bedrooms lower than 8 as these don't follow the 
# trend of increasing the price in a positive linear behavior

df_wat_bed_grouped = df_wat_bed_grouped.loc[df_wat_bed_grouped.bedrooms <= 8]
# now let's redo our plot

# sns.violinplot(data=df_wat_bed_grouped, x='bedrooms', y='price', hue='waterfront')
# plt.savefig('image7.png')

# our plot is still not how we want it
# let's try to switch the waterfront and the bedrooms variables in our plot

# sns.violinplot(data=df_wat_bed_grouped, x='waterfront', y='price', hue='bedrooms')
# plt.savefig('image8.png')


# sns.barplot(data=df_wat_bed_grouped, x='bedrooms', y='price', hue='waterfront')
# plt.savefig('image9.png')

print(df.columns)
print(df.dtypes)
for i in df.columns:
    print(i, len(df[i].unique()))

print(df['bathrooms'].unique())


df['date_bin'] = df['yr_built']
print(df['date_bin'].head())


df['date_bin'] = df['date_bin'].apply(lambda x: (math.floor(x/10) * 10))



print(df['date_bin'].head())

