#!/usr/bin/env python3
"""CLI: Cotizador rápido Decoros."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass


@dataclass
class CotizacionInput:
    ancho_mm: float
    largo_mm: float
    costo_pieza: float
    merma_pct: float
    flete: float
    comision_pct: float
    iva_pct: float
    utilidad_pct: float


@dataclass
class CotizacionOutput:
    precio_sugerido_pieza: float
    precio_m2: float
    utilidad_mxn: float
    utilidad_pct: float


def _validate_non_negative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} no puede ser negativo.")


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} debe ser mayor a 0.")


def validar_entrada(data: CotizacionInput) -> None:
    _validate_positive(data.ancho_mm, "ancho_mm")
    _validate_positive(data.largo_mm, "largo_mm")
    _validate_positive(data.costo_pieza, "costo_pieza")

    _validate_non_negative(data.merma_pct, "merma_pct")
    _validate_non_negative(data.flete, "flete")
    _validate_non_negative(data.comision_pct, "comision_pct")
    _validate_non_negative(data.iva_pct, "iva_pct")
    _validate_non_negative(data.utilidad_pct, "utilidad_pct")


def calcular_cotizacion(data: CotizacionInput) -> CotizacionOutput:
    validar_entrada(data)

    area_m2 = (data.ancho_mm * data.largo_mm) / 1_000_000
    if area_m2 <= 0:
        raise ValueError("El área calculada debe ser mayor a 0.")

    costo_con_merma = data.costo_pieza * (1 + data.merma_pct / 100)
    costo_operativo = costo_con_merma + data.flete
    costo_total = costo_operativo * (1 + data.comision_pct / 100)

    utilidad_mxn = costo_total * (data.utilidad_pct / 100)
    precio_sin_iva = costo_total + utilidad_mxn
    precio_sugerido_pieza = precio_sin_iva * (1 + data.iva_pct / 100)
    precio_m2 = precio_sugerido_pieza / area_m2

    utilidad_pct_real = (utilidad_mxn / costo_total) * 100 if costo_total else 0.0

    return CotizacionOutput(
        precio_sugerido_pieza=round(precio_sugerido_pieza, 2),
        precio_m2=round(precio_m2, 2),
        utilidad_mxn=round(utilidad_mxn, 2),
        utilidad_pct=round(utilidad_pct_real, 2),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cotizador_rapido.py",
        description="Cotizador rápido Decoros: calcula precio sugerido por pieza y por m².",
    )

    parser.add_argument("--ancho-mm", type=float, required=True)
    parser.add_argument("--largo-mm", type=float, required=True)
    parser.add_argument("--costo-pieza", type=float, required=True)
    parser.add_argument("--merma-pct", type=float, required=True)
    parser.add_argument("--flete", type=float, required=True)
    parser.add_argument("--comision-pct", type=float, required=True)
    parser.add_argument("--iva-pct", type=float, required=True)
    parser.add_argument("--utilidad-pct", type=float, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    data = CotizacionInput(
        ancho_mm=args.ancho_mm,
        largo_mm=args.largo_mm,
        costo_pieza=args.costo_pieza,
        merma_pct=args.merma_pct,
        flete=args.flete,
        comision_pct=args.comision_pct,
        iva_pct=args.iva_pct,
        utilidad_pct=args.utilidad_pct,
    )

    try:
        resultado = calcular_cotizacion(data)
    except ValueError as err:
        print(f"Error de validación: {err}", file=sys.stderr)
        return 2

    print(json.dumps(asdict(resultado), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
