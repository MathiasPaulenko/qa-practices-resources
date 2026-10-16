# Alineación de Testing ISO 9001 — Checklist de Evidencia de Auditoría

Úsalo antes de una auditoría de certificación o vigilancia. Cada ítem debería poder producirse en menos de 15 minutos — si tienes que construirlo, no está listo para auditoría.

## Documentación

- [ ] Documento de estrategia de testing con alcance definido y declaración de fuera-de-alcance
- [ ] Plan de testing aprobado y fechado dentro del último ciclo de release
- [ ] Matriz RACI para actividades de testing, publicada y vigente
- [ ] Lista de documentos controlados cubriendo todos los artefactos de testing

## Trazabilidad

- [ ] Cada requisito mapea a al menos un caso de test
- [ ] Los casos de test enlazan de vuelta a los IDs de requisitos
- [ ] Los defectos enlazan a los casos de test que los encontraron
- [ ] La matriz de trazabilidad no muestra requisitos ni tests huérfanos

## Registros de Ejecución

- [ ] Los logs de corrida incluyen: resultado, entorno, versión del build, tester, fecha
- [ ] Las corridas fallidas muestran seguimiento (retest o defecto enlazado)
- [ ] La decisión de release tiene un reporte resumen de testing firmado

## Métricas y Revisión

- [ ] Tasa de defectos escapados trackeada por release
- [ ] Cobertura de testing trackeada contra requisitos
- [ ] Auditoría interna del proceso de QA completada dentro del ciclo
- [ ] Las actas de revisión por la dirección incluyen datos de desempeño de testing

## Mejora

- [ ] Las no-conformidades tienen acciones correctivas registradas
- [ ] Las acciones correctivas están verificadas como cerradas (no solo asignadas)
- [ ] Los ítems de mejora continua están trackeados hasta completarse

## Banderas rojas que los auditores detectan

- Matriz de trazabilidad actualizada la semana antes de la auditoría (las fechas la delatan)
- Defectos cerrados sin evidencia de retest
- Planes de testing que referencian herramientas o personas que ya no existen
- Métricas que existen pero que nadie jamás revisó
