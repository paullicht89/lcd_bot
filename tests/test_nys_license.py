import pytest

from lcd_teams_bot.cards.nys_license import (
    nys_business_license_results_card,
    nys_business_license_search_card,
    nys_individual_license_results_card,
    nys_individual_license_search_card,
    nys_license_start_card,
)
from lcd_teams_bot.services.nys_license import (
    build_nys_business_license_query,
    build_nys_individual_license_query,
)


def test_nys_start_card_routes_to_choose_action() -> None:
    card = nys_license_start_card()

    assert card["actions"][0]["title"] == "Next"
    assert card["actions"][0]["data"] == {"command": "nyslic.choose"}
    assert card["actions"][1]["data"] == {"command": "nyslic.cancel"}


def test_individual_card_has_expected_fields_and_submit_action() -> None:
    card = nys_individual_license_search_card()
    input_ids = {
        element["id"]
        for element in card["body"]
        if element["type"].startswith("Input.")
    }

    assert {"license_type", "last_name", "first_name", "license_number"} <= input_ids
    assert card["actions"][0]["data"] == {
        "command": "nyslic.submit",
        "license_kind": "individual",
    }


def test_business_card_has_expected_fields_and_submit_action() -> None:
    card = nys_business_license_search_card()
    input_ids = {
        element["id"]
        for element in card["body"]
        if element["type"].startswith("Input.")
    }

    assert {"license_type", "business_name", "city", "zip_code", "license_number"} <= input_ids
    assert card["actions"][0]["data"] == {
        "command": "nyslic.submit",
        "license_kind": "business",
    }


def test_individual_query_uppercases_names_and_omits_all_license_type() -> None:
    query = build_nys_individual_license_query(
        {
            "license_type": "ALL",
            "last_name": "licht",
            "first_name": "rich",
            "license_number": "23-6LIFR-SHEL",
        }
    )

    assert query == (
        "SELECT * WHERE upper(`last_name`) LIKE '%LICHT%' AND "
        "upper(`first_name`) LIKE '%RICH%' AND "
        "`license_number` = '23-6LIFR-SHEL'"
    )


def test_individual_query_requires_last_name() -> None:
    with pytest.raises(ValueError):
        build_nys_individual_license_query({"first_name": "Richard"})


def test_business_query_uses_selected_fields_and_license_type() -> None:
    query = build_nys_business_license_query(
        {
            "license_type": "Elevator Contractor License (SH131)",
            "business_name": "lcd",
            "city": "mineola",
            "zip_code": "11501",
        }
    )

    assert query == (
        "SELECT * WHERE `license_type` = 'Elevator Contractor License (SH131)' AND "
        "upper(`business_name`) LIKE '%LCD%' AND upper(`city`) LIKE '%MINEOLA%' AND "
        "`zip_code` = '11501'"
    )


def test_business_query_requires_one_filter() -> None:
    with pytest.raises(ValueError):
        build_nys_business_license_query({"license_type": "ALL"})


def test_individual_results_card_formats_dates_and_type_labels() -> None:
    card = nys_individual_license_results_card(
        [
            {
                "license_number": "23-6LIFR-SHEL",
                "license_type": "Elevator Inspector License (SH132)",
                "first_name": "Richard",
                "last_name": "Licht",
                "issued_date": "2023-11-19T00:00:00.000",
                "expiration_date": "2025-12-31T00:00:00.000",
                "license_status": "Expired",
            }
        ]
    )

    row = next(element for element in card["body"] if element["type"] == "Table")["rows"][1]
    texts = [cell["items"][0]["text"] for cell in row["cells"]]
    assert texts == [
        "Richard Licht",
        "23-6LIFR-SHEL",
        "Expired",
        "11/19/2023",
        "12/31/2025",
        "Inspector",
    ]


def test_business_results_card_formats_address_and_type_labels() -> None:
    card = nys_business_license_results_card(
        [
            {
                "license_number": "26-6LIHP-SHEL",
                "license_type": "Elevator Contractor License (SH131)",
                "business_name": "LCD Elevator Repair Inc",
                "address": "224 East 2nd Street",
                "address_2": "Suite 200",
                "city": "Mineola",
                "state": "NY",
                "zip_code": "11501",
                "phone": "5167058817",
                "issued_date": "2026-02-13T00:00:00.000",
                "expiration_date": "2027-12-31T00:00:00.000",
                "license_status": "Active",
            }
        ]
    )

    row = next(element for element in card["body"] if element["type"] == "Table")["rows"][1]
    texts = [cell["items"][0]["text"] for cell in row["cells"]]
    assert texts[-3:] == [
        "Elev. Contractor",
        "5167058817",
        "224 East 2nd Street\nSuite 200\nMineola, NY 11501",
    ]
