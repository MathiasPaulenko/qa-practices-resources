# Pruebas de Entregabilidad de Correo — Companion

Archivos ejecutables para la guía [Cómo Probar la Entregabilidad de Correos Electrónicos](https://qapractices.com/es/documentation/email-deliverability-testing).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `scripts/dns-auth-check.sh` | Verifica los registros SPF, DKIM y DMARC de un dominio de envío con `dig` |
| `scripts/seed-send.sh` | Envía un mensaje de prueba rastreado a una lista de semillas por tu relay SMTP real con `swaks` |
| `tests/seed_inbox_check.py` | Consulta un buzón semilla por IMAP y reporta si el mensaje llegó a INBOX o a spam |

## Inicio Rápido

```bash
# 1. Verificar los tres registros de autenticación DNS
bash scripts/dns-auth-check.sh staging.qapractices.com s1

# 2. Enviar una prueba rastreada por el pipeline real
export SMTP_HOST=smtp.staging.qapractices.com SMTP_USER=app-smtp SMTP_PASS='***'
bash scripts/seed-send.sh seeds.txt noreply@staging.qapractices.com

# 3. Comprobar dónde aterrizó el mensaje en un buzón semilla
python tests/seed_inbox_check.py \
  --host imap.gmail.com --user qa-seed+001@gmail.com \
  --password 'app-password' --token <token-del-paso-2>
```

## Integración en CI

`dns-auth-check.sh` es seguro para CI — solo lee DNS público. `seed-send.sh` y `seed_inbox_check.py` necesitan credenciales reales, así que ejecútalos en un job programado con secrets, no en cada push.

Requisitos: `dig` (bind-utils/dnsutils), `swaks` v20240103+, solo stdlib de Python 3.10+.
