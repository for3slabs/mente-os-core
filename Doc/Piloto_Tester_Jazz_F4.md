# 🧪 Piloto Tester — Jazz (Frente E F4)

> **Qué es:** el peldaño 3 de la escalera de confianza (Ronda_FrenteE). Que OTRA persona real
> (no Brian) use For3s y sobreviva a sus errores → la confianza se gana viéndolo funcionar en
> manos ajenas. **Regla de Brian (2026-07-16): F4 no es "encender jazz", es CAZAR los bugs que
> solo aparecen cuando un tercero real lo usa.** Este doc = qué se cazó + qué observar.

---

## 1 · Estado del piloto

- **Instancia:** `jazz` (@For3s_Jazzita_bot). Dueña: **Jazz @driade_1** (id 1177279840).
- **Encendida 2026-07-16** con la imagen v0.17.0 + Frente E F1/F2/F3 (expediente, /mision, red
  del sandbox segmentada). Migraciones 42-45 aplicadas. La puerta arranca CERRADA (fail-closed).
- **Falta (acción de Jazz):** darle `/start` a su bot (hasta entonces, "Chat not found" en el menú
  es normal). GitHub no conectado en jazz (como general) — las misiones usan solo el sandbox.

## 2 · 🐛 Bugs cazados en la caza-bugs de F4 (los que un tester habría sufrido)

- **BUG-E1 · /mision y /expediente NO estaban en el menú admin.** Existían pero eran INVISIBLES
  (un tester que abre `/` no los habría descubierto jamás). → añadidos a `_MENU_ADMIN`. Verificado
  en vivo en jazz: 29 comandos, mision+expediente presentes.
- **BUG-E2 · `@con_typing` mal colocado (bug propio de F2).** Mi parche F2 insertó `on_mision`
  ENTRE el `@con_typing` y `on_expediente` → el decorador quedó en `on_mision` (que YA tiene su
  typing interno = DOBLE "escribiendo…") y `on_expediente` se quedó SIN typing (la hoja tarda 1-2s
  sin feedback). → quitado de misión, devuelto a expediente. Verificado.

## 3 · ✅ Vectores investigados que resultaron SANOS (no dar por malo sin probar)

- **Turno mientras el modelo de embeddings carga (~160s en frío):** SANO. Hay warm-up en tarea
  aparte al arrancar + `buscar_semantico` degrada a "sin recuerdos" si el modelo no está, sin
  romper el turno (defensivo).
- **Puerta del equipo:** SANA. Arranca CERRADA por defecto (`DEFAULT false`) → nadie entra hasta
  que Jazz abra con `/invitar`. Fail-closed.
- **Red del sandbox en jazz:** SANA. La segmentación F3 aplicó también aquí (sandbox → postgres =
  `gaierror`). `execute_code` sigue vivo (devolvió 42).

## 4 · ⚠️ Hallazgo de UX (no bug, mejora anotada)

- **`/salud` en una instancia RECIÉN encendida muestra 🔴** ("no hay turnos en memoria", "no hay
  backups"). Es el estado natural de una instancia virgen (nadie ha conversado, el backup nocturno
  no ha corrido), pero **un tester lo leería como "está roto"**. Mejora futura: que `/salud`
  distinga "vacío por nuevo" de "fallo real". Anotado en PENDIENTES, no bloquea el piloto.
- **🐌 `/mision` tarda ~4 min** (hallazgo F2, misión real de Brian = 257s). Para el piloto, avisar
  a Jazz que una misión tarda; idealmente atacar la lentitud antes de que ella pruebe /mision.

## 5 · Qué observar durante el piloto (protocolo)

Cuando Jazz use su bot, mirar y anotar en el expediente / RETOMAR:
1. **¿Descubrió los comandos sola?** (el menú `/` ahora los muestra — validar que sí los ve).
2. **¿Algún mensaje la confundió o asustó?** (ej. el 🔴 de /salud vacío, un error crudo).
3. **¿El bot respondió sin romperse a lo que ella escribió?** (cosas que Brian no probaría).
4. **¿`/mision` le funcionó y entendió el flujo?** (o la lentitud la frustró).
5. **Feedback directo:** ¿le dio confianza? ¿qué le faltó? (esto alimenta F6 = el sentimiento).

## 6 · Criterio de "el piloto salió bien"

Jazz usó su For3s varios días **sin que Brian tuviera que intervenir**, no se rompió con su uso
real, y su feedback quedó registrado. Los bugs que salgan se cazan y arreglan (como BUG-E1/E2).

---

Relacionado: `Cuerpo/Ronda_FrenteE_Confianza_Para_Delegar.md` §F4 · [[project_frente_e_confianza_delegar]]
· [[project_multi_instancia]] · `Doc/Auditoria_Seguridad_For3s_OS.md` (F3).
