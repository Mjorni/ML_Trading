import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler


df = pd.read_csv("LOGI.csv", parse_dates=["Date"])

def get_prewiev(df):
    plt.plot(df[["Open", "Close", "Low", "High"]], label = ["Open", "Close", "Low", "High"], linewidth = 0.5)
    plt.legend()
    