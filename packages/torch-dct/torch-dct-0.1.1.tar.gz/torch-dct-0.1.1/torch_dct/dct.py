import numpy as np
import torch


def dct1(x):
    """
    Discrete Cosine Transform, Type I

    :param x: the input signal
    :return: the DCT-I of the signal over the last dimension
    """
    x_shape = x.shape
    x = x.view(-1, x_shape[-1])

    return torch.rfft(torch.cat([x, x.flip([1])[:, 1:-1]], dim=1), 1)[:, :, 0].view(*x_shape)


def idct1(X):
    """
    The inverse of DCT-I, which is just a scaled DCT-I

    Our definition if idct1 is such that idct1(dct1(x)) == x

    :param X: the input signal
    :return: the inverse DCT-I of the signal over the last dimension
    """
    n = X.shape[-1]
    return dct1(X) / (2 * (n - 1))


def dct(x):
    """
    Discrete Cosine Transform, Type II (a.k.a. the DCT)

    :param x: the input signal
    :return: the DCT-II of the signal over the last dimension
    """
    x_shape = x.shape
    x = x.contiguous().view(-1, x_shape[-1])

    v = torch.cat([x[:, ::2], x[:, 1::2].flip([1])], dim=1)

    Vc = torch.rfft(v, 1, onesided=False)

    k = - torch.arange(x_shape[-1], dtype=x.dtype)[None, :] * np.pi / (2 * x_shape[-1])
    W_r = torch.cos(k)
    W_i = torch.sin(k)

    V = Vc[:, :, 0] * W_r - Vc[:, :, 1] * W_i

    return 2 * V.view(*x_shape)


def idct(X):
    """
    The inverse to DCT-II, which is a scaled Discrete Cosine Transform, Type III

    Our definition of idct is that idct(dct(x)) == x

    :param X: the input signal
    :return: the inverse DCT-II of the signal over the last dimension
    """

    x_shape = X.shape
    X_v = X.contiguous().view(-1, x_shape[-1]) / 2

    k = torch.arange(x_shape[-1], dtype=X.dtype)[None, :] * np.pi / (2 * x_shape[-1])
    W_r = torch.cos(k)
    W_i = torch.sin(k)

    V_t_r = X_v
    V_t_i = torch.cat([X_v[:, :1] * 0, -X_v.flip([1])[:, :-1]], dim=1)

    V_r = V_t_r * W_r - V_t_i * W_i
    V_i = V_t_r * W_i + V_t_i * W_r

    V = torch.cat([V_r.unsqueeze(2), V_i.unsqueeze(2)], dim=2)

    v = torch.irfft(V, 1, onesided=False)
    x = v.new_zeros(v.shape)
    x[:, ::2] += v[:, :x_shape[-1] - (x_shape[-1] // 2)]
    x[:, 1::2] += v.flip([1])[:, :x_shape[-1] // 2]

    return x.view(*x_shape)


def dct_2d(x):
    """
    2-dimentional Discrete Cosine Transform, Type II (a.k.a. the DCT)

    :param x: the input signal
    :return: the DCT-II of the signal over the last 2 dimensions
    """
    X1 = dct(x)
    X2 = dct(X1.transpose(-1, -2))
    return X2.transpose(-1, -2)


def idct_2d(X):
    """
    The inverse to 2D DCT-II, which is a scaled Discrete Cosine Transform, Type III

    Our definition of idct is that idct_2d(dct_2d(x)) == x

    :param x: the input signal
    :return: the DCT-II of the signal over the last 2 dimensions
    """
    x1 = idct(X)
    x2 = idct(x1.transpose(-1, -2))
    return x2.transpose(-1, -2)


def dct_3d(x):
    """
    3-dimentional Discrete Cosine Transform, Type II (a.k.a. the DCT)

    :param x: the input signal
    :return: the DCT-II of the signal over the last 3 dimensions
    """
    X1 = dct(x)
    X2 = dct(X1.transpose(-1, -2))
    X3 = dct(X2.transpose(-1, -3))
    return X3.transpose(-1, -3).transpose(-1, -2)


def idct_3d(X):
    """
    The inverse to 3D DCT-II, which is a scaled Discrete Cosine Transform, Type III

    Our definition of idct is that idct_3d(dct_3d(x)) == x

    :param x: the input signal
    :return: the DCT-II of the signal over the last 3 dimensions
    """
    x1 = idct(X)
    x2 = idct(x1.transpose(-1, -2))
    x3 = idct(x2.transpose(-1, -3))
    return x3.transpose(-1, -3).transpose(-1, -2)
