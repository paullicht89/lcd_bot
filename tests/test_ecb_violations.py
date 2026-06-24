import pytest

from lcd_teams_bot.cards.ecb_violations import ecb_lookup_results_card, ecb_lookup_search_card
from lcd_teams_bot.services.ecb_violations import build_ecb_violations_query


def test_ecb_lookup_card_has_expected_fields_and_actions() -> None:
    card = ecb_lookup_search_card()
    input_ids = {
        element["id"]
        for element in card["body"]
        if element["type"].startswith("Input.")
    }

    assert {
        "ecb_no",
        "bin",
        "ecb_violation_status",
        "hearing_status",
        "severity",
        "certification_status",
    } <= input_ids
    assert card["actions"][0]["data"] == {"command": "ecblookup.submit"}
    assert card["actions"][1]["data"] == {"command": "ecblookup.cancel"}


def test_ecb_query_uses_elevator_filter_and_selected_fields() -> None:
    query = build_ecb_violations_query(
        {
            "ecb_no": "39029310H",
            "bin": "1012699",
            "ecb_violation_status": "RESOLVE",
        }
    )

    assert query == (
        "SELECT * WHERE violation_type = 'Elevators' AND "
        "ecb_violation_number = '39029310H' AND bin = '1012699' AND "
        "ecb_violation_status = 'RESOLVE'"
    )


def test_ecb_query_expands_class_severity_variants() -> None:
    query = build_ecb_violations_query({"severity": "CLASS-1"})

    assert query == (
        "SELECT * WHERE violation_type = 'Elevators' AND "
        "severity IN ('CLASS-1', 'CLASS - 1')"
    )


def test_ecb_query_requires_at_least_one_user_filter() -> None:
    with pytest.raises(ValueError):
        build_ecb_violations_query({})


def test_ecb_results_card_builds_expected_dob_links() -> None:
    card = ecb_lookup_results_card(
        [
            {
                "ecb_violation_number": "39029310H",
                "ecb_violation_status": "RESOLVE",
                "severity": "CLASS - 1",
            }
        ]
    )

    table = next(element for element in card["body"] if element["type"] == "Table")
    row = table["rows"][1]
    assert row["cells"][3]["items"][0]["actions"][0]["isEnabled"] is False
    assert row["cells"][4]["items"][0]["actions"][0]["url"] == (
        "https://a810-bisweb.nyc.gov/bisweb/"
        "ECBQueryByNumberServlet?requestid=3&ecbin=39029310H"
    )
    assert row["cells"][5]["items"][0]["actions"][0]["url"] == (
        "http://a820-ecbticketfinder.nyc.gov/"
        "GetViolationImage?violationNumber=039029310H"
    )
