import pytest

from cijene import prosjecna_cijena


def napravi_csv(tmp_path, sadrzaj):
    p = tmp_path / "r.csv"
    p.write_text(sadrzaj, encoding="utf-8")
    return p


def test_prosjek(tmp_path):
    p = napravi_csv(tmp_path, "gost,noci,cijena_noci\nAna,2,100\nMarko,2,50\n")
    assert prosjecna_cijena(p) == 75.0


def test_ponderisan_prosjek(tmp_path):
    # Ana 3 noci po 80, Ivana 1 noc po 120 -> (240 + 120) / 4 = 90
    p = napravi_csv(tmp_path, "gost,noci,cijena_noci\nAna,3,80\nIvana,1,120\n")
    assert prosjecna_cijena(p) == 90.0


def test_prazan_fajl(tmp_path):
    p = napravi_csv(tmp_path, "gost,noci,cijena_noci\n")
    with pytest.raises(ValueError, match="Nema ostvarenih"):
        prosjecna_cijena(p)


def test_nedostaje_kolona(tmp_path):
    p = napravi_csv(tmp_path, "gost,noci\nAna,2\n")
    with pytest.raises(ValueError, match="kolone"):
        prosjecna_cijena(p)


def test_neispravna_vrijednost(tmp_path):
    p = napravi_csv(tmp_path, "gost,noci,cijena_noci\nAna,abc,100\n")
    with pytest.raises(ValueError, match="Neispravan red"):
        prosjecna_cijena(p)


def test_negativne_noci(tmp_path):
    p = napravi_csv(tmp_path, "gost,noci,cijena_noci\nAna,-2,100\n")
    with pytest.raises(ValueError, match="Negativna"):
        prosjecna_cijena(p)
