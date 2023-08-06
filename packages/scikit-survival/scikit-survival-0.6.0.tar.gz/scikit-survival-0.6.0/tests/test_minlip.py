from nose.plugins.attrib import attr
import numpy
from numpy.testing import TestCase, run_module_suite, assert_array_almost_equal, assert_array_equal
from unittest import SkipTest
import warnings

from sklearn.exceptions import ConvergenceWarning
from sklearn.preprocessing import scale

from sksurv.svm.minlip import MinlipSurvivalAnalysis, HingeLossSurvivalSVM
from sksurv.datasets import load_gbsg2
from sksurv.metrics import concordance_index_censored
from sksurv.column import encode_categorical
from sksurv.svm._minlip import create_difference_matrix
from sksurv.util import Surv


def create_toy_data():
    x = numpy.array([[1., 1.],
                     [10.2, 15.],
                     [20., 5.],
                     [40, 30],
                     [45, 21],
                     [50, 36]])

    y = Surv.from_arrays([True, True, False, True, False, False],
                         numpy.arange(1, 7) + 2 ** numpy.arange(1, 7),
                         name_event='status')
    return x, y


class TestDifferenceMatrix(TestCase):
    def setUp(self):
        self.x, self.y = create_toy_data()

    def test_toy_create_difference_matrix_direct_neighbor_without_censoring(self):
        status = numpy.ones(self.y.shape, dtype=bool)
        mat = create_difference_matrix(status.astype(numpy.uint8), self.y["time"], kind="next")

        expected = numpy.zeros((5, 6), dtype=numpy.int8)
        expected[0, 0] = -1
        expected[0, 1] = 1
        expected[1, 1] = -1
        expected[1, 2] = 1
        expected[2, 2] = -1
        expected[2, 3] = 1
        expected[3, 3] = -1
        expected[3, 4] = 1
        expected[4, 4] = -1
        expected[4, 5] = 1

        assert_array_equal(expected, mat.toarray())

        # should return first-order differences of self.y["time"]
        actual_diff = mat.dot(self.y["time"])
        expected_diff = (self.y["time"][1:] - self.y["time"][:-1])

        assert_array_almost_equal(expected_diff, actual_diff)

    def test_toy_create_difference_matrix_direct_neighbor_without_censoring_shuffled(self):
        status = numpy.ones(self.y.shape, dtype=bool)
        order = [3, 2, 5, 0, 1, 4]  # = [ 20.  11.  70.   3.   6.  37.]
        time = self.y["time"][order]
        mat = create_difference_matrix(status.astype(numpy.uint8), time, kind="next")

        expected = numpy.zeros((5, 6), dtype=numpy.int8)
        expected[0, 3] = -1
        expected[0, 4] = 1
        expected[1, 4] = -1
        expected[1, 1] = 1
        expected[2, 1] = -1
        expected[2, 0] = 1
        expected[3, 0] = -1
        expected[3, 5] = 1
        expected[4, 5] = -1
        expected[4, 2] = 1

        assert_array_equal(expected, mat.toarray())

        # should return first-order differences of self.y["time"]
        actual_diff = mat.dot(time)
        expected_diff = (self.y["time"][1:] - self.y["time"][:-1])

        assert_array_almost_equal(expected_diff, actual_diff)

    def test_toy_create_difference_matrix_direct_neighbor_with_censoring(self):
        mat = create_difference_matrix(self.y["status"].astype(numpy.uint8), self.y["time"], kind="next")

        expected = numpy.zeros((3, 6), dtype=numpy.int8)
        expected[0, 0] = -1
        expected[0, 1] = 1
        expected[1, 1] = -1
        expected[1, 2] = 1
        expected[2, 3] = -1
        expected[2, 4] = 1

        assert_array_equal(expected, mat.toarray())

        # should return first-order differences of self.y["time"]
        actual_diff = mat.dot(self.y["time"])
        comparable_pairs = numpy.array([True, True, False, True, False])
        expected_diff = (self.y["time"][1:] - self.y["time"][:-1])[comparable_pairs]

        assert_array_almost_equal(expected_diff, actual_diff)

    def test_toy_create_difference_matrix_nearest_neighbor(self):
        status = numpy.repeat(True, len(self.y))
        mat = create_difference_matrix(status.astype(numpy.uint8), self.y["time"], kind="nearest")

        expected = numpy.zeros((5, 6), dtype=numpy.int8)
        expected[0, 0] = -1
        expected[0, 1] = 1
        expected[1, 1] = -1
        expected[1, 2] = 1
        expected[2, 2] = -1
        expected[2, 3] = 1
        expected[3, 3] = -1
        expected[3, 4] = 1
        expected[4, 4] = -1
        expected[4, 5] = 1

        assert_array_equal(expected, mat.toarray())

    def test_toy_create_difference_matrix_nearest_neighbor_censored(self):
        mat = create_difference_matrix(self.y["status"].astype(numpy.uint8), self.y["time"], kind="nearest")

        expected = numpy.zeros((5, 6), dtype=numpy.int8)
        expected[0, 0] = -1
        expected[0, 1] = 1
        expected[1, 1] = -1
        expected[1, 2] = 1
        expected[2, 1] = -1
        expected[2, 3] = 1
        expected[3, 3] = -1
        expected[3, 4] = 1
        expected[4, 3] = -1
        expected[4, 5] = 1

        assert_array_equal(expected, mat.toarray())

    def test_toy_create_difference_matrix_full(self):
        status = numpy.repeat(True, len(self.y))
        mat = create_difference_matrix(status.astype(numpy.uint8), self.y["time"], kind="all")

        expected = numpy.zeros((15, 6), dtype=numpy.int8)
        expected[0, 1] = 1
        expected[0, 0] = -1

        expected[1:3, 2] = 1
        expected[1, 0] = -1
        expected[2, 1] = -1

        expected[3:6, 3] = 1
        expected[3, 0] = -1
        expected[4, 1] = -1
        expected[5, 2] = -1

        expected[6:10, 4] = 1
        expected[6, 0] = -1
        expected[7, 1] = -1
        expected[8, 2] = -1
        expected[9, 3] = -1

        expected[10:15, 5] = 1
        expected[10, 0] = -1
        expected[11, 1] = -1
        expected[12, 2] = -1
        expected[13, 3] = -1
        expected[14, 4] = -1

        assert_array_equal(expected, mat.toarray())

    def test_toy_create_difference_matrix_full_censored(self):
        mat = create_difference_matrix(self.y["status"].astype(numpy.uint8), self.y["time"], kind="all")

        expected = numpy.zeros((11, 6), dtype=numpy.int8)
        expected[0, 1] = 1
        expected[0, 0] = -1

        expected[1:3, 2] = 1
        expected[1, 0] = -1
        expected[2, 1] = -1

        expected[3:5, 3] = 1
        expected[3, 0] = -1
        expected[4, 1] = -1

        expected[5:8, 4] = 1
        expected[5, 0] = -1
        expected[6, 1] = -1
        expected[7, 3] = -1

        expected[8:12, 5] = 1
        expected[8, 0] = -1
        expected[9, 1] = -1
        expected[10, 3] = -1

        assert_array_equal(expected, mat.toarray())


class TestToyCvxpyExample(TestCase):
    def setUp(self):
        self.x, self.y = create_toy_data()

    @property
    def minlip_model(self):
        return MinlipSurvivalAnalysis(solver="cvxpy", alpha=1, pairs="next")

    @property
    def svm_model(self):
        return HingeLossSurvivalSVM(solver="cvxpy", alpha=1)

    def test_toy_minlip_fit_cvxpy(self):
        m = self.minlip_model
        m.set_params(alpha=2)
        m.fit(self.x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)
        self.assertEqual(1, m.coef0)
        expected_coef = numpy.array([[-7.18695994e-02, 7.18695994e-02, -7.51880574e-13,
                                      -2.14618562e-01, 2.14618562e-01, 0]])
        assert_array_almost_equal(m.coef_, expected_coef)

    def test_toy_minlip_timeit(self):
        m = self.minlip_model
        m.set_params(timeit=7)
        m.fit(self.x, self.y)

        self.assertEqual(7, len(m.timings_))

    def test_toy_minlip_predict_1_cvxpy(self):
        m = self.minlip_model
        m.fit(self.x, self.y)

        p = m.predict(self.x)
        v = concordance_index_censored(self.y['status'], self.y['time'], p)

        self.assertEqual(1.0, v[0])
        self.assertEqual(11, v[1])
        self.assertEqual(0, v[2])
        self.assertEqual(0, v[3])
        self.assertEqual(0, v[4])

    def test_toy_minlip_predict_2_cvxpy(self):
        m = self.minlip_model
        m.set_params(pairs="next")
        y = self.y.copy()
        y["time"] = numpy.arange(1, 7)
        m.fit(self.x, y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.341626, -5.374394]), p)

    def test_toy_hinge_fit(self):
        m = self.svm_model
        m.fit(self.x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(self.x)
        v = concordance_index_censored(self.y['status'], self.y['time'], p)

        self.assertEqual(1.0, v[0])
        self.assertEqual(11, v[1])
        self.assertEqual(0, v[2])
        self.assertEqual(0, v[3])
        self.assertEqual(0, v[4])

    def test_toy_hinge_predict_cvxpy(self):
        m = self.svm_model
        m.fit(self.x, self.y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.34162189, -5.37433203]), p)

    def test_toy_hinge_nearest_fit(self):
        m = self.svm_model
        m.set_params(pairs="nearest")
        m.fit(self.x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(self.x)
        v = concordance_index_censored(self.y['status'], self.y['time'], p)

        self.assertEqual(1.0, v[0])
        self.assertEqual(11, v[1])
        self.assertEqual(0, v[2])
        self.assertEqual(0, v[3])
        self.assertEqual(0, v[4])

    def test_toy_hinge_nearest_predict_cvxpy(self):
        m = self.svm_model
        m.set_params(pairs="nearest")
        m.fit(self.x, self.y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.34161366, -5.37419721]), p)


def skip_without_cvxopt(func):
    def f(*args, **kwargs):
        try:
            import cvxopt
        except ImportError:
            raise SkipTest("cvxopt not installed")
        return func(*args, **kwargs)
    return f


class TestToyCvxoptExample(TestCase):
    def setUp(self):
        self.x, self.y = create_toy_data()

    @property
    @skip_without_cvxopt
    def minlip_model(self):
        return MinlipSurvivalAnalysis(solver="cvxopt", alpha=1, pairs="next", max_iter=1000)

    @property
    @skip_without_cvxopt
    def svm_model(self):
        return HingeLossSurvivalSVM(solver="cvxopt", alpha=1, max_iter=1000)

    def test_toy_minlip_fit_cvxopt(self):
        m = self.minlip_model
        m.fit(self.x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)
        self.assertEqual(1, m.coef0)
        expected_coef = numpy.array([[-7.18695994e-02, 7.18695994e-02, -7.51880574e-13,
                                      -2.14618562e-01, 2.14618562e-01, 0]])
        assert_array_almost_equal(m.coef_, expected_coef)

    def test_toy_minlip_predict_1_cvxopt(self):
        m = self.minlip_model
        m.fit(self.x, self.y)

        p = m.predict(self.x)
        v = concordance_index_censored(self.y['status'], self.y['time'], p)

        self.assertEqual(1.0, v[0])
        self.assertEqual(11, v[1])
        self.assertEqual(0, v[2])
        self.assertEqual(0, v[3])
        self.assertEqual(0, v[4])

    def test_toy_minlip_predict_2_cvxopt(self):
        m = self.minlip_model
        y = self.y.copy()
        y["time"] = numpy.arange(1, 7)
        m.fit(self.x, y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.34162365, -5.37435297]), p)

    def test_toy_hinge_predict_cvxopt(self):
        m = self.svm_model
        m.fit(self.x, self.y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.341622, -5.374336]), p)

    def test_toy_hinge_nearest_predict_cvxopt(self):
        m = self.svm_model
        m.set_params(pairs="nearest")
        m.fit(self.x, self.y)

        p = m.predict(numpy.array([[3, 4], [41, 29]]))
        assert_array_almost_equal(numpy.array([-0.341623, -5.374339]), p)


class TestMinlipCvxpy(TestCase):
    def setUp(self):
        x, y = load_gbsg2()
        self.x = encode_categorical(x)
        self.y = y

    def test_breast_cancer_cvxpy(self):
        m = MinlipSurvivalAnalysis(solver="cvxpy", alpha=1, pairs="next")
        m.fit(self.x.values, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(self.x.values)
        v = concordance_index_censored(self.y['cens'], self.y['time'], p)
        expected = numpy.array([0.59576770470121443, 79280, 53792, 0, 32])

        assert_array_almost_equal(expected, v)

    @attr('slow')
    def test_breast_cancer_rbf_cvxpy(self):
        x = scale(self.x.values)
        m = MinlipSurvivalAnalysis(solver="cvxpy", alpha=1, kernel="rbf",
                                   gamma=32, pairs="next", max_iter=1000)
        m.fit(x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(x)
        v = concordance_index_censored(self.y['cens'], self.y['time'], p)

        self.assertGreaterEqual(v[0], 0.6402849585186966)
        self.assertGreaterEqual(v[1], 85203)
        self.assertLessEqual(v[2], 47869)
        self.assertEqual(0, v[3])
        self.assertEqual(32, v[4])

    def test_unknown_solver(self):
        m = MinlipSurvivalAnalysis(solver=None)
        self.assertRaisesRegex(ValueError, "unknown solver: None",
                               m.fit, self.x.values, self.y)

        m.set_params(solver="i don't know")
        self.assertRaisesRegex(ValueError, "unknown solver: i don't know",
                               m.fit, self.x.values, self.y)

        m.set_params(solver=[('why', 'are'), ('you', 'doing this')])
        self.assertRaisesRegex(ValueError, r"unknown solver: \[\('why', 'are'\), \('you', 'doing this'\)\]",
                               m.fit, self.x.values, self.y)

    @attr('slow')
    def test_kernel_precomputed(self):
        from sklearn.metrics.pairwise import pairwise_kernels
        from sklearn.utils.metaestimators import _safe_split

        m = MinlipSurvivalAnalysis(kernel="precomputed", solver="cvxpy")
        K = pairwise_kernels(self.x, metric="rbf")

        train_idx = numpy.arange(50, self.x.shape[0])
        test_idx = numpy.arange(50)
        X_fit, y_fit = _safe_split(m, K, self.y, train_idx)
        X_test, y_test = _safe_split(m, K, self.y, test_idx, train_idx)

        m.fit(X_fit, y_fit)

        p = m.predict(X_test)
        v = concordance_index_censored(y_test['cens'], y_test['time'], p)

        expected = numpy.array([0.508748, 378, 365, 0, 0])

        assert_array_almost_equal(expected, v)


class TestMinlipCvxopt(TestCase):
    def setUp(self):
        x, y = load_gbsg2()
        self.x = encode_categorical(x)
        self.y = y

    @property
    @skip_without_cvxopt
    def model(self):
        return MinlipSurvivalAnalysis(solver="cvxopt", alpha=1, pairs="next", max_iter=1000)

    def test_breast_cancer_cvxopt(self):
        m = self.model
        m.fit(self.x.values, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(self.x.values)
        v = concordance_index_censored(self.y['cens'], self.y['time'], p)

        expected = numpy.array([0.59570007214139709, 79271, 53801, 0, 32])

        assert_array_almost_equal(expected, v)

    def test_breast_cancer_rbf_cvxopt(self):
        x = scale(self.x.values)
        m = self.model
        m.set_params(kernel="rbf", gamma=32)
        m.fit(x, self.y)

        self.assertTupleEqual((1, self.x.shape[0]), m.coef_.shape)

        p = m.predict(x)
        v = concordance_index_censored(self.y['cens'], self.y['time'], p)

        self.assertAlmostEqual(0.64607505711193935, v[0])
        self.assertEqual(85974, v[1])
        self.assertEqual(47097, v[2])
        self.assertEqual(1, v[3])
        self.assertEqual(32, v[4])

    def test_max_iter(self):
        x = scale(self.x.values)
        m = MinlipSurvivalAnalysis(solver="cvxopt", alpha=1, kernel="polynomial",
                                   degree=2, pairs="next", max_iter=5)
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            m.fit(x, self.y)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, ConvergenceWarning))
            self.assertRegex(str(w[0].message),
                             r"cvxopt solver did not converge: unknown \(duality gap = [.0-9]+\)")


if __name__ == '__main__':
    run_module_suite()
