# Japan Economic Indicators API

Real-time Japan economic data including GDP, inflation, unemployment, interest rates, trade balance, industrial production, FDI, and government debt. Powered by World Bank Open Data.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All economic indicators snapshot |
| `GET /gdp` | GDP (current USD) |
| `GET /growth` | GDP growth rate (annual %) |
| `GET /gdp-per-capita` | GDP per capita (current USD) |
| `GET /inflation` | Inflation rate — CPI (annual %) |
| `GET /unemployment` | Unemployment rate |
| `GET /interest-rate` | Lending interest rate |
| `GET /current-account` | Current account balance |
| `GET /trade` | Exports of goods & services (% of GDP) |
| `GET /industrial-production` | Industry value added (% of GDP) |
| `GET /fdi` | Foreign direct investment net inflows |
| `GET /debt` | Central government debt (% of GDP) |

## Query Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `limit` | Number of years to return (1–60) | `10` |

## Data Source

World Bank Open Data
https://data.worldbank.org/country/JP

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
