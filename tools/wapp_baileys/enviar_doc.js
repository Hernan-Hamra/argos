import { makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import P from 'pino';
import { readFileSync } from 'fs';

// ---------- CONFIG ----------
const NUMERO = process.argv[2];       // ej: 5491133746540
const MENSAJE = process.argv[3];      // texto del mensaje
const PDF_PATH = process.argv[4];     // path al PDF (opcional)
const PDF_NAME = process.argv[5] || 'documento.pdf';  // nombre del archivo

if (!NUMERO || !MENSAJE) {
    console.log('Uso: node enviar_doc.js <numero> <mensaje> [pdf_path] [pdf_name]');
    process.exit(1);
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
    const logger = P({ level: 'silent' });
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');

    const sock = makeWASocket({
        auth: state,
        logger,
        printQRInTerminal: false,
    });

    sock.ev.on('creds.update', saveCreds);

    const connected = await new Promise((resolve) => {
        sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update;
            if (qr) {
                console.log('\n=== ESCANEA ESTE QR CON TU CELULAR ===');
                qrcode.generate(qr, { small: true });
            }
            if (connection === 'open') {
                console.log('WhatsApp CONECTADO');
                resolve(true);
            }
            if (connection === 'close') {
                const code = lastDisconnect?.error?.output?.statusCode;
                if (code === DisconnectReason.loggedOut || code === 401) {
                    console.log('Sesion expirada. Borrar auth_info/ y reiniciar.');
                }
                resolve(false);
            }
        });
    });

    if (!connected) process.exit(1);

    const jid = NUMERO + '@s.whatsapp.net';

    // Verificar que el numero existe en WhatsApp
    const [exists] = await sock.onWhatsApp(NUMERO);
    if (!exists?.exists) {
        console.log(`ERROR: ${NUMERO} no esta en WhatsApp`);
        await sock.end();
        process.exit(1);
    }
    console.log(`Numero verificado: ${NUMERO}`);

    // Enviar mensaje de texto
    await sock.sendMessage(jid, { text: MENSAJE });
    console.log('Mensaje enviado');

    // Enviar PDF si se proporcionó
    if (PDF_PATH) {
        await sleep(1500);
        const pdfBuffer = readFileSync(PDF_PATH);
        await sock.sendMessage(jid, {
            document: pdfBuffer,
            mimetype: 'application/pdf',
            fileName: PDF_NAME,
        });
        console.log(`PDF enviado: ${PDF_NAME}`);
    }

    await sleep(2000);
    await sock.end();
    console.log('DONE');
    process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
