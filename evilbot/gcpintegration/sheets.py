import dataclasses
from typing import Iterator, List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "186sVppwDaVJkH7-Ha8qvKUEUj77LK76n3QJslR6Ipg4"


@dataclasses.dataclass
class Offering:
    commodity: str
    seller: str
    unit_price: int

    def __str__(self) -> str:
        return f"{self.commodity}@{self.unit_price}/u from {self.seller}"


class Ev1lSheetWrapper:
    def __init__(
        self,
        creds: Credentials,
        sheet_id: str,
    ):
        self._creds = creds
        self._service = build("sheets", "v4", credentials=creds)
        self._sheets = self._service.spreadsheets()
        self.sheet_id = sheet_id

    def offerings(self, filter_commodity: str = "") -> Iterator[Offering]:
        results = (
            self._sheets.values()
            # Its not expensive for us to fetch this data, so we filter post API call
            .get(spreadsheetId=self.sheet_id, range="Offerings!A1:G").execute()
        )
        headers: List[str] = results["values"][0]
        mat_index = headers.index("MAT")
        seller_index = headers.index("Seller [Code]")
        unit_price_index = headers.index("Price/u")
        for result in results["values"][1:]:
            offering = Offering(
                commodity=result[mat_index],
                seller=result[seller_index],
                unit_price=result[unit_price_index],
            )
            if filter_commodity and offering.commodity != filter_commodity:
                # If there is a filter and it does not match, skip
                continue

            yield offering


def spreadsheet_api(
    credentials_file: str,
    sheet_id: str,
):
    return Ev1lSheetWrapper(
        creds=Credentials.from_service_account_file(credentials_file), sheet_id=sheet_id
    )
