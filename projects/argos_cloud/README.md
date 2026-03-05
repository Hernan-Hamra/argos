# ARGOS Cloud - Proyecto paralelo

Proyecto para testear la arquitectura cloud de ARGOS en paralelo al desarrollo local.

## Objetivo
Montar proxy AiControl + API Anthropic + auth basico en un VPS.
Los aprendizajes se migran al proyecto principal.

## Stack
- VPS: Hetzner/DigitalOcean (~$20/mes)
- Proxy: FastAPI (Python)
- Auth: JWT
- API: Anthropic SDK
- DB central: PostgreSQL (solo auth + metricas, NO datos de usuarios)

## Estructura
```
argos_cloud/
├── proxy/          ← proxy API Anthropic + control de tokens
├── auth/           ← registro, login, JWT, planes
├── marketplace/    ← CRUD protocolos compartidos
├── metrics/        ← metricas anonimas de uso
└── deploy/         ← docker-compose, configs, scripts
```

## Checklist seguridad pre-deploy
- [ ] HTTPS obligatorio (Let's Encrypt)
- [ ] Rate limiting por usuario
- [ ] API key nunca expuesta al frontend
- [ ] Logs sin datos personales
- [ ] Compliance Ley 25.326 (T&C, consentimiento)
- [ ] GDPR ready (derecho al olvido, portabilidad)
- [ ] Tokens en vault (no en .env del server)
- [ ] Backup automatico DB auth
- [ ] Monitoreo (uptime, errores, consumo tokens)
