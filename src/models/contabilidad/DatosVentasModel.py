from datetime import datetime
class DatosVentas:
    def __init__(
            self, 
            ruc,
            razon_social,
            periodo, 
            CAR_sunat, 
            fecha_emision,
            fecha_vcto_pago,
            id_tipo_CP, 
            serie_CP, 
            num_CP,
            num_final,
            id_tipo_doc_CP, 
            num_doc_CP, 
            razon_social_CP,
            valor_facturado,
            BI_Gravada, 
            dscto_BI, 
            IGV_IPM, 
            dscto_IGV_IPM,
            monto_exonerado, 
            monto_inafecto, 
            ISC, 
            bi_Grav_IVAP, 
            IVAP, 
            ICBPER, 
            otros_Tributos,
            total,
            moneda,
            tipo_cambio):
        
        self.ruc = ruc
        self.num_doc_CP = num_doc_CP if num_doc_CP != '-' else None
        self.razon_social_CP = razon_social_CP if razon_social_CP != '-' else None
        self.id_tipo_doc_CP = id_tipo_doc_CP if id_tipo_doc_CP != '-' else None
        self.id_tipo_CP = id_tipo_CP
        self.serie_CP = serie_CP
        self.car_sunat = CAR_sunat
        self.num_CP = num_CP
        self.fecha_emision = fecha_emision
        self.periodo = periodo
        self.bi_gravada = BI_Gravada
        self.dscto_BI = dscto_BI
        self.igv_ipm = IGV_IPM
        self.dscto_IGV_IPM = dscto_IGV_IPM
        self.monto_exonerado = monto_exonerado
        self.monto_inafecto = monto_inafecto
        self.isc = ISC
        self.bi_Grav_IVAP = bi_Grav_IVAP
        self.ivap = IVAP
        self.icbper = ICBPER
        self.otros_Tributos = otros_Tributos
        self.id_estado_CP = 0
        self.total = float(total)
        self.moneda = moneda
        self.tipo_cambio = tipo_cambio
    

    def __str__(self):
        return (
            f"DatosVentas:\n"
            f"  RUC: {self.ruc}\n"
            f"  Periodo: {self.periodo}\n"
            f"  CAR SUNAT: {self.car_sunat}\n"
            f"  Fecha Emisión: {self.fecha_emision}\n"
            f"  Tipo CP: {self.id_tipo_CP}\n"
            f"  Serie CP: {self.serie_CP}\n"
            f"  Número CP: {self.num_CP}\n"
            f"  Tipo Doc CP: {self.id_tipo_doc_CP}\n"
            f"  Número Doc CP: {self.num_doc_CP}\n"
            f"  Razón Social CP: {self.razon_social_CP}\n"
            f"  Base Imponible Gravada: {self.bi_gravada}\n"
            f"  Descuento BI: {self.dscto_BI}\n"
            f"  IGV/IPM: {self.igv_ipm}\n"
            f"  Descuento IGV/IPM: {self.dscto_IGV_IPM}\n"
            f"  Monto Exonerado: {self.monto_exonerado}\n"
            f"  Monto Inafecto: {self.monto_inafecto}\n"
            f"  ISC: {self.isc}\n"
            f"  Base Imponible Gravada IVAP: {self.bi_Grav_IVAP}\n"
            f"  IVAP: {self.ivap}\n"
            f"  ICBPER: {self.icbper}\n"
            f"  Otros Tributos: {self.otros_Tributos}\n"
            f"  Total: {self.total}\n"
            f"  Moneda: {self.moneda}\n"
            f"  Tipo Cambio: {self.tipo_cambio}\n"
        )
    
    def __repr__(self) -> str:
        return self.ruc