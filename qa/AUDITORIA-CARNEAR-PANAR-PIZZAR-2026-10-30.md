# Auditoría de solo lectura — CarneAR / PanAR / PizzAR (30/10/2026)

No se tocó ningún dato ni regla publicada. Base: código de cada repo en GitHub (main) + `firestore.rules` de PanAR y PizzAR.

| # | App | Hallazgo | Riesgo | Acción propuesta |
|---|-----|----------|--------|------------------|
| 1 | CarneAR | No existe archivo de reglas en el repo. No se puede saber qué está publicado en Firebase (proyecto carnear-1d2c4). | Alto (desconocido) | Ruben copia las reglas actuales de la consola y se auditan; luego reglas completas nuevas |
| 2 | CarneAR | Cajero de sucursal entra con link `?s=CODIGO` + login anónimo y lee/escribe `negocios/{ownerUid}/...`. Para que funcione, las reglas probablemente permiten a cualquier usuario autenticado (incluso anónimo) tocar datos de otros negocios | Alto | Reglas: cajero solo si existe `carnearLinks/{cod}` con ese uid y membresía registrada |
| 3 | CarneAR | `clientes/{email}` (lista de clientes del admin, planes, features) leída/escrita desde el navegador; el admin se detecta por email en el cliente y por PIN `2580` escrito en el código | Alto: un cliente con sesión podría cambiarse el plan/features o leer otros clientes | Reglas: `clientes` lectura propia + admin verificado; features/plan solo escribe admin |
| 4 | CarneAR | `carnearLinks` leíble por código; código de 6 caracteres con `Math.random` | Medio | Aceptable con membresía registrada; subir a 8 caracteres en nuevas sucursales |
| 5 | CarneAR | `ventas` en la raíz (legado) | Bajo/Medio | Confirmar si hay datos antes de cerrarla |
| 6 | PanAR / PizzAR | Reglas en repo ya aíslan por negocio (`negocios/{uid}`), cajero anónimo con PIN, raíz cerrada | Bajo | Confirmar que ESTAS reglas son las publicadas en la consola |
| 7 | PanAR / PizzAR | PIN de cajero de 4 dígitos (1000–9999) sin límite de intentos; quien conozca el link `?n=` puede probar PINs | Medio | PIN de 6 dígitos o bloqueo por intentos (cambio de app + reglas) |
| 8 | PanAR / PizzAR | Cajero puede modificar productos/insumos/gastos (precios) | Bajo (decisión de producto) | Decidir si solo debe vender |
| 9 | PanAR / PizzAR | No hay registro de usuarios top-level: el panel no los lista | Funcional | Agregar `usuarios/{uid}` al registrarse (mismo patrón que Rodix) |
| 10 | Todas | Admin por email sin exigir `email_verified` en reglas (Rodix ya lo hace) | Medio | Incluir en reglas nuevas |

Orden recomendado: 1) obtener reglas publicadas de CarneAR y PanAR/PizzAR, 2) endurecer CarneAR (#2, #3), 3) PIN 6 dígitos en PanAR/PizzAR.
Regla permanente: ningún cambio puede borrar ni modificar datos de clientes.
