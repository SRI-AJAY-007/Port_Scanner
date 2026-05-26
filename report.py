import csv
import os
from datetime import datetime


def save_results(target, open_ports):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"reports/scan_{timestamp}.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Target",
            "Port",
            "Service",
            "Banner",
            "Risk"
        ])

        for result in open_ports:

            writer.writerow([
                datetime.now(),
                target,
                result["port"],
                result["service"],
                result["banner"],
                result["risk"]
            ])

    print(
        f"\nResults saved to {filename}"
    )