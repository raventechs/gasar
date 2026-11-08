# RavenTechs — Traspaso para arrancar un chat nuevo (8/11/2026, 17:00)

Pegá este archivo (o pedile al chat nuevo que lo lea) y seguí como si fuera el mismo chat. Todo lo que está acá es continuación exacta del chat anterior; no hace falta buscar nada en chats viejos.

## 1. Quién es Ruben y cómo trabajar con él
- Ruben Garaventa, fundador de RavenTechs (raventechs.lat), Argentina. Arma un portfolio de apps SaaS para comercios chicos y las vende. También tiene una empresa de electrónica de seguridad.
- Trabaja desde el celular. No escribe código ni usa terminal: Claude es su ejecutor técnico completo. Él decide, vende, prueba en el celular y pega reglas en Firebase.
- Habla en español. Tono respetuoso, lenguaje medianamente técnico, pasos paso a paso.
- Preferencias fijas:
  1. Preguntas técnicas y de funcionalidad en formato multiple choice, con la recomendación explícita (la mejor desde lo profesional y lo menos complicado).
  2. Listas directamente en el chat.
  3. Siempre dar el texto, archivo o reglas COMPLETOS listos para copiar y pegar de una vez, nunca bloques parciales, con instrucciones paso a paso.
  4. Juntar todos los cambios de reglas Firestore y pedirle que pegue UNA sola vez por app.
  5. Menú admin oculto de las apps: solo botones simples (activar cliente, más días, límites con botones), nunca escribir códigos ni números.
  6. Regla permanente: hay clientes reales con datos cargados. Ningún cambio (código, reglas, migraciones) puede borrar ni modificar sus datos. Acepta una interrupción corta de acceso, nunca pérdida de datos.
  7. Visión comercial: cada app debe ser funcional Y vendible (kit de venta: prueba de 14 días, instructivo, folleto, plus para upgrades).
  8. Antes de cambiar algo, chequear las reglas que ya acordamos para no hacer el trabajo dos veces.
- Modo de trabajo pedido: continuar de forma autónoma, sin pedir confirmación por cada paso, dando permiso total para leer, modificar y subir a los repos de la organización GitHub `raventechs`. Preguntar solo si una decisión es irreversible o puede ir razonablemente para dos lados. Tras cada cambio: probar en el simulador, subir (commit + push), actualizar tablero, ESTADO y memoria, y avisarle qué probar en el celular.
- Límites técnicos de Claude en la sesión: no puede crear repos, activar GitHub Pages, tocar DNS ni Firebase Console, ni ingresar claves o contraseñas. Esos pasos los hace Ruben y hay que dárselos paso a paso. El sitio de la empresa y los repos están en GitHub (`raventechs`); la sesión tiene permiso de escritura vía add_repo.
- Commits: terminar con las dos líneas de atribución que indique el sistema de la sesión.

## 2. Cómo arrancar el chat nuevo (checklist de Claude)
1. Leer este archivo y la memoria del proyecto (`areas/etapa-comercial.md` tiene el historial; `/areas/pendientes.md`, `/areas/mapa-apps.md`, `/areas/estandar-apps.md`).
2. Clonar los repos que se necesiten con `add_repo` (owner `raventechs`, acceso push). Los repos de trabajo del entorno anterior NO persisten: hay que volver a clonar.
3. Recuperar el entorno de pruebas desde el repo `raventechs/gasar`, carpeta `qa/harness/` (simulador Firebase y pruebas, ver sección 6).
4. Seguir por la lista de pendientes de la sección 5.

## 3. Mapa de apps y repos (organización GitHub `raventechs`)
| App | Repo | Dominio / dónde vive | Versión reciente |
|---|---|---|---|
| PizzAR | pizzAr | ver /areas/mapa-apps.md | v3.1 (sucursales, checklist) |
| PanAR | panar | ver /areas/mapa-apps.md | v1.9 |
| lavAR | lavar | lavar | menús admin con botones (SW v2.7) |
| BarbeAR | barbear | barbear | v3.2 (botón Turno, agenda, adicionales) |
| Reservas de BarbeAR | Chicho (carpeta `reservar-barbear/`) | https://ventas.raventechsapp.com/reservar-barbear/?neg=<uid> | corregida |
| Sitio comercial / app de vendedores | Chicho | https://ventas.raventechsapp.com (vendedores, probar, folletos) | vendedores v1.9 |
| PeloteAR | PeloteAr | | checklist, SW v1.2 |
| CarneAR | carneAr (producción), carnear-beta | | v2.9.3 |
| SecuroPro | securepro | | v2.4 (plus) |
| manejAr | ManejAr | | v2.5 (Flota + Análisis avanzado) |
| CompraZona | comprazona | comprazona.raventechsapp.com | panel empresa con plus Ventas (SW v7); reglas v0.3 pendientes de pegar |
| GasAR | gasar (también guarda tablero y ESTADO) | raventechs.github.io/gasar/ | admin v1.7.0-plus |
| TimbreAR | timbrear | timbrear.raventechsapp.com | prueba 14 días, instructivo |
| PuntoVenta | puntoventa | | límites con botones (SW v2.4) |
| MiAgenda | miagenda | | límite con botones, Recordatorios PLUS reparados (SW v2) |
| SaludAR | saludar | | cupo y perfiles con botones (SW v3) |
| Rodix | vehigest-ar | | v1.9.4 |
Otros repos: raventechs.github.io (portfolio, redirige a ventas), panel, mdtc (MTC), legalar, Garrafar, charlar, centralbotAr, ahorrar, raventechs-traductor-habitos, promptAr, admin y betas.
Tablero maestro: `gasar/raventechs-tablero.html` (v2.9.4). Estado del portfolio: `gasar/ESTADO-PORTFOLIO.md`. Auditorías y estándar: `gasar/qa/`.

## 4. Modelos y reglas comerciales ya definidos (no reinventar)
- **Prueba de 14 días**: campo `demoHasta`. Ausente = cliente existente (no ve nada); null = activado. En las apps con el modelo nuevo (CarneAR, PizzAR, PanAR, lavAR, BarbeAR, PeloteAR, GasAR, CompraZona, manejAr, TimbreAR) la prueba NO bloquea: al vencer aparece un cartel rojo titilante fijo que no se cierra. PuntoVenta, SecuroPro, Rodix, SaludAR, MiAgenda y EmpresAR usan el modelo viejo (status/demoExpiry) y Ruben decidió no migrarlos. WhatsApp de activación: 5491136547592.
- **Checklist «Tus primeros pasos»** en las 6 apps con demoHasta (solo dueño y solo durante la prueba; se guarda en el celular, sin reglas).
- **Plus / adicionales (mínimo 2 por app, para ofrecer upgrades)**: regla común: las cuentas anteriores al 9/11/2026 (`PLUS_DESDE = Date.UTC(2026,10,9)`) conservan todo; las nuevas lo ven en la prueba con etiqueta ⭐ Plus; después se activa con botones en el menú admin; sin plus aparece una tarjeta con botón de WhatsApp. Nunca se bloquean ni se borran datos (al activar el plus vuelven a verse).
  - PizzAR y PanAR: varias sucursales (limiteSucursales 1 / hasta 3 / todas), además de comandas y stock.
  - BarbeAR: sucursales y barberos (limiteBarberos).
  - SecuroPro: Agenda y alertas (features.agenda, límite de alertas).
  - manejAr: Flota y Análisis avanzado (plusAnalisis).
  - CompraZona: Destacada y Estadísticas de ventas (plusStats).
  - GasAR: Revendedores y cuentas corrientes (plusRevendedores) y Reparto en camionetas (plusReparto), con botones en Modo Raven.
  - Falta: TimbreAR y EmpresAR.
- **Menú admin oculto**: se abre con 5 toques al logo/título solo para la cuenta rgaraventa@gmail.com (flag `rt_admin` en localStorage). Solo botones.
- **Sucursales (PizzAR/PanAR)**: ventas, gastos, cierres y comandas van a `negocios/{owner}/sucursales/{id}/<col>`; productos, insumos, configuración y recetas son compartidos; cajero entra por link `?n=OWNER&s=SUCID`.
- **Reservas de BarbeAR**: la página pública vive en otro dominio (ventas.raventechsapp.com) a propósito, porque en el mismo dominio la app instalada captura el link. Escribe `turnos` y `ocupados` sin login. La app muestra Turnos con lista y «Agenda por barbero» (calendario mensual, 🌐 web / ✍️ local, tocar un horario libre carga el turno), y un botón 📅 Turno en la caja.

## 5. Pendientes vigentes (en orden recomendado)
1. **Ruben pega las reglas de CompraZona v0.3** (proyecto Firebase ravenmarket-c2739; archivo `firestore-rules.txt` del repo comprazona o `firestore-comprazona.rules.txt`). Evita que el dueño de una empresa se active el plus. Ya pegó las de PizzAR y PanAR.
2. **EmpresAR**: sumar sus 2 plus. El repo no está en la organización; hace falta que Ruben diga dónde está o lo agregue.
3. **Visitas por vendedor** (medir las visitas a la landing /probar/ por código de vendedor): hace falta que Ruben copie las reglas actuales del proyecto Firebase raventech-vendedores (no están en el repo) antes de modificarlas.
4. **TimbreAR**: parte 2 (pasar los edificios de la consola admin, hoy en localStorage del navegador, a la base, con reglas; resolver que la cuenta Google de Ruben llega con token sin correo), luego sus 2 plus; parte 3: aviso push con la app cerrada en Xiaomi (probar con dos celulares). Proyecto aparte, con calma.
5. Pilar 3 del embudo de demos: seguimiento humano.
6. Paquete en pausa (solo si Ruben lo pide): CharlAR, Traductor de Hábitos y MTC (claves expuestas de Anthropic y Groq, Worker en Cloudflare, dominio habitos).
7. Futuro: CarneAR con «máscaras» por rubro (carnicería, bazar, ropa).
8. Cada vez que Ruben prueba en el celular y avisa fallas, corregir, probar, subir y avisar.
Todo lo anterior a hoy ya lo probó Ruben OK en el celular, incluyendo la reserva de BarbeAR, las sucursales de PizzAR/PanAR y los menús admin con botones.

## 6. Entorno de pruebas (en `raventechs/gasar`, carpeta `qa/harness/`)
- `fake_firebase_tw.js`: simulador de Firebase para apps con SDK compat (para usar con Playwright; interceptar `**/www.gstatic.com/**` y entregar este archivo). Para algunas apps hay que agregar `enablePersistence` y `getRedirectResult` (ver cómo lo hacen los test_*.py).
- `fake_modular.py`: simulador para apps con SDK modular (PuntoVenta, MiAgenda, SaludAR). Función `install(pg)`.
- `test_*.py`: pruebas por app (pizzar, panar, lavar, barbear, pelotear, comprazona, gasar, manejar, timbrear, sucursales, toggles, agenda, reservas).
- `patch_sucursales.py`: parcheador genérico de sucursales; `gen_*.py` y `build_ventas.py`: generadores de folletos, instructivos, landing y sitio de ventas.
- Cómo se corre: servidor local (`python3 -m http.server <puerto>` en la carpeta de cada app) y Playwright con chromium; chequeo de sintaxis con acorn (`/tmp/ac`, `npm i acorn` si falta). Los puertos usados antes: 8767 gasar, 8768 pizzar, 8769 panar, 8770 lavar, 8771 barbear, 8773 chicho, 8774 puntoventa, 8775 miagenda, 8776 saludar.
- Aprendizajes: scripts clásicos no ven las variables de un `<script type="module">` (hay que exponerlas en `window`); en HTML con `onclick` dentro de módulos, la función también tiene que estar en `window`; cada release sube el nombre de caché del service worker; las apps instaladas capturan links del mismo dominio.

## 6b. Reglas Firestore (archivos completos para pegar)
- PizzAR y PanAR (idénticas): `pizzar/firestore.rules` y `panar/firestore.rules`. Ya publicadas por Ruben.
- CompraZona v0.3: ver pendiente 1.
- Cada app tiene sus reglas en su repo (`firestore.rules`, `firestore.rules.txt` o `firestore-rules.txt`). Ruben solo pega el archivo completo.

## 7. Memoria
Los hechos durables están en la memoria del proyecto (`areas/etapa-comercial.md`, entradas hasta el 8/11/2026 16:45). Este archivo agrega lo que la memoria no guarda: entorno de pruebas, permisos, orden de pendientes y mapa de versiones.
