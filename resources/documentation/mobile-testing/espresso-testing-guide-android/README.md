# Espresso Testing Guide — Companion

Runnable files from the guide [Espresso Testing Guide for Android UI Testing](https://qapractices.com/documentation/espresso-testing-guide-android/).

## Files

- `src/build.gradle.kts` — androidTest dependencies block (espresso-core, espresso-intents, espresso-contrib, junit-ext, runner, rules — all 3.6.1/1.2.1/1.6.1).
- `src/LoginTest.kt` — a complete login test using `ActivityScenarioRule`.
- `src/LoginPage.kt` — Page Object for the login screen.
- `src/NetworkIdlingResource.kt` — custom `IdlingResource` for your own async work.
- `src/RecyclerViewMatcher.kt` — the `withRecyclerView()` helper (espresso-contrib ships the actions, not this matcher).
- `src/espresso-ci.yml` — GitHub Actions workflow running `connectedAndroidTest` on an API-level matrix via `reactivecircus/android-emulator-runner`.

## Usage

1. Copy `build.gradle.kts`'s dependencies into `app/build.gradle.kts`.
2. Drop the `.kt` files into `app/src/androidTest/java/<your-package>/` and fix the `R.id` references to match your layouts.
3. Copy `espresso-ci.yml` to `.github/workflows/` and adjust the API matrix.
4. Run locally with `./gradlew connectedAndroidTest` on a booted emulator.
