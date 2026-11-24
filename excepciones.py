"""Módulo de excepciones personalizadas para el sistema bancario."""


class BancoError(Exception):
    """Excepción base para todos los errores del dominio bancario."""

    def __init__(self, mensaje: str, codigo: str = "ERROR_BANCO") -> None:
        super().__init__(mensaje)
        self.codigo = codigo


class SaldoInsuficienteError(BancoError):
    """Se lanza cuando una cuenta no tiene saldo suficiente para un retiro o transferencia."""

    def __init__(self, saldo_actual: float, monto_solicitado: float) -> None:
        self.saldo_actual = saldo_actual
        self.monto_solicitado = monto_solicitado
        self.deficit = round(monto_solicitado - saldo_actual, 2)
        mensaje = (
            f"Saldo insuficiente: tienes ${saldo_actual:.2f}, "
            f"necesitas ${monto_solicitado:.2f} (faltan ${self.deficit:.2f})"
        )
        super().__init__(mensaje=mensaje, codigo="SALDO_INSUFICIENTE")


class CuentaNoEncontradaError(BancoError):
    """Se lanza cuando se busca o usa un número de cuenta que no existe."""

    def __init__(self, numero_cuenta: str) -> None:
        self.numero_cuenta = numero_cuenta
        mensaje = f"La cuenta {numero_cuenta} no existe"
        super().__init__(mensaje=mensaje, codigo="CUENTA_NO_ENCONTRADA")


class CuentaBloqueadaError(BancoError):
    """Se lanza cuando se intenta operar con una cuenta que está bloqueada."""

    def __init__(self, numero_cuenta: str) -> None:
        self.numero_cuenta = numero_cuenta
        mensaje = f"La cuenta {numero_cuenta} está bloqueada"
        super().__init__(mensaje=mensaje, codigo="CUENTA_BLOQUEADA")


class MontoInvalidoError(BancoError):
    """Se lanza cuando el monto ingresado es menor o igual a cero o no es válido."""

    def __init__(self, monto: float) -> None:
        self.monto = monto
        mensaje = f"Monto inválido: {monto}. Debe ser positivo"
        super().__init__(mensaje=mensaje, codigo="MONTO_INVALIDO")


class LimiteDiarioExcedidoError(BancoError):
    """Se lanza cuando un retiro supera el límite diario permitido."""

    def __init__(
        self, limite: float, retirado_hoy: float, monto_solicitado: float
    ) -> None:
        self.limite = limite
        self.retirado_hoy = retirado_hoy
        self.monto_solicitado = monto_solicitado
        mensaje = (
            f"Límite diario excedido: límite ${limite:.2f}, "
            f"retirado hoy ${retirado_hoy:.2f}, solicitado ${monto_solicitado:.2f}"
        )
        super().__init__(mensaje=mensaje, codigo="LIMITE_EXCEDIDO")