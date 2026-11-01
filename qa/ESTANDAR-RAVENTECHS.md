# Estándar RavenTechs para toda app nueva (y para llevar las existentes al mismo nivel)

Última actualización: 31/10/2026. Cada app nueva debe cumplir los 12 puntos antes de venderse.

## Los 12 puntos
1. **Reglas Firestore endurecidas** (archivo en `qa/rules/<app>.rules`): todo cerrado por defecto; el dueño solo ve lo suyo; admin = `rgaraventa@gmail.com` con email verificado; el cliente NO puede cambiar `status`, `banned`, `demoHasta`/`demoExpiry`, `isAdmin`, `features`; consultas con los filtros que prueban la regla. Nunca borran ni modifican datos existentes.
2. **Sin PIN fijo.** El menú oculto (5 toques al logo) abre directo solo con la cuenta admin; si no es admin, no pasa nada.
3. **Menú admin solo con botones:** lista de clientes con estado y botones `+7 días`, `+30 días`, `✅ Pasar a cliente` / `Activar`. Nunca escribir números ni códigos.
4. **Prueba gratis de 14 días:** campo `demoHasta` (fin; `null` = cliente real; ausente = cuenta vieja → arranca 14 días al ingresar, una sola vez). Cartel de días (rojo y titilante con 3 o menos), pantalla de bloqueo con botón WhatsApp "Activar mi cuenta" (wa.me/5491136547592), nunca pierde datos. Admin exento. Cajeros no se bloquean.
5. **Modo Práctica:** botón en Config que carga datos de ejemplo marcados `_demo:true` y otro que los quita. Solo toca lo marcado; nunca datos reales. Si la app comparte datos entre usuarios, usar recorrido guiado sin guardar.
6. **Backup:** automático una vez por día al abrir (copia en el equipo) + botones Descargar / Restaurar en Config.
7. **Instructivo** en `ayuda/index.html` + PDF (`Guia-<App>.pdf`) y botón "❓ Instructivo" en Config: qué es, instalar (Android/iPhone), entrar con Google, prueba de 14 días, pantallas, equipo, práctica, backup, preguntas frecuentes, WhatsApp.
8. **PWA:** manifest con `start_url:"/"`, íconos 192/512/maskable, service worker `sw-<app>.js`, banner de instalación, login con Google primero.
9. **Registro de errores** a la colección `errores` (solo crear; lee el admin).
10. **Cajeros/empleados sin cuenta (si aplica):** membresía validada contra el link, atada a su sucursal, código guardado en el equipo; invitaciones de un solo uso.
11. **Sin claves secretas en el código** (Anthropic, Groq, etc.): las claves van en un servidor intermedio. Las claves públicas de Firebase sí pueden estar en el cliente.
12. **Verificación antes de entregar:** chequeo de sintaxis del script, flujo de login, un alta nueva, un cajero/empleado, prueba vencida y pase a cliente.

## Regla permanente
Hay clientes activos con datos reales: ningún cambio de reglas, código o migración puede borrar ni modificar sus datos. Se acepta una interrupción corta, nunca pérdida de datos.

## Forma de trabajo
Juntar todos los cambios de reglas y pegarlas **una sola vez por app**. Siempre entregar archivos o reglas COMPLETOS, listos para copiar y pegar, con pasos.

## Brechas conocidas (31/10/2026)
- Demo de 14 días con bloqueo: solo CarneAR, BarbeAR, LavAR, PanAR, PizzAR. Las demás usan el modelo viejo (`status` + `demoExpiry`, con botones +7/+30/Activar) y MDTC no tiene plan.
- Modo Práctica: faltan AhorrAR, CharlAR, LegalAR, CentralBot, MTC (datos compartidos o personales → recorrido guiado).
- Instructivo con PDF: faltan las demás apps (hecho en Rodix, CarneAR, BarbeAR, LavAR, PuntoVenta, SecurePro).
- Claves expuestas: MTC (Anthropic) y CharlAR (Groq).
- TimbrAR muestra teléfonos de vecinos a visitantes (rediseño pendiente).
- Backup nocturno desde servidor, y Client ID de Google para el panel central.
