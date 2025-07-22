from src.utils.tablas_sunat import TIPO_CP, ESTADO_CP, TIPO_DOCUMENTO
class DatosVentasRequest:
    def __init__(self, 
                 id_venta, 
                 ruc, 
                 serie_CP, 
                 num_CP, 
                 fecha_emision, 
                 cliente, 
                 periodo, 
                 razon_social, 
                 bi_gravada, 
                 monto_inafecto, 
                 igv_ipm, 
                 total,
                 estado_CP,
                 id_estado_CP,
                 id_tipo_CP,
                 tipo_CP):
        
        self.id = id_venta
        self.ruc = ruc
        self.serie_CP = serie_CP
        self.num_CP = num_CP
        self.fecha_emision = fecha_emision
        self.cliente = cliente
        self.periodo = periodo
        self.razon_social = razon_social
        self.bi_gravada = bi_gravada
        self.monto_inafecto = monto_inafecto
        self.igv_ipm = igv_ipm
        self.total = total
        self.estado_CP = estado_CP
        self.id_estado_CP = id_estado_CP
        self.id_tipo_CP = id_tipo_CP
        self.tipo_CP = tipo_CP
    
    def __repr__(self):
        return (
            f"DatosVentasRequest(\n"
            f"  ID Venta: {self.id}\n"
            f"  RUC: {self.ruc}\n"
            f"  Serie CP: {self.serie_CP}\n"
            f"  Número CP: {self.num_CP}\n"
            f"  Fecha Emisión: {self.fecha_emision}\n"
            f"  Cliente: {self.cliente}\n"
            f"  Periodo: {self.periodo}\n"
            f"  Razón Social: {self.razon_social}\n"
            f"  BI Gravada: {self.bi_gravada}\n"
            f"  Monto Inafecto: {self.monto_inafecto}\n"
            f"  IGV/IPM: {self.igv_ipm}\n"
            f"  Total: {self.total}\n"
            f"  Estado CP: {self.estado_CP} (ID: {self.id_estado_CP})\n"
            f")"
        )