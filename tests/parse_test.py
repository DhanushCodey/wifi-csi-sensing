from tools.parse import parse


def test_parse_fixture():
    p = parse("data/fixture/csi_sample.txt")
    assert p["amplitude"].shape == (10, 190)
    assert (p["amplitude"] >= 0).all()
    assert p["ids"][0] == 7219
    assert p["timestamps"][0] == 38036850

