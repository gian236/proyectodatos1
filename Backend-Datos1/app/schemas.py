from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date , datetime


class DireccionCreate(BaseModel):
    depto_nacimiento: str
    muni_nacimiento: str
    vecindad: str


class ReferenciaBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    tercer_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    telefono: str


class ReferenciaCreate(BaseModel):
    referencia1: ReferenciaBase
    referencia2: ReferenciaBase
    referencia3: Optional[ReferenciaBase] = None
    referencia4: Optional[ReferenciaBase] = None


class ClienteSolicitud(BaseModel):
    genero: str
    cui: str
    fecha_nacimiento: date
    estado_civil: str
    nacionalidad: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    tercer_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    apellido_casada: Optional[str] = None
    ocupacion: str  # Nombre de la ocupación
    direccion: DireccionCreate
    referencias: ReferenciaCreate
    monto_prestamo: float
    motivo_prestamo: str
    cuotas_pactadas: int  # Valor entre 1 y 12


class PrestamoResponse(BaseModel):
    message: str
    usuario_id: int
    codigo_prestamo: str
    prestamo_id: int
    cargo_admin_id: int
    monto_solicitado: float
    cuotas_pactadas: int
    porcentaje_interes: float
    prestamo_estatus_id: int

class PrestamoUpdate(BaseModel):
    porcentaje_interes: float
    monto_solicitado: float
    prestamo_iva: float
    prestamo_cargos_administrativos: float


class PrestamoEstadoUpdate(BaseModel):
    estado: str
    fecha_aprobacion: str


class PrestamoCuota(BaseModel):
    fecha_pago: str
    monto_cuota: float


class PrestamoResponse(BaseModel):
    prestamo_id: int
    usuario_id: int
    monto_solicitado: float
    cuotas_pactadas: int
    porcentaje_interes: float
    prestamo_estatus_id: int
    codigo_prestamo: str

class ComprobantePagoRequest(BaseModel):
    codigo_prestamo: str
    codigo_transaccion: str
    monto_pagado: float

class PrestamoDetalleResponse(BaseModel):
    prestamo_id: int
    monto_solicitado: float
    cuotas_pactadas: int
    porcentaje_interes: float
    pagos_realizados: List[Any]
    pagos_futuros: List[Any]
    proximo_pago: dict

class EstadoComprobante(BaseModel):
    aprobado: bool

class PagoRealizado(BaseModel):
    pago_realizado_id: int
    fecha_pago: datetime
    monto_pagado: float
    estado: str
    codigo_transaccion: str


class PagoFuturo(BaseModel):
    pago_id: int
    fecha_pago: date
    monto_pago: float
    estado: str


class PrestamoDetalle(BaseModel):
    prestamo_id: int
    codigo_prestamo: str
    monto_solicitado: float
    cuotas_pactadas: int
    porcentaje_interes: float
    pagos_realizados: List[PagoRealizado]
    pagos_futuros: List[PagoFuturo]


class RegistroComprobante(BaseModel):
    fecha_pago: datetime
    monto_pagado: float
    codigo_transaccion: str


class RegistroComprobanteResponse(BaseModel):
    message: str
    pago_realizado_id: int


class AprobarDenegarPagoResponse(BaseModel):
    message: str
    pago_realizado_id: int

