import csv


def export_csv(orders, path):
    """Write orders (list of dicts with id/total) to a CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "total"])
        writer.writeheader()
        writer.writerows(orders)
