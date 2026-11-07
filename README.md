# np-lucija-djukic

Repozitorijum za predmet Napredno programiranje (FIST4NP), UDG.
Studentkinja: Lucija Đukić

## Struktura

- `cijene.py` - funkcija `prosjecna_cijena`
- `tests/test_cijene.py` - pytest testovi
- `pyproject.toml` - podešavanja za ruff i pytest

## Pokretanje

Radila sam u Google Colabu (Python 3.12).

```
pip install ruff pytest
pytest -q
ruff check .
ruff format --check .
```

## Domaći 1: prosjecna_cijena

### Upotrijebljeni upit

Kao AI asistenta sam koristila Claude. Upit:

> Kontekst: Python 3.12; podaci o rezervacijama u CSV datoteci (kolone: gost, noci, cijena_noci).
> Zadatak: napisati funkciju koja vraća prosječnu cijenu noćenja ponderisanu brojem noćenja.
> Ograničenja: samo standardna biblioteka, type hints, obrada grešaka (prazna datoteka, neispravni podaci).
> Format odgovora: kod, tri pytest testa i kratko obrazloženje rješenja.

### Uočeni nedostaci generisanog koda

1. Ako u fajlu fali kolona (npr. `cijena_noci`), funkcija baca `KeyError` bez jasne poruke.
2. Kod neispravne vrijednosti (npr. `noci = "abc"`) poruka greške ne kaže koji red je problem.
3. Ako red ima manje vrijednosti od broja kolona, dobija se `None` i pada `TypeError` koji se ne hvata.
4. Negativan broj noćenja ili negativna cijena se ne provjeravaju, pa kvare prosjek.
5. Iako je upit tražio obradu neispravnih podataka, obrađen je samo slučaj kad je ukupan broj noćenja 0.
6. Test je koristio fiksnu putanju `/content/r.csv` koja radi samo u Colabu. Zamijenila sam je sa `tmp_path`.

### Ispravke

- dodata provjera da postoje kolone `noci` i `cijena_noci`
- hvatanje `ValueError` i `TypeError` uz poruku koja pokazuje neispravan red
- provjera negativnih vrijednosti
- šest testova: dva za računanje i četiri za greške (prazan fajl, fali kolona, neispravna vrijednost, negativne noći)
- `ruff format` je ispravio formatiranje (prazan red sa razmacima na kraju fajla)
