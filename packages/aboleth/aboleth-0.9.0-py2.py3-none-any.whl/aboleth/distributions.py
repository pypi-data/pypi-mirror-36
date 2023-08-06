"""Helper functions for model parameter distributions."""
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from aboleth.util import pos_variable, summary_histogram


JIT = 1e-15  # cholesky jitter


#
# Streamlined interfaces for initialising the priors and posteriors
#

def norm_prior(dim, std):
    """Make a prior (zero mean, isotropic) Normal distribution.

    Parameters
    ----------
    dim : tuple or list
        the dimension of this distribution.
    std : float, np.array, tf.Tensor, tf.Variable
        the prior standard deviation of this distribution.

    Returns
    -------
    P : tf.distributions.Normal
        the initialised prior Normal object.

    """
    mu = tf.zeros(dim)
    P = tf.distributions.Normal(loc=mu, scale=std)
    return P


def norm_posterior(dim, std0, suffix=None):
    """Initialise a posterior (diagonal) Normal distribution.

    Parameters
    ----------
    dim : tuple or list
        the dimension of this distribution.
    std0 : float, np.array
        the initial (unoptimized) standard deviation of this distribution.
        Must be a scalar or have the same shape as dim.
    suffix : str
        suffix to add to the names of the variables of the parameters of this
        distribution.

    Returns
    -------
    Q : tf.distributions.Normal
        the initialised posterior Normal object.

    Note
    ----
    This will make tf.Variables on the mean standard deviation of the
    posterior. The initialisation of the mean is zero and the initialisation of
    the standard deviation is simply ``std0`` for each element.

    """
    assert (np.ndim(std0) == 0) or (np.shape(std0) == dim)
    mu_0 = tf.zeros(dim)
    mu = tf.Variable(mu_0, name=_add_suffix("W_mu_q", suffix))

    if np.ndim(std0) == 0:
        std0 = tf.ones(dim) * std0

    std = pos_variable(std0, name=_add_suffix("W_std_q", suffix))
    summary_histogram(mu)
    summary_histogram(std)

    Q = tf.distributions.Normal(loc=mu, scale=std)
    return Q


def gaus_posterior(dim, std0, suffix=None):
    """Initialise a posterior Gaussian distribution with a diagonal covariance.

    Even though this is initialised with a diagonal covariance, a full
    covariance will be learned, using a lower triangular Cholesky
    parameterisation.

    Parameters
    ----------
    dim : tuple or list
        the dimension of this distribution.
    std0 : float
        the initial (unoptimized) diagonal standard deviation of this
        distribution.
    suffix : str
        suffix to add to the names of the variables of the parameters of this
        distribution.

    Returns
    -------
    Q : tf.contrib.distributions.MultivariateNormalTriL
        the initialised posterior Gaussian object.

    Note
    ----
    This will make tf.Variables on the mean and covariance of the posterior.
    The initialisation of the mean is zero, and the initialisation of the
    (lower triangular of the) covariance is from diagonal matrices with
    diagonal elements taking the value of `std0`.

    """
    o, i = dim

    # Optimize only values in lower triangular
    u, v = np.tril_indices(i)
    indices = (u * i + v)[:, np.newaxis]
    l0 = (np.tile(np.eye(i, dtype=np.float32) * std0, [o, 1, 1])[:, u, v].T)
    lflat = tf.Variable(l0, name=_add_suffix("W_cov_q", suffix))
    Lt = tf.transpose(tf.scatter_nd(indices, lflat, shape=(i * i, o)))
    L = tf.reshape(Lt, (o, i, i))

    mu_0 = tf.zeros((o, i))
    mu = tf.Variable(mu_0, name=_add_suffix("W_mu_q", suffix))

    summary_histogram(mu)
    summary_histogram(lflat)

    Q = tfp.distributions.MultivariateNormalTriL(mu, L)
    return Q


#
# KL divergence calculations
#

def kl_sum(q, p):
    r"""Compute the total KL between (potentially) many distributions.

    I.e. :math:`\sum_i \text{KL}[q_i || p_i]`

    Parameters
    ----------
    q : tf.distributions.Distribution
        A tensorflow Distribution object
    p : tf.distributions.Distribution
        A tensorflow Distribution object

    Returns
    -------
    kl : Tensor
        the result of the sum of the KL divergences of the ``q`` and ``p``
        distibutions.

    """
    kl = tf.reduce_sum(tf.distributions.kl_divergence(q, p))
    return kl


@tf.distributions.RegisterKL(tfp.distributions.MultivariateNormalTriL,
                             tf.distributions.Normal)
def _kl_gaussian_normal(q, p, name=None):
    """Gaussian-Normal Kullback Leibler divergence calculation.

    Parameters
    ----------
    q : tfp.distributions.MultivariateNormalTriL
        the approximating 'q' distribution(s).
    p : tf.distributions.Normal
        the prior 'p' distribution(s), ``p.scale`` should be a *scalar* value!
    name : str
        name to give the resulting KL divergence Tensor

    Returns
    -------
    KL : Tensor
        the result of KL[q||p].

    """
    assert len(p.scale.shape) == 0, "This KL divergence is only implemented " \
        "for Normal distributions that share a scale parameter for p"
    D = tf.to_float(q.event_shape_tensor())
    n = tf.to_float(q.batch_shape_tensor())
    p_var = p.scale**2
    L = q.scale.to_dense()
    tr = tf.reduce_sum(L * L) / p_var
    # tr = tf.reduce_sum(tf.trace(q.covariance())) / p_var  # Above is faster
    dist = tf.reduce_sum((p.mean() - q.mean())**2) / p_var
    # logdet = n * D * tf.log(p_var) \
    #     - 2 * tf.reduce_sum(q.scale.log_abs_determinant())  # Numerical issue
    logdet = n * D * tf.log(p_var) - _chollogdet(L)
    KL = 0.5 * (tr + dist + logdet - n * D)
    if name:
        KL = tf.identity(KL, name=name)
    return KL


#
# Private module stuff
#

def _chollogdet(L):
    """Log det of a cholesky, where L is (..., D, D)."""
    ldiag = tf.maximum(tf.abs(tf.matrix_diag_part(L)), JIT)  # keep > 0
    logdet = 2. * tf.reduce_sum(tf.log(ldiag))
    return logdet


def _add_suffix(name, suffix):
    """Add a suffix to a name, do nothing if suffix is None."""
    suffix = "" if suffix is None else "_" + suffix
    new_name = name + suffix
    return new_name
