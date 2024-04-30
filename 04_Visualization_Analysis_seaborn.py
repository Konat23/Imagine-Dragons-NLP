# plot line graph
import pandas as pd
import matplotlib.pyplot as plt
album = pd.read_csv("songs_sentiment.tsv", sep="\t", encoding="utf-8")

import seaborn as sns
sns.set(rc={'figure.figsize':(15,7)})

# positive plot
ax = sns.lineplot(x='album', y='positive', data=album, marker='*', color='#0000ff')
ax.set(title='Sentiment Analysis of Album Lyrics')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)  # Rotar los xlabels a 90 grados
ax.set_ylabel('')  # Quitar el ylabel
# quitar yticks
ax.set_yticks([])

# label points on the plot
for x, y in zip(album['album'], album['positive']):
    plt.text(x=x, y=y+0.002, s='{:.2f}%'.format(y * 100), color='#0000ff')

# negative plot
line_neg  = sns.lineplot(x='album', y='negative', data=album, marker='*', color='#FF0000')

for x, y in zip(album['album'], album['negative']):
    plt.text(x=x, y=y-0.003, s='{:.2f}%'.format(y * 100), color='#FF0000')

# Agregar leyenda
plt.legend(handles=[ax.lines[0], line_neg.lines[1]], labels=['Positive', 'Negative'], loc='upper left')
plt.tight_layout()
plt.show()