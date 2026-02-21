# DECOROS

Herramienta CLI en Python: **Cotizador rápido Decoros**.

Calcula:
- `precio_sugerido_pieza`
- `precio_m2`
- `utilidad_mxn`
- `utilidad_pct`

## Requisitos
- Python 3.10+

## Inputs
La CLI recibe los siguientes parámetros (todos obligatorios):

- `--ancho-mm`: ancho de la pieza en milímetros (> 0)
- `--largo-mm`: largo de la pieza en milímetros (> 0)
- `--costo-pieza`: costo base por pieza en MXN (> 0)
- `--merma-pct`: porcentaje de merma (>= 0)
- `--flete`: costo de flete por pieza en MXN (>= 0)
- `--comision-pct`: porcentaje de comisión (>= 0)
- `--iva-pct`: porcentaje de IVA (>= 0)
- `--utilidad-pct`: porcentaje de utilidad objetivo (>= 0)

## Ejecución

```bash
python cotizador_rapido.py \
  --ancho-mm 600 \
  --largo-mm 1200 \
  --costo-pieza 200 \
  --merma-pct 10 \
  --flete 20 \
  --comision-pct 5 \
  --iva-pct 16 \
  --utilidad-pct 30
```

Salida esperada (JSON):

```json
{
  "precio_sugerido_pieza": 380.02,
  "precio_m2": 527.8,
  "utilidad_mxn": 75.6,
  "utilidad_pct": 30.0
}
```

## Fórmula utilizada
1. `area_m2 = (ancho_mm * largo_mm) / 1_000_000`
2. `costo_con_merma = costo_pieza * (1 + merma_pct / 100)`
3. `costo_operativo = costo_con_merma + flete`
4. `costo_total = costo_operativo * (1 + comision_pct / 100)`
5. `utilidad_mxn = costo_total * (utilidad_pct / 100)`
6. `precio_sin_iva = costo_total + utilidad_mxn`
7. `precio_sugerido_pieza = precio_sin_iva * (1 + iva_pct / 100)`
8. `precio_m2 = precio_sugerido_pieza / area_m2`

## Validaciones y errores
- Si algún valor numérico no cumple reglas de negocio, la CLI retorna código `2` y muestra el error en stderr.
- Ejemplo:

```bash
python cotizador_rapido.py --ancho-mm 0 --largo-mm 1200 --costo-pieza 200 --merma-pct 10 --flete 20 --comision-pct 5 --iva-pct 16 --utilidad-pct 30
```

Respuesta:

```text
Error de validación: ancho_mm debe ser mayor a 0.
```

## Pruebas
Incluye 10 casos de prueba automatizados.

```bash
python -m unittest discover -s tests -v
```
