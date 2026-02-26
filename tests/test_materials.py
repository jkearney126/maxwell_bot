"""Tests for material property lookups."""

import pytest
from mcp_server.tools import materials


class TestMaterialLookup:
    """Tests for material property lookups."""

    def test_lookup_iron(self):
        """Test lookup of iron properties."""
        result = materials.lookup_material("iron")
        assert "relative_permeability" in result
        assert result["relative_permeability"] == 5000.0
        assert result["saturation_flux_density_T"] == 2.15

    def test_lookup_silicon_steel(self):
        """Test lookup of silicon steel properties."""
        result = materials.lookup_material("silicon_steel")
        assert result["relative_permeability"] == 4000.0

    def test_lookup_ferrite(self):
        """Test lookup of ferrite properties."""
        result = materials.lookup_material("ferrite")
        assert result["relative_permeability"] == 2000.0

    def test_lookup_neodymium(self):
        """Test lookup of neodymium magnet properties."""
        result = materials.lookup_material("neodymium")
        assert result["relative_permeability"] == 1.05
        assert result["coercivity_A_per_m"] == 955000.0

    def test_lookup_mu_metal(self):
        """Test lookup of mu-metal properties."""
        result = materials.lookup_material("mu_metal")
        assert result["relative_permeability"] == 80000.0

    def test_lookup_air(self):
        """Test lookup of air properties."""
        result = materials.lookup_material("air")
        assert result["relative_permeability"] == 1.0
        assert result["coercivity_A_per_m"] == 0.0

    def test_lookup_case_insensitive(self):
        """Test that lookup is case-insensitive."""
        result1 = materials.lookup_material("IRON")
        result2 = materials.lookup_material("Iron")
        result3 = materials.lookup_material("iron")
        assert result1 == result2 == result3

    def test_lookup_invalid_material(self):
        """Test lookup of non-existent material."""
        result = materials.lookup_material("copper")
        assert "error" in result
        assert "available_materials" in result

    def test_lookup_all_materials(self):
        """Test that all expected materials are available."""
        expected_materials = [
            "air", "iron", "silicon_steel", "ferrite", "neodymium", "mu_metal"
        ]
        for mat in expected_materials:
            result = materials.lookup_material(mat)
            assert "error" not in result
