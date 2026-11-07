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

- ## Mini projekat 1: refaktoring obrade rezervacija

Polazni kod je klasa `UpravljanjeRezervacijama` sa vježbi (nedjelja 2). Ona je radila četiri stvari: učitavala fajl, računala iznos, čuvala izvještaj i slala mail. Zbog toga je imala četiri razloga za promjenu (kršenje principa S), a sama je otvarala konkretan fajl, pa se nije mogla testirati bez pravog fajla (kršenje principa D).

### Nova podjela (`rezervacije.py`)

| Klasa | Odgovornost |
| --- | --- |
| `Rezervacija` (dataclass) | podaci i obračun iznosa, validacija |
| `IzvorPodataka` (Protocol) | ugovor za učitavanje |
| `Izvjestavanje` (Protocol) | ugovor za izvještavanje |
| `CsvIzvor` | čitanje CSV fajla |
| `FajlIzvjestaj` | čuvanje iznosa u fajl |
| `MailObavjestenje` | slanje obavještenja (simulacija) |
| `ObradaRezervacija` | servis koji povezuje sve, prima zavisnosti kroz konstruktor |

- **S:** svaka klasa ima jednu odgovornost.
- **D:** `ObradaRezervacija` zna samo za `IzvorPodataka` i `Izvjestavanje`, a konkretne klase dobija spolja. Zato u testovima koristim `LazniIzvor` i `LazniIzvjestaj`.
- **O:** novi izvor (npr. baza) ili novi izvještaj dodaje se kao nova klasa, bez izmjene servisa.

### Testovi (`tests/test_rezervacije.py`)

7 testova. Tri testiraju servis sa zamjenskim izvorom podataka, a ostali testiraju validaciju, CSV izvor, fajl izvještaj i mail.

### Upotrijebljeni upit

> Uloga: iskusni softverski arhitekta.
> Zadatak: analizirati priloženi Python kod.
> 1. Navesti narušene SOLID principe, sa brojem linije.
> 2. Objasniti praktičnu posljedicu svakog narušavanja.
> 3. Predložiti refaktoring uz kratak primjer.
> 4. Predložiti tri testa koja potvrđuju da se ponašanje nije promijenilo.
> Ograničenje: ne uvoditi apstrakcije koje problem ne zahtijeva.
>
> [kod klase UpravljanjeRezervacijama]

### Problemi u polaznom kodu i ispravke

1. `open()` bez `with`: fajlovi se ne zatvaraju. Sada se koristi `with`.
2. Nema `encoding`, pa naša slova mogu da se pokvare. Dodato je `encoding="utf-8"`.
3. Pristup preko indeksa (`r[1]`, `r[2]`) je nečitljiv. Sada se koristi `csv.DictReader` i dataclass sa imenovanim poljima.
4. Ime fajla `izvjestaj.txt` je bilo fiksno u kodu. Sada se putanja prosljeđuje kroz konstruktor.
5. Nije bilo provjere negativnih vrijednosti. Dodata je u `Rezervacija.__post_init__`.
6. Prema ograničenju iz upita nisam uvodila posebnu apstrakciju za obračun (npr. tarife), jer zadatak to ne traži (YAGNI).
