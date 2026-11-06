import runpy
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.mark.parametrize("primary", [None, "", "   ", "primary-value"])
def test_dataverse_environment_aliases(primary):
    pairs = [
        ("dataverse_url", "DATAVERSE_URL", "DV_BASE_URL"),
        ("dataverse_tenant_id", "DATAVERSE_TENANT_ID", "DV_TENANT_ID"),
        ("dataverse_client_id", "DATAVERSE_CLIENT_ID", "DV_CLIENT_ID"),
        ("dataverse_client_secret", "DATAVERSE_CLIENT_SECRET", "DV_CLIENT_SECRET"),
    ]
    environment = {alias: "alias-value" for _, _, alias in pairs}
    if primary is not None:
        environment.update({name: primary for _, name, _ in pairs})
    path = Path(__file__).resolve().parents[1] / "src/lcd_teams_bot/config.py"
    # Isolate from real environment and .env without reloading the shared settings module.
    with patch.dict("os.environ", environment, clear=True), patch("dotenv.load_dotenv"):
        settings = runpy.run_path(str(path))["settings"]
    for field, _, _ in pairs:
        assert getattr(settings, field) == ("primary-value" if primary == "primary-value" else "alias-value")
