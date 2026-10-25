# Estado del portfolio RavenTechs

Base de trabajo, actualizada el 25/10/2026 (incluye manejAr y la auditoría de backup). Es la misma información del tablero maestro, en un formato que se lee desde cualquier chat.

**Etapas:** 1 Construida · 2 Publicada · 3 Práctica/demo lista · 4 Probada por vos · 5 Con clientes. `✓` = hecha, `·` = falta.

**Fuentes:** tablero maestro (`raventechs-tablero.html`, v2.3.0), portal (`raventechs.github.io`), código de cada repo y lo que Ruben confirmó de palabra. Las tildes que se marcan tocando el tablero se guardan solo en el celular, así que este archivo es la referencia compartida.

## Tabla de apps

| App | Estado | Etapas | Versión | Modo práctica / demo | Backup | Próximo paso |
|---|---|---|---|---|---|---|
| GasAR | 🟡 Para vender/probar | ✓✓✓·· | admin 1.4.0 · vendedor 1.3.0 | 🎓 Práctica (Modo Raven) | ❌ ninguno (solo CSV) | Firebase → Authentication → Comenzar; habilitar Google y Correo/Contraseña. Después crear la distribuidora de PRÁCTICA y tildar los 10 pasos. |
| manejAr | 🟢 Con clientes | ✓✓✓✓✓ | v2.2.0 | Demo propio (?demo=1, 4 semanas de datos) | 🟡 solo manual (JSON y CSV) + copia en la nube; sin auto ni restaurar | Plan Flota: revisar cómo se crea desde Ajustes y probarlo con Firebase real. Después, el backup automático de las 2 AM. |
| MTC | 🔴 Urgente | ✓✓··· | — | — falta | ❌ ninguno (solo CSV) | Sacar la API key del cliente con un proxy en Netlify Functions. |
| CarneAR | 🟢 Con clientes | ✓✓✓·· | v2.6 prod · v2.7 beta | 🎓 Práctica (prod y beta) | 🔴 roto: llama a una función que no existe (prod y beta) | Probar 🎓 Modo Práctica en una cuenta tuya; después pasar peso libre y login anónimo de la beta a producción. |
| CompraZona | 🟡 Para vender/probar | ✓✓✓·· | — | Demo propio (modo demo + simulador) | ❌ ninguno | Publicar reglas v0.2, activar App Check y salir a conseguir las primeras garraferas. |
| Rodix | 🟢 Con clientes | ✓✓✓·✓ | v1.9.0 | 🎓 Práctica | ✅ auto + manual + restaurar (completo) | Probar 🎓 Modo Práctica en Ajustes con una cuenta de pruebas. |
| SecuroPro | 🟡 Para vender/probar | ✓✓✓·· | v2.2 | 🎓 Práctica | ✅ auto + manual + restaurar (verificar `seguimiento`) | Probar 🎓 Modo Práctica en Mi Empresa y revisar los precios del catálogo (son estimativos). |
| PizzAR | 🟡 Para vender/probar | ✓✓✓·· | v2.8 | 🎓 Práctica | ✅ auto + manual + restaurar (le faltan gastos y comandas) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. |
| PanAR | 🟡 Para vender/probar | ✓✓✓·· | v1.6 | 🎓 Práctica | ✅ auto + manual + restaurar (le faltan gastos) | Publicar firestore.rules (Firebase), probar link de cajero + 🎓 Práctica; después cierre de caja por WhatsApp. |
| lavAR | 🟡 Para vender/probar | ✓✓✓·· | v2.3 | 🎓 Práctica | ✅ auto + manual + restaurar (le faltan gastos y empleados) | Probar 🎓 Modo Práctica y activar una sede para ver la caja. |
| MiAgenda | 🟢 Con clientes | ✓✓✓✓· | v2.4 | 🎓 Práctica (actividades de ejemplo) | ❌ ninguno (solo CSV) | Agregar el botón "Eliminar usuario". |
| SaludAR | 🟡 Para vender/probar | ✓✓··· | — | — falta | ❌ ninguno (solo CSV) | Confirmar que llega una sola notificación a la hora correcta con la app instalada. |
| BarbeAR | 🟡 Para vender/probar | ✓✓·✓· | — | — falta | 🔴 roto: igual que CarneAR | Sumarle el 🎓 Modo Práctica como a las demás cajas y probarla con una barbería real. |
| PeloteAR | 🟡 Para vender/probar | ✓✓✓✓· | — | Demo propio (/demo, sin Firebase) | 🟡 solo al cierre del día, vía servidor Railway; sin manual ni restaurar | Pasarla a offline-first (hoy depende de un servidor en Railway) y sumar el aviso de turnos por WhatsApp. |
| TimbreAr | 🟡 Para vender/probar | ✓✓✓✓· | — | Demo propio (edificio raventechs-hq) | ❌ ninguno | Validar el aviso con la app cerrada en Xiaomi y probarla en un edificio real; después video y modo no molestar. |
| LogisAR | 🔵 En desarrollo | ····· | demo v0.3 (sin backend) | Demo con datos locales | ❌ ninguno (solo CSV) | Crear el proyecto Firebase, pegar la config y publicar las reglas de Firestore (todavía sin probar); después mostrar la demo al cliente y definir tarifas. |
| Embudo de demos | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Hacer la landing de entrega genérica para las 10 apps. |
| Módulo demo/vencimiento | 🔵 En desarrollo | ····· | — | n/a (proyecto interno) | n/a (proyecto interno) | Esperar a que CarneAR tenga peso libre y login anónimo; recién ahí integrarlo. |
| Panel RavenTechs | 🔵 En desarrollo | ✓···· | — | n/a (proyecto interno) | n/a (proyecto interno) | Crear el proyecto Firebase raventechs-admin y pegar su config. |
| CentralbotAr | 🔵 En desarrollo | ✓✓··· | — | — falta | ❌ ninguno | Renovar el token de Meta (vence cada 24 h) y hacer la pantalla "Mi equipo". |
| PuntoVenta | 🟡 Para vender/probar | ✓✓··· | — | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar (verificar `empleados`) | Probar crear una sucursal nueva y la cuenta corriente con morosidad; después límite de crédito y reporte de morosos. |
| EmpresAR | 🟡 Para vender/probar | ✓✓··· | — | Solo cartel de vencimiento (sin datos de ejemplo) | ✅ auto + manual + restaurar | Probarla con la empresa de gas envasado cargando sus documentos reales; los módulos Plus (ventas, stock, flota) quedan para la próxima versión. |
| CharlAR | 🔴 Urgente | ✓✓··· | — | — falta | ❌ ninguno (solo CSV) | Pasar la key de GROQ a un Worker de Cloudflare (hoy está expuesta en el código); después el panel familiar con historial de conversaciones. |
| AhorrAR | 🔵 En desarrollo | ✓✓··· | — | — falta | ❌ ninguno (solo CSV) | Definir el modelo comercial para comercios; después el panel admin de promociones y la geolocalización por zona. |
| legalAR | 🔵 En desarrollo | ✓✓··· | — | — falta | 🟡 auto + manual, sin restaurar (solo historial) | Crear el Worker de LegalAR en Cloudflare (el código ya está listo) y agregar el dominio en Firebase Auth. |

## Backup (auditoría del 25/10/2026)

**Regla de Ruben:** todas las apps con backup automático y backup manual. Estándar aprobado: automático una vez por día al abrir la app (JSON al dispositivo), botón manual en Configuración, y botón para restaurar; archivo `[app]-backup-AAAA-MM-DD.json`.

Se revisó el código de las 22 apps (sin iniciar sesión en ellas: se verificó que la sintaxis es válida, que el botón y el disparo diario existen y que están conectados al ingreso).

- **Completo, automático + manual + restaurar (7):** PizzAR, PanAR, lavAR, SecuroPro, Rodix, PuntoVenta, EmpresAR.
- **Parcial (3):** legalAR (sin restaurar), manejAr (solo manual), PeloteAR (solo al cierre del día y depende de Railway).
- **Roto (2):** CarneAR (producción y beta) y BarbeAR. El código llama a `chequearBackupDiario()` pero la función no existe, y un chequeo `typeof` lo oculta: no falla, pero tampoco respalda nada. Se perdió al reescribir CarneAR desde v1.3 a v2.5.
- **Sin backup (10):** GasAR, MiAgenda, SaludAR, TimbreAr, CharlAR, AhorrAR, CentralbotAr, CompraZona, MTC, LogisAR. La mayoría solo exporta CSV, que sirve para mirar datos pero no para restaurarlos.
- **Backups incompletos (verificados):** PizzAR no incluye gastos ni comandas; PanAR no incluye gastos; lavAR no incluye gastos ni empleados. Hay que sumar esas colecciones al backup y a la restauración.
- **Ninguna app tiene backup desde el servidor.** El automático actual solo corre si el dueño abre la app ese día. Pendiente decidir la opción de backup nocturno a las 2 AM (GitHub Actions) que se propuso para manejAr.
- **Orden sugerido para arreglar:** 1) CarneAR y BarbeAR (hay usuarios reales), 2) completar PizzAR, PanAR y lavAR, 3) sumar el estándar a las apps sin backup que ya van a clientes (GasAR, MiAgenda, SaludAR), 4) el resto.

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
