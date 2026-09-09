def midpoint(value):

    value = str(value).strip()

    if "N/A" in value:
        return 0

    value = value.replace("%", "")

    if "-" in value:

        parts = value.split("-")

        low = parts[0].replace(">", "").strip()
        high = parts[1].replace(">", "").strip()

        return (
            float(low) + float(high)
        ) / 2

    value = value.replace(">", "").strip()

    return float(value)