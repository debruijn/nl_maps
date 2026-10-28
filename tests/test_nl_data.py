import pytest

from nl_maps import NLData


PROVINCES = {
    "zuid-holland",
    "noord-holland",
    "utrecht",
    "zeeland",
    "noord-brabant",
    "limburg",
    "gelderland",
    "flevoland",
    "overijssel",
    "drenthe",
    "friesland",
    "groningen",
}
BES_ISLANDS = {"bonaire", "saba", "statia"}
NOT_APPLICABLE_COLOR = [127, 127, 127, 255]


def test_provinces_and_bes_initialize_as_not_applicable():
    data = NLData(kind="provinces")

    assert set(data.mapping) == PROVINCES | BES_ISLANDS
    assert set(data.mapping.values()) == {"N/A"}
    assert data.color_mapping["N/A"] == NOT_APPLICABLE_COLOR


def test_bes_can_be_excluded():
    data = NLData(kind="provinces", include_bes=False)

    assert set(data.mapping) == PROVINCES
    assert data.mapping["friesland"] == "N/A"


def test_municipality_map_kind_fails_explicitly():
    with pytest.raises(
        NotImplementedError,
        match="Municipality-level map generation is not implemented",
    ):
        NLData(kind="municipalities")


def test_none_kind_preserves_bes_only_data_for_existing_map_workflow():
    data = NLData(kind="none")

    assert set(data.mapping) == BES_ISLANDS
    assert set(data.mapping.values()) == {"N/A"}


def test_unknown_map_kind_fails_with_value_error():
    with pytest.raises(ValueError, match="kind must be 'provinces' or 'none'"):
        NLData(kind="counties")


def test_update_normalizes_region_aliases_and_case():
    data = NLData(kind="provinces")

    data.update(
        {
            "ZH": "Party A",
            "UT": "Party B",
            "BO": "Party A",
            "St Eustatius": "Party C",
        }
    )

    assert data.mapping["zuid-holland"] == "Party A"
    assert data.mapping["utrecht"] == "Party B"
    assert data.mapping["bonaire"] == "Party A"
    assert data.mapping["statia"] == "Party C"


def test_other_category_fills_regions_not_explicitly_updated():
    data = NLData(kind="provinces")

    data.update({"FR": "Party A", "other": "Other"})

    assert data.mapping["friesland"] == "Party A"
    assert all(
        value == ("Party A" if region == "friesland" else "Other")
        for region, value in data.mapping.items()
    )


def test_get_categories_returns_category_to_color_mapping():
    data = NLData(kind="provinces", include_bes=False)
    custom_color = [12, 34, 56, 255]
    data.update({"FR": "holiday", "UT": "work"})
    data.set_colors({"holiday": custom_color})

    categories = data.get_categories()

    assert set(categories) == {"N/A", "holiday", "work"}
    assert categories["N/A"] == NOT_APPLICABLE_COLOR
    assert categories["holiday"] == custom_color
    assert len(categories["work"]) == 4


@pytest.mark.parametrize("region", ["Atlantis", "Adam"])
def test_update_rejects_unknown_or_unsupported_regions(region):
    data = NLData(kind="provinces")
    original_mapping = data.mapping.copy()
    original_colors = dict(data.color_mapping)

    with pytest.raises(ValueError, match=f"Unknown or unsupported region '{region}'"):
        data.update({region: "Party"})

    assert data.mapping == original_mapping
    assert dict(data.color_mapping) == original_colors


def test_update_with_invalid_region_does_not_partially_apply_valid_regions():
    data = NLData(kind="provinces")
    original_mapping = data.mapping.copy()
    original_colors = dict(data.color_mapping)

    with pytest.raises(ValueError, match="Unknown or unsupported region 'Atlantis'"):
        data.update({"FR": "Holiday", "Atlantis": "Party"})

    assert data.mapping == original_mapping
    assert dict(data.color_mapping) == original_colors
