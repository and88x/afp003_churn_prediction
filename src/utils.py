""" Some useful functions """
from pandas import unique, DataFrame
from time import time
from sklearn.metrics import mutual_info_score
from sklearn.feature_extraction import DictVectorizer
from scipy.stats import t, sem
from numpy import mean

def tic() -> None:
    """Homemade version of matlab tic and toc functions"""
    global startTime_for_tictoc
    startTime_for_tictoc = time()


def toc() -> None:
    """Homemade version of matlab tic and toc functions"""
    if "startTime_for_tictoc" in globals():
        val = time() - startTime_for_tictoc
        print("Elapsed time is %f seconds." % val)
    else:
        print("Toc: initial time is not set")


def categoy2feature(df, group_by: str, column: str, value: str):
    """Transform a categorical column in features
    from:
        group_by    column      value
        A           trans_1     -294.03
        B           trans_1     1297.97
        C           trans_1     191.28
        A           trans_2     2299.07
        B           trans_2     1612.10
        A           trans_4     2145.3
        ...
    to:
        group_by    trans_1   trans_2   trans_3   trans_4
        A           -294.03   2299.07   -255.36   2145.3
        B           1297.97   1612.10   6456.69   897.02
        C           191.28    1111.11   4665.12   -256.09

    """
    new_features = unique(df[column])
    new_df = DataFrame(
        unique(df["CustomerId"]),
        columns=[group_by],
    )

    for feature in new_features:
        df_to_merge = df[df[column] == feature][[group_by, value]]
        df_to_merge = df_to_merge.rename({value: feature}, axis=1)
        new_df = new_df.merge(right=df_to_merge, how="left", on=group_by)

    return new_df


def calculate_mi(series, labels):
    """Mutual information using Scikit-Learn"""
    return mutual_info_score(series, labels)


def one_hot_encoding(df):
    """Docstring"""
    # To use scikit-learn we need the data as dictionary
    cat = df.to_dict(orient="rows")

    dv = DictVectorizer(sparse=False)
    dv.fit(cat)

    # Convert the dictionaries to a matrix
    X = dv.transform(cat)

    X_as_df = DataFrame(X, columns=dv.get_feature_names())

    return X_as_df


def confidence_interval_t(data):
    """ Create 95% confidence interval for population mean weight """
    return t.interval(
        alpha=0.95, df=len(data)-1, loc=mean(data), scale=sem(data)
    )