import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from main import path_to_file

df = pd.read_csv(path_to_file, parse_dates=["Date"])
print(df)
def get_prewiev(df):
    plt.plot(df[["Open", "Close", "Low", "High"]], label = ["Open", "Close", "Low", "High"], linewidth = 0.5)
    plt.legend()
    