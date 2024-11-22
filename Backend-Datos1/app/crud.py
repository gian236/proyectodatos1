from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from datetime import datetime, timedelta

router = APIRouter()

def get_ocupacion_by_name(db: Session, ocupacion_name: str):
    return db.query(models.Ocupaciones).filter(models.Ocupaciones.nombre_ocupacion == ocupacion_name).first()

def create_ocupacion(db: Session, ocupacion_name: str):
    ocupacion = models.Ocupaciones(nombre_ocupacion=ocupacion_name)
    db.add(ocupacion)
    db.commit()
    db.refresh(ocupacion)
    return ocupacion

@router.post("/prestamos/solicitud", response_model=schemas.PrestamoResponse)
def crear_solicitud_prestamo(
    cliente: schemas.ClienteSolicitud, db: Session = Depends(database.get_db)
):
    # 1. Verificar si la ocupación ya existe o crearla
    ocupacion = db.query(models.Ocupaciones).filter(models.Ocupaciones.nombre_ocupacion == cliente.ocupacion).first()
    if not ocupacion:
        ocupacion = models.Ocupaciones(nombre_ocupacion=cliente.ocupacion)
        db.add(ocupacion)
        db.commit()
        db.refresh(ocupacion)

    # 2. Verificar si el usuario ya existe
    usuario = db.query(models.User).filter(models.User.cui == cliente.cui).first()
    if not usuario:
        # Crear usuario si no existe
        usuario = models.User(
            codigo_cliente=f"U-{cliente.cui[-4:]}",
            genero=cliente.genero,
            cui=cliente.cui,
            fecha_nacimiento=cliente.fecha_nacimiento,
            estado_civil=cliente.estado_civil,
            nacionalidad=cliente.nacionalidad,
            primer_nombre=cliente.primer_nombre,
            segundo_nombre=cliente.segundo_nombre,
            tercer_nombre=cliente.tercer_nombre,
            primer_apellido=cliente.primer_apellido,
            segundo_apellido=cliente.segundo_apellido,
            apellido_casada=cliente.apellido_casada,
            ocupaciones_id=ocupacion.ocupacion_id,
            rol_id=2,  # Rol de cliente
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    # 3. Crear dirección del usuario
    direccion = models.DireccionUser(
        usuario_id=usuario.usuario_id,
        depto_nacimiento=cliente.direccion.depto_nacimiento,
        muni_nacimiento=cliente.direccion.muni_nacimiento,
        vecindad=cliente.direccion.vecindad,
    )
    db.add(direccion)

    # 4. Crear referencias personales
    referencias = models.Referencias(
        usuario_id=usuario.usuario_id,
        referencia1_primer_nombre=cliente.referencias.referencia1.primer_nombre,
        referencia1_segundo_nombre=cliente.referencias.referencia1.segundo_nombre,
        referencia1_tercer_nombre=cliente.referencias.referencia1.tercer_nombre,
        referencia1_primer_apellido=cliente.referencias.referencia1.primer_apellido,
        referencia1_segundo_apellido=cliente.referencias.referencia1.segundo_apellido,
        referencia1_telefono=cliente.referencias.referencia1.telefono,
        referencia2_primer_nombre=cliente.referencias.referencia2.primer_nombre,
        referencia2_segundo_nombre=cliente.referencias.referencia2.segundo_nombre,
        referencia2_tercer_nombre=cliente.referencias.referencia2.tercer_nombre,
        referencia2_primer_apellido=cliente.referencias.referencia2.primer_apellido,
        referencia2_segundo_apellido=cliente.referencias.referencia2.segundo_apellido,
        referencia2_telefono=cliente.referencias.referencia2.telefono,
        referencia3_primer_nombre=cliente.referencias.referencia3.primer_nombre,
        referencia3_segundo_nombre=cliente.referencias.referencia3.segundo_nombre,
        referencia3_tercer_nombre=cliente.referencias.referencia3.tercer_nombre,
        referencia3_primer_apellido=cliente.referencias.referencia3.primer_apellido,
        referencia3_segundo_apellido=cliente.referencias.referencia3.segundo_apellido,
        referencia3_telefono=cliente.referencias.referencia3.telefono,
        referencia4_primer_nombre=cliente.referencias.referencia4.primer_nombre,
        referencia4_segundo_nombre=cliente.referencias.referencia4.segundo_nombre,
        referencia4_tercer_nombre=cliente.referencias.referencia4.tercer_nombre,
        referencia4_primer_apellido=cliente.referencias.referencia4.primer_apellido,
        referencia4_segundo_apellido=cliente.referencias.referencia4.segundo_apellido,
        referencia4_telefono=cliente.referencias.referencia4.telefono,
    )
    db.add(referencias)

    # 5. Crear el préstamo
    nuevo_prestamo = models.Prestamos(
        usuario_id=usuario.usuario_id,
        codigo_prestamo=f"P-{usuario.usuario_id}-{cliente.monto_prestamo:.0f}",
        motivo_prestamo=cliente.motivo_prestamo,
        prestamo_estatus_id=2,  # Estatus de pendiente
        monto_solicitado=cliente.monto_prestamo,
        cuotas_pactadas=cliente.cuotas_pactadas,
        porcentaje_interes=0,
    )
    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)

    # 6. Crear el cargo administrativo asociado al préstamo
    nuevo_cargo_admin = models.CargosAdmin(
        prestamo_id=nuevo_prestamo.prestamo_id,
        prestamo_iva=0.0,
        prestamo_cargos_administrativos=0.0,
        prestamo_total=0.0,
    )
    db.add(nuevo_cargo_admin)
    db.commit()

    # 7. Responder con los datos del préstamo
    return {
        "message": "Solicitud de préstamo creada con éxito",
        "usuario_id": usuario.usuario_id,
        "codigo_prestamo": nuevo_prestamo.codigo_prestamo,
        "prestamo_id": nuevo_prestamo.prestamo_id,
        "cargo_admin_id": nuevo_cargo_admin.cargos_id,
        "monto_solicitado": nuevo_prestamo.monto_solicitado,
        "cuotas_pactadas": nuevo_prestamo.cuotas_pactadas,
        "porcentaje_interes": nuevo_prestamo.porcentaje_interes,
        "prestamo_estatus_id": nuevo_prestamo.prestamo_estatus_id,
}
# Endpoint para obtener préstamos pendientes
@router.get("/prestamos/pendientes", response_model=list[schemas.PrestamoResponse])
def obtener_prestamos_pendientes(db: Session = Depends(database.get_db)):
    prestamos_pendientes = db.query(models.Prestamos).filter(
        models.Prestamos.prestamo_estatus_id == 2  # 2 representa "Pendiente"
    ).all()

    if not prestamos_pendientes:
        raise HTTPException(status_code=404, detail="No hay préstamos pendientes")
    return prestamos_pendientes


# Endpoint para obtener detalles de un préstamo específico
@router.get("/prestamos/{prestamo_id}", response_model=schemas.PrestamoResponse)
def obtener_detalles_prestamo(prestamo_id: int, db: Session = Depends(database.get_db)):
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.prestamo_id == prestamo_id).first()

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo


# Endpoint para actualizar datos del préstamo
@router.put("/prestamos/{prestamo_id}")
def actualizar_datos_prestamo(
    prestamo_id: int,
    prestamo_update: schemas.PrestamoUpdate,
    db: Session = Depends(database.get_db),
):
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.prestamo_id == prestamo_id).first()

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Actualizar datos del préstamo
    prestamo.porcentaje_interes = prestamo_update.porcentaje_interes
    prestamo.monto_solicitado = prestamo_update.monto_solicitado

    # Actualizar datos de cargos administrativos
    cargo_admin = db.query(models.CargosAdmin).filter(models.CargosAdmin.prestamo_id == prestamo_id).first()
    if not cargo_admin:
        raise HTTPException(status_code=404, detail="Cargos administrativos no encontrados")

    cargo_admin.prestamo_iva = prestamo_update.prestamo_iva
    cargo_admin.prestamo_cargos_administrativos = prestamo_update.prestamo_cargos_administrativos
    cargo_admin.prestamo_total = (
        prestamo.monto_solicitado
        + prestamo.monto_solicitado * prestamo.porcentaje_interes / 100
        + cargo_admin.prestamo_iva
        + cargo_admin.prestamo_cargos_administrativos
    )

    db.commit()
    db.refresh(prestamo)
    db.refresh(cargo_admin)

    return {
        "message": "Préstamo y cargos administrativos actualizados correctamente",
        "prestamo_id": prestamo.prestamo_id,
        "total_a_pagar": cargo_admin.prestamo_total,
    }


# Endpoint para aprobar el estado del préstamo
@router.put("/prestamos/{prestamo_id}/aprobar", response_model=schemas.PrestamoResponse)
def aprobar_prestamo(prestamo_id: int, db: Session = Depends(database.get_db)):
    # Obtener el préstamo
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.prestamo_id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Cambiar el estado a 'aprobado'
    prestamo.prestamo_estatus_id = 1  # Suponiendo que 1 = 'Aprobado'

    # Calcular el monto total
    cargos_admin = db.query(models.CargosAdmin).filter(models.CargosAdmin.prestamo_id == prestamo_id).first()
    if not cargos_admin:
        raise HTTPException(status_code=404, detail="Cargos administrativos no encontrados para este préstamo")
    
    monto_total = (
        float(prestamo.monto_solicitado)
        + float(cargos_admin.prestamo_iva)
        + float(cargos_admin.prestamo_cargos_administrativos)
    )
    monto_total += monto_total * (prestamo.porcentaje_interes / 100)
    cargos_admin.prestamo_total = monto_total

    # Guardar los cambios
    db.commit()
    db.refresh(prestamo)
    db.refresh(cargos_admin)

    return {
        "message": "Préstamo aprobado",
        "prestamo_id": prestamo.prestamo_id,
        "usuario_id": prestamo.usuario_id,
        "monto_solicitado": prestamo.monto_solicitado,
        "cuotas_pactadas": prestamo.cuotas_pactadas,
        "porcentaje_interes": prestamo.porcentaje_interes,
        "prestamo_estatus_id": prestamo.prestamo_estatus_id,
        "codigo_prestamo": prestamo.codigo_prestamo,
    }


@router.put("/prestamos/{prestamo_id}/denegar", response_model=schemas.PrestamoResponse)
def denegar_prestamo(prestamo_id: int, db: Session = Depends(database.get_db)):
    # Obtener el préstamo
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.prestamo_id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Cambiar el estado a 'denegado'
    prestamo.prestamo_estatus_id = 3  # Suponiendo que 3 = 'Denegado'

    # Guardar los cambios
    db.commit()
    db.refresh(prestamo)

    return {
        "message": "Préstamo denegado",
        "prestamo_id": prestamo.prestamo_id,
        "usuario_id": prestamo.usuario_id,
        "monto_solicitado": prestamo.monto_solicitado,
        "cuotas_pactadas": prestamo.cuotas_pactadas,
        "porcentaje_interes": prestamo.porcentaje_interes,
        "prestamo_estatus_id": prestamo.prestamo_estatus_id,
        "codigo_prestamo": prestamo.codigo_prestamo,
    }


@router.get("/prestamos/{codigo_prestamo}/detalle", response_model=schemas.PrestamoDetalleResponse)
def obtener_detalle_prestamo(codigo_prestamo: str, db: Session = Depends(database.get_db)):
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.codigo_prestamo == codigo_prestamo).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    pagos_realizados = db.query(models.PagosRealizados).filter(models.PagosRealizados.prestamo_id == prestamo.prestamo_id).all()
    pagos_futuros = db.query(models.PagosFuturos).filter(models.PagosFuturos.prestamo_id == prestamo.prestamo_id).all()

    detalle_proximo_pago = db.query(models.CargosAdmin).filter(models.CargosAdmin.prestamo_id == prestamo.prestamo_id).first()
    total_pago = prestamo.monto_solicitado + detalle_proximo_pago.prestamo_iva + detalle_proximo_pago.prestamo_cargos_administrativos

    return {
        "prestamo_id": prestamo.prestamo_id,
        "monto_solicitado": prestamo.monto_solicitado,
        "cuotas_pactadas": prestamo.cuotas_pactadas,
        "porcentaje_interes": prestamo.porcentaje_interes,
        "pagos_realizados": pagos_realizados,
        "pagos_futuros": pagos_futuros,
        "proximo_pago": {
            "total_pago": total_pago,
            "fecha_pago": pagos_futuros[0].fecha_pago if pagos_futuros else None
        }
    }


@router.post("/pagos/comprobante-general")
def registrar_comprobante_pago(
    comprobante: schemas.ComprobantePagoRequest, db: Session = Depends(database.get_db)
):
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.codigo_prestamo == comprobante.codigo_prestamo).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    # Aquí generas un correlativo, lo cual está bien para pago_realizado_correlativo.
    ultimo_pago = db.query(models.PagosRealizados).order_by(models.PagosRealizados.pago_realizado_id.desc()).first()
    correlativo = f"PAGO-{(ultimo_pago.pago_realizado_id + 1) if ultimo_pago else 1}"

    # Sin embargo, verifica que no estás intentando establecer manualmente pago_realizado_id.
    nuevo_pago = models.PagosRealizados(
        prestamo_id=prestamo.prestamo_id,
        pago_realizado_fecha_creacion=datetime.now(),
        pago_realizado_monto_pagado=comprobante.monto_pagado,
        codigo_transaccion=comprobante.codigo_transaccion,
        estado="pendiente",
        pago_realizado_correlativo=correlativo  # Esto está bien
    )
    db.add(nuevo_pago)  # pago_realizado_id se genera automáticamente aquí.
    db.commit()
    db.refresh(nuevo_pago)
    return {"message": "Comprobante registrado exitosamente", "pago_realizado_id": nuevo_pago.pago_realizado_id}



@router.put("/pagos/{pago_realizado_id}/validar")
def validar_comprobante(
    pago_realizado_id: int, estado: schemas.EstadoComprobante, db: Session = Depends(database.get_db)
):
    pago = db.query(models.PagosRealizados).filter(models.PagosRealizados.pago_realizado_id == pago_realizado_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    if estado.aprobado:
        pago.estado = "aprobado"
        # Actualizar estado del préstamo si todas las cuotas están pagadas
        prestamo = db.query(models.Prestamos).filter(models.Prestamos.prestamo_id == pago.prestamo_id).first()
        pagos_futuros = db.query(models.PagosFuturos).filter(models.PagosFuturos.prestamo_id == prestamo.prestamo_id, models.PagosFuturos.estado == "pendiente").all()
        if not pagos_futuros:
            prestamo.prestamo_estatus_id = 1  # Estatus aprobado
    else:
        pago.estado = "rechazado"

    db.commit()
    return {"message": f"Comprobante {'aprobado' if estado.aprobado else 'rechazado'} exitosamente"}

@router.get("/prestamos/{codigo_prestamo}/detalle", response_model=schemas.PrestamoDetalle)
def obtener_detalle_prestamo(codigo_prestamo: str, db: Session = Depends(database.get_db)):
    prestamo = db.query(models.Prestamos).filter(models.Prestamos.codigo_prestamo == codigo_prestamo).first()

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    pagos_realizados = db.query(models.PagosRealizados).filter(models.PagosRealizados.prestamo_id == prestamo.prestamo_id).all()
    pagos_futuros = db.query(models.PagosFuturos).filter(models.PagosFuturos.prestamo_id == prestamo.prestamo_id).all()

    return {
        "prestamo": prestamo,
        "pagos_realizados": pagos_realizados,
        "pagos_futuros": pagos_futuros
    }


@router.post("/pagos/{pago_id}/registrar-cuota", response_model=schemas.RegistroComprobanteResponse)
def registrar_comprobante_pago(
    pago_id: int,
    comprobante: schemas.RegistroComprobante,
    db: Session = Depends(database.get_db),
):
    # Buscar el pago futuro relacionado
    pago = db.query(models.PagosFuturos).filter(models.PagosFuturos.pago_id == pago_id).first()

    if not pago:
        raise HTTPException(status_code=404, detail="Pago futuro no encontrado")

    # Obtener el último pago realizado para generar el correlativo
    ultimo_pago = db.query(models.PagosRealizados).order_by(models.PagosRealizados.pago_realizado_id.desc()).first()
    correlativo = f"PAGO-{(ultimo_pago.pago_realizado_id + 1) if ultimo_pago else 1}"

    # Crear un nuevo registro en pagos realizados
    nuevo_pago_realizado = models.PagosRealizados(
        prestamo_id=pago.prestamo_id,
        pago_realizado_fecha_creacion=datetime.now(),  # Fecha actual como creación
        pago_realizado_fecha_pago=comprobante.fecha_pago,
        pago_realizado_monto_pagado=comprobante.monto_pagado,
        codigo_transaccion=comprobante.codigo_transaccion,
        estado="pendiente",  # Estado inicial del pago
        pago_realizado_correlativo=correlativo,  # Correlativo generado
    )

    # Guardar el nuevo pago en la base de datos
    db.add(nuevo_pago_realizado)
    db.commit()
    db.refresh(nuevo_pago_realizado)

    return {
        "message": "Comprobante registrado con estado pendiente",
        "pago_realizado_id": nuevo_pago_realizado.pago_realizado_id,
    }




@router.put("/pagos/{pago_realizado_id}/aprobar", response_model=schemas.AprobarDenegarPagoResponse)
def aprobar_pago(pago_realizado_id: int, db: Session = Depends(database.get_db)):
    pago_realizado = db.query(models.PagosRealizados).filter(models.PagosRealizados.pago_realizado_id == pago_realizado_id).first()

    if not pago_realizado:
        raise HTTPException(status_code=404, detail="Pago realizado no encontrado")

    if pago_realizado.estado != "pendiente":
        raise HTTPException(status_code=400, detail="Solo se pueden aprobar pagos pendientes")

    # Actualizar estado a aprobado
    pago_realizado.estado = "aprobado"
    db.commit()

    return {
        "message": "Pago aprobado exitosamente",
        "pago_realizado_id": pago_realizado.pago_realizado_id
    }


@router.put("/pagos/{pago_realizado_id}/denegar", response_model=schemas.AprobarDenegarPagoResponse)
def denegar_pago(pago_realizado_id: int, db: Session = Depends(database.get_db)):
    pago_realizado = db.query(models.PagosRealizados).filter(models.PagosRealizados.pago_realizado_id == pago_realizado_id).first()

    if not pago_realizado:
        raise HTTPException(status_code=404, detail="Pago realizado no encontrado")

    if pago_realizado.estado != "pendiente":
        raise HTTPException(status_code=400, detail="Solo se pueden denegar pagos pendientes")

    # Actualizar estado a denegado
    pago_realizado.estado = "denegado"
    db.commit()

    return {
        "message": "Pago denegado exitosamente",
        "pago_realizado_id": pago_realizado.pago_realizado_id
    }