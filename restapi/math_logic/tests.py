import pytest
from lalg import (
    Matrix,
    Vec,
    )

class TestVectors:
   
    def test_addition(self):
        """Test if vector addition works."""
        v1 = Vec([2,3,4,5])
        assert v1 + v1 == [4,6,8,10]

    def test_subtraction(self):
        """Test if vector subtraction works."""
        v1 = Vec([2,3,4,5])
        assert v1 - v1 == [0, 0, 0, 0]

    def test_dot_product(self):
        """Test if dot product works."""
        v3 = Vec([-6,8])
        v4 = Vec([5,12])
        assert v3 * v4 == 66

    def test_unit_vector(self):
        """Test if is_unit_vector() works."""
        v2 = Vec([6,8])
        v5 = Vec([1,0,0])
        assert v2.is_unit_vector() == False
        assert v5.is_unit_vector() == True

    def test_multiply_by_scalar(self):
        """Test if multiplying a vector by a scalar works."""
        v1 = Vec([2,3,4,5])
        assert v1 * 3 == [6,9,12,15]

    def test_magnitude(self):
        """Test is magnitude() works."""
        v2 = Vec([6,8])
        assert v2.magnitude() == 10

class TestMatrix:

    def test_addition(self):
        """Test if addition of matrices works."""
        m = Matrix([[2,3,5], [5,6,7]])
        m2 = Matrix([[3,4,5], [5,6,7]])
        assert m + m2 == [[5,7,10], [10,12,14]]

    def test_subtraction(self):
        """Test if subtraction of matrices works."""
        m3 = Matrix([[4,5,6], [5,6,7]])
        m4 = Matrix([[2,3,4], [2,3,4]])
        assert m3 - m4 == [[2,2,2], [3,3,3]]

    def test_by_scalar(self):
        """Test if the multiplication of a matrix by scalar works."""
        m = Matrix([[2,3,5], [5,6,7]])
        assert m * 2 == [[4,6,10], [10,12,14]]

    def test_multiplication(self):
        """Test if multiplication by matrices works."""
        m5 = Matrix([[1,2,3], [4,5,6]])
        m6 = Matrix([[7,8], [9,10], [11,12]])
        assert m5 * m6 == [[58,64], [139, 154]]

    def test_transpose(self):
        """Test if transpose() works."""
        m7 = Matrix([[2,3,4], [5,6,7]])
        assert m7.transpose() == [[2,5], [3,6], [4,7]]
