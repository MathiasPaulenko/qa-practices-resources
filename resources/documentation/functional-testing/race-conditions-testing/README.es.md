# Testing de Condiciones de Carrera — Harness de Estrés Java Ejecutable

Código companion de [Cómo Probar Condiciones de Carrera: Guía de Concurrencia](https://qapractices.com/es/documentation/race-conditions-testing/) en QAPractices.

Java 17+ puro, cero dependencias — solo necesitas `javac` y `java`.

## Qué hay dentro

| Archivo | Qué muestra |
|---------|-------------|
| `java/UnsafeInventory.java` | Carrera de verificación-acción: el check `stock > 0` y el `stock--` no son atómicos, así que dos compradores pueden ganar la última unidad. |
| `java/SafeInventory.java` | El mismo contrato hecho atómico con `AtomicInteger.compareAndSet` — la carrera desaparece. |
| `java/RaceDemo.java` | Harness de estrés: demo de actualización perdida con contador (8 hilos, barrera de salida) más un demo de sobreventa que itera hasta que dos compradores toman la misma unidad. |

## Ejecutarlo

```bash
cd java
javac *.java
java RaceDemo
```

Salida típica (los números varían según la máquina y el planificador):

```text
Counter: expected 400000, got 234360 -> 165640 lost updates
Oversell: 37 rounds out of 20000 sold the same unit twice
```

Después cambia `UnsafeInventory` por `SafeInventory` dentro de `RaceDemo.oversellDemo` y vuelve a ejecutar: el contador de sobreventas cae a cero mientras el demo del contador sigue mostrando actualizaciones perdidas — ese contraste es el punto del ejercicio.

## Recurso relacionado

- [Cómo Probar Condiciones de Carrera: Guía de Concurrencia](https://qapractices.com/es/documentation/race-conditions-testing/) — estrategias, herramientas (jcstress, ThreadSanitizer, rr, TLA+) y el ejemplo jcstress ejecutable que este harness complementa.
