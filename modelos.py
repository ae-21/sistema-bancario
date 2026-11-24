"""Clases principales del sistema bancario: CuentaBancaria y Banco."""

from datetime import datetime
from excepciones import (
    BancoError,
    CuentaBloqueadaError,
    CuentaNoEncontradaError,
    LimiteDiarioExcedidoError,
    MontoInvalidoError,
    SaldoInsuficienteError,
)


class CuentaBancaria:
    """Representa una cuenta bancaria individual con historial y límite diario."""

    LIMITE_DIARIO_DEFECTO = 5000.0

    def __init__(
        self,
        numero: str,
        titular: str,
        saldo_inicial: float = 0.0,
        limite_diario: float = LIMITE_DIARIO_DEFECTO,
    ) -> None:
        """Inicializa una cuenta bancaria validando el saldo inicial."""
        if saldo_inicial < 0:
            raise MontoInvalidoError(saldo_inicial)

        self.numero = numero.strip()
        self.titular = titular.strip()
        self._saldo = float(saldo_inicial)
        self._bloqueada = False
        self._retirado_hoy = 0.0
        self._limite_diario = float(limite_diario)
        self._historial: list[str] = []

        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._historial.append(
            f"[{marca}] Cuenta creada para {self.titular} con saldo inicial ${self._saldo:.2f}"
        )

    @property
    def saldo(self) -> float:
        """Devuelve el saldo actual en modo de solo lectura."""
        return self._saldo

    def _validar_monto_positivo(self, monto: float) -> None:
        """Verifica que el monto sea un número positivo mayor que cero."""
        if isinstance(monto, bool) or not isinstance(monto, (int, float)) or monto <= 0:
            raise MontoInvalidoError(monto)

    def _validar_no_bloqueada(self) -> None:
        """Verifica que la cuenta no se encuentre bloqueada."""
        if self._bloqueada:
            raise CuentaBloqueadaError(self.numero)

    def depositar(self, monto: float) -> None:
        """Deposita dinero en la cuenta si está activa y el monto es válido."""
        self._validar_no_bloqueada()
        self._validar_monto_positivo(monto)

        monto_val = float(monto)
        self._saldo = round(self._saldo + monto_val, 2)
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._historial.append(
            f"[{marca}] Depósito: +${monto_val:.2f} | Saldo: ${self._saldo:.2f}"
        )

    def retirar(self, monto: float) -> None:
        """Retira dinero validando bloqueo, monto, límite diario y saldo disponible."""
        self._validar_no_bloqueada()
        self._validar_monto_positivo(monto)

        monto_val = float(monto)

        if self._retirado_hoy + monto_val > self._limite_diario:
            raise LimiteDiarioExcedidoError(
                limite=self._limite_diario,
                retirado_hoy=self._retirado_hoy,
                monto_solicitado=monto_val,
            )

        if monto_val > self._saldo:
            raise SaldoInsuficienteError(
                saldo_actual=self._saldo,
                monto_solicitado=monto_val,
            )

        self._saldo = round(self._saldo - monto_val, 2)
        self._retirado_hoy = round(self._retirado_hoy + monto_val, 2)
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._historial.append(
            f"[{marca}] Retiro: -${monto_val:.2f} | Saldo: ${self._saldo:.2f}"
        )

    def consultar_saldo(self) -> float:
        """Consulta y devuelve el saldo actual de la cuenta."""
        self._validar_no_bloqueada()
        return self._saldo

    def bloquear(self) -> None:
        """Bloquea la cuenta para impedir operaciones."""
        self._bloqueada = True
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._historial.append(f"[{marca}] Cuenta BLOQUEADA")

    def desbloquear(self) -> None:
        """Desbloquea la cuenta para permitir operaciones nuevamente."""
        self._bloqueada = False
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._historial.append(f"[{marca}] Cuenta DESBLOQUEADA")

    def esta_bloqueada(self) -> bool:
        """Indica si la cuenta está bloqueada."""
        return self._bloqueada

    def mostrar_historial(self) -> list[str]:
        """Devuelve la lista de movimientos registrados en la cuenta."""
        return list(self._historial)


class Banco:
    """Administra múltiples cuentas bancarias y operaciones entre ellas."""

    def __init__(self, nombre: str = "Banco Digital") -> None:
        """Inicializa el banco con un diccionario vacío de cuentas."""
        self.nombre = nombre
        self._cuentas: dict[str, CuentaBancaria] = {}

    def crear_cuenta(
        self, numero: str, titular: str, saldo_inicial: float = 0.0
    ) -> CuentaBancaria:
        """Crea una cuenta nueva si el número no está duplicado."""
        numero_limpio = numero.strip()
        if not numero_limpio:
            raise ValueError("El número de cuenta no puede estar vacío.")

        if numero_limpio in self._cuentas:
            raise ValueError(f"Ya existe una cuenta con el número {numero_limpio}.")

        try:
            cuenta = CuentaBancaria(
                numero=numero_limpio,
                titular=titular,
                saldo_inicial=saldo_inicial,
            )
        except MontoInvalidoError:
            raise

        self._cuentas[numero_limpio] = cuenta
        return cuenta

    def obtener_cuenta(self, numero: str) -> CuentaBancaria:
        """Busca una cuenta por número o lanza CuentaNoEncontradaError."""
        numero_limpio = numero.strip()
        if numero_limpio not in self._cuentas:
            raise CuentaNoEncontradaError(numero_limpio)
        return self._cuentas[numero_limpio]

    def transferir(self, origen: str, destino: str, monto: float) -> None:
        """Transfiere dinero entre dos cuentas usando try/except/else/finally."""
        cuenta_origen = self.obtener_cuenta(origen)
        cuenta_destino = self.obtener_cuenta(destino)

        if isinstance(monto, bool) or not isinstance(monto, (int, float)) or monto <= 0:
            raise MontoInvalidoError(monto)

        monto_val = float(monto)
        retiro_exitoso = False

        try:
            cuenta_origen.retirar(monto_val)
            retiro_exitoso = True
            cuenta_destino.depositar(monto_val)
        except BancoError:
            if retiro_exitoso:
                cuenta_origen._saldo = round(cuenta_origen._saldo + monto_val, 2)
                cuenta_origen._retirado_hoy = round(
                    max(0.0, cuenta_origen._retirado_hoy - monto_val), 2
                )
            raise
        except TypeError as exc:
            raise MontoInvalidoError(monto) from exc
        else:
            marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cuenta_origen._historial.append(
                f"[{marca}] Transferencia enviada a {cuenta_destino.numero}: -${monto_val:.2f}"
            )
            cuenta_destino._historial.append(
                f"[{marca}] Transferencia recibida de {cuenta_origen.numero}: +${monto_val:.2f}"
            )
        finally:
            pass

    @classmethod
    def total_cuentas(cls, banco_instancia: "Banco") -> int:
        """Devuelve el total de cuentas registradas en el banco."""
        return len(banco_instancia._cuentas)