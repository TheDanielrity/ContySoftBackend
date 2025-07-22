CREATE DATABASE dbContySoft
GO

USE dbContySoft
GO
CREATE SCHEMA Seguridad
GO

CREATE SCHEMA Catalogo
GO


CREATE SCHEMA Contabilidad
GO

CREATE TABLE Catalogo.TipoPersona(
	id smallint identity(3,1) PRIMARY KEY,
	nombre varchar(50) NOT NULL,
	activo nvarchar(10) NOT NULL

)
GO


CREATE TABLE Seguridad.Persona(
	id bigint IDENTITY(1,1) PRIMARY KEY,
	nombres varchar(50) NOT NULL,
	apellidos varchar(50) NOT NULL,
	telefono varchar(11) NULL,
	email varchar(150) NOT NULL,
	id_tipo_persona smallint NOT NULL,
	activo bit NOT NULL,
	id_usuario_crea int NULL,
	fecha_crea datetime NOT NULL,
	id_usuario_modifica int NULL,
	fecha_modifica datetime NULL
	)
GO

CREATE TABLE Seguridad.Usuario(
	id int IDENTITY(1,1) PRIMARY KEY,
	id_persona bigint NOT NULL,
	usuario varchar(150) NOT NULL,
	password varchar(max) NOT NULL,
	activo nchar(10) NOT NULL,
	id_usuario_crea int NULL,
	fecha_crea datetime NOT NULL,
	id_usuario_modifica int NULL,
	fecha_modifica datetime NULL,
	CONSTRAINT FK_Usuario_Persona FOREIGN KEY (id_persona) REFERENCES Seguridad.Persona(id)
	)
GO

CREATE TABLE Seguridad.UsuarioContable(
	id int IDENTITY(1,1) PRIMARY KEY,
	ruc varchar(11) UNIQUE NOT NULL,
	razon_social varchar(250) NOT NULL,
	tipo_persona varchar(20) NOT NULL,
	usuario_sol varchar(20) NOT NULL,
	password_sol varchar(max) NOT NULL,
	id_persona bigint NOT NULL,
	id_plan smallint NOT NULL,
	id_usuario_crea int NULL,
	fecha_crea datetime NULL,
	id_usuario_modifica int NULL,
	fecha_modifica datetime NULL,
	CONSTRAINT FK_UsuarioContable_Persona FOREIGN KEY (id_persona) REFERENCES Seguridad.Persona(id)
)
GO

CREATE TABLE Contabilidad.TipoDocumento(
	id tinyint PRIMARY KEY,
	descripcion varchar(50) NOT NULL
)
go

CREATE TABLE Contabilidad.ClienteComprobantePago(
	id bigint identity(1,1) PRIMARY KEY,
	num_doc varchar(20) UNIQUE NOT NULL,
	razon_social varchar(50),
	id_tipo_doc tinyint NOT NULL,
	constraint FK_ClienteComprobantePago_TipoDocumento foreign key (id_tipo_doc) references Contabilidad.TipoDocumento(id)
)
go


CREATE TABLE Contabilidad.TipoComprobantePago(
	id tinyint primary key,
	descripcion varchar(50) NOT NULL
)
go

CREATE TABLE Contabilidad.ComprobantePago(
	id bigint identity (1,1),
	id_tipo_CP tinyint NOT NULL,
	serie_CP VARCHAR(8),
	id_emisor int NOT NULL,
	constraint PK_ID_SERIE  PRIMARY KEY (id, serie_CP),
	constraint FK_ComprobantePago_UsuarioContable foreign key (id_emisor) references Seguridad.UsuarioContable(id),
	constraint FK_ComprobantePago_TipoComprobantePago foreign key (id_tipo_CP) references Contabilidad.TipoComprobantePago(id)
)
go


CREATE TABLE Contabilidad.datosVentas(
	id_venta bigint identity(1,1) PRIMARY KEY,
	CAR_sunat varchar(27) UNIQUE NOT NULL,
	num_CP varchar(30),
	fecha_emision date NOT NULL,
	periodo varchar(6) NOT NULL,
	BI_Gravada float NOT NULL, 
	dscto_BI float NOT NULL,	
	IGV_IPM	float NOT NULL,
	dscto_IGV_IPM float NOT NULL,
	monto_exonerado float NOT NULL,
	monto_inafecto float NOT NULL,
	ISC float NOT NULL,
	BI_Grav_IVAP float NOT NULL,
	IVAP float NOT NULL, 
	ICBPER float NOT NULL, 
	otros_Tributos float NOT NULL,
	id_estado_CP tinyint NOT NULL,
	total float NOT NULL,
	moneda varchar(3) NOT NULL,
	tipo_cambio float NOT NULL,
	id_comprobante bigint,
	id_cliente bigint,
	serie_CP VARCHAR(8),
	CONSTRAINT FK_datosVentas_ComprobantePago foreign key (id_comprobante, serie_CP) references Contabilidad.ComprobantePago(id, serie_CP),
	CONSTRAINT FK_datosVentas_ClienteComprobantePago foreign key (id_cliente) references Contabilidad.ClienteComprobantePago(id),
	CONSTRAINT FK_datosVentas_estadoComprobantePago foreign key (id_estado_CP) references Contabilidad.estadoComprobantePago(id)

)
go




CREATE TABLE Contabilidad.datosCompras(
	id_compra bigint identity(1,1) PRIMARY KEY,
	CAR_sunat varchar(27) UNIQUE NOT NULL,
	num_CP varchar(20),
	fecha_emision date NOT NULL,
	fecha_vencimiento date NOT NULL,
	periodo varchar(6) NOT NULL,
	BI_Gravado_DG float NOT NULL,
	IGV_IPM_DG float NOT NULL,
	BI_Gravado_DGNG float NOT NULL,
	IGV_IPM_DGNG float NOT NULL,
	BI_Gravado_DNG float NOT NULL,
	IGV_IPM_DNG float NOT NULL,
	valor_adq_NG float NOT NULL,
	ISC float NOT NULL,
	ICBPER float NOT NULL, 
	otros_Tributos float NOT NULL,
	id_estado_CP tinyint NOT NULL,
	total float NOT NULL,
	moneda varchar(3) NOT NULL,
	tipo_cambio float NOT NULL,
	id_comprobante bigint,
	id_cliente bigint,
	serie_CP varchar(8),
	CONSTRAINT FK_datos_compras_ComprobantePago foreign key (id_comprobante, serie_CP) references Contabilidad.ComprobantePago(id, serie_CP),
	CONSTRAINT FK_datos_compras_ClienteComprobantePago foreign key (id_cliente) references Contabilidad.ClienteComprobantePago(id),
	CONSTRAINT FK_datosCompras_estadoComprobantePago foreign key (id_estado_CP) references Contabilidad.estadoComprobantePago(id)
)
go

CREATE TABLE Contabilidad.estadoComprobantePago(
	id tinyint PRIMARY KEY,
	descripcion varchar(30) NOT NULL
)
GO
INSERT INTO Contabilidad.estadoComprobantePago VALUES   (0, 'NO EXISTE'),
														(1, 'ACEPTADO'),
														(2, 'ANULADO'),
														(3, 'AUTORIZADO'),
														(4, 'NO AUTORIZADO')
GO


insert into Contabilidad.TipoDocumento values(0, 'Doc.trib.no.dom.sin.ruc'),
							(1, 'Doc. Nacional de identidad '),
							(4, 'Carnet de extranjeria '),
							(6, 'Registro Unico de contribuyentes (RUC)'),
							(7, 'Pasaporte')
go
insert into Contabilidad.TipoComprobantePago VALUES (0, 'Otros'),
							(1, 'Factura'),
							(2, 'Recibo por Honorarios'),
							(3, 'Boleta de Venta'),
							(4, 'Liquidación de compra'),
							(7, 'Nota de crédito')
GO




CREATE OR ALTER PROCEDURE Contabilidad.Usp_ExistePeriodo
	@Id int,
	@periodo varchar(6)
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		DECLARE @IdPersona bigint;
		SET @IdPersona = (SELECT id_persona FROM Seguridad.Usuario WHERE id = @Id);
		SELECT 1 FROM Contabilidad.datosVentas DV
		INNER JOIN Contabilidad.ComprobantePago CP ON DV.id_comprobante = CP.id
		INNER JOIN Seguridad.UsuarioContable UC ON UC.id = CP.id_emisor
		WHERE DV.periodo = @periodo AND UC.id_persona = @IdPersona
		
	END TRY
    BEGIN CATCH
        -- Manejo de errores
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
GO


CREATE OR ALTER PROCEDURE Contabilidad.Usp_ObtenerDatosContables
	@Id int
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		DECLARE @IdPersona bigint;
		SET @IdPersona = (SELECT id_persona FROM Seguridad.Usuario WHERE id = @Id);
		SELECT ruc, usuario_sol, password_sol FROM Seguridad.UsuarioContable WHERE id_persona = @IdPersona;
	END TRY
    BEGIN CATCH
        -- Manejo de errores
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
GO

CREATE OR ALTER PROCEDURE Contabilidad.Usp_ValidarRuc 
	@Id int, 
	@ruc varchar(11)
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		DECLARE @IdPersona bigint;
		SET @IdPersona = (SELECT id_persona FROM Seguridad.Usuario WHERE id = @Id);

		IF ((SELECT ruc FROM Seguridad.UsuarioContable WHERE id_persona = @IdPersona) != @ruc)
			BEGIN
				RAISERROR('El RUC no es igual al registrado.', 16, 1);
			END
		ELSE
			SELECT ruc FROM Seguridad.UsuarioContable WHERE id_persona = @IdPersona;
	END TRY
    BEGIN CATCH
        -- Manejo de errores
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
GO


CREATE OR ALTER PROCEDURE Contabilidad.Usp_ObtenerDatosVentas  
	@Id int,
	@periodo varchar(6)
AS
BEGIN
		DECLARE @IdUsuarioContable int;
		SET @IdUsuarioContable = (SELECT id FROM Seguridad.UsuarioContable WHERE id_persona = (SELECT id_persona FROM Seguridad.Usuario WHERE id = @Id))


		IF @periodo = 'ALL'
			BEGIN
				SELECT v.id_venta, uc.ruc, cp.serie_CP, v.num_CP, v.fecha_emision, (SELECT razon_social FROM Contabilidad.ClienteComprobantePago where id = v.id_cliente) as cliente, 
				v.periodo, uc.razon_social as 'RAZON_SOCIAL',  v.BI_Gravada, v.monto_inafecto, v.IGV_IPM, v.total, ecp.descripcion as 'estado_CP', v.id_estado_CP, t_cp.descripcion as 'tipo_CP'
				FROM Contabilidad.datosVentas v
				INNER JOIN  Contabilidad.ComprobantePago cp ON v.id_comprobante = cp.id
				INNER JOIN Contabilidad.TipoComprobantePago t_cp ON t_cp.id = cp.id_tipo_CP
				INNER JOIN Seguridad.UsuarioContable uc ON uc.id = cp.id_emisor
				INNER JOIN Contabilidad.estadoComprobantePago ecp ON ecp.id = v.id_estado_CP
				WHERE uc.id = 1
			END
		ELSE
			BEGIN
				SELECT v.id_venta, uc.ruc, cp.serie_CP, v.num_CP, v.fecha_emision, (SELECT razon_social FROM Contabilidad.ClienteComprobantePago where id = v.id_cliente) as cliente, 
					v.periodo, uc.razon_social as 'RAZON_SOCIAL',  v.BI_Gravada, v.monto_inafecto, v.IGV_IPM, v.total, ecp.descripcion as 'estado_CP', v.id_estado_CP, t_cp.descripcion as 'tipo_CP'
					FROM Contabilidad.datosVentas v
					INNER JOIN  Contabilidad.ComprobantePago cp ON v.id_comprobante = cp.id
					INNER JOIN Contabilidad.TipoComprobantePago t_cp ON t_cp.id = cp.id_tipo_CP
					INNER JOIN Seguridad.UsuarioContable uc ON uc.id = cp.id_emisor
					INNER JOIN Contabilidad.estadoComprobantePago ecp ON ecp.id = v.id_estado_CP
					WHERE uc.id = @IdUsuarioContable AND v.periodo = @periodo
			END
END
GO

CREATE OR ALTER PROCEDURE Contabilidad.Usp_InsertarDatosVentas
    @ruc VARCHAR(11),

	@num_doc_cliente_CP VARCHAR(20),
    @razon_social_cliente_CP VARCHAR(50),
    @id_tipo_doc_cliente_CP TINYINT,
    
	@id_tipo_CP TINYINT,
    @serie_CP VARCHAR(8),


    @CAR_sunat_ventas VARCHAR(27),
    @num_CP_ventas VARCHAR(30),
    @fecha_emision_ventas DATE,
    @periodo_ventas VARCHAR(6),
    @BI_Gravada FLOAT,
	@dscto_BI float,	
    @IGV_IPM FLOAT,
	@dscto_IGV_IPM float,
	@monto_exonerado float,
	@monto_inafecto float,
	@ISC float,
	@BI_Grav_IVAP float,
	@IVAP float, 
	@ICBPER float, 
	@otros_Tributos float,
	@id_estado_CP tinyint,
	@total float,
	@moneda varchar(3),
	@tipo_cambio float
AS
BEGIN
    SET NOCOUNT ON;
	DECLARE @id_emisor_CP BIGINT,
			@id_cliente_CP BIGINT,
			@id_comprobante bigint;

    BEGIN TRY
		
		IF EXISTS(SELECT 1 FROM Contabilidad.datosVentas WHERE CAR_sunat = @CAR_sunat_ventas)
			BEGIN 
				RETURN
			END
		
		IF NOT EXISTS(SELECT 1 FROM Seguridad.UsuarioContable WHERE ruc = @ruc)
		BEGIN
			RAISERROR('|No se recibió la información correcta.|', 16, 1);
		END

		SET @id_emisor_CP = (SELECT id FROM Seguridad.UsuarioContable WHERE ruc = @ruc)

		-- Verificar y insertar el cliente en ClienteComprobantePago
		IF @num_doc_cliente_CP IS NOT NULL 
		BEGIN
			IF EXISTS (SELECT 1 FROM Contabilidad.ClienteComprobantePago WHERE num_doc = @num_doc_cliente_CP)
				BEGIN
					SET @id_cliente_CP = (SELECT id FROM Contabilidad.ClienteComprobantePago WHERE num_doc = @num_doc_cliente_CP)
				END
			ELSE
				BEGIN
					INSERT INTO Contabilidad.ClienteComprobantePago (num_doc, razon_social, id_tipo_doc)
					VALUES (@num_doc_cliente_CP, @razon_social_cliente_CP, @id_tipo_doc_cliente_CP);
					SET @id_cliente_CP = SCOPE_IDENTITY()
				END

		END
			-- Insertar en ComprobantePago
		IF EXISTS(SELECT 1 FROM Contabilidad.ComprobantePago WHERE serie_CP = @serie_CP AND id_emisor = @id_emisor_CP)
			BEGIN
				SET @id_comprobante = (SELECT id FROM Contabilidad.ComprobantePago WHERE serie_CP = @serie_CP AND id_emisor = @id_emisor_CP)
			END
		ELSE
			BEGIN
				INSERT INTO Contabilidad.ComprobantePago (id_tipo_CP, serie_CP, id_emisor)
				VALUES (@id_tipo_CP, @serie_CP, @id_emisor_CP);
				SET @id_comprobante = SCOPE_IDENTITY()		
			END

        -- Insertar en datos_ventas
        INSERT INTO Contabilidad.datosVentas (
            CAR_sunat,
			num_CP,
			fecha_emision,
			periodo,
			BI_Gravada,
			dscto_BI,
			IGV_IPM,
			dscto_IGV_IPM,
			monto_exonerado,
			monto_inafecto,
			ISC,
			BI_Grav_IVAP,
			IVAP,
			ICBPER,
			otros_Tributos,
			id_comprobante,
			id_cliente,
			serie_CP,
			id_estado_CP,
			total,
			moneda,
			tipo_cambio
        )
        VALUES (
            @CAR_sunat_ventas,
			@num_CP_ventas,
			@fecha_emision_ventas,
			@periodo_ventas,
			@BI_Gravada,
			@dscto_BI,
			@IGV_IPM,
			@dscto_IGV_IPM,
			@monto_exonerado,
			@monto_inafecto,
			@ISC,
			@BI_Grav_IVAP,
			@IVAP,
			@ICBPER,
			@otros_Tributos,
			@id_comprobante,
			@id_cliente_CP,
			@serie_CP,
			@id_estado_CP,
			@total,
			@moneda,
			@tipo_cambio
        );
    END TRY
    BEGIN CATCH
        -- Manejo de errores
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END
GO




CREATE OR ALTER PROCEDURE Seguridad.Usp_Usuario_Obtener 
	@usuario VARCHAR(150)
AS
BEGIN
	SELECT 
		U.id,
		CASE WHEN ISNULL(P.apellidos, '') = '' THEN P.nombres ELSE CONCAT(P.nombres, ' ', P.apellidos) END  as 'fullname',
		[password],
		UC.ruc
	FROM Seguridad.Usuario U
	INNER JOIN Seguridad.Persona P ON U.id_persona = P.id
	INNER JOIN Seguridad.UsuarioContable UC ON UC.id_persona = P.id
	WHERE usuario = @usuario
END
GO


CREATE OR ALTER PROCEDURE Seguridad.Usp_Usuario_Registrar 
	@ruc VARCHAR(11),
	@razon_social VARCHAR(250),
	@tipo_persona VARCHAR(20),
	@usuario_sol VARCHAR(20),
	@password_sol VARCHAR(MAX),
	@usuario VARCHAR(150),
	@password VARCHAR(MAX),
	@id_plan smallint
AS
BEGIN TRY
	SET NOCOUNT ON
	IF EXISTS(SELECT 1 FROM Seguridad.Usuario WHERE usuario = @usuario)
	BEGIN
		-- Arrojar un error con un mensaje específico
		RAISERROR('|Ya existe un usuario registrado con el mismo email.|', 16, 1);
	END ELSE
	BEGIN
		BEGIN TRANSACTION
			DECLARE @id_persona BIGINT,
					@id_usuario INT

			INSERT INTO Seguridad.Persona(
				nombres,
				apellidos,
				email,
				id_tipo_persona,
				activo,
				id_usuario_crea,
				fecha_crea
			)
			VALUES(
				@razon_social,
				'',
				@usuario,
				1,
				1,
				0,
				GETDATE()
			)

			SET @id_persona = SCOPE_IDENTITY()

			INSERT INTO Seguridad.Usuario(
				id_persona,
				usuario,
				password,
				activo,
				id_usuario_crea,
				fecha_crea
			)
			VALUES(
				@id_persona,
				@usuario,
				@password,
				1,
				0,
				GETDATE()
			)

			SET @id_usuario = SCOPE_IDENTITY()

			INSERT INTO Seguridad.UsuarioContable(
				ruc,
				razon_social,
				tipo_persona,
				usuario_sol,
				password_sol,
				id_persona,
				id_usuario_crea,
				fecha_crea,
				id_plan
			)
			VALUES(
				@ruc,
				@razon_social,
				@tipo_persona,
				@usuario_sol,
				@password_sol,
				@id_persona,
				@id_usuario,
				GETDATE(),
				@id_plan
			)
		COMMIT TRANSACTION;
		SELECT 
			U.id,
			CASE WHEN ISNULL(P.apellidos, '') = '' THEN P.nombres ELSE CONCAT(P.nombres, ' ', P.apellidos) END  as 'fullname',
			[password]
		FROM Seguridad.Usuario U
		INNER JOIN Seguridad.Persona P ON U.id_persona = P.id
		WHERE usuario = @usuario
	END
END TRY
BEGIN CATCH
		-- Rollback de la transacción si hay un error
	IF @@TRANCOUNT > 0
	BEGIN
		ROLLBACK;
	END

	-- Manejo del error: captura detalles del error
	DECLARE @ErrorMessage NVARCHAR(4000);
	DECLARE @ErrorSeverity INT;
	DECLARE @ErrorState INT;

	-- Obtener detalles del error
	SELECT 
		@ErrorMessage = ERROR_MESSAGE(),
		@ErrorSeverity = ERROR_SEVERITY(),
		@ErrorState = ERROR_STATE();

	-- Arrojar el error para que pueda ser capturado en el backend
	RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
END CATCH

GO

