import { makeWASocket, useMultiFileAuthState, DisconnectReason, makeInMemoryStore } from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import P from 'pino';
import { readFileSync, existsSync } from 'fs';
import path from 'path';

// ---------- CONFIG ----------
const IMAGENES_DIR = 'C:\\Users\\HERNAN\\OneDrive\\PRUEBA ARGOS NATALIA\\PURIM_5786\\imagenes';
const MEGUILAT_PDF = 'C:\\Users\\HERNAN\\OneDrive\\PRUEBA ARGOS NATALIA\\PURIM_5786\\MEGUILAT ESTER PARA NIÑOS .pdf';
const IMAGEN_PRUEBA = path.join(IMAGENES_DIR, 'ABAD ISAAC salutacion purim 5786.jpg');

const PRUEBAS = [
    { contacto: 'Natalia Indibo', nombre: 'Natalia' },
    { contacto: 'Hernán Hamra',   nombre: 'Hernán' },
    { contacto: 'Ariel Indibo',   nombre: 'Ariel' },
    { contacto: 'Jonathan Indibo', nombre: 'Jonathan' },
];

function textoIntro(nombre) {
    return `Hola ${nombre}\nTe envío una nota de parte del Gran Rabino Isaac Sacca con motivo de la festividad de Purim.\nEnviamos también una Meguilat Esther para niños, una oportunidad ideal para compartir en familia.`;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ---------- MAIN ----------
async function main() {
    const logger = P({ level: 'silent' });
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    const store = makeInMemoryStore({ logger });

    const sock = makeWASocket({
        auth: state,
        logger,
        printQRInTerminal: false,
    });

    store.bind(sock.ev);
    sock.ev.on('creds.update', saveCreds);

    // Esperar conexion
    const connected = await new Promise((resolve) => {
        sock.ev.on('connection.update', (update) => {
            const { connection, lastDisconnect, qr } = update;

            if (qr) {
                console.log('\n=== ESCANEA ESTE QR CON TU CELULAR ===');
                console.log('WhatsApp > Dispositivos vinculados > Vincular\n');
                qrcode.generate(qr, { small: true });
            }

            if (connection === 'open') {
                console.log('\nWhatsApp CONECTADO!\n');
                resolve(true);
            }

            if (connection === 'close') {
                const code = lastDisconnect?.error?.output?.statusCode;
                console.log(`Desconectado (code: ${code})`);
                if (code === DisconnectReason.loggedOut || code === 401) {
                    console.log('Borrar auth_info/ y reiniciar.');
                    resolve(false);
                }
                // Otros codigos: reintentar
            }
        });
    });

    if (!connected) { process.exit(1); }

    console.log('Sincronizando contactos (15 seg)...');
    await sleep(15000);

    const contactos = store.contacts || {};
    const total = Object.keys(contactos).length;
    console.log(`Contactos: ${total}\n`);

    // Buscar contactos de prueba
    const envios = [];
    for (const prueba of PRUEBAS) {
        const jid = buscar(contactos, prueba.contacto);
        if (jid) {
            console.log(`  OK  ${prueba.contacto} => ${jid}`);
            envios.push({ ...prueba, jid });
        } else {
            console.log(`  ??  ${prueba.contacto}`);
            const p = parcial(contactos, prueba.contacto.split(' ')[0]);
            p.slice(0, 3).forEach(x => console.log(`      ~ ${x.name} => ${x.jid}`));
        }
    }

    if (envios.length === 0) {
        console.log('\nSin contactos. Primeros 30:');
        let i = 0;
        for (const [jid, c] of Object.entries(contactos)) {
            if (!jid.endsWith('@s.whatsapp.net')) continue;
            console.log(`  ${c.name || c.notify || '?'} => ${jid}`);
            if (++i >= 30) break;
        }
        process.exit(1);
    }

    console.log(`\n${envios.length} contactos listos. Enter para enviar, Ctrl+C para cancelar.`);
    await new Promise(r => process.stdin.once('data', r));

    for (const e of envios) {
        console.log(`\nEnviando a: ${e.contacto}`);
        try {
            await sock.sendMessage(e.jid, { text: textoIntro(e.nombre) });
            console.log('  [1/3] Texto OK');
            await sleep(1000);

            if (existsSync(IMAGEN_PRUEBA)) {
                await sock.sendMessage(e.jid, {
                    document: readFileSync(IMAGEN_PRUEBA),
                    mimetype: 'image/jpeg',
                    fileName: path.basename(IMAGEN_PRUEBA),
                });
                console.log('  [2/3] Carta OK');
            }
            await sleep(1000);

            if (existsSync(MEGUILAT_PDF)) {
                await sock.sendMessage(e.jid, {
                    document: readFileSync(MEGUILAT_PDF),
                    mimetype: 'application/pdf',
                    fileName: path.basename(MEGUILAT_PDF),
                });
                console.log('  [3/3] PDF OK');
            }
            console.log('  COMPLETADO');
        } catch (err) {
            console.log(`  ERROR: ${err.message}`);
        }
        await sleep(3000);
    }

    console.log('\n=== PRUEBA COMPLETADA ===');
    await sleep(3000);
    process.exit(0);
}

function buscar(contactos, nombre) {
    const t = nombre.toLowerCase().trim();
    for (const [jid, c] of Object.entries(contactos)) {
        if (!jid.endsWith('@s.whatsapp.net')) continue;
        const n = (c.name || c.notify || c.verifiedName || '').toLowerCase().trim();
        if (n === t) return jid;
    }
    for (const [jid, c] of Object.entries(contactos)) {
        if (!jid.endsWith('@s.whatsapp.net')) continue;
        const n = (c.name || c.notify || c.verifiedName || '').toLowerCase().trim();
        if (n.includes(t) || t.includes(n)) return jid;
    }
    return null;
}

function parcial(contactos, term) {
    const t = term.toLowerCase();
    return Object.entries(contactos)
        .filter(([jid, c]) => jid.endsWith('@s.whatsapp.net') && (c.name || c.notify || '').toLowerCase().includes(t))
        .map(([jid, c]) => ({ jid, name: c.name || c.notify || '?' }));
}

main().catch(console.error);
