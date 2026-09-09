from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

import json

# Load mine data
with open("mine_data.json", "r") as f:
    mines = json.load(f)

pdf = SimpleDocTemplate(
    "MOIL_Production_Report.pdf"
)

styles = getSampleStyleSheet()

elements = []

# Title
elements.append(
    Paragraph(
        "MOIL AI Production Forecast Report",
        styles["Title"]
    )
)

elements.append(Spacer(1, 20))

# Summary
high = sum(
    1 for m in mines
    if m["risk"] == "HIGH"
)

medium = sum(
    1 for m in mines
    if m["risk"] == "MEDIUM"
)

low = sum(
    1 for m in mines
    if m["risk"] == "LOW"
)

elements.append(
    Paragraph(
        f"Total Mines Analyzed: {len(mines)}",
        styles["Normal"]
    )
)

elements.append(
    Paragraph(
        f"High Risk Mines: {high}",
        styles["Normal"]
    )
)

elements.append(
    Paragraph(
        f"Medium Risk Mines: {medium}",
        styles["Normal"]
    )
)

elements.append(
    Paragraph(
        f"Low Risk Mines: {low}",
        styles["Normal"]
    )
)

elements.append(Spacer(1, 20))

# Mine-by-mine report
for mine in mines:

    elements.append(
        Paragraph(
            mine["mine_name"],
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Expected Production: "
            f"{mine['expected_production']} MT",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Predicted Production: "
            f"{mine['predicted_production']} MT",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Estimated Shortfall: "
            f"{mine['shortfall']} MT",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Risk Level: "
            f"{mine['risk']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Equipment Availability: "
            f"{mine['equipment_availability']} %",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Downtime Hours: "
            f"{mine['downtime_hours']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Blast Delay Days: "
            f"{mine['blast_delay_days']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "Major Contributing Factors:",
            styles["Heading3"]
        )
    )

    if mine["issues"]:
        for issue in mine["issues"]:
            elements.append(
                Paragraph(
                    f"• {issue}",
                    styles["Normal"]
                )
            )
    else:
        elements.append(
            Paragraph(
                "No major issues detected.",
                styles["Normal"]
            )
        )

    elements.append(
        Paragraph(
            "Recommendations:",
            styles["Heading3"]
        )
    )

    if mine["recommendations"]:
        for rec in mine["recommendations"]:
            elements.append(
                Paragraph(
                    f"• {rec}",
                    styles["Normal"]
                )
            )
    else:
        elements.append(
            Paragraph(
                "No recommendations required.",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 15))

pdf.build(elements)

print(
    "MOIL_Production_Report.pdf created!"
)