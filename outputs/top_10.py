import pandas as pd
import numpy as np

df = pd.read_csv('outputs/teams_ouput')
rank = df.sort_values('elo',ascending=False).loc[df['tracking'] == 1].head(10)
rank = rank.drop(['short_name', 'division', 'mascot','conference','tracking'], axis=1)
rank.columns = ['School', 'Elo']
rank = rank.to_string(index=False)

print(rank)
