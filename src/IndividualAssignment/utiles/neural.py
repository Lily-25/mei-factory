import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    """
    Sigmoid激活函数
    公式: σ(x) = 1 / (1 + e^(-x))
    """
    return 1 / (1 + np.exp(-x))

if __name__ == '__main__':
    print(sigmoid(2.356))