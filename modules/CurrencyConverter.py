import requests
import numpy as np


class CurrencyConverter:
    def __init__(self):
        pass

    country_currency = {
        "United Arab Emirates": "AED",
        "Afghanistan": "AFN",
        "Albania": "ALL",
        "Armenia": "AMD",
        "Netherlands Antilles": "ANG",
        "Angola": "AOA",
        "Argentina": "ARS",
        "Australia": "AUD",
        "Aruba": "AWG",
        "Azerbaijan": "AZN",
        "Bosnia and Herzegovina": "BAM",
        "Barbados": "BBD",
        "Bangladesh": "BDT",
        "Bulgaria": "BGN",
        "Bahrain": "BHD",
        "Burundi": "BIF",
        "Bermuda": "BMD",
        "Brunei": "BND",
        "Bolivia": "BOB",
        "Brazil": "BRL",
        "Bahamas": "BSD",
        "Bhutan": "BTN",
        "Botswana": "BWP",
        "Belarus": "BYN",
        "Belize": "BZD",
        "Canada": "CAD",
        "Democratic Republic of the Congo": "CDF",
        "Switzerland": "CHF",
        "Chile": "CLP",
        "China": "CNY",
        "Colombia": "COP",
        "Costa Rica": "CRC",
        "Cuba": "CUP",
        "Cape Verde": "CVE",
        "Czech Republic": "CZK",
        "Djibouti": "DJF",
        "Denmark": "DKK",
        "Dominican Republic": "DOP",
        "Algeria": "DZD",
        "Egypt": "EGP",
        "Eritrea": "ERN",
        "Ethiopia": "ETB",
        "European Union": "EUR",
        "Fiji": "FJD",
        "Falkland Islands": "FKP",
        "Faroe Islands": "FOK",
        "United Kingdom": "GBP",
        "Georgia": "GEL",
        "Guernsey": "GGP",
        "Ghana": "GHS",
        "Gibraltar": "GIP",
        "The Gambia": "GMD",
        "Guinea": "GNF",
        "Guatemala": "GTQ",
        "Guyana": "GYD",
        "Hong Kong": "HKD",
        "Honduras": "HNL",
        "Croatia": "HRK",
        "Haiti": "HTG",
        "Hungary": "HUF",
        "Indonesia": "IDR",
        "Israel": "ILS",
        "Isle of Man": "IMP",
        "India": "INR",
        "Iraq": "IQD",
        "Iran": "IRR",
        "Iceland": "ISK",
        "Jersey": "JEP",
        "Jamaica": "JMD",
        "Jordan": "JOD",
        "Japan": "JPY",
        "Kenya": "KES",
        "Kyrgyzstan": "KGS",
        "Cambodia": "KHR",
        "Kiribati": "KID",
        "Comoros": "KMF",
        "South Korea": "KRW",
        "Kuwait": "KWD",
        "Cayman Islands": "KYD",
        "Kazakhstan": "KZT",
        "Laos": "LAK",
        "Lebanon": "LBP",
        "Sri Lanka": "LKR",
        "Liberia": "LRD",
        "Lesotho": "LSL",
        "Libya": "LYD",
        "Morocco": "MAD",
        "Moldova": "MDL",
        "Madagascar": "MGA",
        "North Macedonia": "MKD",
        "Myanmar": "MMK",
        "Mongolia": "MNT",
        "Macau": "MOP",
        "Mauritania": "MRU",
        "Mauritius": "MUR",
        "Maldives": "MVR",
        "Malawi": "MWK",
        "Mexico": "MXN",
        "Malaysia": "MYR",
        "Mozambique": "MZN",
        "Namibia": "NAD",
        "Nigeria": "NGN",
        "Nicaragua": "NIO",
        "Norway": "NOK",
        "Nepal": "NPR",
        "New Zealand": "NZD",
        "Oman": "OMR",
        "Panama": "PAB",
        "Peru": "PEN",
        "Papua New Guinea": "PGK",
        "Philippines": "PHP",
        "Pakistan": "PKR",
        "Poland": "PLN",
        "Paraguay": "PYG",
        "Qatar": "QAR",
        "Romania": "RON",
        "Serbia": "RSD",
        "Russia": "RUB",
        "Rwanda": "RWF",
        "Saudi Arabia": "SAR",
        "Solomon Islands": "SBD",
        "Seychelles": "SCR",
        "Sudan": "SDG",
        "Sweden": "SEK",
        "Singapore": "SGD",
        "Saint Helena": "SHP",
        "Sierra Leone": "SLE",
        "Somalia": "SOS",
        "Suriname": "SRD",
        "South Sudan": "SSP",
        "São Tomé and Príncipe": "STN",
        "Syria": "SYP",
        "Eswatini": "SZL",
        "Thailand": "THB",
        "Tajikistan": "TJS",
        "Turkmenistan": "TMT",
        "Tunisia": "TND",
        "Tonga": "TOP",
        "Turkey": "TRY",
        "Trinidad and Tobago": "TTD",
        "Tuvalu": "TVD",
        "Taiwan": "TWD",
        "Tanzania": "TZS",
        "Ukraine": "UAH",
        "Uganda": "UGX",
        "United States": "USD",
        "Uruguay": "UYU",
        "Uzbekistan": "UZS",
        "Venezuela": "VES",
        "Vietnam": "VND",
        "Vanuatu": "VUV",
        "Samoa": "WST",
        "CEMAC": "XAF",
        "Organisation of Eastern Caribbean States": "XCD",
        "International Monetary Fund": "XDR",
        "CFA": "XOF",
        "Collectivités d'Outre-Mer": "XPF",
        "Yemen": "YER",
        "South Africa": "ZAR",
        "Zambia": "ZMW",
        "Zimbabwe": "ZWL",
    }

    def convert_currency(self, pay_column, to_country):
        currency_symbol = self.country_currency[to_country]

        np_pay_column = np.array(pay_column)

        base_url = "https://v6.exchangerate-api.com/v6/d80999cce6ff3f7b7e4cc7b9/latest/"
        url = f"{base_url}USD"

        try:
            # Send API request
            response = requests.get(url)
            data = response.json()

            # Check if the API call was successful
            if "result" in data:
                exchange_rate = data["conversion_rates"][currency_symbol]
                converted_column = np_pay_column * exchange_rate
                return converted_column, currency_symbol
            else:
                error_message = data["error-type"]
                print(f"An error occurred: {error_message}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")


# Example usage
pay_column = [100, 200, 300, 400, 500]
to_country = "Pakistan"
converter = CurrencyConverter()
converted_column, currency_symbol = converter.convert_currency(pay_column, to_country)
print(converted_column, end=" ")
print(currency_symbol)
