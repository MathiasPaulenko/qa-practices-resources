# Guía de Espresso Testing — Companion

Archivos ejecutables de la guía [Guía de Espresso Testing para Android UI Testing](https://qapractices.com/es/documentation/espresso-testing-guide-android/).

## Archivos

- `src/build.gradle.kts` — bloque de dependencias androidTest (espresso-core, espresso-intents, espresso-contrib, junit-ext, runner, rules — todas 3.6.1/1.2.1/1.6.1).
- `src/LoginTest.kt` — test de login completo con `ActivityScenarioRule`.
- `src/LoginPage.kt` — Page Object de la pantalla de login.
- `src/NetworkIdlingResource.kt` — `IdlingResource` a medida para tu trabajo asíncrono.
- `src/RecyclerViewMatcher.kt` — el helper `withRecyclerView()` (espresso-contrib trae las actions, no este matcher).
- `src/espresso-ci.yml` — workflow de GitHub Actions que corre `connectedAndroidTest` en una matriz de API levels vía `reactivecircus/android-emulator-runner`.

## Uso

1. Copia las dependencias de `build.gradle.kts` a tu `app/build.gradle.kts`.
2. Suelta los `.kt` en `app/src/androidTest/java/<tu-paquete>/` y ajusta los `R.id` a tus layouts.
3. Copia `espresso-ci.yml` a `.github/workflows/` y ajusta la matriz de APIs.
4. Corre en local con `./gradlew connectedAndroidTest` sobre un emulador arrancado.
