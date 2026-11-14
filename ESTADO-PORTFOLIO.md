# Estado del portfolio RavenTechs

Base de trabajo, actualizada el 1/11/2026 (ver la sección de actualización); la tabla es del 26/10/2026 a la noche (incluye manejAr, la auditoría de backup, los arreglos del 26/10 y su verificación independiente). Es la misma información del tablero maestro, en un formato que se lee desde cualquier chat.

**Etapas:** 1 Construida · 2 Publicada · 3 Práctica/demo lista · 4 Probada por vos · 5 Con clientes. `✓` = hecha, `·` = falta.

**Fuentes:** tablero maestro (`raventechs-tablero.html`, v2.4.0, ahora con una línea de backup por app), portal (`raventechs.github.io`), código de cada repo y lo que Ruben confirmó de palabra. Las tildes que se marcan tocando el tablero se guardan solo en el celular, así que este archivo es la referencia compartida.

## Actualización del 14/11/2026 (leer primero)

**Hecho:**
- **Estándar «sucursales en versión simple + Plus Panel del dueño»** aplicado y publicado en PuntoVenta (v3.11/3.12), CarneAR v2.10, PizzAR, PanAR, BarbeAR v3.3 y lavAR v2.5. Negocio único = caja base sin panel; 2+ locales = selector de local y pestaña «Dueño» (candado + WhatsApp sin el Plus; total del día y detalle por local con el Plus, que activa el admin con «⭐ Activar Panel dueño»). Probado solo en simulado.
- **Reglas pegadas por Ruben el 14/11:** lavAR (obligatoria, protege `panelDueno`) y PizzAR/PanAR (recomendadas). CarneAR, BarbeAR y PuntoVenta no cambian.
- **Panel de actividad** con uso real por app (ver resumen del tablero 2.9.14); faltan EmpresAR y CompraZona.
- Estándar de entrega: instructivo único para pegar reglas (página con enlace directo + botón Copiar).

**Pendientes en orden:** 1) probar el Plus con una cuenta real en cada app; 2) dos animaciones de venta (Básica con sucursales y Completa); 3) panel de actividad de EmpresAR y CompraZona; 4) lista del 8/11.

## Actualización del 8/11/2026 (noche — leer primero)

**Hecho (todo probado e/o instalado por Ruben en el celular salvo lo marcado):**
- **SaludAR v2.11** (repo saludar; sin probar en el celular): un familiar invitado entraba pero veía la app vacía «desde cero» en lugar de la medicación del titular. Causa probable: el perfil compartido se buscaba con una consulta `collectionGroup` sobre `miembros`, que en Firebase exige un índice y fallaba sin avisar. Ahora al unirse se guarda `perfilId` en la cuenta del familiar y el perfil se abre directo; si no se puede abrir aparece un aviso rojo; reenviar un link repara cuentas ya unidas. Además el familiar hereda el estado del titular (el plus familiar lo cobra el titular): si el titular está activo no ve pared de prueba; si su prueba venció, el familiar también; el titular deja su estado en el perfil (`titularStatus`, `titularVence`) cada vez que abre la app, así que tras activar al titular hay que pedirle que abra la app una vez. Sin cambios de reglas. Test: `qa/harness/test_sa_familiar.py` (10). Pendiente: probar con el segundo teléfono (la cuenta ya unida necesita un link nuevo del titular una sola vez).
- **PuntoVenta v3.0 → v3.2** (repo puntoventa; SIN probar todavía en el celular; reglas SIN pegar): una sola app con plan Básico (cuentas nuevas: Vender, Caja, En cuenta, Gastos; 1 negocio, 1 sucursal) y plan Avanzada (sucursales, empleados, Dashboard; se activa con un botón en el menú admin). Venta rápida con efectivo, Mercado Pago, débito, crédito, transferencia, «En cuenta» y pago con dos medios. «En cuenta» (antes «fiado»): cuenta corriente por cliente, búsqueda por nombre, historial, cobros en partes, aviso por WhatsApp, notas con fecha y hora, anular movimientos. Caja: resumen del día por medio de pago y botón «Cerrar caja y enviar resumen por WhatsApp» (ya no hay «Cierre» aparte). Prueba de 14 días nueva (`demoHasta`) sin bloqueo, con cartel rojo; las cuentas anteriores conservan todo. Corregidos: la fecha del día salía en UTC (ventas de la noche caían en el día siguiente) y los empleados quedaban bloqueados por la prueba. Reglas completas en `qa/rules/puntoventa.rules` (protegen `plan` y `demoHasta`); Ruben debe pegarlas una sola vez. Barra con el nombre del negocio grande y «PuntoVenta» chico (v3.3). Rubros (v3.4): al empezar la app pregunta el rubro (kiosco, almacén, fiambrería, verdulería, panadería, bazar, tienda de ropa, ferretería, farmacia, otro) y cambia ícono, ejemplo y atajos de venta; se cambia en Configuración. v3.5: en Básico «Caja» es el inicio (vender + un único resumen + cerrar caja por WhatsApp) e «Historial» es la lista de ventas por fecha con buscador en todo el historial (cliente, producto, medio, importe). Instructivo web y PDF nuevos. Tests: `qa/harness/test_pv3.py` (52) y `test_pv3b.py` (14) y `test_pv3c.py` (8, rubros). v3.6: en Básico se sacaron los departamentos (importe + medio + descripción opcional). v3.7: tablero del dueño en Avanzada: «Lo importante de hoy» (frases automáticas contra ayer y la semana pasada, sucursal que más vendió, deuda, gastos altos), barras de 7 días, torta de medios, comparativa entre sucursales y ficha por sucursal (hoy/7 días/mes, historial y buscador). v3.8: el empleado cierra su caja y manda el resumen por WhatsApp desde su pantalla (el aviso nocturno automático queda descartado). Test: `test_pv4.py` (14), `test_pv5.py` (3). v3.9 (etapa 2): Plus «Catálogo con stock y alertas» (productos dentro del negocio, venta tocando productos, stock calculado con las ventas, tarjeta de faltantes en tablero y Caja) y Plus «Tablero del dueño»; solo Avanzada; botones en el menú admin (features.catalogo / features.tablero, sin reglas nuevas); cuentas anteriores y pruebas de 14 días los ven con etiqueta ⭐. Límite conocido: las ventas de empleados no descuentan stock (su pantalla no tiene catálogo). Test: test_pv6.py (15). Pendiente: catálogo en la pantalla del empleado. Pendiente: , alertas de stock y 2 adicionales Plus.
- **CompraZona:** reglas Firestore v0.3 publicadas (proyecto ravenmarket-c2739): el dueño de una empresa ya no puede cambiar su prueba (`demoHasta`), plan, plus, destacada ni activa; solo el administrador.
- **App de vendedores v2.0** (ventas.raventechsapp.com/vendedores/): visitas por vendedor. La landing `/probar/` (v1.1) registra una visita por sesión y app (colección `visitas`, con campos validados por reglas, sin login) y el panel Admin la muestra por vendedor, hoy, 7 días y total. Probado OK.
- **App de vendedores v2.2:** solapas en Admin, «Ventas» y «Uso de las apps» (abre el Panel de actividad, que sigue en raventechs.github.io/panel/; mudarlo a ventas.raventechsapp.com/panel/ es opcional y pide autorizar ese dominio en el login de Google). Probado en el celular.
- **App de vendedores v2.1:** seguimiento humano (Pilar 3 del embudo). Cada envío genera una tarea al día 1 («¿pudiste entrar?») y otra al día 3 («¿necesitás ayuda?») con botón de WhatsApp y mensaje armado, «Hecho» y «No seguir con este cliente»; las tareas dejan de mostrarse a los 7 días. Cada vendedor ve solo las suyas; el admin ve los pendientes de todos. Colección `seguimientos`; el vendedor ahora puede leer sus propios envíos. Reglas completas en `vendedores/firestore.rules` del repo Chicho (y `qa/rules/vendedores.rules`). Aviso y tarea probados en el celular.
- **SaludAR v2.8 → v2.10** (repo saludar): auditoría contra el estándar de 12 puntos (cumple 1–3 y 5–11; el 4 sigue con el modelo viejo `status`/`demoExpiry` por decisión de Ruben). Correcciones: la fecha del día usaba UTC (desde las 21:00 las tomas marcadas pasaban al día siguiente y el resumen de las 22:00 decía que faltaba todo); service worker de notificaciones en red primero con estado guardado y ventana de 30 min; menú admin abre con la sesión activa y avisa con qué cuenta se ingresó; al cerrar sesión Google muestra el selector de cuentas. Ruben probó: ingreso con su cuenta, menú admin, Familiar habilitado e invitación a un pariente.
- Versión visible al pie de Perfil en SaludAR («SaludAR v2.10») para confirmar que el celular tiene la última.

**Pendiente de decisión (SaludAR):** probar unos días si los avisos llegan en hora con la app cerrada. Los avisos locales dependen de que el sistema despierte el service worker; el único método confiable con la app cerrada es el aviso por servidor (función en Netlify + cron-job.org cada 15 min, como antes de la v2.2). Si se vuelve a ese esquema hay que reactivar la función y registrar los tokens en la app.

**Pendientes en orden:** 1) SaludAR: decidir aviso por servidor tras la prueba; 2) EmpresAR: sus 2 Plus (el repo no está en la organización `raventechs`); 3) TimbreAR parte 2 y 3 y sus Plus; 4) Traductor de Hábitos y claves expuestas de MTC/CharlAR (pasos en qa/pegar-habitos.html); 5) pedirle a Google que saque la marca de raventechs.github.io; 6) CarneAR con máscaras por rubro.

## Actualización del 2/11/2026 (etapa comercial — leer primero)

**Actualización 8/11/2026 (tarde).** Sitio viejo de vendedores (raventechs.github.io/vendedores/ y /probar/) ahora redirige a ventas.raventechsapp.com conservando parámetros; su service worker se desinstala solo. Checklist «Tus primeros pasos» (solo prueba, solo dueño, guardado en el celular, sin tocar datos ni reglas) ya está en CarneAR v2.9.3, PizzAR v3.0, PanAR v1.8, lavAR v2.5, BarbeAR v2.7 y PeloteAR (cada una con sus 4 pasos propios, probadas en simulador).

**Sitio comercial en dominio propio (2/11 noche).** Google marcó `raventechs.github.io` con la alerta "Sitio peligroso" (Navegación segura). Se armó un sitio aparte en el repo `raventechs/Chicho` (vacío, reutilizado) publicado en **ventas.raventechsapp.com** (Pages en main, CNAME ventas → raventechs.github.io, HTTPS activo, dominio autorizado en Firebase Auth de raventech-vendedores): app de vendedores v1.9 en /vendedores/, landing en /probar/, folletos en /folletos/ (incluye folleto-gasar) y guías de GasAR y manejAr en /ayuda/gasar/ y /ayuda/manejar/. Los vendedores y clientes deben usar SOLO estos links nuevos. NO ponerle dominio propio al repo raventechs.github.io: ManejAr (clientes reales) y GasAR cuelgan de ahí y cambiarían de origen (se pierden sesiones y PWAs instaladas). Las apps manejAr, GasAR y LogisAR siguen en raventechs.github.io hasta tener dominio propio. Pendiente: pedir la revisión a Google (safebrowsing.google.com/safebrowsing/report_error) y, cuando el vendedor pruebe el link nuevo, dejar en el sitio viejo un aviso que redirija al nuevo.


**Kit de venta por app (demo + instructivo con PDF + folleto).** Las 16 apps que se pueden vender lo tienen completo y están en la app de vendedores (ventas.raventechsapp.com/vendedores/, v1.7): CarneAR, PizzAR, PanAR, PuntoVenta, lavAR, BarbeAR, PeloteAR, SecuroPro, EmpresAR, Rodix, manejAr, SaludAR, MiAgenda, TimbreAR, CompraZona y GasAR. MTC, CharlAR, AhorrAR, legalAR y LogisAR figuran como "Próximamente" (no se envían).

**Hecho hoy:**
- Folletos nuevos: BarbeAR, EmpresAR, manejAr, CompraZona y Traductor de Hábitos (folletos/folleto-<app>.html; GasAR usa gasar/gasar-folleto.html).
- Instructivos con PDF nuevos: TimbreAR, CompraZona, GasAR y Traductor de Hábitos (ayuda/index.html + Guia-<App>.pdf en cada repo).
- Landing de entrega instantánea de la prueba: ventas.raventechsapp.com/probar/?app=<id>&ref=<código>. La app de vendedores manda ese link al cliente. Los datos salen del catálogo de vendedores/index.html: si cambia, regenerar la landing.
- Página del portfolio (raventechs.github.io): enlaces a folletos corregidos (apuntaban a archivos que no existían) y se suma Traductor de Hábitos.
- Traductor de Hábitos v2.0 (repo raventechs-traductor-habitos, Firebase traductor-habitos): estándar completo, clave de Groq fuera del código, reglas en qa/rules/habitos.rules y servidor de IA en qa/worker-ia/worker.js (sirve también a CharlAR). Probado en simulador, no contra Firebase real.

**Pendiente de Ruben (página con botones: raventechs.github.io/gasar/qa/pegar-habitos.html):** crear clave nueva de Groq y borrar las viejas; crear el Worker raventechs-ia en Cloudflare con el secreto GROQ_KEY y pasar su dirección (se carga en IA_URL de Traductor de Hábitos y de CharlAR); CNAME habitos y Pages del repo; autorizar el dominio en Firebase Auth y pegar las reglas; probarla en el celular. Después pasar la app a vendible en vendedores (ok:true) y regenerar la landing.

**Tanda única de reglas Firestore para más adelante (pegar una sola vez por app):** modelo nuevo de prueba de 14 días (demoHasta) en PuntoVenta, SecuroPro, EmpresAR, Rodix, SaludAR y MiAgenda; medir visitas por vendedor; TimbreAR parte 2.

**Prueba de 14 días SIN bloqueo (8/11/2026):** GasAR (admin 1.6.0, vendedor 1.4.0: por distribuidora, botones en Modo Raven), CompraZona (empresa v0.8, admin v0.6: por empresa), manejAr (v2.4.0: al vencer sigue funcionando) y TimbreAR (cartel en la app del residente; la consola guarda la prueba solo en el navegador hasta que los edificios pasen a la base). En las 4: durante la prueba, cartel ámbar con los días; al vencer, cartel rojo titilante fijo que no se puede cerrar, con botón de WhatsApp. Los clientes que ya existen no tienen fecha de prueba y no ven nada. No se pidieron reglas nuevas. Falta probarlas en el celular. Se reparó `timbrear-residente.html` (función de sonido cortada que impedía ejecutar la página). Botón "Instructivo" dentro de la app: falta en CompraZona, GasAR y Rodix.

## Actualización del 1/11/2026 (leer primero)

**Cambios desde el 26/10 (la tabla de abajo todavía muestra el estado del 26/10, salvo lo marcado acá):**
- Las apps viven en dominios propios `*.raventechsapp.com` (ej. `saludar.raventechsapp.com`); las direcciones viejas `raventechs.github.io/<app>/` y `raventechs.lat/<app>/` ya no sirven. Los folletos, `protocolo.html`, `pruebas.html` y las notificaciones del sitio ya apuntan a los dominios nuevos.
- **CompraZona** (app cliente v1.2): probada por Ruben, etapa 4 ✓. Permisos de ubicación y notificaciones, botón "Ubicación activa", "Cerca de vos", "Tu último pedido", instalación como app, bloqueo y menú oculto OK.
- **SaludAR:** probada OK en `saludar.raventechsapp.com` (instala, queda logueada, ícono nuevo).
- **TimbreAr:** portada en la raíz del dominio (daba 404) y demo completa simulada en `/demo.html` (visita toca un depto → al residente le llega el aviso → atender → chat → abrir puerta); rutas `/timbrear/` viejas corregidas. **Privacidad (parte 1) cerrada y probada:** la visita lee un directorio público (solo depto y piso); herramienta `timbrear-directorio.html`; reglas v2 publicadas.
- **PuntoVenta:** ingreso con Google OK tras autorizar el dominio en Firebase; menú admin se abre con 5 toques al título "Dashboard" en el celular (confirmar).
- **PanAR y PizzAR:** corregido el corte de pantalla en el celular (grilla de la caja).
- **Íconos nuevos** (dibujo + 3-4 colores) en 21 apps; Rodix con ambulancia + auto. Panel de actividades no tiene ícono ni manifest.
- **Del 31/10:** menú oculto sin PIN en 17 apps, reglas de Firestore endurecidas publicadas en 18 apps (sin probar contra Firebase real), prueba de 14 días con bloqueo en CarneAR, BarbeAR, lavAR, PanAR y PizzAR, Modo Práctica en 12 apps, instructivo con PDF en varias, PeloteAR migrada a Firestore, claves expuestas sacadas del código de MTC y CharlAR.

**Pendientes, en orden recomendado:**
1. **Claves expuestas:** anular las claves viejas de Anthropic (MTC) y Groq (CharlAR), crear el Worker de Cloudflare (`worker.js` ya entregado) y pasar su dirección para cargarla en CharlAR (`IA_URL`).
2. **TimbreAr parte 2:** pasar los edificios de la consola de administración (hoy solo en el navegador) a la base.
3. **TimbreAr parte 3:** aviso al residente con la app cerrada (probar en Xiaomi con dos celulares).
4. **Confirmar en el celular:** CompraZona v1.2 ("Cerca de vos", "Tu último pedido"), los service workers de PuntoVenta, MTC y SaludAR, y decidir si el botón del folleto de TimbreAr apunta a la demo (`/demo.html`).
5. **PeloteAR:** cargar una reserva real. **Instructivos y prueba de 14 días** que faltan: AhorrAR, CharlAR, LegalAR, MTC, GasAR, manejAr, CompraZona y TimbreAr.
6. **Más adelante:** backup nocturno desde servidor, probar el backup en el celular app por app, ícono para el Panel de actividades, panel con el historial de apps probadas, botones de Rodix a 390 px, error de importación en AhorrAR.

**Plan para mañana (2/11):** 1) claves expuestas de MTC y CharlAR · 2) TimbreAr parte 2 · 3) TimbreAr parte 3 · mientras tanto, seguir probando apps una por una y anotar las que quedan OK.

**TimbreAr, limitaciones conocidas:** la cuenta de Google del administrador llega a ese proyecto de Firebase sin correo en el token (las reglas por correo no la reconocen); cualquier visita anónima podría escribir el token de aviso de un departamento.

**Historial de apps probadas y OK por Ruben:** CompraZona (1/11), SaludAR (1/11), TimbreAr portada/demo (1/11); PuntoVenta (ingreso OK, falta confirmar menú).

## Tabla de apps

| App | Estado | Etapas | Versión | Modo práctica / demo | Backup | Próximo paso |
|---|---|---|---|---|---|---|
| GasAR | 🟡 Para vender/probar | ✓✓✓·· | admin 1.5.0 · vendedor 1.3.0 | 🎓 Práctica (Modo Raven) | ✅ auto (solo administrador) + manual + restaurar catálogo (26/10; el historial de ventas/cajas NO se restaura desde la app por las reglas; probado en simulador, falta probar en tu celular) | Firebase → Authentication → Comenzar; habilitar Google y Correo/Contraseña. Después crear la distribuidora de PRÁCTICA y tildar los 10 pasos. |
| manejAr | 🟢 Con clientes | ✓✓✓✓✓ | v2.3.0 | Demo propio (?demo=1, 4 semanas de datos) | ✅ auto diario + manual + restaurar (26/10, probado en simulador y en la página real); el archivo ya no lleva el plan/vencimiento | Plan Flota: revisar cómo se crea desde Ajustes y probarlo con Firebase real. Después, el backup nocturno de las 2 AM. |
| MTC | 🔴 Urgente | ✓✓··· | v1.3 | — falta | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular). Además se corrigieron las sesiones de juegos y el historial del modo estudio, que nunca se guardaban | Sacar la API key del cliente con un proxy en Netlify Functions. |
| CarneAR | 🟢 Con clientes | ✓✓✓·· | v2.7 prod · v2.8-beta | 🎓 Práctica (prod y beta) | ✅ auto + manual + restaurar (arreglado 26/10, probado en simulador; falta probar en tu celular) | Probar 🎓 Modo Práctica en una cuenta tuya; después pasar peso libre y login anónimo de la beta a producción. |
| CompraZona | 🟡 Para vender/probar | ✓✓✓·· | admin v0.5 | Demo propio (modo demo + simulador) | ✅ auto + manual + restaurar catálogo, solo super admin (26/10); pedidos y usuarios van en el archivo pero no se restauran (reglas) | Publicar reglas v0.2, activar App Check y salir a conseguir las primeras garraferas. |
| Rodix | 🟢 Con clientes | ✓✓✓·✓ | v1.9.1 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar 🎓 Modo Práctica en Ajustes con una cuenta de pruebas. |
| SecuroPro | 🟡 Para vender/probar | ✓✓✓·· | v2.3 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar 🎓 Modo Práctica en Mi Empresa y revisar los precios del catálogo (son estimativos). |
| Traductor de Hábitos | 🔴 Urgente | ✓·✓·· | v2.0 | 🎓 Práctica + prueba de 14 días | ✅ auto diario + manual + restaurar (2/11; probado en simulador; falta probar en el celular) | Anular la clave vieja de Groq (estaba en el código), crear el Worker de IA (qa/worker-ia/worker.js), configurar el dominio habitos.raventechsapp.com, pegar qa/rules/habitos.rules y probar en el celular. Repo raventechs-traductor-habitos, proyecto Firebase traductor-habitos. |
| PizzAR | 🟡 Para vender/probar | ✓✓✓·· | v3.0 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: incluye gastos y comandas; falta probar en tu celular) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. |
| PanAR | 🟡 Para vender/probar | ✓✓✓·· | v1.7 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: incluye gastos; falta probar en tu celular) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. ⚠️ Falta la vista Stock (el botón existe pero no hay pantalla). |
| lavAR | 🟡 Para vender/probar | ✓✓✓·· | v2.4 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: sucursales, gastos, fidelización y empleados; falta probar en tu celular) | Probar 🎓 Modo Práctica y activar una sede para ver la caja. |
| MiAgenda | 🟢 Con clientes | ✓✓✓✓· | v2.5 | 🎓 Práctica (actividades de ejemplo) | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular) | Agregar el botón "Eliminar usuario". |
| SaludAR | 🟡 Para vender/probar | ✓✓·✓· | v2.10 | — falta | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular) | Confirmar que llega una sola notificación a la hora correcta con la app instalada. |
| BarbeAR | 🟡 Para vender/probar | ✓✓·✓· | v2.6 | — falta | ✅ auto + manual + restaurar (arreglado 26/10, probado en simulador; falta probar en tu celular) | Sumarle el 🎓 Modo Práctica como a las demás cajas y probarla con una barbería real. |
| PeloteAR | 🟡 Para vender/probar | ✓✓✓✓· | — | Demo propio (/demo, sin Firebase) | 🟡 solo al cierre del día, vía servidor Railway; sin manual ni restaurar | Pasarla a offline-first (hoy depende de un servidor en Railway) y sumar el aviso de turnos por WhatsApp. |
| TimbreAr | 🟡 Para vender/probar | ✓✓✓✓· | admin v1.1 | Demo propio (edificio raventechs-hq) | ✅ consola admin: auto + manual + restaurar (26/10). Ojo: los edificios de la consola viven solo en el navegador (localStorage); pasarlos a la base | Validar el aviso con la app cerrada en Xiaomi y probarla en un edificio real; después video y modo no molestar. |
| LogisAR | 🔵 En desarrollo | ····· | demo v0.3 (sin backend) | Demo con datos locales | ❌ ninguno (solo CSV) | Crear el proyecto Firebase, pegar la config y publicar las reglas de Firestore (todavía sin probar); después mostrar la demo al cliente y definir tarifas. |
| Embudo de demos | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Hacer la landing de entrega genérica para las 10 apps. |
| Módulo demo/vencimiento | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Esperar a que CarneAR tenga peso libre y login anónimo; recién ahí integrarlo. |
| Panel RavenTechs | 🔵 En desarrollo | ✓···· | — | n/a (proyecto interno) | n/a (proyecto interno) | Crear el proyecto Firebase raventechs-admin y pegar su config. |
| CentralbotAr | 🔵 En desarrollo | ✓✓··· | v0.2 | — falta | ✅ auto + manual + restaurar, sin el token de WhatsApp (26/10) | Renovar el token de Meta (vence cada 24 h) y hacer la pantalla "Mi equipo". |
| PuntoVenta | 🟡 Para vender/probar | ✓✓··· | v3.2 (Básica/Avanzada, En cuenta, Caja con cierre WhatsApp; reglas por pegar) | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar crear una sucursal nueva y la cuenta corriente con morosidad; después límite de crédito y reporte de morosos. |
| EmpresAR | 🟡 Para vender/probar | ✓✓··· | v2.1 | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probarla con la empresa de gas envasado cargando sus documentos reales; los módulos Plus (ventas, stock, flota) quedan para la próxima versión. |
| CharlAR | 🔴 Urgente | ✓✓··· | v1.1 | — falta | ✅ auto + manual + restaurar (26/10); además se arreglaron las pestañas Perfil y Ánimo, que daban error | Pasar la key de GROQ a un Worker de Cloudflare (hoy está expuesta en el código); después el panel familiar con historial de conversaciones. |
| AhorrAR | 🔵 En desarrollo | ✓✓··· | v1.1 | — falta | ✅ auto + manual + restaurar, solo administrador (26/10); datos de toda la comunidad. El PIN de admin está en el código | Definir el modelo comercial para comercios; después el panel admin de promociones y la geolocalización por zona. |
| legalAR | 🔵 En desarrollo | ✓✓··· | v2.2 | — falta | ✅ auto + manual + restaurar (26/10). El backup anterior dejaba afuera causas y honorarios; ahora los incluye | Crear el Worker de LegalAR en Cloudflare (el código ya está listo) y agregar el dominio en Firebase Auth. |

## Backup (auditoría del 25/10/2026)

**Regla de Ruben:** todas las apps con backup automático y backup manual. Estándar aprobado: automático una vez por día al abrir la app (JSON al dispositivo), botón manual en Configuración, y botón para restaurar; archivo `[app]-backup-AAAA-MM-DD.json`.

Se revisó el código de las 22 apps (sin iniciar sesión en ellas: se verificó que la sintaxis es válida, que el botón y el disparo diario existen y que están conectados al ingreso).

- **Arreglado y probado el 26/10/2026 (9 apps):** CarneAR (prod v2.7 y beta v2.8-beta), BarbeAR v2.6, PizzAR v2.9, PanAR v1.7, lavAR v2.4, SecuroPro v2.3, Rodix v1.9.1, PuntoVenta v2.2, EmpresAR v2.1. Descarga el archivo solo una vez por día, deja copia local de los últimos 7 días, tiene botón manual y restaurar, vuelve las fechas a su tipo y no pisa plan ni permisos. Pruebas en simulador (24, 25, 23, 22, 20, 18, 16, 17 y 16 comprobaciones). **Falta probarlo en tu celular** (botón "Descargar backup" en Configuración/Ajustes).
- **Corrección de la auditoría anterior (la revisión por código había dado "completo" y era falso):** el "automático" de PizzAR, PanAR, PuntoVenta y EmpresAR no guardaba nada; en lavAR nunca corría para el dueño y el archivo salía sin sucursales; en SecuroPro y Rodix el backup estaba en un script aparte que no veía la base de datos y fallaba siempre (en SecuroPro además buscaba por `uid` cuando los datos están por `negocioId`, y no incluía `seguimiento`); en PuntoVenta el botón no funcionaba. Todo eso ya está corregido en las 9 apps.
- **Hallazgo PanAR:** un error de carga (faltaba la vista Stock) cortaba el script y dejaba sin funcionar cierre de caja, gastos, modo práctica y service worker. Corregido en v1.7; la vista Stock sigue faltando.
- **Parcial (1):** PeloteAR (solo al cierre del día y depende de un servidor en Railway; pendiente de decisión).
- **Puntos de resguardo:** cada repo tocado tiene una rama `pre-backup-2026-10-25` (CarneAR, BarbeAR) o `pre-backup-2026-10-26` (PizzAR, PanAR, lavAR) con el código anterior, por si hay que volver atrás.
- **Sin backup (1):** LogisAR (hoy es una demo sin base de datos; el backup se hace cuando tenga backend).
- **Agregado el 26/10 (segunda tanda, 9 apps):** GasAR admin 1.5.0, MiAgenda v2.5, SaludAR v2.7, AhorrAR 1.1, CharlAR 1.1, TimbreAr admin 1.1, CentralbotAr 0.2, CompraZona admin 0.5, MTC 1.3; y completados legalAR 2.2 (causas y honorarios no estaban en el backup; se agrega restaurar) y manejAr 2.3.0 (automático + restaurar). Todas con automático diario, manual y restaurar, probadas en simulador. Cada repo tiene la rama `pre-backup-2026-10-26` con el código anterior.
- **Hallazgos al revisar esas apps:** CharlAR tenía las pestañas Perfil y Ánimo rotas y un script mal cerrado (sin service worker ni registro de errores); MTC no guardaba sesiones de juegos ni historial de estudio (usaba `me.uid` siendo `me` ya el uid) y los juegos Plus daban error; CompraZona admin tenía una variable sin declarar; TimbreAr guarda los edificios solo en el navegador y su historial de visitas no funciona; GasAR solo puede restaurar el catálogo por las reglas de la base.
- **Verificación independiente (noche del 26/10/2026):** se repitió la prueba completa (generar → borrar los datos → restaurar → comparar) sobre una base Firestore simulada para CarneAR producción v2.7 y beta v2.8 (22 chequeos cada una), BarbeAR v2.6 (22), PizzAR v2.9 (21), PanAR v1.7 (20) y lavAR v2.4 (23): todas pasan. Se comprobó que restaura registros idénticos, que las fechas vuelven a ser fechas, que no pisa plan ni PIN, que rechaza archivos de otra app o rotos, que el cajero no puede respaldar ni restaurar y que el automático corre una sola vez por día. En las otras 15 apps (SecuroPro, Rodix, PuntoVenta, EmpresAR, MiAgenda, SaludAR, CharlAR, AhorrAR, GasAR, TimbreAr, legalAR, CentralbotAr, CompraZona, MTC, manejAr) se comprobó que el código compila y que el automático, el botón manual y el de restaurar están conectados; su prueba de ida y vuelta es la que se hizo en simulador el 26/10. **Nada de esto reemplaza la prueba en el celular real**, que sigue pendiente app por app.
- **Ninguna app tiene backup desde el servidor (punto D, pendiente de decidir).** El automático actual solo corre si el dueño abre la app ese día y baja el archivo a su celular. Opciones: (a) copias programadas nativas de Firestore, una por proyecto: exigen plan Blaze (con facturación), son diarias o semanales, retienen hasta 14 semanas y se restauran en una base nueva; se cobra el almacenamiento y la restauración ([documentación](https://firebase.google.com/docs/firestore/backups)); (b) exportación nocturna con GitHub Actions y una cuenta de servicio por proyecto guardada como secreto (más trabajo y más superficie de seguridad); (c) quedarse con el backup en el celular del dueño y sumar un aviso si pasan varios días sin respaldo.
- **Orden sugerido para arreglar:** 1) ✅ CarneAR y BarbeAR, 2) ✅ PizzAR, PanAR y lavAR, 2b) ✅ SecuroPro, Rodix, PuntoVenta y EmpresAR, 3) ✅ GasAR, MiAgenda y SaludAR, 4) ✅ TimbreAr, CharlAR, AhorrAR, CentralbotAr, CompraZona, MTC; 5) ✅ legalAR y manejAr; pendiente: PeloteAR (depende del servidor Railway) y LogisAR (cuando tenga backend). Punto D (backup nocturno desde el servidor): pendiente de decidir.

## Modo demo / práctica en todas las apps

Regla de Ruben: todas las apps deben tener Modo Práctica (o demo) por defecto. Orden elegido: primero la familia de cajas, después el resto.

- **Con 🎓 Modo Práctica en el código (8):** CarneAR, PizzAR, PanAR, lavAR, SecuroPro, Rodix, MiAgenda, GasAR.
- **Con demo propio (5):** manejAr (`?demo=1`), PeloteAR (`/demo`, sin Firebase), TimbreAr (edificio `raventechs-hq`), CompraZona (modo demo + simulador), LogisAR (demo con datos locales).
- **Solo cartel de vencimiento, sin datos de ejemplo (2):** PuntoVenta, EmpresAR.
- **Sin nada (7):** BarbeAR, SaludAR, CharlAR, AhorrAR, legalAR, CentralbotAr, MTC.
- **Siguiente en el orden:** BarbeAR y PuntoVenta, porque son cajas y la familia de cajas era la primera prioridad.
- manejAr ya tiene demo de 14 días con pantalla de bloqueo y cobro manual desde el panel interno. Sirve de modelo para el módulo genérico de demo/vencimiento, que sigue sin integrarse en CarneAR.

## Pendientes que no son una app

- **Keys expuestas:** MTC (Anthropic) y CharlAR (GROQ). Solución: proxy en Netlify Functions o Worker de Cloudflare.
- **Workers por crear en Cloudflare:** legalAR y CentralbotAr (el código ya está listo).
- **Dato a confirmar:** el token de Meta de CentralbotAr vence cada 24 h según el tablero y cada 60 días según el portal.
- **Repo `Chicho`:** vacío.

## Adicionales comerciales (8/11/2026)

Regla: cuentas anteriores a 9/11/2026 conservan todo; las nuevas lo ven en la prueba con ⭐ y después hay que activarlo con botones en el menú admin.
- **PizzAR v3.1 / PanAR v1.9:** Varias sucursales (1 / hasta 3 / todas); PizzAR además comandas, stock por receta; PanAR stock y recetas. Requiere pegar firestore.rules.
- **BarbeAR v3.2:** sucursales y barberos adicionales; agenda por barbero con carga tocando un horario libre; link de reserva en ventas.raventechsapp.com (probar).
- **SecuroPro v2.4:** Agenda y alertas. **manejAr v2.5:** Flota + Análisis avanzado. **CompraZona:** Destacada + Estadísticas de ventas. **GasAR v1.7:** Revendedores y cuentas corrientes + Reparto en camionetas.
- **Menús admin:** ya sin números tipeados (lavAR, PuntoVenta, MiAgenda, SaludAR). MiAgenda: Recordatorios PLUS reparados. BarbeAR v3.2: botón Turno con calendario.
- **Pendiente:** TimbreAR (parte 2 + 2 plus, requiere reglas), EmpresAR (repo sin clonar); CompraZona plusStats puede auto-activarse el dueño (endurecer reglas).

## Cómo usar este archivo

1. Leerlo al arrancar cualquier tarea sobre las apps.
2. Al terminar una prueba o un cambio, actualizar la fila de esa app (etapas, backup y próximo paso).
3. Una sola fuente de verdad: si el tablero y esto no coinciden, se corrige acá y en el tablero.
