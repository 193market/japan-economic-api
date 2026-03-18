from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Japan Economic Indicators API",
    description="Real-time Japan economic data including GDP, inflation, unemployment, interest rates, trade balance, and industrial production. Powered by World Bank Open Data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/JP/indicator"

INDICATORS = {
    "gdp":              {"id": "NY.GDP.MKTP.CD",    "name": "GDP",                          "unit": "Current USD"},
    "gdp_growth":       {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP Growth Rate",              "unit": "Annual %"},
    "gdp_per_capita":   {"id": "NY.GDP.PCAP.CD",    "name": "GDP Per Capita",               "unit": "Current USD"},
    "inflation":        {"id": "FP.CPI.TOTL.ZG",   "name": "Inflation (CPI)",              "unit": "Annual %"},
    "unemployment":     {"id": "SL.UEM.TOTL.ZS",   "name": "Unemployment Rate",            "unit": "% of Labor Force"},
    "lending_rate":     {"id": "FR.INR.LEND",       "name": "Lending Interest Rate",        "unit": "%"},
    "current_account":  {"id": "BN.CAB.XOKA.CD",   "name": "Current Account Balance",      "unit": "Current USD"},
    "trade_balance":    {"id": "NE.EXP.GNFS.ZS",   "name": "Exports of Goods & Services",  "unit": "% of GDP"},
    "industrial_prod":  {"id": "NV.IND.TOTL.ZS",   "name": "Industry Value Added",         "unit": "% of GDP"},
    "gni":              {"id": "NY.GNP.MKTP.CD",    "name": "Gross National Income",        "unit": "Current USD"},
    "fdi":              {"id": "BX.KLT.DINV.CD.WD", "name": "FDI Net Inflows",              "unit": "Current USD"},
    "debt":             {"id": "GC.DOD.TOTL.GD.ZS", "name": "Central Government Debt",      "unit": "% of GDP"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {"format": "json", "mrv": limit, "per_page": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url, params=params)
        data = res.json()
    if not data or len(data) < 2:
        return []
    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Japan Economic Indicators API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "World Bank Open Data",
        "country": "Japan (JP)",
        "endpoints": [
            "/summary", "/gdp", "/growth", "/gdp-per-capita",
            "/inflation", "/unemployment", "/interest-rate",
            "/current-account", "/trade", "/industrial-production",
            "/fdi", "/debt"
        ],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=5, ge=1, le=30)):
    """All key Japan economic indicators snapshot"""
    results = {}
    for key, meta in INDICATORS.items():
        results[key] = await fetch_wb(meta["id"], limit)
    formatted = {
        key: {
            "name": INDICATORS[key]["name"],
            "unit": INDICATORS[key]["unit"],
            "data": results[key],
        }
        for key in INDICATORS
    }
    return {
        "country": "Japan",
        "country_code": "JP",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": formatted,
    }


@app.get("/gdp")
async def gdp(limit: int = Query(default=10, ge=1, le=60)):
    """Japan GDP (current USD)"""
    data = await fetch_wb("NY.GDP.MKTP.CD", limit)
    return {
        "indicator": "GDP",
        "series_id": "NY.GDP.MKTP.CD",
        "unit": "Current USD",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/growth")
async def gdp_growth(limit: int = Query(default=10, ge=1, le=60)):
    """Japan GDP growth rate (annual %)"""
    data = await fetch_wb("NY.GDP.MKTP.KD.ZG", limit)
    return {
        "indicator": "GDP Growth Rate",
        "series_id": "NY.GDP.MKTP.KD.ZG",
        "unit": "Annual %",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/gdp-per-capita")
async def gdp_per_capita(limit: int = Query(default=10, ge=1, le=60)):
    """Japan GDP per capita (current USD)"""
    data = await fetch_wb("NY.GDP.PCAP.CD", limit)
    return {
        "indicator": "GDP Per Capita",
        "series_id": "NY.GDP.PCAP.CD",
        "unit": "Current USD",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/inflation")
async def inflation(limit: int = Query(default=10, ge=1, le=60)):
    """Japan inflation rate — Consumer Price Index (annual %)"""
    data = await fetch_wb("FP.CPI.TOTL.ZG", limit)
    return {
        "indicator": "Inflation, Consumer Prices",
        "series_id": "FP.CPI.TOTL.ZG",
        "unit": "Annual %",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/unemployment")
async def unemployment(limit: int = Query(default=10, ge=1, le=60)):
    """Japan unemployment rate (% of labor force)"""
    data = await fetch_wb("SL.UEM.TOTL.ZS", limit)
    return {
        "indicator": "Unemployment Rate",
        "series_id": "SL.UEM.TOTL.ZS",
        "unit": "% of Labor Force",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/interest-rate")
async def interest_rate(limit: int = Query(default=10, ge=1, le=60)):
    """Japan lending interest rate (%)"""
    data = await fetch_wb("FR.INR.LEND", limit)
    return {
        "indicator": "Lending Interest Rate",
        "series_id": "FR.INR.LEND",
        "unit": "%",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/current-account")
async def current_account(limit: int = Query(default=10, ge=1, le=60)):
    """Japan current account balance (BoP, current USD)"""
    data = await fetch_wb("BN.CAB.XOKA.CD", limit)
    return {
        "indicator": "Current Account Balance",
        "series_id": "BN.CAB.XOKA.CD",
        "unit": "Current USD (Balance of Payments)",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/trade")
async def trade(limit: int = Query(default=10, ge=1, le=60)):
    """Japan exports of goods and services (% of GDP)"""
    data = await fetch_wb("NE.EXP.GNFS.ZS", limit)
    return {
        "indicator": "Exports of Goods & Services",
        "series_id": "NE.EXP.GNFS.ZS",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/industrial-production")
async def industrial_production(limit: int = Query(default=10, ge=1, le=60)):
    """Japan industry value added (% of GDP)"""
    data = await fetch_wb("NV.IND.TOTL.ZS", limit)
    return {
        "indicator": "Industry Value Added",
        "series_id": "NV.IND.TOTL.ZS",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/fdi")
async def fdi(limit: int = Query(default=10, ge=1, le=60)):
    """Japan foreign direct investment net inflows (current USD)"""
    data = await fetch_wb("BX.KLT.DINV.CD.WD", limit)
    return {
        "indicator": "FDI Net Inflows",
        "series_id": "BX.KLT.DINV.CD.WD",
        "unit": "Current USD",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }


@app.get("/debt")
async def debt(limit: int = Query(default=10, ge=1, le=60)):
    """Japan central government debt (% of GDP)"""
    data = await fetch_wb("GC.DOD.TOTL.GD.ZS", limit)
    return {
        "indicator": "Central Government Debt",
        "series_id": "GC.DOD.TOTL.GD.ZS",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
