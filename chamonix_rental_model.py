import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Chamonix Valley · Rental Income Model",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Alpine-luxury aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* Main background */
.stApp { background-color: #F4F1EC; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1C2B3A !important;
}
section[data-testid="stSidebar"] * {
    color: #E8E0D5 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label {
    color: #B8A99A !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E0D9D0;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(28,43,58,0.06);
}

/* Section headers */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #1C2B3A;
    border-bottom: 2px solid #C8A87A;
    padding-bottom: 0.4rem;
    margin: 2rem 0 1rem;
}

.warning-box {
    background: #FDF3E7;
    border-left: 4px solid #C8A87A;
    border-radius: 4px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #5A4A3A;
    margin: 0.5rem 0;
}

.info-box {
    background: #EEF3F8;
    border-left: 4px solid #2E6DA4;
    border-radius: 4px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #1C2B3A;
    margin: 0.5rem 0;
}

.regime-badge {
    display: inline-block;
    background: #1C2B3A;
    color: #C8A87A;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.04em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #C8A87A;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #5A4A3A;
    padding: 0.6rem 1.4rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #1C2B3A !important;
    border-bottom-color: #C8A87A !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="background:#1C2B3A;padding:2rem 2.5rem 1.5rem;border-radius:12px;margin-bottom:1.5rem;">
  <div style="display:flex;align-items:center;gap:1rem;">
    <div style="font-size:2.5rem;">🏔️</div>
    <div>
      <h1 style="color:#E8E0D5;margin:0;font-size:1.8rem;">Chamonix Valley · Rental Income Analyser</h1>
      <p style="color:#B8A99A;margin:0.2rem 0 0;font-size:0.88rem;">
        Fiscal modelling for non-resident EU owners · 2025 Le Meur Law · Haute-Savoie (74)
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# REGULATORY NOTICE
# ─────────────────────────────────────────────
with st.expander("⚖️ Regulatory Context (2024–2025 Legislative Changes)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Loi Le Meur (19 Nov 2024)**
- Micro-BIC allowance for *non-classified* STR: 50% → **30%**, capped at €15,000 gross  
- Micro-BIC for *classified* meublé de tourisme: remains **50%**, capped at €77,700  
- Municipalities can cut primary-residence cap from 120 → **90 days/year**  
- DPE (Energy cert) mandatory: **E or better** from 2025, F from 2028, D from 2034  
- Co-ownership rules tightened; 2/3 majority now sufficient to ban STR in a copropriété

**Chamonix PLU & Commune Rules (May 2025)**
- Les Houches & Chamonix: **max 1 STR per private owner**, 3-year renewal  
- Servoz: max 2 properties; Vallorcine: no limit, 1-year renewal  
- Company-held multi-properties restricted from **May 2026**  
- Registration with commune mandatory before listing
        """)
    with col2:
        st.markdown("""
**Non-Resident Taxation — EU Resident (Italy)**
- Income Tax: minimum **20%** (on taxable base); 30% above €29,315  
- Solidarity levy: **7.5%** (EU/EEA residents affiliated to home country social security)  
- CSG/CRDS: **not applicable** to EU-affiliated non-residents (De Ruyter ruling)  
- Effective combined rate: **27.5%** (20% IT + 7.5% solidarity levy)  
- Must file annual *Déclaration des Revenus* in France  
- Double-tax treaty France–Italy: French tax creditable against Italian liability

**BIC Regimes for Furnished Short-Term (LMNP)**
| Regime | Allowance | Threshold |
|--------|-----------|-----------|
| Micro-BIC (unclassified) | 30% | ≤ €15,000 gross |
| Micro-BIC (classified MTI) | 50% | ≤ €77,700 gross |
| Régime Réel | Actual costs | Any level |

*Taxe foncière, tourist tax (taxe de séjour), and SIRET registration required.*
        """)

# ─────────────────────────────────────────────
# SIDEBAR — PROPERTY INPUTS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 Property 1 — Les Houches")
    st.caption("90m² apt · sleeps 9 · off-street parking · Bellvue lift")

    p1_value = st.number_input("Estimated property value (€)", 900_000, 3_000_000, 1_350_000, 50_000, key="p1v")
    p1_nightly = st.number_input("Nightly rate STR (€)", 100, 2000, 350, 10, key="p1n")
    p1_occ_weeks = st.slider("Occupied weeks / year (STR)", 1, 52, 6, 1, key="p1w")
    p1_classified = st.toggle("Classified 'Meublé de Tourisme'?", value=False, key="p1c",
                               help="Classification gives 50% micro-BIC vs 30%; must apply to Atout France")
    p1_regime = st.selectbox("Tax regime", ["Micro-BIC (auto)", "Régime Réel (actual costs)"], key="p1r")

    st.markdown("---")
    st.markdown("### 🏠 Property 2")
    p2_label = st.text_input("Property nickname", "Chamonix Town Apt", key="p2l")
    p2_value = st.number_input("Estimated property value (€)", 400_000, 3_000_000, 950_000, 50_000, key="p2v")
    p2_size = st.number_input("Size (m²)", 20, 300, 65, 5, key="p2s")
    p2_sleeps = st.number_input("Sleeps", 1, 20, 6, 1, key="p2sl")
    p2_mode = st.selectbox(
        "Rental mode",
        ["Short-term (STR)", "Long-term unfurnished (bail nu)", "Long-term furnished (bail meublé)"],
        key="p2mode"
    )
    if p2_mode == "Short-term (STR)":
        p2_nightly = st.number_input("Nightly rate STR (€)", 100, 2000, 280, 10, key="p2n")
        p2_occ_weeks = st.slider("Occupied weeks / year", 1, 52, 8, 1, key="p2w")
        p2_classified = st.toggle("Classified 'Meublé de Tourisme'?", value=False, key="p2c")
    else:
        p2_monthly = st.number_input("Monthly rent (€)", 500, 8000, 2_200, 50, key="p2m",
                                      help="Chamonix avg ~€30/m²/month; market rate for LT")
        p2_void_months = st.slider("Void months / year", 0, 4, 1, 1, key="p2void")
    p2_regime = st.selectbox("Tax regime P2", ["Micro-BIC (auto)", "Régime Réel (actual costs)",
                                                "Micro-foncier (unfurnished)", "Régime Réel foncier"], key="p2r")

    st.markdown("---")
    st.markdown("### ⚙️ Shared Cost Assumptions")
    mgmt_fee_pct = st.slider("Management fee (%)", 0, 25, 10, 1,
                              help="Applied to gross rental revenue")
    mgmt_exp_pct = st.slider("Other variable operating costs (%)", 0, 30, 15, 1,
                               help="Includes cleaning, linen, consumables, platform fees, insurance top-up etc.")
    taxe_fonciere_p1 = st.number_input("Taxe Foncière P1 (€/yr)", 0, 10000, 2_800, 100)
    taxe_fonciere_p2 = st.number_input("Taxe Foncière P2 (€/yr)", 0, 10000, 1_800, 100)
    tourist_tax_pppn = st.number_input("Taxe de séjour (€/person/night)", 0.5, 5.0, 1.5, 0.1,
                                        help="Collected from guests; not revenue to owner but admin obligation")

    st.markdown("---")
    st.markdown("### 📊 Scenario")
    sensitivity_mode = st.toggle("Run sensitivity analysis", value=False)

# ─────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────

def calc_str(nightly, occ_weeks, classified, regime_choice, value,
             mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere, sleeps=9,
             tourist_tax_pppn=1.5):
    nights = occ_weeks * 7
    gross_revenue = nightly * nights
    # Tourist tax collected from guests — pass-through, not owner income
    tourist_tax_collected = tourist_tax_pppn * sleeps * nights  # worst-case (all beds)

    mgmt_fee = gross_revenue * mgmt_fee_pct / 100
    op_costs = gross_revenue * mgmt_exp_pct / 100
    total_direct_costs = mgmt_fee + op_costs

    net_before_tax = gross_revenue - total_direct_costs - taxe_fonciere

    # BIC regime selection
    if "Micro-BIC" in regime_choice or regime_choice == "Micro-BIC (auto)":
        if classified:
            allowance_pct = 50
            ceiling = 77_700
        else:
            allowance_pct = 30
            ceiling = 15_000

        if gross_revenue <= ceiling:
            taxable_income = gross_revenue * (1 - allowance_pct / 100)
        else:
            # Must use régime réel if above ceiling
            taxable_income = max(0, net_before_tax)
            regime_choice = "Régime Réel (actual costs)"
    else:
        # Régime réel — deduct actual expenses
        taxable_income = max(0, net_before_tax)

    # Tax: EU resident, Italy → 20% IT + 7.5% solidarity
    income_tax = taxable_income * 0.20
    solidarity = taxable_income * 0.075
    total_tax = income_tax + solidarity

    net_income = net_before_tax - total_tax

    yield_gross = gross_revenue / value * 100 if value else 0
    yield_net = net_income / value * 100 if value else 0

    return {
        "gross_revenue": gross_revenue,
        "mgmt_fee": mgmt_fee,
        "op_costs": op_costs,
        "taxe_fonciere": taxe_fonciere,
        "total_direct_costs": total_direct_costs + taxe_fonciere,
        "net_before_tax": net_before_tax,
        "taxable_income": taxable_income,
        "income_tax": income_tax,
        "solidarity": solidarity,
        "total_tax": total_tax,
        "net_income": net_income,
        "yield_gross": yield_gross,
        "yield_net": yield_net,
        "nights": nights,
        "tourist_tax_collected": tourist_tax_collected,
        "allowance_pct": allowance_pct if "Micro-BIC" in regime_choice else None,
    }


def calc_lt(monthly_rent, void_months, regime_choice, value, taxe_fonciere, mgmt_fee_pct, mgmt_exp_pct, furnished=False):
    occupied_months = 12 - void_months
    gross_revenue = monthly_rent * occupied_months
    mgmt_fee = gross_revenue * mgmt_fee_pct / 100
    op_costs = gross_revenue * mgmt_exp_pct / 100 * 0.3  # much lower for LT (no linen/clean/platform)

    total_direct_costs = mgmt_fee + op_costs
    net_before_tax = gross_revenue - total_direct_costs - taxe_fonciere

    if furnished:
        # Micro-BIC 50% (furnished LT, meublé bail)
        if "Micro-BIC" in regime_choice or "Micro" in regime_choice:
            taxable_income = max(0, gross_revenue * 0.50)
        else:
            taxable_income = max(0, net_before_tax)
    else:
        # Revenu foncier — Micro-foncier 30% if < €15k
        if gross_revenue < 15_000 and ("Micro" in regime_choice or "foncier" in regime_choice):
            taxable_income = max(0, gross_revenue * 0.70)
        else:
            taxable_income = max(0, net_before_tax)

    income_tax = taxable_income * 0.20
    solidarity = taxable_income * 0.075
    total_tax = income_tax + solidarity

    net_income = net_before_tax - total_tax
    yield_gross = gross_revenue / value * 100 if value else 0
    yield_net = net_income / value * 100 if value else 0

    return {
        "gross_revenue": gross_revenue,
        "mgmt_fee": mgmt_fee,
        "op_costs": op_costs,
        "taxe_fonciere": taxe_fonciere,
        "total_direct_costs": total_direct_costs + taxe_fonciere,
        "net_before_tax": net_before_tax,
        "taxable_income": taxable_income,
        "income_tax": income_tax,
        "solidarity": solidarity,
        "total_tax": total_tax,
        "net_income": net_income,
        "yield_gross": yield_gross,
        "yield_net": yield_net,
        "nights": None,
        "tourist_tax_collected": 0,
        "allowance_pct": None,
    }


# ─── Compute P1 (always STR) ───
r1 = calc_str(p1_nightly, p1_occ_weeks, p1_classified, p1_regime,
              p1_value, mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere_p1, sleeps=9,
              tourist_tax_pppn=tourist_tax_pppn)

# ─── Compute P2 ───
if p2_mode == "Short-term (STR)":
    r2 = calc_str(p2_nightly, p2_occ_weeks, p2_classified, p2_regime,
                  p2_value, mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere_p2,
                  sleeps=p2_sleeps, tourist_tax_pppn=tourist_tax_pppn)
elif p2_mode == "Long-term unfurnished (bail nu)":
    r2 = calc_lt(p2_monthly, p2_void_months, p2_regime, p2_value,
                 taxe_fonciere_p2, mgmt_fee_pct, mgmt_exp_pct, furnished=False)
else:  # long-term furnished
    r2 = calc_lt(p2_monthly, p2_void_months, p2_regime, p2_value,
                 taxe_fonciere_p2, mgmt_fee_pct, mgmt_exp_pct, furnished=True)

combined_gross = r1["gross_revenue"] + r2["gross_revenue"]
combined_net = r1["net_income"] + r2["net_income"]
combined_tax = r1["total_tax"] + r2["total_tax"]
combined_value = p1_value + p2_value

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Portfolio Overview",
    "🏠 Property Detail",
    "🔀 Scenario Comparison",
    "📈 Sensitivity Analysis"
])

# ══════════════════════════════════════════════
# TAB 1 — PORTFOLIO OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Portfolio Summary</div>', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Combined Gross Revenue", f"€{combined_gross:,.0f}")
    c2.metric("Combined Net Income", f"€{combined_net:,.0f}",
              delta=f"{combined_net/combined_gross*100:.1f}% margin" if combined_gross else None)
    c3.metric("Total Tax Paid", f"€{combined_tax:,.0f}",
              delta=f"{combined_tax/combined_gross*100:.1f}% effective rate" if combined_gross else None,
              delta_color="inverse")
    c4.metric("Portfolio Gross Yield", f"{combined_gross/combined_value*100:.2f}%")
    c5.metric("Portfolio Net Yield", f"{combined_net/combined_value*100:.2f}%")

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title">Waterfall — Combined P&L</div>', unsafe_allow_html=True)

        labels = ["Gross Revenue", "Mgmt Fee", "Op. Costs", "Taxe Foncière",
                  "Income Tax", "Solidarity Levy", "Net Income"]
        values = [
            combined_gross,
            -(r1["mgmt_fee"] + r2["mgmt_fee"]),
            -(r1["op_costs"] + r2["op_costs"]),
            -(taxe_fonciere_p1 + taxe_fonciere_p2),
            -(r1["income_tax"] + r2["income_tax"]),
            -(r1["solidarity"] + r2["solidarity"]),
            combined_net,
        ]
        measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"]
        colours = ["#2E6DA4", "#C8A87A", "#C8A87A", "#C8A87A", "#8B3A3A", "#8B3A3A", "#2A6041"]

        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=measure,
            x=labels,
            y=values,
            connector={"line": {"color": "#C8A87A", "width": 1}},
            increasing={"marker": {"color": "#2E6DA4"}},
            decreasing={"marker": {"color": "#C8A87A"}},
            totals={"marker": {"color": "#2A6041"}},
            text=[f"€{v:,.0f}" for v in values],
            textposition="outside",
        ))
        fig_wf.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(244,241,236,0.5)",
            font={"family": "DM Sans", "color": "#1C2B3A"},
            yaxis={"gridcolor": "#E0D9D0", "tickprefix": "€", "tickformat": ",.0f"},
            margin={"t": 20, "b": 20, "l": 10, "r": 10},
            showlegend=False,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">Revenue & Net by Property</div>', unsafe_allow_html=True)

        props = ["Les Houches (P1)", p2_label + " (P2)"]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Gross Revenue", x=props,
                                  y=[r1["gross_revenue"], r2["gross_revenue"]],
                                  marker_color="#2E6DA4", text=[f"€{v:,.0f}" for v in [r1["gross_revenue"], r2["gross_revenue"]]],
                                  textposition="auto"))
        fig_bar.add_trace(go.Bar(name="Net Income", x=props,
                                  y=[r1["net_income"], r2["net_income"]],
                                  marker_color="#2A6041", text=[f"€{v:,.0f}" for v in [r1["net_income"], r2["net_income"]]],
                                  textposition="auto"))
        fig_bar.update_layout(
            barmode="group",
            height=220,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(244,241,236,0.5)",
            font={"family": "DM Sans", "color": "#1C2B3A"},
            yaxis={"gridcolor": "#E0D9D0", "tickprefix": "€", "tickformat": ",.0f"},
            legend={"orientation": "h", "y": -0.25},
            margin={"t": 10, "b": 10, "l": 10, "r": 10},
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Yield comparison
        st.markdown('<div class="section-title">Yield Comparison</div>', unsafe_allow_html=True)
        yields_df = pd.DataFrame({
            "Property": ["Les Houches (P1)", p2_label + " (P2)", "Portfolio"],
            "Gross Yield %": [r1["yield_gross"], r2["yield_gross"], combined_gross/combined_value*100],
            "Net Yield %": [r1["yield_net"], r2["yield_net"], combined_net/combined_value*100],
        })
        fig_yield = go.Figure()
        fig_yield.add_trace(go.Bar(name="Gross Yield", x=yields_df["Property"],
                                    y=yields_df["Gross Yield %"], marker_color="#2E6DA4",
                                    text=[f"{v:.2f}%" for v in yields_df["Gross Yield %"]], textposition="auto"))
        fig_yield.add_trace(go.Bar(name="Net Yield", x=yields_df["Property"],
                                    y=yields_df["Net Yield %"], marker_color="#2A6041",
                                    text=[f"{v:.2f}%" for v in yields_df["Net Yield %"]], textposition="auto"))
        fig_yield.update_layout(
            barmode="group", height=200,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(244,241,236,0.5)",
            font={"family": "DM Sans", "color": "#1C2B3A"},
            yaxis={"gridcolor": "#E0D9D0", "ticksuffix": "%"},
            legend={"orientation": "h", "y": -0.3},
            margin={"t": 10, "b": 10, "l": 10, "r": 10},
        )
        st.plotly_chart(fig_yield, use_container_width=True)

    # Key regulatory warnings
    st.markdown('<div class="section-title">⚖️ Regulatory Flags</div>', unsafe_allow_html=True)
    w1, w2 = st.columns(2)
    with w1:
        st.markdown("""
<div class="warning-box">
<strong>1-Property Limit — Les Houches</strong><br>
From May 2025, private owners in Les Houches & Chamonix may only operate <strong>one</strong> 
short-term rental. If both properties are in these communes and both are STR, you may need 
authorisation review or convert one to long-term.
</div>
""", unsafe_allow_html=True)
        if r1["gross_revenue"] > 15_000 and not p1_classified and "Micro-BIC" in p1_regime:
            st.markdown("""
<div class="warning-box">
<strong>Micro-BIC Threshold Breach — P1</strong><br>
Gross revenue exceeds €15,000. For an <em>unclassified</em> meublé, 
Micro-BIC is not available; <strong>Régime Réel applies automatically</strong>. 
Actual expenses deducted instead.
</div>
""", unsafe_allow_html=True)
    with w2:
        st.markdown("""
<div class="info-box">
<strong>Italy-France Double Tax Treaty</strong><br>
As Italian residents, French rental income is taxable <em>in France</em> under Art. 6 of the 
France–Italy DTA. Tax paid in France is creditable against Italian IRPEF. 
Effective combined EU rate: <strong>27.5%</strong> (20% IT + 7.5% solidarity levy). 
A1 certificate from INPS may be needed to confirm social security affiliation.
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="info-box">
<strong>SIRET Registration Required</strong><br>
All furnished rental income (BIC) requires registration at the <em>Guichet Unique</em> 
to obtain a SIRET number. Annual <em>Déclaration des Revenus</em> 
(Form 2042-C-PRO + 2031) must be filed in France by May each year.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — PROPERTY DETAIL
# ══════════════════════════════════════════════
with tab2:
    d1, d2 = st.columns(2)

    def render_property_detail(col, name, r, value, mode="STR", classified=False, regime="Micro-BIC"):
        with col:
            st.markdown(f'<div class="section-title">{name}</div>', unsafe_allow_html=True)
            badge_text = "STR" if mode == "STR" else "LONG-TERM"
            badge_class = "MTI" if classified else "Standard"
            st.markdown(f'<span class="regime-badge">{badge_text} · {badge_class} · {regime[:10]}</span>',
                        unsafe_allow_html=True)
            st.markdown("")

            rows = [
                ("Gross Revenue", r["gross_revenue"], False),
                ("Management Fee", -r["mgmt_fee"], False),
                ("Operating Costs", -r["op_costs"], False),
                ("Taxe Foncière", -r["taxe_fonciere"], False),
                ("Net Before Tax", r["net_before_tax"], False),
                ("──────────", None, None),
                ("Taxable Income", r["taxable_income"], False),
                ("Income Tax (20%)", -r["income_tax"], False),
                ("Solidarity Levy (7.5%)", -r["solidarity"], False),
                ("Total Tax", -r["total_tax"], False),
                ("══════════", None, None),
                ("NET INCOME", r["net_income"], True),
            ]

            for label, val, bold in rows:
                if val is None:
                    st.markdown(f"<hr style='margin:4px 0;border-color:#E0D9D0'>", unsafe_allow_html=True)
                    continue
                color = "#2A6041" if (bold and val > 0) else ("#8B3A3A" if val < 0 else "#1C2B3A")
                weight = "600" if bold else "400"
                sign = "+" if val > 0 else ""
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;margin:2px 0;font-weight:{weight};'>"
                    f"<span style='color:#5A4A3A'>{label}</span>"
                    f"<span style='color:{color}'>{sign}€{val:,.0f}</span></div>",
                    unsafe_allow_html=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            col_a.metric("Gross Yield", f"{r['yield_gross']:.2f}%")
            col_b.metric("Net Yield", f"{r['yield_net']:.2f}%")

            if r.get("allowance_pct"):
                eff_rate = r["total_tax"] / r["gross_revenue"] * 100 if r["gross_revenue"] else 0
                st.caption(f"Micro-BIC {r['allowance_pct']}% allowance · Effective tax rate on gross: {eff_rate:.1f}%")
            if mode == "STR" and r.get("nights"):
                st.caption(f"Nights booked: {r['nights']} · Average nightly: €{r['gross_revenue']/r['nights']:,.0f}")

    render_property_detail(d1, "🏔 P1 — Les Houches (90m²)",
                           r1, p1_value, "STR", p1_classified, p1_regime)
    render_property_detail(d2, f"🏠 P2 — {p2_label}",
                           r2, p2_value, p2_mode, False, p2_regime)

    # Pie chart — cost breakdown
    st.markdown('<div class="section-title">Cost Structure</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    def pie_chart(r, title):
        labels = ["Net Income", "Mgmt Fee", "Op. Costs", "Taxe Foncière", "Income Tax", "Solidarity"]
        values_p = [max(0, r["net_income"]), r["mgmt_fee"], r["op_costs"],
                    r["taxe_fonciere"], r["income_tax"], r["solidarity"]]
        colors = ["#2A6041", "#C8A87A", "#D4B896", "#A08060", "#8B3A3A", "#B85050"]
        fig = go.Figure(go.Pie(labels=labels, values=values_p, hole=0.45,
                                marker={"colors": colors},
                                textinfo="label+percent",
                                textfont={"size": 11, "family": "DM Sans"}))
        fig.update_layout(title=title, height=300,
                          paper_bgcolor="rgba(0,0,0,0)",
                          font={"family": "DM Sans", "color": "#1C2B3A"},
                          legend={"orientation": "h", "y": -0.2},
                          margin={"t": 30, "b": 10})
        return fig

    c1.plotly_chart(pie_chart(r1, "P1 — Les Houches"), use_container_width=True)
    c2.plotly_chart(pie_chart(r2, f"P2 — {p2_label}"), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — SCENARIO COMPARISON
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">P2 — Scenario Comparison: STR vs Long-Term</div>',
                unsafe_allow_html=True)
    st.caption("Compare three rental strategies for Property 2 side-by-side.")

    sc_col1, sc_col2, sc_col3 = st.columns(3)
    with sc_col1:
        sc_nightly = st.number_input("Sc A: STR nightly (€)", 100, 2000,
                                      int(p2_nightly) if p2_mode == "Short-term (STR)" else 280, 10, key="sc_n")
        sc_weeks = st.slider("Sc A: Weeks occupied", 1, 52,
                              int(p2_occ_weeks) if p2_mode == "Short-term (STR)" else 8, 1, key="sc_w")
        sc_classified_a = st.toggle("Classified (Sc A)", False, key="sc_ca")
    with sc_col2:
        sc_lt_monthly = st.number_input("Sc B: LT monthly rent (€)", 500, 8000,
                                         int(p2_monthly) if p2_mode != "Short-term (STR)" else 2200, 50, key="sc_m")
        sc_void = st.slider("Sc B: Void months", 0, 4, 1, 1, key="sc_v")
    with sc_col3:
        sc_lt_furn = st.number_input("Sc C: Furnished LT monthly (€)", 500, 8000,
                                      int(p2_monthly) if p2_mode != "Short-term (STR)" else 2500, 50, key="sc_f")
        sc_void_c = st.slider("Sc C: Void months", 0, 4, 1, 1, key="sc_vc")

    # Compute all 3 scenarios for P2
    sc_a = calc_str(sc_nightly, sc_weeks, sc_classified_a, "Micro-BIC (auto)",
                    p2_value, mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere_p2, sleeps=p2_sleeps)
    sc_b = calc_lt(sc_lt_monthly, sc_void, "Micro-foncier (unfurnished)",
                   p2_value, taxe_fonciere_p2, mgmt_fee_pct, mgmt_exp_pct, furnished=False)
    sc_c = calc_lt(sc_lt_furn, sc_void_c, "Micro-BIC (auto)",
                   p2_value, taxe_fonciere_p2, mgmt_fee_pct, mgmt_exp_pct, furnished=True)

    # Comparison table
    metrics = ["Gross Revenue", "Total Costs", "Net Before Tax", "Total Tax", "Net Income",
               "Gross Yield %", "Net Yield %", "Effective Tax Rate %"]
    sc_labels = ["Sc A: STR", "Sc B: LT Unfurnished", "Sc C: LT Furnished"]

    def effective_rate(r):
        return r["total_tax"] / r["gross_revenue"] * 100 if r["gross_revenue"] else 0

    table_data = {
        "Metric": metrics,
        "Sc A: STR": [
            f"€{sc_a['gross_revenue']:,.0f}",
            f"€{sc_a['total_direct_costs']:,.0f}",
            f"€{sc_a['net_before_tax']:,.0f}",
            f"€{sc_a['total_tax']:,.0f}",
            f"€{sc_a['net_income']:,.0f}",
            f"{sc_a['yield_gross']:.2f}%",
            f"{sc_a['yield_net']:.2f}%",
            f"{effective_rate(sc_a):.1f}%",
        ],
        "Sc B: LT Unfurnished": [
            f"€{sc_b['gross_revenue']:,.0f}",
            f"€{sc_b['total_direct_costs']:,.0f}",
            f"€{sc_b['net_before_tax']:,.0f}",
            f"€{sc_b['total_tax']:,.0f}",
            f"€{sc_b['net_income']:,.0f}",
            f"{sc_b['yield_gross']:.2f}%",
            f"{sc_b['yield_net']:.2f}%",
            f"{effective_rate(sc_b):.1f}%",
        ],
        "Sc C: LT Furnished": [
            f"€{sc_c['gross_revenue']:,.0f}",
            f"€{sc_c['total_direct_costs']:,.0f}",
            f"€{sc_c['net_before_tax']:,.0f}",
            f"€{sc_c['total_tax']:,.0f}",
            f"€{sc_c['net_income']:,.0f}",
            f"{sc_c['yield_gross']:.2f}%",
            f"{sc_c['yield_net']:.2f}%",
            f"{effective_rate(sc_c):.1f}%",
        ],
    }
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    # Visual comparison
    fig_sc = go.Figure()
    for label, r in zip(sc_labels, [sc_a, sc_b, sc_c]):
        fig_sc.add_trace(go.Bar(
            name=label,
            x=["Gross Revenue", "Net Before Tax", "Tax", "Net Income"],
            y=[r["gross_revenue"], r["net_before_tax"], r["total_tax"], r["net_income"]],
            text=[f"€{v:,.0f}" for v in [r["gross_revenue"], r["net_before_tax"], r["total_tax"], r["net_income"]]],
            textposition="auto"
        ))
    fig_sc.update_layout(
        barmode="group", height=350,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(244,241,236,0.5)",
        font={"family": "DM Sans", "color": "#1C2B3A"},
        yaxis={"gridcolor": "#E0D9D0", "tickprefix": "€", "tickformat": ",.0f"},
        legend={"orientation": "h", "y": -0.2},
        margin={"t": 10, "b": 10},
        colorway=["#2E6DA4", "#C8A87A", "#2A6041"],
    )
    st.plotly_chart(fig_sc, use_container_width=True)

    # Combined totals with P1 (always STR)
    st.markdown('<div class="section-title">Combined Portfolio — P1 STR + P2 Each Scenario</div>',
                unsafe_allow_html=True)
    comb_labels = ["P2 as STR", "P2 as LT Unfurn.", "P2 as LT Furn."]
    comb_nets = [r1["net_income"] + sc_a["net_income"],
                 r1["net_income"] + sc_b["net_income"],
                 r1["net_income"] + sc_c["net_income"]]
    comb_gross = [r1["gross_revenue"] + sc_a["gross_revenue"],
                  r1["gross_revenue"] + sc_b["gross_revenue"],
                  r1["gross_revenue"] + sc_c["gross_revenue"]]

    fig_comb = go.Figure()
    fig_comb.add_trace(go.Bar(name="Gross Revenue", x=comb_labels, y=comb_gross,
                               marker_color="#2E6DA4", text=[f"€{v:,.0f}" for v in comb_gross], textposition="auto"))
    fig_comb.add_trace(go.Bar(name="Net Income", x=comb_labels, y=comb_nets,
                               marker_color="#2A6041", text=[f"€{v:,.0f}" for v in comb_nets], textposition="auto"))
    fig_comb.update_layout(
        barmode="group", height=300,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(244,241,236,0.5)",
        font={"family": "DM Sans", "color": "#1C2B3A"},
        yaxis={"gridcolor": "#E0D9D0", "tickprefix": "€", "tickformat": ",.0f"},
        legend={"orientation": "h", "y": -0.25},
        margin={"t": 10, "b": 10},
    )
    st.plotly_chart(fig_comb, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — SENSITIVITY ANALYSIS
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Sensitivity Analysis — P1 Les Houches STR</div>',
                unsafe_allow_html=True)
    st.caption("How does net income and net yield respond to changes in occupancy and nightly rate?")

    # Heatmap: nightly rate x occupancy weeks
    rates = list(range(200, 701, 50))
    weeks_range = list(range(4, 25, 2))

    net_matrix = []
    for wk in weeks_range:
        row = []
        for rate in rates:
            res = calc_str(rate, wk, p1_classified, p1_regime, p1_value,
                           mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere_p1)
            row.append(round(res["net_income"], 0))
        net_matrix.append(row)

    fig_heat = go.Figure(go.Heatmap(
        z=net_matrix,
        x=[f"€{r}" for r in rates],
        y=[f"{w}wk" for w in weeks_range],
        colorscale=[[0, "#8B3A3A"], [0.4, "#C8A87A"], [0.7, "#E8E0D5"], [1, "#2A6041"]],
        text=[[f"€{v:,.0f}" for v in row] for row in net_matrix],
        texttemplate="%{text}",
        textfont={"size": 9},
        colorbar={"title": "Net Income €", "tickprefix": "€"},
    ))
    fig_heat.add_shape(
        type="rect",
        x0=rates.index(min(rates, key=lambda x: abs(x - p1_nightly))) - 0.5,
        x1=rates.index(min(rates, key=lambda x: abs(x - p1_nightly))) + 0.5,
        y0=weeks_range.index(min(weeks_range, key=lambda x: abs(x - p1_occ_weeks))) - 0.5,
        y1=weeks_range.index(min(weeks_range, key=lambda x: abs(x - p1_occ_weeks))) + 0.5,
        line={"color": "#1C2B3A", "width": 3},
    )
    fig_heat.update_layout(
        title="Net Income Heatmap (P1) — current scenario highlighted",
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#1C2B3A"},
        xaxis_title="Nightly Rate", yaxis_title="Occupancy",
        margin={"t": 40, "b": 20},
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="section-title">Occupancy Break-Even Analysis</div>', unsafe_allow_html=True)

    weeks_all = list(range(1, 53))
    gross_all = [p1_nightly * w * 7 for w in weeks_all]
    net_all = [calc_str(p1_nightly, w, p1_classified, p1_regime, p1_value,
                         mgmt_fee_pct, mgmt_exp_pct, taxe_fonciere_p1)["net_income"]
               for w in weeks_all]
    yield_all = [n / p1_value * 100 for n in net_all]

    fig_be = make_subplots(specs=[[{"secondary_y": True}]])
    fig_be.add_trace(go.Scatter(x=weeks_all, y=gross_all, name="Gross Revenue",
                                 line={"color": "#2E6DA4", "width": 2}), secondary_y=False)
    fig_be.add_trace(go.Scatter(x=weeks_all, y=net_all, name="Net Income",
                                 line={"color": "#2A6041", "width": 2, "dash": "dash"}), secondary_y=False)
    fig_be.add_trace(go.Scatter(x=weeks_all, y=yield_all, name="Net Yield %",
                                 line={"color": "#C8A87A", "width": 2}), secondary_y=True)
    fig_be.add_vline(x=p1_occ_weeks, line_dash="dot", line_color="#1C2B3A",
                      annotation_text=f"Current: {p1_occ_weeks}wk", annotation_position="top right")
    # Break-even line
    fig_be.add_hline(y=0, line_dash="dot", line_color="#8B3A3A", secondary_y=False,
                      annotation_text="Break-even", annotation_position="bottom right")
    fig_be.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(244,241,236,0.5)",
        font={"family": "DM Sans", "color": "#1C2B3A"},
        legend={"orientation": "h", "y": -0.25},
        xaxis={"title": "Weeks Occupied", "gridcolor": "#E0D9D0"},
        yaxis={"title": "€", "tickprefix": "€", "gridcolor": "#E0D9D0"},
        yaxis2={"title": "Net Yield %", "ticksuffix": "%"},
        margin={"t": 10, "b": 10},
    )
    st.plotly_chart(fig_be, use_container_width=True)

    # Micro-BIC threshold alert
    if p1_classified:
        threshold = 77_700
        regime_name = "Classified MTI (50%)"
    else:
        threshold = 15_000
        regime_name = "Unclassified (30%)"
    be_weeks_threshold = threshold / (p1_nightly * 7)
    st.markdown(f"""
<div class="info-box">
<strong>Micro-BIC Threshold ({regime_name}):</strong> 
At €{p1_nightly}/night, the €{threshold:,} ceiling is hit at 
<strong>{be_weeks_threshold:.1f} weeks</strong> ({be_weeks_threshold*7:.0f} nights). 
Beyond that, <em>Régime Réel</em> automatically applies and actual expenses are deducted instead.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** This model is for illustrative purposes only. "
    "Tax calculations are based on publicly available 2025 rules and the France–Italy DTA. "
    "Figures assume owners are affiliated to Italian social security (INPS). "
    "Always consult a qualified French tax adviser (expert-comptable) for your specific situation. "
    "Regulations are subject to change. | Loi Le Meur (Nov 2024) · PLU Chamonix (May 2025)"
)
