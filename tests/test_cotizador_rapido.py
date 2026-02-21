import json
import subprocess
import sys
import unittest

from cotizador_rapido import CotizacionInput, calcular_cotizacion, validar_entrada


class CotizadorRapidoTests(unittest.TestCase):
    def test_calculo_base(self):
        entrada = CotizacionInput(600, 1200, 200, 10, 20, 5, 16, 30)
        out = calcular_cotizacion(entrada)
        self.assertEqual(out.precio_sugerido_pieza, 380.02)
        self.assertEqual(out.precio_m2, 527.8)
        self.assertEqual(out.utilidad_mxn, 75.6)
        self.assertEqual(out.utilidad_pct, 30.0)

    def test_sin_porcentajes_adicionales(self):
        entrada = CotizacionInput(1000, 1000, 100, 0, 0, 0, 0, 0)
        out = calcular_cotizacion(entrada)
        self.assertEqual(out.precio_sugerido_pieza, 100.0)
        self.assertEqual(out.precio_m2, 100.0)
        self.assertEqual(out.utilidad_mxn, 0.0)
        self.assertEqual(out.utilidad_pct, 0.0)

    def test_merma_incrementa_costo(self):
        base = calcular_cotizacion(CotizacionInput(500, 500, 100, 0, 0, 0, 0, 10))
        con_merma = calcular_cotizacion(CotizacionInput(500, 500, 100, 20, 0, 0, 0, 10))
        self.assertGreater(con_merma.precio_sugerido_pieza, base.precio_sugerido_pieza)

    def test_flete_incrementa_precio(self):
        base = calcular_cotizacion(CotizacionInput(500, 500, 100, 0, 0, 0, 0, 10))
        con_flete = calcular_cotizacion(CotizacionInput(500, 500, 100, 0, 50, 0, 0, 10))
        self.assertGreater(con_flete.precio_sugerido_pieza, base.precio_sugerido_pieza)

    def test_rechaza_ancho_cero(self):
        with self.assertRaisesRegex(ValueError, "ancho_mm"):
            validar_entrada(CotizacionInput(0, 1000, 100, 10, 10, 10, 16, 20))

    def test_rechaza_largo_negativo(self):
        with self.assertRaisesRegex(ValueError, "largo_mm"):
            validar_entrada(CotizacionInput(600, -1, 100, 10, 10, 10, 16, 20))

    def test_rechaza_costo_no_positivo(self):
        with self.assertRaisesRegex(ValueError, "costo_pieza"):
            validar_entrada(CotizacionInput(600, 1200, 0, 10, 10, 10, 16, 20))

    def test_rechaza_merma_negativa(self):
        with self.assertRaisesRegex(ValueError, "merma_pct"):
            validar_entrada(CotizacionInput(600, 1200, 100, -5, 10, 10, 16, 20))

    def test_rechaza_iva_negativo(self):
        with self.assertRaisesRegex(ValueError, "iva_pct"):
            validar_entrada(CotizacionInput(600, 1200, 100, 5, 10, 10, -1, 20))

    def test_cli_salida_json(self):
        cmd = [
            sys.executable,
            "cotizador_rapido.py",
            "--ancho-mm",
            "600",
            "--largo-mm",
            "1200",
            "--costo-pieza",
            "200",
            "--merma-pct",
            "10",
            "--flete",
            "20",
            "--comision-pct",
            "5",
            "--iva-pct",
            "16",
            "--utilidad-pct",
            "30",
        ]
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIn("precio_sugerido_pieza", data)
        self.assertIn("precio_m2", data)
        self.assertIn("utilidad_mxn", data)
        self.assertIn("utilidad_pct", data)


if __name__ == "__main__":
    unittest.main()
