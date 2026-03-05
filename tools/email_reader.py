"""
ARGOS Email Reader + Sender
Lee emails via IMAP, envía via SMTP. Soporta múltiples cuentas.

Configuración en .env:
    # Cuenta principal (Gmail)
    EMAIL_IMAP_HOST=imap.gmail.com
    EMAIL_SMTP_HOST=smtp.gmail.com
    EMAIL_SMTP_PORT=587
    EMAIL_ADDRESS=tu@gmail.com
    EMAIL_PASSWORD=app_password_aqui
    EMAIL_FOLDERS=INBOX

    # Cuenta secundaria (SBD / otra)
    EMAIL2_IMAP_HOST=mail.softwarebydesign.com.ar
    EMAIL2_SMTP_HOST=mail.softwarebydesign.com.ar
    EMAIL2_SMTP_PORT=587
    EMAIL2_ADDRESS=hernan@softwarebydesign.com.ar
    EMAIL2_PASSWORD=password_aqui
    EMAIL2_FOLDERS=INBOX
    EMAIL2_LABEL=SBD

Para Gmail: usar App Password (no la contraseña normal).
    https://myaccount.google.com/apppasswords

Uso:
    from tools.email_reader import leer_inbox, buscar_emails, resumen_inbox
    from tools.email_reader import enviar_email, responder_email
"""

import os
import sys
import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.config import BASE_DIR


def _get_config(cuenta=None):
    """Lee configuración de email desde .env.

    Args:
        cuenta: None para principal, '2' para secundaria, o dict con config directa
    """
    if isinstance(cuenta, dict):
        return cuenta

    prefix = f'EMAIL{cuenta}_' if cuenta else 'EMAIL_'
    return {
        'imap_host': os.environ.get(f'{prefix}IMAP_HOST', 'imap.gmail.com'),
        'imap_port': int(os.environ.get(f'{prefix}IMAP_PORT', '993')),
        'smtp_host': os.environ.get(f'{prefix}SMTP_HOST', 'smtp.gmail.com'),
        'smtp_port': int(os.environ.get(f'{prefix}SMTP_PORT', '587')),
        'user': os.environ.get(f'{prefix}ADDRESS', ''),
        'password': os.environ.get(f'{prefix}PASSWORD', ''),
        'folders': os.environ.get(f'{prefix}FOLDERS', 'INBOX').split(','),
        'label': os.environ.get(f'{prefix}LABEL', 'Principal' if not cuenta else cuenta),
    }


def get_cuentas_configuradas():
    """Retorna lista de cuentas de email configuradas."""
    cuentas = []
    # Cuenta principal
    cfg1 = _get_config()
    if cfg1['user'] and cfg1['password']:
        cuentas.append({'id': None, 'label': cfg1['label'], 'address': cfg1['user']})
    # Cuenta secundaria
    cfg2 = _get_config('2')
    if cfg2['user'] and cfg2['password']:
        cuentas.append({'id': '2', 'label': cfg2['label'], 'address': cfg2['user']})


    return cuentas


def _conectar(cuenta=None):
    """Conecta al servidor IMAP con SSL."""
    cfg = _get_config(cuenta)
    if not cfg['user'] or not cfg['password']:
        label = cfg.get('label', 'principal')
        return None, f"Email ({label}) no configurado. Agregar credenciales en .env"

    try:
        mail = imaplib.IMAP4_SSL(cfg['imap_host'], cfg['imap_port'])
        mail.login(cfg['user'], cfg['password'])
        return mail, None
    except imaplib.IMAP4.error as e:
        return None, f"Error IMAP ({cfg.get('label', '')}): {e}"
    except Exception as e:
        return None, f"Error conexión ({cfg.get('label', '')}): {e}"


def _conectar_smtp(cuenta=None):
    """Conecta al servidor SMTP con STARTTLS."""
    cfg = _get_config(cuenta)
    if not cfg['user'] or not cfg['password']:
        label = cfg.get('label', 'principal')
        return None, cfg, f"Email ({label}) no configurado para envío."

    try:
        server = smtplib.SMTP(cfg['smtp_host'], cfg['smtp_port'], timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(cfg['user'], cfg['password'])
        return server, cfg, None
    except smtplib.SMTPAuthenticationError as e:
        return None, cfg, f"Error autenticación SMTP ({cfg.get('label', '')}): {e}"
    except Exception as e:
        return None, cfg, f"Error SMTP ({cfg.get('label', '')}): {e}"


def _decodificar_header(header_value):
    """Decodifica headers con encoding (=?UTF-8?Q?...?=)."""
    if not header_value:
        return ""
    decoded = decode_header(header_value)
    parts = []
    for content, charset in decoded:
        if isinstance(content, bytes):
            parts.append(content.decode(charset or 'utf-8', errors='replace'))
        else:
            parts.append(str(content))
    return ' '.join(parts)


def _parsear_email(msg):
    """Extrae campos relevantes de un email."""
    return {
        'de': _decodificar_header(msg.get('From', '')),
        'para': _decodificar_header(msg.get('To', '')),
        'asunto': _decodificar_header(msg.get('Subject', '')),
        'fecha': msg.get('Date', ''),
        'message_id': msg.get('Message-ID', ''),
        'tiene_adjuntos': _tiene_adjuntos(msg),
    }


def _tiene_adjuntos(msg):
    """Verifica si el email tiene archivos adjuntos."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
    return False


def _clasificar_email(email_data):
    """Clasifica un email por tipo/prioridad."""
    asunto = email_data['asunto'].lower()
    de = email_data['de'].lower()

    # Circulares de licitaciones
    if any(kw in asunto for kw in ['circular', 'adenda', 'aclaraci', 'modifica']):
        return 'circular_licitacion', 'alta'

    # COMPR.AR / Argentina Compra
    if any(kw in de or kw in asunto for kw in ['compr.ar', 'argentinacompra', 'compras públicas']):
        return 'comprar', 'alta'

    # BAC (Buenos Aires Compras)
    if any(kw in de or kw in asunto for kw in ['buenosairescompras', 'bac.']):
        return 'bac', 'alta'

    # Proveedores conocidos
    if any(kw in de for kw in ['furukawa', 'panduit', 'ubiquiti', 'grandstream']):
        return 'proveedor', 'media'

    # Facturas / pagos
    if any(kw in asunto for kw in ['factura', 'pago', 'recibo', 'cobro', 'transferencia']):
        return 'financiero', 'media'

    # Agenda / reuniones
    if any(kw in asunto for kw in ['reunión', 'reunion', 'invitación', 'invitacion', 'meet', 'zoom']):
        return 'agenda', 'media'

    return 'general', 'baja'


def leer_inbox(dias=1, max_emails=50, cuenta=None):
    """
    Lee emails de los últimos N días.

    Args:
        dias: cuántos días hacia atrás (default: 1 = hoy)
        max_emails: máximo de emails a leer
        cuenta: None para principal, '2' para secundaria, 'todas' para ambas

    Returns:
        dict con:
        - emails: lista de emails parseados y clasificados
        - total: cantidad total
        - por_tipo: dict con conteo por tipo
        - error: mensaje de error si hubo
    """
    # Si pide todas las cuentas, combinar resultados
    if cuenta == 'todas':
        combinado = {'emails': [], 'total': 0, 'por_tipo': {}, 'error': None, 'errores': []}
        for c_info in get_cuentas_configuradas():
            r = leer_inbox(dias=dias, max_emails=max_emails, cuenta=c_info['id'])
            if r.get('error'):
                combinado['errores'].append(f"{c_info['label']}: {r['error']}")
            combinado['emails'].extend(r.get('emails', []))
            combinado['total'] += r.get('total', 0)
            for tipo, cnt in r.get('por_tipo', {}).items():
                combinado['por_tipo'][tipo] = combinado['por_tipo'].get(tipo, 0) + cnt
        if combinado['errores'] and not combinado['emails']:
            combinado['error'] = '; '.join(combinado['errores'])
        # Re-sort by priority
        orden = {'alta': 0, 'media': 1, 'baja': 2}
        combinado['emails'].sort(key=lambda x: orden.get(x.get('prioridad', 'baja'), 3))
        return combinado

    mail, error = _conectar(cuenta)
    if error:
        return {'emails': [], 'total': 0, 'por_tipo': {}, 'error': error}

    desde = (date.today() - timedelta(days=dias)).strftime('%d-%b-%Y')
    emails_result = []
    por_tipo = {}

    cfg = _get_config(cuenta)
    label = cfg.get('label', '')
    for folder in cfg['folders']:
        try:
            mail.select(folder.strip())
            _, messages = mail.search(None, f'(SINCE {desde})')
            ids = messages[0].split()

            for msg_id in ids[-max_emails:]:
                _, data = mail.fetch(msg_id, '(RFC822)')
                raw = data[0][1]
                msg = email.message_from_bytes(raw)
                parsed = _parsear_email(msg)
                tipo, prioridad = _clasificar_email(parsed)
                parsed['tipo'] = tipo
                parsed['prioridad'] = prioridad
                parsed['folder'] = folder.strip()
                parsed['cuenta'] = label
                emails_result.append(parsed)
                por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        except Exception as e:
            emails_result.append({'error': f"Error leyendo {folder}: {e}"})

    mail.logout()

    # Ordenar por prioridad
    orden_prioridad = {'alta': 0, 'media': 1, 'baja': 2}
    emails_result.sort(key=lambda x: orden_prioridad.get(x.get('prioridad', 'baja'), 3))

    return {
        'emails': emails_result,
        'total': len(emails_result),
        'por_tipo': por_tipo,
        'error': None,
    }


def buscar_emails(termino, dias=7, max_emails=20, cuenta=None):
    """Busca emails que contengan el término en asunto o remitente.

    Args:
        termino: texto a buscar en asunto
        dias: días hacia atrás (default: 7)
        max_emails: máximo de resultados
        cuenta: None, '2', o 'todas'
    """
    if cuenta == 'todas':
        combinado = {'emails': [], 'total': 0, 'error': None}
        for c_info in get_cuentas_configuradas():
            r = buscar_emails(termino, dias, max_emails, cuenta=c_info['id'])
            combinado['emails'].extend(r.get('emails', []))
        combinado['total'] = len(combinado['emails'])
        return combinado

    mail, error = _conectar(cuenta)
    if error:
        return {'emails': [], 'error': error}

    desde = (date.today() - timedelta(days=dias)).strftime('%d-%b-%Y')
    emails_result = []

    cfg = _get_config(cuenta)
    for folder in cfg['folders']:
        try:
            mail.select(folder.strip())
            _, messages = mail.search(None, f'(SINCE {desde} SUBJECT "{termino}")')
            ids = messages[0].split()

            for msg_id in ids[-max_emails:]:
                _, data = mail.fetch(msg_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                parsed = _parsear_email(msg)
                tipo, prioridad = _clasificar_email(parsed)
                parsed['tipo'] = tipo
                parsed['prioridad'] = prioridad
                emails_result.append(parsed)
        except Exception:
            pass

    mail.logout()
    return {'emails': emails_result, 'total': len(emails_result), 'error': None}


def enviar_email(destinatario, asunto, cuerpo, cuenta=None, adjuntos=None, html=False, cc=None):
    """
    Envía un email via SMTP.

    Args:
        destinatario: email del destinatario (str o list)
        asunto: asunto del email
        cuerpo: cuerpo del email (texto plano o HTML)
        cuenta: None para principal, '2' para secundaria
        adjuntos: lista de paths de archivos a adjuntar (opcional)
        html: si True, envía como HTML
        cc: email(s) en copia (str o list)

    Returns:
        dict con: enviado (bool), error (str o None), desde (str)
    """
    server, cfg, error = _conectar_smtp(cuenta)
    if error:
        return {'enviado': False, 'error': error, 'desde': ''}

    try:
        # Crear mensaje
        if adjuntos:
            msg = MIMEMultipart()
            msg.attach(MIMEText(cuerpo, 'html' if html else 'plain', 'utf-8'))
        else:
            msg = MIMEMultipart()
            msg.attach(MIMEText(cuerpo, 'html' if html else 'plain', 'utf-8'))

        msg['From'] = cfg['user']
        if isinstance(destinatario, list):
            msg['To'] = ', '.join(destinatario)
            todos = destinatario
        else:
            msg['To'] = destinatario
            todos = [destinatario]

        if cc:
            if isinstance(cc, list):
                msg['Cc'] = ', '.join(cc)
                todos.extend(cc)
            else:
                msg['Cc'] = cc
                todos.append(cc)

        msg['Subject'] = asunto

        # Adjuntos
        if adjuntos:
            for filepath in adjuntos:
                if not os.path.exists(filepath):
                    continue
                filename = os.path.basename(filepath)
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)

        server.sendmail(cfg['user'], todos, msg.as_string())
        server.quit()
        return {'enviado': True, 'error': None, 'desde': cfg['user']}

    except Exception as e:
        try:
            server.quit()
        except Exception:
            pass
        return {'enviado': False, 'error': str(e), 'desde': cfg['user']}


def responder_email(message_id, cuerpo, cuenta=None):
    """
    Responde a un email (busca el original por message_id y responde).

    Args:
        message_id: Message-ID del email original
        cuerpo: texto de la respuesta
        cuenta: None para principal, '2' para secundaria

    Returns:
        dict con resultado del envío
    """
    # Buscar email original para obtener remitente y asunto
    mail, error = _conectar(cuenta)
    if error:
        return {'enviado': False, 'error': error}

    cfg = _get_config(cuenta)
    original = None

    for folder in cfg['folders']:
        try:
            mail.select(folder.strip())
            _, messages = mail.search(None, f'(HEADER Message-ID "{message_id}")')
            ids = messages[0].split()
            if ids:
                _, data = mail.fetch(ids[0], '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                original = _parsear_email(msg)
                break
        except Exception:
            continue

    mail.logout()

    if not original:
        return {'enviado': False, 'error': f'Email con Message-ID {message_id} no encontrado'}

    asunto = original['asunto']
    if not asunto.lower().startswith('re:'):
        asunto = f"Re: {asunto}"

    return enviar_email(
        destinatario=original['de'],
        asunto=asunto,
        cuerpo=cuerpo,
        cuenta=cuenta
    )


def leer_cuerpo_email(message_id=None, asunto_parcial=None, dias=7, cuenta=None):
    """
    Lee el cuerpo completo de un email específico.

    Args:
        message_id: Message-ID del email (exacto)
        asunto_parcial: texto parcial del asunto (búsqueda)
        dias: días hacia atrás para la búsqueda
        cuenta: None, '2', o 'todas'

    Returns:
        dict con: cuerpo (str), email_data (dict), error (str o None)
    """
    if cuenta == 'todas':
        for c_info in get_cuentas_configuradas():
            r = leer_cuerpo_email(message_id, asunto_parcial, dias, cuenta=c_info['id'])
            if r.get('cuerpo'):
                return r
        return {'cuerpo': None, 'error': 'Email no encontrado en ninguna cuenta'}

    mail, error = _conectar(cuenta)
    if error:
        return {'cuerpo': None, 'error': error}

    cfg = _get_config(cuenta)
    desde = (date.today() - timedelta(days=dias)).strftime('%d-%b-%Y')

    for folder in cfg['folders']:
        try:
            mail.select(folder.strip())
            if message_id:
                _, messages = mail.search(None, f'(HEADER Message-ID "{message_id}")')
            elif asunto_parcial:
                _, messages = mail.search(None, f'(SINCE {desde} SUBJECT "{asunto_parcial}")')
            else:
                mail.logout()
                return {'cuerpo': None, 'error': 'Especificar message_id o asunto_parcial'}

            ids = messages[0].split()
            if not ids:
                continue

            # Tomar el último match
            _, data = mail.fetch(ids[-1], '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            parsed = _parsear_email(msg)

            # Extraer cuerpo
            cuerpo = _extraer_cuerpo(msg)
            mail.logout()
            return {'cuerpo': cuerpo, 'email_data': parsed, 'error': None}

        except Exception as e:
            continue

    mail.logout()
    return {'cuerpo': None, 'error': 'Email no encontrado'}


def _extraer_cuerpo(msg):
    """Extrae el cuerpo de texto de un email (prefiere text/plain)."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get('Content-Disposition', ''))

            if 'attachment' in disposition:
                continue

            if content_type == 'text/plain':
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    return part.get_payload(decode=True).decode(charset, errors='replace')
                except Exception:
                    return part.get_payload(decode=True).decode('utf-8', errors='replace')
            elif content_type == 'text/html':
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    html_content = part.get_payload(decode=True).decode(charset, errors='replace')
                    # Limpieza básica de HTML
                    import re
                    text = re.sub(r'<br\s*/?>', '\n', html_content)
                    text = re.sub(r'<[^>]+>', '', text)
                    text = re.sub(r'\n{3,}', '\n\n', text)
                    return text.strip()
                except Exception:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or 'utf-8'
            return msg.get_payload(decode=True).decode(charset, errors='replace')
        except Exception:
            return str(msg.get_payload())

    return ''


def resumen_inbox():
    """
    Resumen rápido del inbox para apertura de sesión.
    Lee TODAS las cuentas configuradas.
    Retorna texto legible + alertas si hay emails importantes.
    """
    cuentas = get_cuentas_configuradas()
    if not cuentas:
        return {
            'texto': "Email no configurado. Agregar credenciales en .env",
            'alertas': [],
            'configurado': False,
        }

    resultado = leer_inbox(dias=1, max_emails=30, cuenta='todas')

    if resultado.get('error') and not resultado.get('emails'):
        return {
            'texto': f"Email: {resultado['error']}",
            'alertas': [],
            'configurado': True,
        }

    alertas = []
    for e in resultado.get('emails', []):
        if e.get('prioridad') == 'alta':
            alertas.append({
                'tipo': e.get('tipo', 'general'),
                'asunto': e.get('asunto', '')[:80],
                'de': e.get('de', ''),
                'cuenta': e.get('cuenta', ''),
            })

    # Texto resumen
    if resultado['total'] == 0:
        texto = "Sin emails nuevos hoy."
    else:
        partes = [f"{resultado['total']} emails hoy ({len(cuentas)} cuentas)"]
        for tipo, count in resultado.get('por_tipo', {}).items():
            partes.append(f"{count} {tipo}")
        texto = ' | '.join(partes)
        if alertas:
            texto += f" | {len(alertas)} REQUIEREN ATENCION"

    return {
        'texto': texto,
        'alertas': alertas,
        'total': resultado.get('total', 0),
        'configurado': True,
        'cuentas': [c['address'] for c in cuentas],
    }


def email_configurado():
    """Retorna True si al menos una cuenta de email está configurada."""
    return len(get_cuentas_configuradas()) > 0


def smtp_configurado(cuenta=None):
    """Retorna True si se puede enviar email por SMTP."""
    cfg = _get_config(cuenta)
    return bool(cfg['user'] and cfg['password'] and cfg['smtp_host'])


if __name__ == '__main__':
    import sys as _sys

    cuentas = get_cuentas_configuradas()
    if not cuentas:
        print("Email no configurado.")
        print("Agregar a .env:")
        print("  EMAIL_ADDRESS=tu@email.com")
        print("  EMAIL_PASSWORD=tu_app_password")
        print("  EMAIL_IMAP_HOST=imap.gmail.com")
        print("  EMAIL_SMTP_HOST=smtp.gmail.com")
        print("  EMAIL_SMTP_PORT=587")
        print("\nPara cuenta secundaria, usar prefijo EMAIL2_")
    else:
        print(f"Cuentas configuradas: {len(cuentas)}")
        for c in cuentas:
            print(f"  [{c['label']}] {c['address']}")

        if len(_sys.argv) > 1 and _sys.argv[1] == 'test_send':
            # Test: enviar email de prueba a sí mismo
            if len(_sys.argv) > 2:
                dest = _sys.argv[2]
            else:
                dest = cuentas[0]['address']
            r = enviar_email(dest, "Test ARGOS Email", "Este es un email de prueba de ARGOS.")
            print(f"Enviado: {r}")
        else:
            resultado = leer_inbox(dias=1, cuenta='todas')
            print(f"\nTotal: {resultado['total']} emails")
            for e in resultado.get('emails', [])[:10]:
                print(f"  [{e.get('prioridad','?')}] [{e.get('cuenta','')}] {e.get('tipo','')} | {e.get('asunto','')[:50]}")
            resumen = resumen_inbox()
            print(f"\nResumen: {resumen['texto']}")
