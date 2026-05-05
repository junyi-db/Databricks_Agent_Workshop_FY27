"""
Generate synthetic PDFs for the workshop's Knowledge Assistant.

Uses reportlab to write professionally-formatted PDFs that mimic the kind of
operational documents the workshop's KA will answer questions over.

All content is synthetic. Page counts vary so the KA has different doc shapes.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data" / "pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)

PETRONAS_TEAL = HexColor("#00A19A")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("title", parent=styles["Heading1"], textColor=PETRONAS_TEAL, spaceAfter=12)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], textColor=black, spaceAfter=8, spaceBefore=10)
body = ParagraphStyle("body", parent=styles["BodyText"], alignment=TA_LEFT, leading=14, spaceAfter=6)
small = ParagraphStyle("small", parent=styles["BodyText"], fontSize=8, textColor=HexColor("#555555"))


def build_pdf(filename: str, title: str, doc_id: str, version: str, sections: list[tuple[str, list[str]]]):
    out = PDF_DIR / filename
    pdf = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm)
    flow = []

    flow.append(Paragraph("PETRONAS - INTERNAL USE ONLY", small))
    flow.append(Paragraph(title, title_style))
    meta_table = Table(
        [["Document ID", doc_id], ["Version", version], ["Owner", "Group Operational Excellence"], ["Classification", "Internal"]],
        colWidths=[4 * cm, 10 * cm],
    )
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#F2F2F2")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#999999")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, HexColor("#CCCCCC")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(meta_table)
    flow.append(Spacer(1, 0.6 * cm))

    for heading, paragraphs in sections:
        flow.append(Paragraph(heading, h2))
        for p in paragraphs:
            flow.append(Paragraph(p, body))
        flow.append(Spacer(1, 0.2 * cm))

    flow.append(Spacer(1, 0.6 * cm))
    flow.append(Paragraph("This document is synthetic and prepared solely for the PETRONAS AI Enterprise Adoption Workshop. It does not represent actual operational policies of PETRONAS or its subsidiaries.", small))

    pdf.build(flow)
    print(f"  Wrote {out.name}")


# ---------- 1. Operational Excellence SOP ----------
build_pdf(
    filename="01_operational_excellence_sop.pdf",
    title="Operational Excellence Standard Operating Procedure",
    doc_id="OE-SOP-001",
    version="3.2",
    sections=[
        ("1. Purpose", [
            "This Standard Operating Procedure defines the minimum operating discipline expected of every PETRONAS asset, business unit and operating site within the Group. It establishes a common language for operational performance and provides the basis for cross-business benchmarking.",
            "All sites are expected to comply with this SOP regardless of business unit, geography, or asset type.",
        ]),
        ("2. Scope", [
            "This SOP applies to all PETRONAS-operated facilities including Upstream offshore platforms and onshore fields, Downstream refineries and petrochemical plants, Gas & New Energy LNG plants, Trading desks, Retail clusters, and Logistics terminals.",
            "It does not apply to non-operated joint ventures or facilities operated under third-party operating models.",
        ]),
        ("3. Operating Discipline Pillars", [
            "<b>3.1 Throughput Reliability.</b> Every operated site shall report a daily throughput figure against an approved throughput target. Sites operating below 90% of approved target for three consecutive days shall trigger an Operational Performance Review.",
            "<b>3.2 Energy Stewardship.</b> Energy consumption per unit of throughput shall be tracked daily and reported monthly to Group Operational Excellence. Sites are expected to deliver year-on-year energy intensity improvements aligned with the Group's Net Zero 2050 pathway.",
            "<b>3.3 Emissions Accounting.</b> Scope 1 emissions in tCO2e shall be calculated daily using approved emission factors for the asset type. Reporting cadence is monthly with annual external assurance.",
            "<b>3.4 Asset Integrity.</b> Every critical asset shall have an inspection cadence registered in the Asset Register. Overdue inspections shall be escalated to the Asset Integrity Manager within 5 business days.",
        ]),
        ("4. Reporting Standards", [
            "All operational data shall flow into the Group Operations Data Platform on Databricks Unity Catalog. Each business unit is responsible for daily ingestion of throughput, uptime, energy and emissions data into the operations_daily Delta table.",
            "Data quality expectations: completeness >= 98% per site per month, latency <= 24 hours from event time to availability in the platform, and column-level lineage maintained through Unity Catalog.",
        ]),
        ("5. Roles & Responsibilities", [
            "Site Operations Lead: Owns daily data submission and first-line investigation of variances against target.",
            "Business Unit Operations Manager: Reviews weekly performance, approves variance explanations, sponsors corrective actions.",
            "Group Operational Excellence: Maintains the SOP, the Group dashboard, and benchmarks performance across business units.",
        ]),
        ("6. Performance Review Cadence", [
            "Daily: Site Operations huddle (15 min) to review overnight throughput, uptime and exceptions.",
            "Weekly: Business Unit Operations Review covering trailing 7-day performance and forward-week look-ahead.",
            "Monthly: Group Operations Council reviewing Group-wide KPIs, energy intensity trend, and emissions performance.",
            "Quarterly: External assurance review for emissions data ahead of regulatory submissions.",
        ]),
        ("7. Definitions", [
            "<b>Throughput Target:</b> The approved throughput plan for the operating period as agreed by the BU Operations Manager.",
            "<b>Uptime:</b> Hours an asset is producing within design tolerances divided by total hours in the period.",
            "<b>Energy Intensity:</b> MWh of energy consumed per unit of throughput, normalised to a reference site within the same site type.",
            "<b>Tier-1 Variance:</b> A throughput shortfall exceeding 15% versus target sustained for more than 24 hours.",
        ]),
    ],
)

# ---------- 2. Net Zero 2050 brief ----------
build_pdf(
    filename="02_net_zero_2050_brief.pdf",
    title="PETRONAS Net Zero 2050 Pathway - Operations Brief",
    doc_id="SUS-BRF-014",
    version="2.0",
    sections=[
        ("Executive Summary", [
            "PETRONAS has committed to achieving Net Zero Carbon Emissions (NZCE) by 2050 across operated assets. This brief summarises the pathway, the operational levers, and the data infrastructure required to track progress.",
            "The pathway is anchored on four levers: (1) operational efficiency, (2) electrification of operations, (3) carbon capture, utilisation and storage (CCUS), and (4) low-carbon fuels and feedstocks.",
        ]),
        ("Scope and Boundaries", [
            "Scope 1: Direct emissions from operated assets - the primary focus of operational reporting and the scope tracked in the operations_daily Delta table.",
            "Scope 2: Emissions from purchased electricity, steam, heat or cooling consumed by operated assets.",
            "Scope 3: Indirect emissions across the value chain - addressed through portfolio decisions and customer collaboration.",
        ]),
        ("Interim Targets", [
            "<b>By 2030:</b> 25% reduction in absolute Group operational Scope 1+2 GHG emissions versus a 2019 baseline.",
            "<b>By 2040:</b> Methane intensity of less than 0.2% across operated upstream assets.",
            "<b>By 2050:</b> Net zero across all operated Scope 1+2 emissions.",
        ]),
        ("Operational Levers", [
            "<b>Energy Efficiency:</b> Targeted 15% improvement in energy intensity by 2030, primarily through compressor optimisation, heat integration and digital advanced process control.",
            "<b>Flaring Reduction:</b> Zero routine flaring by 2030 in line with the World Bank Zero Routine Flaring initiative.",
            "<b>Electrification:</b> Selective electrification of offshore platforms and refinery utilities where renewable power is technically and commercially viable.",
            "<b>CCUS:</b> Build CCUS capacity at the Kasawari and Pengerang complexes to abate hard-to-decarbonise emissions.",
        ]),
        ("Data and Reporting", [
            "All operational sites contribute to the Group emissions ledger via the operations_daily.emissions_tco2e column. Emission factors are maintained centrally and refreshed annually following external assurance.",
            "The Group's Net Zero performance dashboard is published monthly on Databricks AI/BI Dashboards and shared with the Sustainability Council.",
        ]),
        ("Frequently Asked Questions", [
            "<b>Q: What is the Group's Scope 1 reduction target by 2030?</b> A: 25% absolute reduction versus a 2019 baseline, covering operated assets across all business units.",
            "<b>Q: Does Net Zero 2050 cover Scope 3?</b> A: The headline 2050 commitment covers Scope 1 and Scope 2. Scope 3 is addressed through portfolio strategy.",
            "<b>Q: How is methane intensity measured?</b> A: Methane intensity is the volume of methane emissions divided by the volume of marketed natural gas, expressed as a percentage.",
        ]),
    ],
)

# ---------- 3. Asset Integrity policy ----------
build_pdf(
    filename="03_asset_integrity_policy.pdf",
    title="Asset Integrity Management Policy",
    doc_id="AIM-POL-007",
    version="4.1",
    sections=[
        ("1. Policy Statement", [
            "PETRONAS shall maintain the integrity of every operated asset throughout its lifecycle to safeguard people, the environment, and shareholder value. Asset integrity is non-negotiable and supersedes commercial considerations.",
        ]),
        ("2. Asset Criticality Classification", [
            "Every asset shall be classified as Critical, High, Medium, or Low based on the consequence of failure. Criticality drives inspection frequency, spares strategy, and competency requirements for operations and maintenance staff.",
            "<b>Critical:</b> Failure may cause loss of life, major environmental impact, or production loss exceeding USD 10 million. Inspection cadence: 6 months.",
            "<b>High:</b> Failure may cause serious injury or production loss between USD 1-10 million. Inspection cadence: 12 months.",
            "<b>Medium:</b> Failure may cause minor injury or production loss between USD 100k-1M. Inspection cadence: 24 months.",
            "<b>Low:</b> Failure has minimal safety, environmental or commercial consequence. Inspection cadence: as specified by the Original Equipment Manufacturer.",
        ]),
        ("3. Inspection Cadence", [
            "Inspection cadence shall not exceed the maximum interval defined by criticality. Sites may inspect more frequently based on equipment age, failure history or operating severity.",
            "Inspection records shall be maintained in the Group Asset Register and made available to Unity Catalog as part of the assets table. Each row shall carry the asset_id, last_inspection_date, next_inspection_date and criticality.",
        ]),
        ("4. Overdue Inspections", [
            "Any asset whose next_inspection_date is past due shall be flagged as Overdue. Overdue Critical assets shall be reported to the BU Operations Manager and Group Asset Integrity within 24 hours.",
            "Continued operation of an Overdue Critical asset requires a written deviation approved by the BU Vice President and the Group Head of Asset Integrity. Deviation validity shall not exceed 30 days.",
        ]),
        ("5. Decommissioning", [
            "Assets at end-of-life shall be moved to Decommissioned status in the asset register and physically isolated. Decommissioned assets shall not appear in throughput-bearing rows of operations_daily.",
        ]),
        ("6. Reporting", [
            "Group Asset Integrity publishes the monthly Integrity Scorecard on Databricks. The scorecard shows percentage of inspections completed on time, overdue counts by criticality, and trailing 12-month trend by business unit.",
        ]),
    ],
)

# ---------- 4. Production Reporting Standard ----------
build_pdf(
    filename="04_production_reporting_standard.pdf",
    title="Group Production and Operations Reporting Standard",
    doc_id="OPR-STD-022",
    version="5.0",
    sections=[
        ("1. Purpose", [
            "This standard defines how operational throughput, uptime, energy and emissions are measured, recorded, and reported within the Group. It is the authoritative reference for the operations_daily Delta table maintained in Unity Catalog.",
        ]),
        ("2. Reporting Units", [
            "Throughput shall be reported in the standard unit appropriate to the site type:",
            "&nbsp;&nbsp;- Offshore Platforms and Onshore Fields: thousand barrels per day (kbbl/d) for liquids, million standard cubic feet per day (MMscf/d) for gas.",
            "&nbsp;&nbsp;- Refineries and Trading Desks: thousand barrels per day (kbbl/d).",
            "&nbsp;&nbsp;- LNG Plants: million tonnes per annum (MTPA).",
            "&nbsp;&nbsp;- Petrochemical Plants: kilotonnes per day (kt/d).",
            "&nbsp;&nbsp;- Retail Clusters: kilolitres per day (kL/d).",
            "&nbsp;&nbsp;- Marine Terminals: thousand barrels per day (kbbl/d).",
        ]),
        ("3. Data Submission", [
            "Site Operations is responsible for submitting daily data by 09:00 local time the following day. Submissions land in the bronze schema, are validated by Group Data Engineering, and promoted to silver.",
            "The gold table operations_daily presents the assured Group-wide view used by leadership dashboards, the Genie Space and the AI Co-Pilot.",
        ]),
        ("4. Data Quality Rules", [
            "Each row in operations_daily shall contain a non-null operation_date, site_id, business_unit, throughput_value, throughput_unit, uptime_pct, energy_consumed_mwh, and emissions_tco2e.",
            "throughput_value must be >= 0. Negative values are rejected at the bronze layer.",
            "uptime_pct must be in [0, 100]. Values outside the range are flagged for review.",
            "emissions_tco2e shall be calculated using the latest approved emission factor for the site_type.",
        ]),
        ("5. Variance Investigation", [
            "Variances exceeding 10% versus throughput_target shall include a written explanation in the variance_notes column at the silver layer. Variances exceeding 15% trigger an automatic notification to the BU Operations Manager.",
        ]),
        ("6. Auditability and Lineage", [
            "All transformations from bronze to silver to gold shall be authored as Lakeflow Spark Declarative Pipelines and registered in Unity Catalog. Column-level lineage shall be available for every gold column.",
        ]),
    ],
)

# ---------- 5. Equipment Maintenance Manual excerpt ----------
build_pdf(
    filename="05_compressor_maintenance_manual.pdf",
    title="Centrifugal Gas Compressor - Maintenance Manual (Excerpt)",
    doc_id="EQ-MAN-CGC-009",
    version="2.4",
    sections=[
        ("Section 4: Routine Maintenance", [
            "This manual excerpt covers Type CGC-3 centrifugal gas compressors deployed across PETRONAS Upstream platforms and Gas & New Energy LNG complexes.",
            "Routine maintenance comprises three cadences: daily walkdown, monthly preventive maintenance, and annual major inspection.",
        ]),
        ("4.1 Daily Walkdown", [
            "Operations staff shall perform a daily walkdown of each compressor unit. The walkdown checklist includes: visual inspection of seals for leaks, vibration spot-check at bearings, lubrication oil level check, and verification that suction and discharge pressures are within normal operating envelope.",
            "Findings shall be recorded in the Site Operations Log and abnormal conditions raised as a maintenance work order in the CMMS.",
        ]),
        ("4.2 Monthly Preventive Maintenance", [
            "Monthly preventive maintenance covers: replacement of suction filter elements, sampling of lubrication oil for laboratory analysis, inspection of inlet guide vane actuators, and recalibration of vibration probes.",
            "Estimated downtime: 4 hours. The work shall be scheduled in the Plant Maintenance Plan to coincide with low demand periods.",
        ]),
        ("4.3 Annual Major Inspection", [
            "The annual major inspection requires the unit to be isolated and locked out following the site Permit-to-Work procedure. Activities include: rotor borescopy, replacement of dry-gas seals, full lubrication system flush, and re-alignment of the driver-driven train.",
            "Estimated downtime: 5 days. The inspection shall be performed by a qualified rotating equipment specialist with Type CGC-3 endorsement.",
        ]),
        ("Section 5: Failure Modes", [
            "<b>Surge:</b> Recognised by rapid pressure oscillation and audible bark. Operators shall reduce load and open the recycle valve to recover. Sustained surge may damage the rotor and shall be reported within 1 hour.",
            "<b>High Vibration:</b> A vibration trip is configured at 7.1 mm/s peak. On trip, the unit shall not be restarted until the root cause is identified.",
            "<b>Seal Gas Leak:</b> Indicated by rising secondary seal vent flow. The unit shall be shut down within 4 hours and the seal cartridge replaced.",
        ]),
        ("Section 6: Reporting", [
            "All maintenance events shall be logged against the asset_id in the Group Asset Register and surfaced to the operations_daily table via the maintenance_event_count column at the silver layer.",
        ]),
    ],
)


print("Done.")
