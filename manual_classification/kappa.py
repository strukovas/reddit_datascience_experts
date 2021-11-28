
import argparse
import pandas as pd
from sklearn.metrics import cohen_kappa_score

def main(a, b):
    A = pd.read_csv(a)
    B = pd.read_csv(b)

    A = A[~A['category'].isnull()]
    B = B[~B['category'].isnull()]

    print(A['id'].equals(B['id']))

    print(cohen_kappa_score(list(A['category']), list(B['category'])))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('a')
    parser.add_argument('b')
    args = parser.parse_args()

    main(args.a, args.b)
