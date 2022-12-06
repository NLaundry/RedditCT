import pandas as pd
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt

from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten
import matplotlib.pyplot as plt


df = pd.read_csv('test.csv', sep=',')
df_solved = pd.read_csv('solved.csv', sep=',')

# print(df.values)
print(sc.stats.describe(df["explanation_sentence_count"]))
print(sc.stats.describe(df["explanation_word_count"]))
print(sc.stats.describe(df["explanation_nesting_level_count"]))
print(sc.stats.describe(df["explanation_score"]))

# separate the CT and Non-CT data into two separate arrays.
mask = df['is_author_ct'] == True
df_ct = df[mask]
df_nonct = df[~mask]

# do a check for similar variances and skewness not too far from normal
print(sc.stats.describe(df_ct["explanation_sentence_count"]))
print(sc.stats.describe(df_nonct["explanation_sentence_count"]))

# Generate histograms
# plt.hist(df_ct["explanation_sentence_count"], bins=100)
# plt.show()

# Variances are really close - high but close
# super skewed, cannot do a t-test

# then you do a mannwhitneyu test non-parametric doesn't assume normality
print(sc.stats.ttest_ind(df_ct["explanation_sentence_count"], df_nonct["explanation_sentence_count"]))
print(sc.stats.mannwhitneyu(df_ct["explanation_sentence_count"], df_nonct["explanation_sentence_count"]))
print(sc.stats.mannwhitneyu(df_ct["explanation_word_count"], df_nonct["explanation_word_count"]))
print(sc.stats.mannwhitneyu(df_ct["explanation_score"], df_nonct["explanation_score"]))
print(sc.stats.ttest_ind(df_ct["explanation_word_count"], df_nonct["explanation_word_count"]))
# not even close to significant LOL


# check if length correlates with score just for shits
# print(sc.stats.pearsonr(df["explanation_sentence_count"], df["explanation_score"]))


# Okay so next steps are to see what happens when you get more data, merge it, random sample for similar pop sizessc.stats.pearsonr(df["explanation_sentence_count"], df["explanation_score"])

frames = [df, df_solved]
df_concat = pd.concat(frames)

mask = df_concat['is_author_ct'] == True
df_ct = df_concat[mask]
df_nonct = df_concat[~mask]

print(sc.stats.describe(df_ct["explanation_sentence_count"]))
print(sc.stats.describe(df_nonct["explanation_sentence_count"]))

plt.hist(df_ct["explanation_sentence_count"], bins=100)
plt.show()
plt.hist(df_nonct["explanation_sentence_count"], bins=100)
plt.show()


# do a check for similar variances and skewness not too far from normal
# print(sc.stats.describe(df_ct["explanation_sentence_count"]))

# For random sampling - adjusting for sample size difference
ct_sample = np.random.choice(df_ct["explanation_sentence_count"], 100)
nonct_sample = np.random.choice(df_nonct["explanation_sentence_count"], 100)

df_ur_concat = np.array((ct_sample, nonct_sample))
whitened = whiten(df_ur_concat)
# Find 2 clusters in the data
codebook, distortion = kmeans(whitened, 2)
# Plot whitened data and cluster centers in red
plt.scatter(whitened[:, 0], whitened[:, 1], c='b')
plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
plt.show()

print(sc.stats.describe(ct_sample))
print(sc.stats.describe(nonct_sample))

plt.hist(ct_sample, bins=100)
plt.show()
plt.hist(nonct_sample, bins=100)
plt.show()

# Now you can just re-run the tests
print(sc.stats.mannwhitneyu(ct_sample, nonct_sample))

# print(sc.stats.mannwhitneyu(ct_sample, nonct_sample))
# print(sc.stats.mannwhitneyu(ct_sample, nonct_sample))

