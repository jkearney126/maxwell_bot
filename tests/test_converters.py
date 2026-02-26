"""Tests for unit conversions."""

import pytest
import math
from mcp_server.tools import converters


class TestTeslaGaussConversion:
    """Tests for Tesla to Gauss conversions."""

    def test_tesla_to_gauss(self):
        """Test Tesla to Gauss conversion."""
        result = converters.convert_unit(1.0, "T", "Gauss")
        assert result["converted_value"] == 10000

    def test_gauss_to_tesla(self):
        """Test Gauss to Tesla conversion."""
        result = converters.convert_unit(10000, "Gauss", "T")
        assert abs(result["converted_value"] - 1.0) < 1e-10

    def test_tesla_to_gauss_fractional(self):
        """Test fractional Tesla to Gauss."""
        result = converters.convert_unit(0.05, "T", "Gauss")
        assert result["converted_value"] == 500


class TestWeberMaxwellConversion:
    """Tests for Weber to Maxwell conversions."""

    def test_weber_to_maxwell(self):
        """Test Weber to Maxwell conversion."""
        result = converters.convert_unit(1.0, "Wb", "Maxwell")
        assert result["converted_value"] == 1e8

    def test_maxwell_to_weber(self):
        """Test Maxwell to Weber conversion."""
        result = converters.convert_unit(1e8, "Maxwell", "Wb")
        assert abs(result["converted_value"] - 1.0) < 1e-10


class TestAmpereMetrOerstedConversion:
    """Tests for A/m to Oersted conversions."""

    def test_a_per_m_to_oersted(self):
        """Test A/m to Oersted conversion."""
        result = converters.convert_unit(1000, "A/m", "Oersted")
        expected = 1000 / 79.577
        assert abs(result["converted_value"] - expected) < 0.1

    def test_oersted_to_a_per_m(self):
        """Test Oersted to A/m conversion."""
        result = converters.convert_unit(10, "Oersted", "A/m")
        expected = 10 * 79.577
        assert abs(result["converted_value"] - expected) < 0.1


class TestInductanceConversion:
    """Tests for Henries to mH to uH conversions."""

    def test_h_to_mh(self):
        """Test Henry to milliHenry conversion."""
        result = converters.convert_unit(1.0, "H", "mH")
        assert result["converted_value"] == 1000

    def test_mh_to_h(self):
        """Test milliHenry to Henry conversion."""
        result = converters.convert_unit(1000, "mH", "H")
        assert abs(result["converted_value"] - 1.0) < 1e-10

    def test_h_to_uh(self):
        """Test Henry to microHenry conversion."""
        result = converters.convert_unit(1.0, "H", "uH")
        assert result["converted_value"] == 1e6

    def test_uh_to_h(self):
        """Test microHenry to Henry conversion."""
        result = converters.convert_unit(1e6, "uH", "H")
        assert abs(result["converted_value"] - 1.0) < 1e-10

    def test_mh_to_uh(self):
        """Test milliHenry to microHenry conversion."""
        result = converters.convert_unit(1.0, "mH", "uH")
        assert result["converted_value"] == 1000


class TestSameUnitConversion:
    """Tests for same unit conversions."""

    def test_same_unit(self):
        """Test conversion between same units."""
        result = converters.convert_unit(5.0, "T", "T")
        assert result["converted_value"] == 5.0
        assert "message" in result


class TestInvalidConversion:
    """Tests for invalid conversions."""

    def test_unsupported_conversion(self):
        """Test unsupported conversion."""
        result = converters.convert_unit(1.0, "T", "Kelvin")
        assert "error" in result
        assert "supported_units" in result

    def test_invalid_units(self):
        """Test conversion with non-existent units."""
        result = converters.convert_unit(1.0, "NotAUnit", "AlsoNotAUnit")
        assert "error" in result
