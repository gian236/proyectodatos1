from .database import Base
from sqlalchemy import Column, Integer, VARCHAR, Date, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    codigo_cliente = Column(VARCHAR(50), unique=True, index=True)
    rol_id = Column(Integer, ForeignKey('roles.rol_id'), index=True)
    genero = Column(String, index=True)
    cui = Column(VARCHAR(20), unique=True, index=True)
    fecha_nacimiento = Column(Date, index=True)
    estado_civil = Column(VARCHAR(50), index=True)
    nacionalidad = Column(VARCHAR(50), index=True)
    primer_nombre = Column(VARCHAR(100), index=True)
    segundo_nombre = Column(VARCHAR(100), index=True)
    tercer_nombre = Column(VARCHAR(100), index=True)
    primer_apellido = Column(VARCHAR(100), index=True)
    segundo_apellido = Column(VARCHAR(100), index=True)
    apellido_casada = Column(VARCHAR(100), index=True)
    ocupaciones_id = Column(Integer, ForeignKey('ocupaciones.ocupacion_id'), index=True)

    direccion = relationship("DireccionUser", back_populates="usuarios")
    prestamos = relationship("Prestamos", back_populates="usuario")
    referencias = relationship("Referencias", back_populates="usuario")
    rol = relationship("Roles", back_populates="usuarios")
    ocupacion = relationship("Ocupaciones", back_populates="usuarios")


class CargosAdmin(Base):
    __tablename__ = "cargos_administrativos"

    cargos_id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamo.prestamo_id"), index=True)
    prestamo_iva = Column(Float, index=True, default=0.0)
    prestamo_cargos_administrativos = Column(Float, index=True, default=0.0)
    prestamo_total = Column(Float, index=True, default=0.0)

    prestamo = relationship("Prestamos", back_populates="cargos_administrativos")


class DireccionUser(Base):
    __tablename__ = "direccion_usuario"

    direccion_usuario_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), index=True)
    depto_nacimiento = Column(VARCHAR(100), index=True)
    muni_nacimiento = Column(VARCHAR(100), index=True)
    vecindad = Column(VARCHAR(100), index=True)

    usuarios = relationship("User", back_populates="direccion")


class Ocupaciones(Base):
    __tablename__ = "ocupaciones"

    ocupacion_id = Column(Integer, primary_key=True, index=True)
    nombre_ocupacion = Column(VARCHAR(100), index=True)

    usuarios = relationship("User", back_populates="ocupacion")


class PagosRealizados(Base):
    __tablename__ = "pagos_realizados"

    pago_realizado_id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamo.prestamo_id"), index=True)
    pago_realizado_fecha_creacion = Column(DateTime, index=True)
    pago_realizado_fecha_pago = Column(DateTime, index=True)
    pago_realizado_monto_pagado = Column(Float, index=True)
    pago_realizado_correlativo = Column(String(50), nullable=False)
    validacion1_validado_por = Column(VARCHAR(100), ForeignKey("validadores.validador_id"), index=True)
    estado = Column(String(20), default="pendiente", index=True)
    codigo_transaccion = Column(VARCHAR(50), unique=True, nullable=True)
    monto_pagado = Column(Float, nullable=True, default=0.0)

    prestamo = relationship("Prestamos", back_populates="pagos_realizados")
    validador1 = relationship("Validadores", foreign_keys=[validacion1_validado_por])


class Prestamos(Base):
    __tablename__ = "prestamo"

    prestamo_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), index=True)
    codigo_prestamo = Column(VARCHAR(50), index=True)
    motivo_prestamo = Column(Text, index=True)
    prestamo_estatus_id = Column(Integer, ForeignKey("prestamo_estatus.estatus_id"), index=True)
    monto_solicitado = Column(Float, index=True)
    cuotas_pactadas = Column(Integer, index=True)
    porcentaje_interes = Column(Float, nullable=False, default=0.0)

    usuario = relationship("User", back_populates="prestamos")
    estatus = relationship("PrestamoEstatus", back_populates="prestamo")
    cargos_administrativos = relationship("CargosAdmin", back_populates="prestamo")
    pagos_realizados = relationship("PagosRealizados", back_populates="prestamo")
    pagos_futuros = relationship("PagosFuturos", back_populates="prestamo")


class PrestamoEstatus(Base):
    __tablename__ = "prestamo_estatus"

    estatus_id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(VARCHAR(100), index=True)

    prestamo = relationship("Prestamos", back_populates="estatus")


class Referencias(Base):
    __tablename__ = "referencias"

    referencia_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), index=True)

    referencia1_primer_nombre = Column(VARCHAR(100), index=True)
    referencia1_segundo_nombre = Column(VARCHAR(100), index=True)
    referencia1_tercer_nombre = Column(VARCHAR(100), index=True)
    referencia1_primer_apellido = Column(VARCHAR(100), index=True)
    referencia1_segundo_apellido = Column(VARCHAR(100), index=True)
    referencia1_telefono = Column(VARCHAR(20), index=True)
    referencia2_primer_nombre = Column(VARCHAR(100), index=True)
    referencia2_segundo_nombre = Column(VARCHAR(100), index=True)
    referencia2_tercer_nombre = Column(VARCHAR(100), index=True)
    referencia2_primer_apellido = Column(VARCHAR(100), index=True)
    referencia2_segundo_apellido = Column(VARCHAR(100), index=True)
    referencia2_telefono = Column(VARCHAR(20), index=True)
    referencia3_primer_nombre = Column(VARCHAR(100), index=True)
    referencia3_segundo_nombre = Column(VARCHAR(100), index=True)
    referencia3_tercer_nombre = Column(VARCHAR(100), index=True)
    referencia3_primer_apellido = Column(VARCHAR(100), index=True)
    referencia3_segundo_apellido = Column(VARCHAR(100), index=True)
    referencia3_telefono = Column(VARCHAR(20), index=True)
    referencia4_primer_nombre = Column(VARCHAR(100), index=True)
    referencia4_segundo_nombre = Column(VARCHAR(100), index=True)
    referencia4_tercer_nombre = Column(VARCHAR(100), index=True)
    referencia4_primer_apellido = Column(VARCHAR(100), index=True)
    referencia4_segundo_apellido = Column(VARCHAR(100), index=True)
    referencia4_telefono = Column(VARCHAR(20), index=True)

    usuario = relationship("User", back_populates="referencias")


class Roles(Base):
    __tablename__ = "roles"

    rol_id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(VARCHAR(100), index=True)
    descripcion = Column(Text, index=True)

    usuarios = relationship("User", back_populates="rol")


class Validadores(Base):
    __tablename__ = "validadores"

    validador_id = Column(VARCHAR(100), primary_key=True, index=True)
    validador_nombre = Column(VARCHAR(100), index=True)

    pagos_realizados = relationship("PagosRealizados", back_populates="validador1")


class PagosFuturos(Base):
    __tablename__ = "pagos_futuros"

    pago_id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamo.prestamo_id"), index=True)
    fecha_pago = Column(Date, index=True, nullable=False)
    monto_pago = Column(Float, index=True, nullable=False)
    estado = Column(String(20), default="pendiente", index=True)

    prestamo = relationship("Prestamos", back_populates="pagos_futuros")
