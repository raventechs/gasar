# Estado del portfolio RavenTechs

Base de trabajo, actualizada el 26/10/2026 (incluye manejAr, la auditoría de backup y los arreglos del 26/10). Es la misma información del tablero maestro, en un formato que se lee desde cualquier chat.

**Etapas:** 1 Construida · 2 Publicada · 3 Práctica/demo lista · 4 Probada por vos · 5 Con clientes. `✓` = hecha, `·` = falta.

**Fuentes:** tablero maestro (`raventechs-tablero.html`, v2.3.0), portal (`raventechs.github.io`), código de cada repo y lo que Ruben confirmó de palabra. Las tildes que se marcan tocando el tablero se guardan solo en el celular, así que este archivo es la referencia compartida.

## Tabla de apps

| App | Estado | Etapas | Versión | Modo práctica / demo | Backup | Próximo paso |
|---|---|---|---|---|---|---|
| GasAR | 🟡 Para vender/probar | ✓✓✓·· | admin 1.5.0 · vendedor 1.3.0 | 🎓 Práctica (Modo Raven) | ✅ auto (solo administrador) + manual + restaurar catálogo (26/10; el historial de ventas/cajas NO se restaura desde la app por las reglas; probado en simulador, falta probar en tu celular) | Firebase → Authentication → Comenzar; habilitar Google y Correo/Contraseña. Después crear la distribuidora de PRÁCTICA y tildar los 10 pasos. |
| manejAr | 🟢 Con clientes | ✓✓✓✓✓ | v2.2.0 | Demo propio (?demo=1, 4 semanas de datos) | 🟡 solo manual (JSON y CSV) + copia en la nube; sin auto ni restaurar | Plan Flota: revisar cómo se crea desde Ajustes y probarlo con Firebase real. Después, el backup automático de las 2 AM. |
| MTC | 🔴 Urgente | ✓✓··· | v1.3 | — falta | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular). Además se corrigieron las sesiones de juegos y el historial del modo estudio, que nunca se guardaban | Sacar la API key del cliente con un proxy en Netlify Functions. |
| CarneAR | 🟢 Con clientes | ✓✓✓·· | v2.7 prod · v2.8-beta | 🎓 Práctica (prod y beta) | ✅ auto + manual + restaurar (arreglado 26/10, probado en simulador; falta probar en tu celular) | Probar 🎓 Modo Práctica en una cuenta tuya; después pasar peso libre y login anónimo de la beta a producción. |
| CompraZona | 🟡 Para vender/probar | ✓✓✓·· | admin v0.5 | Demo propio (modo demo + simulador) | ✅ auto + manual + restaurar catálogo, solo super admin (26/10); pedidos y usuarios van en el archivo pero no se restauran (reglas) | Publicar reglas v0.2, activar App Check y salir a conseguir las primeras garraferas. |
| Rodix | 🟢 Con clientes | ✓✓✓·✓ | v1.9.1 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar 🎓 Modo Práctica en Ajustes con una cuenta de pruebas. |
| SecuroPro | 🟡 Para vender/probar | ✓✓✓·· | v2.3 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar 🎓 Modo Práctica en Mi Empresa y revisar los precios del catálogo (son estimativos). |
| PizzAR | 🟡 Para vender/probar | ✓✓✓·· | v2.9 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: incluye gastos y comandas; falta probar en tu celular) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. |
| PanAR | 🟡 Para vender/probar | ✓✓✓·· | v1.7 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: incluye gastos; falta probar en tu celular) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. ⚠️ Falta la vista Stock (el botón existe pero no hay pantalla). |
| lavAR | 🟡 Para vender/probar | ✓✓✓·· | v2.4 | 🎓 Práctica | ✅ auto + manual + restaurar (arreglado 26/10: sucursales, gastos, fidelización y empleados; falta probar en tu celular) | Probar 🎓 Modo Práctica y activar una sede para ver la caja. |
| MiAgenda | 🟢 Con clientes | ✓✓✓✓· | v2.5 | 🎓 Práctica (actividades de ejemplo) | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular) | Agregar el botón "Eliminar usuario". |
| SaludAR | 🟡 Para vender/probar | ✓✓··· | v2.7 | — falta | ✅ auto + manual + restaurar (agregado 26/10; falta probar en tu celular) | Confirmar que llega una sola notificación a la hora correcta con la app instalada. |
| BarbeAR | 🟡 Para vender/probar | ✓✓·✓· | v2.6 | — falta | ✅ auto + manual + restaurar (arreglado 26/10, probado en simulador; falta probar en tu celular) | Sumarle el 🎓 Modo Práctica como a las demás cajas y probarla con una barbería real. |
| PeloteAR | 🟡 Para vender/probar | ✓✓✓✓· | — | Demo propio (/demo, sin Firebase) | 🟡 solo al cierre del día, vía servidor Railway; sin manual ni restaurar | Pasarla a offline-first (hoy depende de un servidor en Railway) y sumar el aviso de turnos por WhatsApp. |
| TimbreAr | 🟡 Para vender/probar | ✓✓✓✓· | admin v1.1 | Demo propio (edificio raventechs-hq) | ✅ consola admin: auto + manual + restaurar (26/10). Ojo: los edificios de la consola viven solo en el navegador (localStorage); pasarlos a la base | Validar el aviso con la app cerrada en Xiaomi y probarla en un edificio real; después video y modo no molestar. |
| LogisAR | 🔵 En desarrollo | ····· | demo v0.3 (sin backend) | Demo con datos locales | ❌ ninguno (solo CSV) | Crear el proyecto Firebase, pegar la config y publicar las reglas de Firestore (todavía sin probar); después mostrar la demo al cliente y definir tarifas. |
| Embudo de demos | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Hacer la landing de entrega genérica para las 10 apps. |
| Módulo demo/vencimiento | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Esperar a que CarneAR tenga peso libre y login anónimo; recién ahí integrarlo. |
| Panel RavenTechs | 🔵 En desarrollo | ✓···· | — | n/a (proyecto interno) | n/a (proyecto interno) | Crear el proyecto Firebase raventechs-admin y pegar su config. |
| CentralbotAr | 🔵 En desarrollo | ✓✓··· | v0.2 | — falta | ✅ auto + manual + restaurar, sin el token de WhatsApp (26/10) | Renovar el token de Meta (vence cada 24 h) y hacer la pantalla "Mi equipo". |
| PuntoVenta | 🟡 Para vender/probar | ✓✓··· | v2.2 | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probar crear una sucursal nueva y la cuenta corriente con morosidad; después límite de crédito y reporte de morosos. |
| EmpresAR | 🟡 Para vender/probar | ✓✓··· | v2.1 | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar (arreglado 26/10; falta probar en tu celular) | Probarla con la empresa de gas envasado cargando sus documentos reales; los módulos Plus (ventas, stock, flota) quedan para la próxima versión. |
| CharlAR | 🔴 Urgente | ✓✓··· | v1.1 | — falta | ✅ auto + manual + restaurar (26/10); además se arreglaron las pestañas Perfil y Ánimo, que daban error | Pasar la key de GROQ a un Worker de Cloudflare (hoy está expuesta en el código); después el panel familiar con historial de conversaciones. |
| AhorrAR | 🔵 En desarrollo | ✓✓··· | v1.1 | — falta | ✅ auto + manual + restaurar, solo administrador (26/10); datos de toda la comunidad. El PIN de admin está en el código | Definir el modelo comercial para comercios; después el panel admin de promociones y la geolocalización por zona. |
| legalAR | 🔵 En desarrollo | ✓✓··· | — | — falta | 🟡 auto + manual, sin restaurar (solo historial) | Crear el Worker de LegalAR en Cloudflare (el código ya está listo) y agregar el dominio en Firebase Auth. |

## Backup (auditoría del 25/10/2026)

**Regla de Ruben:** todas las apps con backup automático y backup manual. Estándar aprobado: automático una vez por día al abrir la app (JSON al dispositivo), botón manual en Configuración, y botón para restaurar; archivo `[app]-backup-AAAA-MM-DD.json`.

Se revisó el código de las 22 apps (sin iniciar sesión en ellas: se verificó que la sintaxis es válida, que el botón y el disparo diario existen y que están conectados al ingreso).

- **Arreglado y probado el 26/10/2026 (9 apps):** CarneAR (prod v2.7 y beta v2.8-beta), BarbeAR v2.6, PizzAR v2.9, PanAR v1.7, lavAR v2.4, SecuroPro v2.3, Rodix v1.9.1, PuntoVenta v2.2, EmpresAR v2.1. Descarga el archivo solo una vez por día, deja copia local de los últimos 7 días, tiene botón manual y restaurar, vuelve las fechas a su tipo y no pisa plan ni permisos. Pruebas en simulador (24, 25, 23, 22, 20, 18, 16, 17 y 16 comprobaciones). **Falta probarlo en tu celular** (botón "Descargar backup" en Configuración/Ajustes).
- **Corrección de la auditoría anterior (la revisión por código había dado "completo" y era falso):** el "automático" de PizzAR, PanAR, PuntoVenta y EmpresAR no guardaba nada; en lavAR nunca corría para el dueño y el archivo salía sin sucursales; en SecuroPro y Rodix el backup estaba en un script aparte que no veía la base de datos y fallaba siempre (en SecuroPro además buscaba por `uid` cuando los datos están por `negocioId`, y no incluía `seguimiento`); en PuntoVenta el botón no funcionaba. Todo eso ya está corregido en las 9 apps.
- **Hallazgo PanAR:** un error de carga (faltaba la vista Stock) cortaba el script y dejaba sin funcionar cierre de caja, gastos, modo práctica y service worker. Corregido en v1.7; la vista Stock sigue faltando.
- **Parcial (3):** legalAR (sin restaurar), manejAr (solo manual), PeloteAR (solo al cierre del día y depende de Railway).
- **Puntos de resguardo:** cada repo tocado tiene una rama `pre-backup-2026-10-25` (CarneAR, BarbeAR) o `pre-backup-2026-10-26` (PizzAR, PanAR, lavAR) con el código anterior, por si hay que volver atrás.
- **Sin backup (1):** LogisAR (hoy es una demo sin base de datos; el backup se hace cuando tenga backend).
- **Agregado el 26/10 (segunda tanda, 9 apps):** GasAR admin 1.5.0, MiAgenda v2.5, SaludAR v2.7, AhorrAR 1.1, CharlAR 1.1, TimbreAr admin 1.1, CentralbotAr 0.2, CompraZona admin 0.5, MTC 1.3. Todas con automático diario, manual y restaurar, probadas en simulador. Cada repo tiene la rama `pre-backup-2026-10-26` con el código anterior.
- **Hallazgos al revisar esas apps:** CharlAR tenía las pestañas Perfil y Ánimo rotas y un script mal cerrado (sin service worker ni registro de errores); MTC no guardaba sesiones de juegos ni historial de estudio (usaba `me.uid` siendo `me` ya el uid) y los juegos Plus daban error; CompraZona admin tenía una variable sin declarar; TimbreAr guarda los edificios solo en el navegador y su historial de visitas no funciona; GasAR solo puede restaurar el catálogo por las reglas de la base.
- **Ninguna app tiene backup desde el servidor.** El automático actual solo corre si el dueño abre la app ese día. Pendiente decidir la opción de backup nocturno a las 2 AM (GitHub Actions) que se propuso para manejAr.
- **Orden sugerido para arreglar:** 1) ✅ CarneAR y BarbeAR, 2) ✅ PizzAR, PanAR y lavAR, 2b) ✅ SecuroPro, Rodix, PuntoVenta y EmpresAR, 3) ✅ GasAR, MiAgenda y SaludAR, 4) ✅ TimbreAr, CharlAR, AhorrAR, CentralbotAr, CompraZona, MTC; 5) pendiente: legalAR restaurar, manejAr auto + restaurar, PeloteAR, y LogisAR cuando tenga backend.

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

## Cómo usar este archivo

1. Leerlo al arrancar cualquier tarea sobre las apps.
2. Al terminar una prueba o un cambio, actualizar la fila de esa app (etapas, backup y próximo paso).
3. Una sola fuente de verdad: si el tablero y esto no coinciden, se corrige acá y en el tablero.
