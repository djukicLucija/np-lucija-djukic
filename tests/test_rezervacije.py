import pytest

from rezervacije import (
    CsvIzvor,
    FajlIzvjestaj,
    MailObavjestenje,
    ObradaRezervacija,
    Rezervacija,
)

# Zamjenski (lazni) objekti umjesto pravog fajla i maila


class LazniIzvor:
    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class LazniIzvjestaj:
    def __init__(self) -> None:
        self.primljeno: list[float] | None = None

    def posalji(self, iznosi: list[float]) -> None:
        self.primljeno = iznosi


def test_servis_racuna_iznose():
    izvor = LazniIzvor([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 5, 65)])
    servis = ObradaRezervacija(izvor, [])
    assert servis.obradi() == [240, 325]


def test_servis_salje_iznose_svim_izvjestajima():
    izvor = LazniIzvor([Rezervacija("Ivana", 2, 120)])
    prvi, drugi = LazniIzvjestaj(), LazniIzvjestaj()
    ObradaRezervacija(izvor, [prvi, drugi]).obradi()
    assert prvi.primljeno == [240]
    assert drugi.primljeno == [240]


def test_prazan_izvor():
    izvjestaj = LazniIzvjestaj()
    iznosi = ObradaRezervacija(LazniIzvor([]), [izvjestaj]).obradi()
    assert iznosi == []
    assert izvjestaj.primljeno == []


def test_negativne_noci():
    with pytest.raises(ValueError):
        Rezervacija("Ana", -1, 80)


def test_csv_izvor(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("gost,noci,cijena_noci\nAna,3,80\n", encoding="utf-8")
    assert CsvIzvor(p).ucitaj() == [Rezervacija("Ana", 3, 80.0)]


def test_fajl_izvjestaj(tmp_path):
    p = tmp_path / "izvjestaj.txt"
    FajlIzvjestaj(p).posalji([240.0, 325.0])
    assert p.read_text(encoding="utf-8") == "[240.0, 325.0]"


def test_mail_obavjestenje(capsys):
    MailObavjestenje().posalji([240.0, 325.0])
    assert capsys.readouterr().out == "Poslato: 565.0\n"
