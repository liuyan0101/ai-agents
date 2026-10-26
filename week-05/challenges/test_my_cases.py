"""My chosen A case: zero and negative values must be counted."""


def test_my_summarize_case(summarize_values):
    values = [0, -2, 0, -2, 5]
    before = values.copy()
    expected = {
        "unique": [0, -2, 5],
        "counts": {0: 2, -2: 2, 5: 1},
        "repeated": {0, -2},
    }
    result = summarize_values(values)
    assert result == expected
    assert values == before
    assert result["unique"] is not values
