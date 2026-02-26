"""Tests for magnetic circuit calculations."""

import pytest
import math
from mcp_server.tools import circuits


class TestReluctance:
    """Tests for reluctance calculation."""

    def test_reluctance_iron_core(self):
        """Test reluctance of an iron core."""
        result = circuits.reluctance(
            length_m=0.1,
            area_m2=0.0002,
            relative_permeability=5000
        )
        assert "reluctance_H_inv" in result
        # R = l / (μ₀ · μᵣ · A)
        mu_0 = 4 * math.pi * 1e-7
        expected = 0.1 / (mu_0 * 5000 * 0.0002)
        assert abs(result["reluctance_H_inv"] - expected) < 1e-4

    def test_reluctance_air_path(self):
        """Test reluctance of an air path (μᵣ = 1)."""
        result = circuits.reluctance(
            length_m=0.01,
            area_m2=0.0001,
            relative_permeability=1
        )
        assert "reluctance_H_inv" in result
        mu_0 = 4 * math.pi * 1e-7
        expected = 0.01 / (mu_0 * 0.0001)
        assert abs(result["reluctance_H_inv"] - expected) < 1e-1

    def test_reluctance_invalid_length(self):
        """Test reluctance with zero length."""
        result = circuits.reluctance(
            length_m=0,
            area_m2=0.0001,
            relative_permeability=1000
        )
        assert "error" in result

    def test_reluctance_invalid_area(self):
        """Test reluctance with zero area."""
        result = circuits.reluctance(
            length_m=0.1,
            area_m2=0,
            relative_permeability=1000
        )
        assert "error" in result

    def test_reluctance_invalid_permeability(self):
        """Test reluctance with zero permeability."""
        result = circuits.reluctance(
            length_m=0.1,
            area_m2=0.0001,
            relative_permeability=0
        )
        assert "error" in result


class TestMMFRequired:
    """Tests for magnetomotive force calculation."""

    def test_mmf_basic(self):
        """Test basic MMF calculation."""
        result = circuits.mmf_required(H_field=1000, path_length_m=0.1)
        assert "mmf_AT" in result
        assert result["mmf_AT"] == 100  # 1000 * 0.1

    def test_mmf_zero_field(self):
        """Test MMF with zero field."""
        result = circuits.mmf_required(H_field=0, path_length_m=0.1)
        assert result["mmf_AT"] == 0

    def test_mmf_zero_length(self):
        """Test MMF with zero length."""
        result = circuits.mmf_required(H_field=1000, path_length_m=0)
        assert result["mmf_AT"] == 0

    def test_mmf_invalid_length(self):
        """Test MMF with negative length."""
        result = circuits.mmf_required(H_field=1000, path_length_m=-0.1)
        assert "error" in result

    def test_mmf_large_values(self):
        """Test MMF with large values."""
        result = circuits.mmf_required(H_field=955000, path_length_m=0.05)
        assert result["mmf_AT"] == 47750
