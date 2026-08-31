# Companion de la Guía de Testing HIL

Framework de pytest ejecutable para testing HIL: abstracción HilRig, test de inyección de fallas, fixtures de conftest y workflow de CI para la [Guía de Testing HIL](https://qapractices.com/es/documentation/hardware-in-the-loop-testing/).

## Contenidos

| Archivo | Qué hace |
| --- | --- |
| `hil_rig.py` | Clase HilRig que wrappea el simulador en tiempo real (dSPACE, NI, OPAL-RT) |
| `dut_interface.py` | Clase DutInterface que se comunica con el DUT por CAN |
| `conftest.py` | Fixtures de pytest para setup/teardown del rig |
| `test_hil_motor.py` | Test de ejemplo: protección de sobrecorriente con inyección de fallas |
| `.github/workflows/hil-tests.yml` | Workflow de GitHub Actions para regresión HIL programada |

## Quick Start

```bash
# 1. Instalar dependencias
pip install pytest python-can

# 2. Configurar la URL del rig y el bus CAN
export HIL_SIMULATOR_URL="dspace://hil-rig-01"
export HIL_CAN_BUS="vcan0"
export HIL_DUT_NODE_ID="0x12"

# 3. Correr la suite de tests HIL
pytest test_hil_motor.py -v

# 4. Correr con grabación de trazas
pytest test_hil_motor.py -v --hil-traces=./traces
```

## CI

El archivo `.github/workflows/hil-tests.yml` corre la smoke suite de HIL en un schedule (nocturno) y on-demand. Los tests HIL necesitan un rig físico, así que no pueden correr en cada commit — el workflow usa triggers `workflow_dispatch` y `schedule`.

## Licencia

MIT — ver el repositorio principal para detalles.
