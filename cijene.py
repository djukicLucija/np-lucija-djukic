%%writefile cijene.py
import csv
from pathlib import Path


def prosjecna_cijena(putanja: Path) -> float:
    """Prosjecna cijena nocenja, ponderisana brojem nocenja."""
    ukupno = 0.0
    noci = 0

    with putanja.open(newline="", encoding="utf-8") as f:
        citac = csv.DictReader(f)
        kolone = citac.fieldnames or []
        if "noci" not in kolone or "cijena_noci" not in kolone:
            raise ValueError("Fajl mora imati kolone noci i cijena_noci")

        for red in citac:
            try:
                n = int(red["noci"])
                cijena = float(red["cijena_noci"])
            except (TypeError, ValueError):
                raise ValueError(f"Neispravan red: {red}") from None

            if n < 0 or cijena < 0:
                raise ValueError(f"Negativna vrijednost u redu: {red}")

            ukupno += n * cijena
            noci += n

    if noci == 0:
        raise ValueError("Nema ostvarenih nocenja")
    return ukupno / noci
    
