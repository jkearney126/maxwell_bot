"""Tests for magnetic field calculations."""

import pytest
import math
from mcp_server.tools import fields


class TestSolenoidField:
    """Tests for solenoid field calculation."""

    def test_solenoid_field_basic(self):
        """Test basic solenoid field calculation."""
        result = fields.solenoid_field(turns=500, length_m=0.2, current_A=2.0)
        assert "B_tesla" in result
        # B = μ₀ · (N/L) · I = 4π×10⁻⁷ · (500/0.2) · 2
        expected = 4 * math.pi * 1e-7 * (500 / 0.2) * 2
        assert abs(result["B_tesla"] - expected) < 1e-10

    def test_solenoid_field_zero_current(self):
        """Test solenoid with zero current."""
        result = fields.solenoid_field(turns=100, length_m=0.1, current_A=0)
        assert result["B_tesla"] == 0

    def test_solenoid_field_invalid_length(self):
        """Test solenoid with invalid length."""
        result = fields.solenoid_field(turns=100, length_m=0, current_A=2)
        assert "error" in result

    def test_solenoid_field_negative_turns(self):
        """Test solenoid with negative turns."""
        result = fields.solenoid_field(turns=-100, length_m=0.1, current_A=2)
        assert "error" in result


class TestBiotSavartWire:
    """Tests for Biot-Savart wire field calculation."""

    def test_biot_savart_basic(self):
        """Test basic wire field calculation."""
        result = fields.biot_savart_wire(current_A=10.0, distance_m=0.1)
        assert "B_tesla" in result
        # B = μ₀ · I / (2π · r)
        expected = 4 * math.pi * 1e-7 * 10.0 / (2 * math.pi * 0.1)
        assert abs(result["B_tesla"] - expected) < 1e-10

    def test_biot_savart_zero_current(self):
        """Test wire with zero current."""
        result = fields.biot_savart_wire(current_A=0, distance_m=0.1)
        assert result["B_tesla"] == 0

    def test_biot_savart_invalid_distance(self):
        """Test wire with invalid distance."""
        result = fields.biot_savart_wire(current_A=10, distance_m=0)
        assert "error" in result


class TestMagneticFlux:
    """Tests for magnetic flux calculation."""

    def test_magnetic_flux_perpendicular(self):
        """Test flux with perpendicular field."""
        result = fields.magnetic_flux(B_tesla=0.1, area_m2=0.01, angle_deg=0)
        assert "flux_Wb" in result
        assert result["flux_Wb"] == 0.001  # 0.1 * 0.01 * cos(0)

    def test_magnetic_flux_parallel(self):
        """Test flux with parallel field (90 degrees)."""
        result = fields.magnetic_flux(B_tesla=0.1, area_m2=0.01, angle_deg=90)
        assert abs(result["flux_Wb"]) < 1e-10  # cos(90) = 0

    def test_magnetic_flux_45_degrees(self):
        """Test flux at 45 degrees."""
        result = fields.magnetic_flux(B_tesla=0.1, area_m2=0.01, angle_deg=45)
        expected = 0.1 * 0.01 * math.cos(math.radians(45))
        assert abs(result["flux_Wb"] - expected) < 1e-10

    def test_magnetic_flux_invalid_area(self):
        """Test flux with negative area."""
        result = fields.magnetic_flux(B_tesla=0.1, area_m2=-0.01)
        assert "error" in result


class TestEnergyStored:
    """Tests for magnetic energy storage."""

    def test_energy_stored_basic(self):
        """Test basic energy calculation."""
        result = fields.energy_stored(B_tesla=0.05, volume_m3=0.0005)
        assert "energy_J" in result
        # W = (B² / (2μ₀)) · V
        expected = (0.05 ** 2 / (2 * 4 * math.pi * 1e-7)) * 0.0005
        assert abs(result["energy_J"] - expected) < 1e-10

    def test_energy_stored_zero_field(self):
        """Test energy with zero field."""
        result = fields.energy_stored(B_tesla=0, volume_m3=0.0005)
        assert result["energy_J"] == 0

    def test_energy_stored_zero_volume(self):
        """Test energy with zero volume."""
        result = fields.energy_stored(B_tesla=0.05, volume_m3=0)
        assert result["energy_J"] == 0

    def test_energy_stored_invalid_volume(self):
        """Test energy with negative volume."""
        result = fields.energy_stored(B_tesla=0.05, volume_m3=-0.0005)
        assert "error" in result
