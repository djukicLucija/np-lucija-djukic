"""Mini projekat 1: refaktoring obrade rezervacija (principi S i D)."""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Rezervacija:
    """Podaci o jednoj rezervaciji i obracun iznosa."""

    gost: str
    noci: int
    cijena_noci: float

    def __post_init__(self) -> None:
        if self.noci < 0 or self.cijena_noci < 0:
            raise ValueError("Broj nocenja i cijena ne smiju biti negativni")

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci


# Ugovori (Protocol) - servis zavisi samo od njih (princip D)


class IzvorPodataka(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestavanje(Protocol):
    def posalji(self, iznosi: list[float]) -> None: ...


# Konkretne implementacije - svaka klasa ima jednu odgovornost (princip S)


class CsvIzvor:
    """Ucitava rezervacije iz CSV fajla (kolone: gost, noci, cijena_noci)."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(newline="", encoding="utf-8") as f:
            return [
                Rezervacija(red["gost"], int(red["noci"]), float(red["cijena_noci"]))
                for red in csv.DictReader(f)
            ]


class FajlIzvjestaj:
    """Cuva iznose u tekstualni fajl."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def posalji(self, iznosi: list[float]) -> None:
        self.putanja.write_text(str(iznosi), encoding="utf-8")


class MailObavjestenje:
    """Simulira slanje maila (ispis na ekran), kao u originalnom kodu."""

    def posalji(self, iznosi: list[float]) -> None:
        print("Poslato:", sum(iznosi))


class ObradaRezervacija:
    """Servis: ucita rezervacije, izracuna iznose i proslijedi ih izvjestajima."""

    def __init__(self, izvor: IzvorPodataka, izvjestaji: list[Izvjestavanje]) -> None:
        self.izvor = izvor
        self.izvjestaji = izvjestaji

    def obradi(self) -> list[float]:
        iznosi = [r.iznos for r in self.izvor.ucitaj()]
        for izvjestaj in self.izvjestaji:
            izvjestaj.posalji(iznosi)
        return iznosi


if __name__ == "__main__":
    servis = ObradaRezervacija(
        CsvIzvor(Path("rezervacije.csv")),
        [FajlIzvjestaj(Path("izvjestaj.txt")), MailObavjestenje()],
    )
    servis.obradi()
