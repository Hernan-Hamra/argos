/**
 * WhatsApp sender via whatsapp-web.js
 * Envío masivo: texto + carta JPG (inline) + Meguilat PDF
 *
 * Uso:
 *   node enviar_wwjs.js test     → 4 contactos de prueba
 *   node enviar_wwjs.js full     → 300 contactos del Excel
 *   node enviar_wwjs.js dry      → solo busca contactos, no envía
 *
 * Primera vez: escanear QR con el celular
 */

import pkg from 'whatsapp-web.js';
const { Client, LocalAuth, MessageMedia } = pkg;
import { readFileSync, existsSync, readdirSync, writeFileSync, copyFileSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import path from 'path';
import qrcode from 'qrcode-terminal';

// ---------- CONFIG ----------
const PURIM_DIR = 'C:\\Users\\HERNAN\\OneDrive\\PRUEBA ARGOS NATALIA\\PURIM_5786';
const IMAGENES_DIR = path.join(PURIM_DIR, 'imagenes');
const EXCEL_PATH = path.join(PURIM_DIR, 'listado purim 5786 full.xlsx');
const TEMP_DIR = path.resolve('./temp');

// Anti-ban: tiempos entre envíos
const DELAY_ENTRE_MENSAJES = 2000;   // 2 seg entre texto/carta/pdf del mismo contacto
const DELAY_ENTRE_CONTACTOS = 5000;  // 5 seg entre contactos
const DELAY_ENTRE_TANDAS = 60000;    // 1 min entre tandas
const TANDA_SIZE = 30;               // contactos por tanda

// ---------- HELPERS ----------

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

/** Normaliza texto: lowercase, trim, quita acentos */
function normalizar(texto) {
    return (texto || '').toLowerCase().trim()
        .normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
}

// Buscar el PDF de Meguilat (evita problemas encoding NFD/NFC con Ñ)
function findMeguilat() {
    try {
        const files = readdirSync(PURIM_DIR);
        const meguilat = files.find(f => f.toUpperCase().includes('MEGUILAT') && f.endsWith('.pdf'));
        if (meguilat) return path.join(PURIM_DIR, meguilat);
    } catch (e) { /* ignore */ }
    return null;
}

const MEGUILAT_PDF = findMeguilat();

// Cartas JPG disponibles (leídas del filesystem)
const IMAGENES_FS = (() => {
    try { return readdirSync(IMAGENES_DIR).filter(f => f.endsWith('.jpg')); }
    catch (e) { return []; }
})();

/** Busca la carta JPG personalizada: "APELLIDO NOMBRE salutacion purim 5786.jpg" */
function findCarta(nombre, apellido) {
    const target = normalizar(`${apellido} ${nombre} salutacion purim 5786`);
    const archivo = IMAGENES_FS.find(f => normalizar(f.replace('.jpg', '')) === target);
    if (archivo) return path.join(IMAGENES_DIR, archivo);
    return null;
}

/** Copia imagen a temp con nombre ASCII (evita problemas encoding en paths) */
function prepararImagen(srcPath, nombre, apellido) {
    if (!existsSync(TEMP_DIR)) mkdirSync(TEMP_DIR, { recursive: true });
    const safeName = `carta_${normalizar(apellido)}_${normalizar(nombre)}.jpg`.replace(/\s+/g, '_');
    const tempPath = path.join(TEMP_DIR, safeName);
    copyFileSync(srcPath, tempPath);
    return tempPath;
}

function textoIntro(nombre) {
    return `Hola ${nombre}\nTe envío una nota de parte del Gran Rabino Isaac Sacca con motivo de la festividad de Purim.\nEnviamos también una Meguilat Esther para niños, una oportunidad ideal para compartir en familia.`;
}

// ---------- BÚSQUEDA DE CONTACTOS ----------

/**
 * Busca un contacto por nombre completo.
 * Prioridad: 1) match exacto, 2) nombre+apellido ambos presentes, 3) inverso
 * Nunca devuelve un JID ya usado.
 */
function buscarContacto(contacts, nombreCompleto, usados) {
    const partes = normalizar(nombreCompleto).split(/\s+/);
    const textoFull = normalizar(nombreCompleto);

    const candidatos = contacts.filter(c =>
        !c.isGroup &&
        c.id._serialized.endsWith('@c.us') &&
        !usados.has(c.id._serialized)
    );

    // 1) Match exacto
    for (const c of candidatos) {
        const n = normalizar(c.name || c.pushname || '');
        if (n === textoFull) return c;
    }

    // 2) Todas las partes del nombre buscado en el contacto
    if (partes.length >= 2) {
        for (const c of candidatos) {
            const n = normalizar(c.name || c.pushname || '');
            if (partes.every(p => n.includes(p))) return c;
        }
    }

    // 3) Todas las partes del contacto en el nombre buscado
    if (partes.length >= 2) {
        for (const c of candidatos) {
            const n = normalizar(c.name || c.pushname || '');
            if (!n || n.length < 3) continue;
            const pc = n.split(/\s+/);
            if (pc.length >= 2 && pc.every(p => textoFull.includes(p))) return c;
        }
    }

    return null;
}

// ---------- MODO DE OPERACIÓN ----------
const MODO = process.argv[2] || 'test';

const PRUEBAS = [
    { contacto: 'Natalia Indibo',  nombre: 'Natalia',  apellido: 'Indibo' },
    { contacto: 'Hernán Hamra',    nombre: 'Hernán',   apellido: 'Hamra' },
    { contacto: 'Ariel Indibo',    nombre: 'Ariel',    apellido: 'Indibo' },
    { contacto: 'Joni Indibo',     nombre: 'Jonathan',  apellido: 'Indibo' },
];

// ---------- MAIN ----------
async function main() {
    console.log(`\n=== WHATSAPP PURIM 5786 - Modo: ${MODO.toUpperCase()} ===\n`);
    console.log(`Meguilat PDF: ${MEGUILAT_PDF ? 'OK' : 'NO ENCONTRADO'}`);
    console.log(`Cartas JPG: ${IMAGENES_FS.length}`);

    const client = new Client({
        authStrategy: new LocalAuth({ dataPath: './wwjs_auth' }),
        puppeteer: {
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: false,
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
        },
    });

    client.on('qr', (qr) => {
        console.log('\n=== ESCANEA ESTE QR CON TU CELULAR ===\n');
        qrcode.generate(qr, { small: true });
    });

    client.on('authenticated', () => console.log('Autenticado!'));

    client.on('ready', async () => {
        console.log('\nWhatsApp Web LISTO!\n');

        const contacts = await client.getContacts();
        console.log(`Contactos WhatsApp: ${contacts.length}\n`);

        // --- Armar lista de destinatarios ---
        let lista;
        if (MODO === 'full' || MODO === 'dry') {
            lista = leerExcel();
            console.log(`Contactos del Excel: ${lista.length}\n`);
        } else {
            lista = PRUEBAS;
        }

        // --- Buscar cada contacto en WhatsApp ---
        const envios = [];
        const noEncontrados = [];
        const usados = new Set();

        for (const item of lista) {
            const contact = buscarContacto(contacts, item.contacto, usados);
            if (contact) {
                const jid = contact.id._serialized;
                usados.add(jid);
                const cartaPath = findCarta(item.nombre, item.apellido);
                envios.push({ ...item, id: jid, cartaPath, waName: contact.name || contact.pushname });
                console.log(`  OK  ${item.contacto} => ${contact.name || contact.pushname} (${jid})${cartaPath ? '' : ' [SIN CARTA]'}`);
            } else {
                noEncontrados.push(item.contacto);
                console.log(`  ??  ${item.contacto}`);
            }
        }

        console.log(`\n--- Resumen ---`);
        console.log(`Encontrados: ${envios.length}`);
        console.log(`No encontrados: ${noEncontrados.length}`);
        if (noEncontrados.length > 0) {
            writeFileSync('no_encontrados.txt', noEncontrados.join('\n'), 'utf-8');
            console.log(`  (guardados en no_encontrados.txt)`);
        }

        // --- Modo dry: solo buscar, no enviar ---
        if (MODO === 'dry') {
            console.log('\nModo DRY: no se envía nada.');
            process.exit(0);
        }

        if (envios.length === 0) {
            console.log('\nSin contactos para enviar.');
            process.exit(1);
        }

        console.log(`\nEnviando a ${envios.length} contactos en tandas de ${TANDA_SIZE}...`);
        console.log(`Tiempo estimado: ~${Math.ceil(envios.length / TANDA_SIZE * 1.5)} minutos\n`);

        // --- Envío por tandas ---
        let enviados = 0;
        let errores = 0;

        for (let i = 0; i < envios.length; i++) {
            const e = envios[i];
            const nro = i + 1;

            // Pausa entre tandas
            if (i > 0 && i % TANDA_SIZE === 0) {
                const tanda = Math.floor(i / TANDA_SIZE);
                console.log(`\n--- Pausa entre tandas (tanda ${tanda} completa, ${i}/${envios.length}) ---`);
                console.log(`  Esperando ${DELAY_ENTRE_TANDAS / 1000} seg...\n`);
                await sleep(DELAY_ENTRE_TANDAS);
            }

            console.log(`[${nro}/${envios.length}] ${e.contacto} (${e.id})`);
            try {
                // 1. Texto intro
                await client.sendMessage(e.id, textoIntro(e.nombre));
                console.log('  [1/3] Texto OK');
                await sleep(DELAY_ENTRE_MENSAJES);

                // 2. Carta JPG personalizada (inline, se ve en el chat)
                if (e.cartaPath) {
                    const tempImg = prepararImagen(e.cartaPath, e.nombre, e.apellido);
                    const media = MessageMedia.fromFilePath(tempImg);
                    await client.sendMessage(e.id, media);  // sin sendMediaAsDocument => inline
                    console.log(`  [2/3] Carta OK`);
                } else {
                    console.log(`  [2/3] Carta SKIP (no existe)`);
                }
                await sleep(DELAY_ENTRE_MENSAJES);

                // 3. PDF Meguilat (como documento adjunto)
                if (MEGUILAT_PDF) {
                    const pdfData = readFileSync(MEGUILAT_PDF);
                    const pdfMedia = new MessageMedia('application/pdf', pdfData.toString('base64'), 'MEGUILAT ESTER PARA NINOS.pdf');
                    await client.sendMessage(e.id, pdfMedia, { sendMediaAsDocument: true });
                    console.log('  [3/3] Meguilat OK');
                } else {
                    console.log('  [3/3] Meguilat SKIP');
                }

                enviados++;
                console.log('  COMPLETADO');
            } catch (err) {
                errores++;
                console.log(`  ERROR: ${err.message}`);
            }
            await sleep(DELAY_ENTRE_CONTACTOS);
        }

        console.log(`\n=== ENVÍO FINALIZADO ===`);
        console.log(`Enviados: ${enviados} | Errores: ${errores} | No encontrados: ${noEncontrados.length}`);
        await sleep(3000);
        process.exit(0);
    });

    client.on('auth_failure', (msg) => {
        console.log('Error de autenticacion:', msg);
        process.exit(1);
    });

    await client.initialize();
}

// ---------- LEER EXCEL ----------
function leerExcel() {
    const json = execSync(`python -c "
import openpyxl, json, sys
sys.stdout.reconfigure(encoding='utf-8')
wb = openpyxl.load_workbook(r'${EXCEL_PATH.replace(/\\/g, '\\\\')}', data_only=True)
ws = wb.active
rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is None: break
    nombre = str(row[1] or '').strip()
    apellido = str(row[2] or '').strip()
    if nombre and apellido:
        rows.append({'nombre': nombre, 'apellido': apellido, 'contacto': nombre + ' ' + apellido})
print(json.dumps(rows, ensure_ascii=False))
"`, { encoding: 'utf-8' });
    return JSON.parse(json);
}

main().catch(console.error);
