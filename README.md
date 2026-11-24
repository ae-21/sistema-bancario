# Sistema Bancario con Excepciones Personalizadas

**Autora:** Aylín Aseret Rosales Luévano  
**Actividad:** Actividad 2 — Sistema Bancario con Excepciones Personalizadas

## Descripción

Aplicación en Python orientada a objetos que gestiona cuentas bancarias y operaciones mediante una jerarquía de excepciones personalizadas, traducción y encadenamiento de errores (`raise ... from ...`), bloques `try / except / else / finally` y registro de incidencias en `errores_banco.log`.

## Estructura del repositorio

- `excepciones.py`: Define `BancoError` y las excepciones específicas (`SaldoInsuficienteError`, `CuentaNoEncontradaError`, `CuentaBloqueadaError`, `MontoInvalidoError`, `LimiteDiarioExcedidoError`) con sus atributos y códigos.
- `modelos.py`: Implementa `CuentaBancaria` y `Banco` con validaciones, límite diario, historial de movimientos, relanzamiento y `try / except / else / finally`.
- `main.py`: Menú interactivo de consola (opciones 1 a 8), captura específica de cada excepción y registro en log.

## Cómo ejecutar el programa

1. Clona o descarga el repositorio en tu computadora.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Ejecuta:
   ```bash
   python main.py
