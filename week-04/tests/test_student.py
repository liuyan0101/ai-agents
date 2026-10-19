"""Independent expectations for W4 configuration isolation."""
import pytest


@pytest.fixture
def case():
    return {"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}


def test_requested_content(make_variant, case):
    result = make_variant(case, 2031, 1, 3600)
    assert result == {"seed": 2031, "sample_sizes": [240, 3600, 6000, 18000]}


def test_source_preserved(make_variant, case):
    make_variant(case, 2031, 1, 3600)
    assert case == {"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}


def test_both_container_identities(make_variant, case):
    result = make_variant(case, 2031, 1, 3600)
    assert result is not case
    assert result["sample_sizes"] is not case["sample_sizes"]


def test_later_mutations(make_variant, case):
    result = make_variant(case, 2031, 1, 3600)
    result["seed"] = 99
    result["sample_sizes"][0] = 480
    result["sample_sizes"].append(72000)
    assert case == {"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}


def test_two_calls_independent(make_variant, case):
    first = make_variant(case, 2031, 1, 3600)
    second = make_variant(case, 2031, 1, 3600)
    expected = {"seed": 2031, "sample_sizes": [240, 3600, 6000, 18000]}
    assert first == second == expected
    assert first is not second
    assert first["sample_sizes"] is not second["sample_sizes"]
    first["seed"] = 99
    first["sample_sizes"][1] = 7200
    first["sample_sizes"].append(90000)
    assert second == expected
    assert case == {"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}


def test_unchanged_values_still_independent(make_variant, case):
    first = make_variant(case, 17, 1, 1200)
    second = make_variant(case, 17, 1, 1200)
    assert first == second == case
    assert first is not case
    assert second is not case
    assert first is not second
    assert first["sample_sizes"] is not case["sample_sizes"]
    assert second["sample_sizes"] is not case["sample_sizes"]
    assert first["sample_sizes"] is not second["sample_sizes"]
    first["sample_sizes"][1] = 2400
    assert second == {"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}
    assert case == second
