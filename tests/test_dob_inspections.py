from lcd_teams_bot.cards.dob_inspections import (
    dob_inspections_results_card,
    dob_inspections_search_card,
    dob_inspections_start_card,
)
from lcd_teams_bot.services.dob_safety import build_dob_safety_query


def test_dob_start_card_routes_to_choose_action() -> None:
    card = dob_inspections_start_card()

    assert card["actions"][0]["title"] == "Next"
    assert card["actions"][0]["data"] == {"command": "dobinsp.choose"}
    assert card["actions"][1]["data"] == {"command": "dobinsp.cancel"}


def test_address_card_has_expected_required_inputs() -> None:
    card = dob_inspections_search_card("address")
    input_ids = {
        element["id"]
        for element in card["body"]
        if element["type"].startswith("Input.")
    }

    assert {"borough", "house_number", "street_name"} <= input_ids
    assert card["actions"][0]["data"] == {
        "command": "dobinsp.submit",
        "search_type": "address",
    }


def test_address_query_uppercases_street_and_uses_optional_borough() -> None:
    query = build_dob_safety_query(
        "address",
        {"borough": "queens", "house_number": "94-00", "street_name": "Ditmars"},
    )

    assert query == (
        "SELECT * WHERE house_number = '94-00' AND "
        "upper(`street_name`) LIKE '%DITMARS%' AND borough = 'QUEENS'"
    )


def test_device_query_escapes_single_quotes() -> None:
    query = build_dob_safety_query("device", {"device_number": "1p'29384"})

    assert query == "SELECT * WHERE device_number = '1P''29384'"


def test_results_card_formats_dates_and_empty_values() -> None:
    card = dob_inspections_results_card(
        [
            {
                "house_number": "345",
                "street_name": "EAST  101 STREET",
                "borough": "MANHATTAN",
                "device_number": "1P29384",
                ":updated_at": "2026-01-26T21:32:03.312Z",
                "cat1_report_year": "2025",
                "cat1_latest_report_filed": "2025-04-17T00:00:00.000",
                "cat5_latest_report_filed": "",
                "periodic_report_year": "2025",
                "periodic_latest_inspection": "2025-08-14T00:00:00.000",
            }
        ]
    )

    rendered_text = "\n".join(
        element.get("text", "")
        for container in card["body"]
        for element in container.get("items", [container])
    )
    assert "Last Updated: 01/26/2026 21:32:03" in rendered_text
    assert "Last CAT1 Filed:** 04/17/2025" in rendered_text
    assert "Last CAT5 Filed:** N/A" in rendered_text
