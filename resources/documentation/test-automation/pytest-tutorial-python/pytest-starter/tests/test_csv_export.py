from csv_export import export_csv


def test_export_csv(sample_orders, tmp_path):
    path = tmp_path / "orders.csv"
    export_csv(sample_orders, path)
    content = path.read_text()
    assert "id,total" in content
    assert "1,100" in content


def test_export_csv_empty(sample_orders, tmp_path):
    path = tmp_path / "empty.csv"
    export_csv([], path)
    content = path.read_text()
    assert "id,total" in content
    assert "1,100" not in content
