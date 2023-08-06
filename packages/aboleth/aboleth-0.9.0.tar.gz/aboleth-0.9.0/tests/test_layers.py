"""Test the layers module."""
import pytest
import numpy as np
import tensorflow as tf
import aboleth as ab

from aboleth.layers import SampleLayer, SampleLayer3


D = 10
DIM = (10, 2)
EDIM = (10, 20)


def test_net_outputs(make_graph):
    """Test for expected output dimensions from a net."""
    x, y, N, X_, Y_, N_, layers = make_graph
    Net, kl = layers(X=X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()

        P = Net.eval(feed_dict={X_: x, Y_: y, N_: float(N)})

        assert P.shape == (10, N, 1)


def test_input(make_data):
    """Test the input layer."""
    x, _, X = make_data
    s = ab.InputLayer(name='myname')

    F, KL = s(myname=x)
    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval()
        assert KL == 0.0
        assert np.array_equal(f, x[np.newaxis, ...])


def test_input_sample(make_data):
    """Test the input and tiling layer."""
    x, _, X = make_data
    n_samples = tf.placeholder_with_default(3, [])
    s = ab.InputLayer(name='myname', n_samples=n_samples)

    F, KL = s(myname=x)
    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval()
        X_array = X.eval()
        assert KL == 0.0
        assert np.array_equal(f, X_array)
        for i in range(3):
            assert np.array_equal(f[i], x)


def test_ncp_con_input_samples(make_data):
    """Test we are making the ncp extra samples correctly."""
    x, _, X = make_data

    net = (
        ab.InputLayer(name='X', n_samples=1) >>
        ab.NCPContinuousPerturb(input_noise=1.)
    )

    F, KL = net(X=x)
    tc = tf.test.TestCase()

    with tc.test_session():
        f = F.eval()
        assert KL.eval() == 0.0
        assert f.shape[0] == 2
        assert np.all(f[0] == x)
        assert np.all(f[1] != x)


def test_ncp_cat_input_samples(make_categories):
    """Test we are making the ncp extra samples correctly."""
    x, K = make_categories

    pflip = 0.5
    pcats = 1. / K
    pdiff = pflip * (1 - pcats)

    net = (
        ab.InputLayer(name='X', n_samples=1) >>
        ab.NCPCategoricalPerturb(flip_prob=pflip, n_categories=K)
    )

    F, KL = net(X=x)
    tc = tf.test.TestCase()

    with tc.test_session():
        f = F.eval()
        assert KL.eval() == 0.0
        assert f.shape[0] == 2
        assert np.all(f[0] == x)
        prob = np.mean(f[1] != x)
        assert np.allclose(prob, pdiff, atol=0.1)


def test_ncp_output(make_data):
    """Test we are making the ncp extra samples correctly, and KL is OK."""
    x, _, X = make_data
    x = x.astype(np.float32)

    net_ncp = (
        ab.InputLayer(name='X', n_samples=1) >>
        ab.NCPContinuousPerturb(input_noise=1.) >>
        ab.DenseNCP(output_dim=1)
    )

    net = (
        ab.InputLayer(name='X', n_samples=1) >>
        ab.DenseVariational(output_dim=1)
    )

    F, KL = net_ncp(X=x)
    F_var, KL_var = net(X=x)
    tc = tf.test.TestCase()

    with tc.test_session():
        tf.global_variables_initializer().run()
        f, f_var = F.eval(), F_var.eval()
        assert f.shape[0] == 1
        assert f.shape == f_var.shape
        assert KL.eval() >= KL_var.eval()


def test_activation(make_data):
    """Test nonlinear activation layer."""
    x, _, X = make_data
    act = ab.Activation(tf.tanh)

    tc = tf.test.TestCase()
    with tc.test_session():
        F, KL = act(X)

        assert np.allclose(np.tanh(X.eval()), F.eval())
        assert KL == 0


@pytest.mark.parametrize('indep', [True, False])
def test_dropout(random, indep):
    """Test dropout layer."""
    samples, rows, cols = 3, 5, 1000
    keep_prob = 0.9
    X = (random.randn(samples, rows, cols) + 1).astype(np.float32)
    ab.set_hyperseed(666)
    drop = ab.DropOut(keep_prob, independent=indep)

    F, KL = drop(X)

    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval()
        dropped = np.where(f == 0)

        # Check we dropout whole columns
        if not indep:
            for s, _, c in zip(*dropped):
                assert np.allclose(f[s, :, c], 0.)

        # Check the dropout proportions are approximately correct
        active = 1 - np.sum(f[:, 0, :] == 0) / (samples * cols)

        assert f.shape == X.shape
        assert (active >= keep_prob - 0.05) and (active <= keep_prob + 0.05)
        assert KL == 0


def test_max_pooling2d(make_image_data):
    """Test dropout layer."""
    x, _, X = make_image_data

    # downsample by 2x
    max_pool = ab.MaxPool2D(pool_size=(2, 2),
                            strides=(2, 2))

    F, KL = max_pool(X)

    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval()

        # test equivalence of first window across batches
        assert np.all(np.max(x[:, :2, :2, :], axis=(1, 2)) == f[0, :, 0, 0, :])

        # n_samples and batch size remain unchanged
        assert f.shape[:2] == X.eval().shape[:2]

        # downsampled by 2x
        assert 2 * f.shape[2] == X.eval().shape[2]
        assert 2 * f.shape[3] == X.eval().shape[3]

        # number of channels remain unchanged
        assert f.shape[-1] == X.eval().shape[-1]

        assert KL == 0


def test_flatten(make_image_data):
    """Test flatten layer."""
    x, _, X = make_image_data

    # reshape. useful for feeding output of conv layer into dense layer
    reshape = ab.Flatten()

    F, KL = reshape(X)

    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval()

        assert f.shape[-1] == np.prod(X.eval().shape[2:])
        assert np.all(f == np.reshape(X.eval(), (3, 100, 28*28*3)))

        assert KL == 0


def test_arc_cosine(make_data):
    """Test the random Arc Cosine kernel."""
    S = 3
    x, _, _ = make_data
    x_, X_ = _make_placeholders(x, S)

    F, KL = ab.RandomArcCosine(n_features=10)(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        f = F.eval(feed_dict={x_: x})

        assert f.shape == (3, x.shape[0], 10)
        assert KL == 0


@pytest.mark.parametrize('reps', [1, 3, 10])
@pytest.mark.parametrize('layer', [ab.EmbedVariational, ab.Embed])
def test_dense_embeddings(make_categories, reps, layer):
    """Test the embedding layer."""
    x, K = make_categories
    x = np.repeat(x, reps, axis=-1)
    N = len(x)
    S = 3
    x_, X_ = _make_placeholders(x, S, tf.int32)
    output, reg = layer(output_dim=D, n_categories=K)(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        r = reg.eval()

        assert np.isscalar(r)
        assert r >= 0

        Phi = output.eval(feed_dict={x_: x})

        assert Phi.shape == (S, N, D * reps)


@pytest.mark.parametrize('dense', [ab.Dense, ab.DenseVariational])
def test_dense_outputs(dense, make_data):
    """Make sure the dense layers output expected dimensions."""
    x, _, _ = make_data
    S = 3

    x_, X_ = _make_placeholders(x, S)
    N = x.shape[0]

    Phi, KL = dense(output_dim=D)(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        P = Phi.eval(feed_dict={x_: x})
        assert P.shape == (S, N, D)
        assert P.dtype == np.float32
        assert np.isscalar(KL.eval(feed_dict={x_: x}))


@pytest.mark.parametrize('conv2d', [ab.Conv2D, ab.Conv2DVariational])
@pytest.mark.parametrize(
    'kwargs', [
        dict(filters=D, kernel_size=(4, 4)),
        dict(filters=D, kernel_size=(2, 3)),
        dict(filters=D, kernel_size=(4, 4), strides=(5, 2)),
        dict(filters=D, kernel_size=(2, 3), strides=(5, 2)),
        dict(filters=D, kernel_size=(4, 4), padding='VALID'),
        dict(filters=D, kernel_size=(2, 3), padding='VALID'),
        dict(filters=D, kernel_size=(4, 4), strides=(5, 2), padding='VALID'),
        dict(filters=D, kernel_size=(2, 3), strides=(5, 2), padding='VALID')
    ]
)
def test_conv2d_outputs(conv2d, kwargs, make_image_data):
    """Make sure the dense layers output expected dimensions."""
    x, _, X = make_image_data
    S = 3

    x_, X_ = _make_placeholders(x, S)
    N, height, width, channels = x.shape

    Phi, KL = conv2d(**kwargs)(X_)

    if kwargs.get('padding', 'SAME') == 'SAME':
        filter_height = filter_width = 1
    else:
        filter_height, filter_width = kwargs['kernel_size']

    strides = kwargs.get('strides', (1, 1))

    out_height = np.ceil((height - filter_height + 1) / strides[0])
    out_width = np.ceil((width - filter_width + 1) / strides[1])

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        P = Phi.eval(feed_dict={x_: x})
        assert P.shape == (S, N, out_height, out_width, D)
        assert P.dtype == np.float32
        assert np.isscalar(KL.eval(feed_dict={x_: x}))


@pytest.mark.parametrize('layer_args', [
    (SampleLayer, ()),
    (SampleLayer3, ()),
    (ab.Dense, (D,)),
    (ab.DenseVariational, (D,)),
    (ab.EmbedVariational, (2, D)),
    (ab.Conv2D, (8, (4, 4))),
    (ab.Conv2DVariational, (8, (4, 4))),
    (ab.RandomFourier, (2, ab.RBF())),
    (ab.RandomArcCosine, (2,)),
])
def test_sample_layer_input_exception(layer_args, make_data):
    """Make sure sample layers fail when the don't get a rank 3 tensor."""
    x, _, _ = make_data
    layer, args = layer_args
    with pytest.raises(AssertionError):
        layer(*args)(x)


@pytest.mark.parametrize('kernels', [
    (ab.RBF, {}),
    (ab.RBFVariational, {}),
    (ab.Matern, {'p': 1}),
    (ab.Matern, {'p': 2})
])
def test_fourier_features(kernels, make_data):
    """Test random fourier kernels approximations."""
    D = 100
    S = 3
    kern, p = kernels
    k = kern(D, **p)

    x, _, _ = make_data
    x_, X_ = _make_placeholders(x, S)
    N = x.shape[0]

    Phi, KL = ab.RandomFourier(D, k)(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        P = Phi.eval(feed_dict={x_: x})
        for i in range(P.shape[0]):
            p = P[i]
            assert p.shape == (N, 2 * D)
            # Check behaving properly with k(x, x) ~ 1.0
            assert np.allclose((p**2).sum(axis=1), np.ones(N))

        # Make sure we get a valid KL
        kl = KL.eval() if isinstance(KL, tf.Tensor) else KL
        assert kl >= 0


def test_conv2d_distribution(make_image_data):
    """Test initialising dense variational layers with distributions."""
    x, _, X = make_image_data
    S = 3

    x_, X_ = _make_placeholders(x, S)
    N, height, width, channels = x.shape

    Phi, KL = ab.Conv2DVariational(filters=D, kernel_size=(4, 4))(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        P = Phi.eval(feed_dict={x_: x})
        assert P.shape == (S, N, height, width, D)
        assert KL.eval() >= 0.


def test_dense_distribution(make_data):
    """Test initialising dense variational layers with distributions."""
    x, _, _ = make_data
    S = 3

    x_, X_ = _make_placeholders(x, S)
    N = x.shape[0]

    Phi, KL = ab.DenseVariational(output_dim=D)(X_)
    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        P = Phi.eval(feed_dict={x_: x})
        assert P.shape == (S, N, D)
        assert KL.eval() >= 0.


def test_embeddings_distribution(make_categories):
    """Test initialising embedding variational layers with distributions."""
    x, K = make_categories
    N = len(x)
    S = 3
    x_, X_ = _make_placeholders(x, S, tf.int32)
    output, KL = ab.EmbedVariational(output_dim=D, n_categories=K)(X_)

    tc = tf.test.TestCase()
    with tc.test_session():
        tf.global_variables_initializer().run()
        Phi = output.eval(feed_dict={x_: x})
        assert Phi.shape == (S, N, D)
        assert KL.eval() >= 0.


def _make_placeholders(x, S, xtype=tf.float32):
    x_ = tf.placeholder(xtype, x.shape)
    X_ = tf.tile(tf.expand_dims(x_, 0), [S] + np.ones_like(x.shape).tolist())
    return x_, X_
