import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.manifold import TSNE

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression


# load expression data
f = open("./GSE123302_series_matrix.txt/GSE123302_series_matrix.txt", "r")
#f = open("/content/drive/MyDrive/Laura Speggiorin - TCC/GSE123302_series_matrix.txt/GSE123302_series_matrix.txt", "r")

tmp = f.readlines()

f.close()

# select relevant parts (as strings)
header_str = tmp[69]
class_str = tmp[42]
matrix_str = tmp[70:-1]

# make list of instance ID's
header = header_str.replace("\"", "")
header = header.replace("\n", "")
header = header.replace("ID_REF\t", "")
header = header.split("\t")

# make list of diagnosis class ('ASD', 'Non-TD', 'TD')
classes = class_str.replace("\"", "")
classes = classes.replace("\n", "")
classes = classes.replace("!Sample_characteristics_ch1\t", "")
classes = classes.replace("diagnosis: ", "")
classes = classes.split("\t")

# make dataframe out of expression matrix
matrix_str = [matrix_str[i].replace("\n", "") for i in range(len(matrix_str))]

header.insert(0,"ID")
df = []
string = ""
for i in range(len(matrix_str)):
  string = matrix_str[i]
  df.append(string.split("\t"))

df = pd.DataFrame(df)
df.columns = header
df.set_index('ID', inplace=True)

df_t = df.transpose()


# load platform data
f = open("/content/drive/MyDrive/Laura Speggiorin - TCC/GSE123302_family.soft", "r")

tmp = f.readlines()

f.close()

# select relevant parts (as strings)
platform_table_str = tmp[309:54291]

# make dataframe out of platform matrix
platform_table = []
line = ""
for i in range(len(platform_table_str)):
  line = platform_table_str[i]
  platform_table.append(line.split("\t"))

platform_table = pd.DataFrame(platform_table)

platform_table.columns = platform_table.iloc[0]
platform_table = platform_table[1:]


#selecionar IDs das sondas com prefixo 'NM' na coluna 'GB_ACC'
filtered_list = platform_table[platform_table['GB_ACC'].str.startswith('NM')]

filtered_list = list(filtered_list['ID'])

teste = transformed_df.loc[:,[sonda for sonda in transformed_df.columns.tolist() if sonda in filtered_list]]


#filtrar por variancia (manter top 5000 atributos que mais variam)
variance = teste.var(axis=0)
filtered_varlist = variance.rank().sort_values(ascending=False)

filtered_varlist = list(filtered_varlist[0:5000].index)

teste2 = transformed_df.loc[:,[sonda for sonda in transformed_df.columns.tolist() if sonda in filtered_varlist]]
