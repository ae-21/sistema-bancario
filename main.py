"""Programa principal con menú interactivo y manejo específico de excepciones."""

import logging
from excepciones import (
    CuentaBloqueadaError,
    CuentaNoEncontradaError,
    LimiteDiarioExcedidoError,
    MontoInvalidoError,
    SaldoInsuficienteError,
)
from modelos import Banco

logging.basicConfig(
    filename="errores_banco.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("SistemaBancario")


def leer_monto(texto: str = "Ingresa el monto: ") -> float:
    """Lee un número decimal del usuario y traduce errores de formato con 'from'."""
    entrada = input(texto).strip().replace(",", ".")
    try:
        return float(entrada)
    except ValueError as exc:
        raise MontoInvalidoError(entrada) from exc


def registrar_error(codigo: str, detalle: str) -> None:
    """Guarda el error en el archivo log y muestra un aviso amigable en pantalla."""
    logger.error("[%s] %s", codigo, detalle)
    print(f"\n⚠️  Error ({codigo}): {detalle}")


def mostrar_menu(banco: Banco) -> None:
    """Muestra el menú principal del banco digital."""
    total = Banco.total_cuentas(banco)
    print("\n" + "=" * 45)
    print(f"   {banco.nombre}  |  Cuentas activas: {total}")
    print("=" * 45)
    print("1. Crear cuenta")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Transferir")
    print("5. Consultar saldo")
    print("6. Bloquear/desbloquear cuenta")
    print("7. Ver historial")
    print("8. Salir")
    print("=" * 45)


def ejecutar() -> None:
    """Ejecuta el ciclo principal del sistema bancario."""
    banco = Banco("Banco Digital")

    while True:
        mostrar_menu(banco)
        opcion = input("Elige una opción (1-8): ").strip()

        try:
            if opcion == "1":
                numero = input("Número de cuenta: ").strip()
                titular = input("Nombre del titular: ").strip()
                saldo_inicial = leer_monto("Saldo inicial: ")
                cuenta = banco.crear_cuenta(numero, titular, saldo_inicial)
                print(
                    f"✅ Cuenta {cuenta.numero} creada para {cuenta.titular} "
                    f"con saldo ${cuenta.saldo:.2f}."
                )

            elif opcion == "2":
                numero = input("Número de cuenta: ").strip()
                cuenta = banco.obtener_cuenta(numero)
                monto = leer_monto("Monto a depositar: ")
                cuenta.depositar(monto)
                print(f"✅ Depósito realizado. Nuevo saldo: ${cuenta.saldo:.2f}")

            elif opcion == "3":
                numero = input("Número de cuenta: ").strip()
                cuenta = banco.obtener_cuenta(numero)
                monto = leer_monto("Monto a retirar: ")
                cuenta.retirar(monto)
                print(f"✅ Retiro realizado. Nuevo saldo: ${cuenta.saldo:.2f}")

            elif opcion == "4":
                origen = input("Cuenta origen: ").strip()
                destino = input("Cuenta destino: ").strip()
                monto = leer_monto("Monto a transferir: ")
                banco.transferir(origen, destino, monto)
                print("✅ Transferencia completada con éxito.")

            elif opcion == "5":
                numero = input("Número de cuenta: ").strip()
                cuenta = banco.obtener_cuenta(numero)
                saldo_actual = cuenta.consultar_saldo()
                print(f"💰 Saldo de la cuenta {cuenta.numero}: ${saldo_actual:.2f}")

            elif opcion == "6":
                numero = input("Número de cuenta: ").strip()
                cuenta = banco.obtener_cuenta(numero)
                if cuenta.esta_bloqueada():
                    cuenta.desbloquear()
                    print(f"🔓 La cuenta {cuenta.numero} ahora está DESBLOQUEADA.")
                else:
                    cuenta.bloquear()
                    print(f"🔒 La cuenta {cuenta.numero} ahora está BLOQUEADA.")

            elif opcion == "7":
                numero = input("Número de cuenta: ").strip()
                cuenta = banco.obtener_cuenta(numero)
                print(f"\n📜 Historial de la cuenta {cuenta.numero} ({cuenta.titular}):")
                for evento in cuenta.mostrar_historial():
                    print("  -", evento)

            elif opcion == "8":
                print("👋 ¡Gracias por usar el Banco Digital! Hasta pronto.")
                break

            else:
                print("❌ Opción no válida. Escribe un número del 1 al 8.")

        except CuentaNoEncontradaError as err:
            registrar_error(err.codigo, str(err))
        except CuentaBloqueadaError as err:
            registrar_error(err.codigo, str(err))
        except MontoInvalidoError as err:
            registrar_error(err.codigo, str(err))
        except SaldoInsuficienteError as err:
            registrar_error(err.codigo, str(err))
        except LimiteDiarioExcedidoError as err:
            registrar_error(err.codigo, str(err))
        except ValueError as err:
            registrar_error("DATO_INVALIDO", str(err))


if __name__ == "__main__":
    ejecutar()