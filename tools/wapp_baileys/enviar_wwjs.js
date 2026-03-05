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
import { readFileSync, existsSync, readdirSync, writeFileSync, copyFileSync, mkdirSync, renameSync } from 'fs';
import { execSync } from 'child_process';
import path from 'path';
import qrcode from 'qrcode-terminal';

// ---------- CONFIG ----------
const PURIM_DIR = 'C:\\Users\\HERNAN\\OneDrive\\PRUEBA ARGOS NATALIA\\PURIM_5786';
const IMAGENES_DIR = path.join(PURIM_DIR, 'imagenes');
const NO_ENVIADAS_DIR = path.join(IMAGENES_DIR, 'no_enviadas');
const ENVIADAS_DIR = path.join(IMAGENES_DIR, 'enviadas');
const CARTAS_NO_ENV = path.join(PURIM_DIR, 'cartas', 'no_enviadas');
const CARTAS_ENV = path.join(PURIM_DIR, 'cartas', 'enviadas');
const EXCEL_PATH = path.join(PURIM_DIR, 'listado purim 5786 full.xlsx');
const TEMP_DIR = path.resolve('./temp');

// Anti-ban V2: delays aleatorios + tandas + variaciones texto
// Config "envío masivo 1 día" — ~6-7hs para 126 contactos
const DELAY_MSG_MIN = 5000;          // 5-10 seg entre texto/carta/pdf del mismo contacto
const DELAY_MSG_MAX = 10000;
const DELAY_POST_PDF_MIN = 15000;    // 15-30 seg después del PDF (upload pesado)
const DELAY_POST_PDF_MAX = 30000;
const DELAY_CONTACTO_MIN = 25000;    // 25-50 seg entre contactos
const DELAY_CONTACTO_MAX = 50000;
const DELAY_TANDA_MIN = 600000;      // 10-20 min entre tandas
const DELAY_TANDA_MAX = 1200000;
const TANDA_SIZE = 8;                // 8 contactos por tanda
const LIMITE_DIARIO = 6;

// WHITELIST: solo enviar a estos contactos (aprobados por Hernán)
// Si está vacío, envía todos los PENDIENTE/REENVIAR del Excel
const WHITELIST = [
    'Alan Muller', 'Ilan Olkies', 'Gustavo Rubinsztein',
    'Ruben Ezra Saiegh', 'Aki Slelatt', 'Adrián Wais',
].map(n => normalizar(n));

// ---------- HELPERS ----------

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

/** Delay aleatorio entre min y max ms */
function randomDelay(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

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

// Cartas JPG disponibles (solo de no_enviadas)
const IMAGENES_FS = (() => {
    try { return readdirSync(NO_ENVIADAS_DIR).filter(f => f.toLowerCase().endsWith('.jpg')); }
    catch (e) { return []; }
})();

/** Busca la carta JPG personalizada en no_enviadas */
function findCarta(nombre, apellido) {
    const target = normalizar(`${apellido} ${nombre} salutacion purim 5786`);
    const archivo = IMAGENES_FS.find(f => normalizar(f.replace('.jpg', '')) === target);
    if (archivo) return path.join(NO_ENVIADAS_DIR, archivo);
    return null;
}

/** Mueve carta de no_enviadas a enviadas (jpg + docx) */
function moverAEnviadas(nombre, apellido) {
    const target = normalizar(`${apellido} ${nombre} salutacion purim 5786`);
    // JPG
    try {
        const jpgFiles = readdirSync(NO_ENVIADAS_DIR).filter(f => normalizar(f.replace('.jpg', '')) === target && f.endsWith('.jpg'));
        for (const f of jpgFiles) {
            renameSync(path.join(NO_ENVIADAS_DIR, f), path.join(ENVIADAS_DIR, f));
        }
    } catch (e) { /* ignore */ }
    // DOCX
    try {
        const docxTarget = normalizar(`${apellido} ${nombre} salutacion purim 5786`);
        const docxFiles = readdirSync(CARTAS_NO_ENV).filter(f => normalizar(f.replace('.docx', '')) === docxTarget && f.endsWith('.docx'));
        for (const f of docxFiles) {
            renameSync(path.join(CARTAS_NO_ENV, f), path.join(CARTAS_ENV, f));
        }
    } catch (e) { /* ignore */ }
}

/** Copia imagen a temp con nombre ASCII (evita problemas encoding en paths) */
function prepararImagen(srcPath, nombre, apellido) {
    if (!existsSync(TEMP_DIR)) mkdirSync(TEMP_DIR, { recursive: true });
    const safeName = `carta_${normalizar(apellido)}_${normalizar(nombre)}.jpg`.replace(/\s+/g, '_');
    const tempPath = path.join(TEMP_DIR, safeName);
    copyFileSync(srcPath, tempPath);
    return tempPath;
}

/** Texto intro con variaciones sutiles para evitar detección de contenido repetitivo */
function textoIntro(nombre) {
    const saludos = [
        `Hola ${nombre}`,
        `Hola ${nombre}!`,
        `${nombre}, hola`,
        `Hola ${nombre}, buen día`,
    ];
    const cuerpos = [
        `Te envío una nota de parte del Gran Rabino Isaac Sacca con motivo de la festividad de Purim.`,
        `Te comparto una nota del Gran Rabino Isaac Sacca por la festividad de Purim.`,
        `Te acerco una salutación del Gran Rabino Isaac Sacca con motivo de Purim.`,
        `Te hago llegar una nota del Gran Rabino Isaac Sacca en esta festividad de Purim.`,
    ];
    const cierres = [
        `Enviamos también una Meguilat Esther para niños, una oportunidad ideal para compartir en familia.`,
        `Adjuntamos también una Meguilat Esther para niños, ideal para compartir en familia.`,
        `Te enviamos además una Meguilat Esther para niños, para disfrutar en familia.`,
        `Incluimos una Meguilat Esther para niños, una linda oportunidad para compartir en familia.`,
    ];
    const s = saludos[Math.floor(Math.random() * saludos.length)];
    const c = cuerpos[Math.floor(Math.random() * cuerpos.length)];
    const ci = cierres[Math.floor(Math.random() * cierres.length)];
    return `${s}\n${c}\n${ci}`;
}

// ---------- BÚSQUEDA DE CONTACTOS ----------

/**
 * Busca un contacto por nombre completo.
 * Prioridad: 1) exacto, 2) todas partes en contacto, 3) inverso,
 *            4) solo primer nombre + apellido (ignora segundo nombre)
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

    // 4) Solo primer nombre + último apellido (ignora segundos nombres)
    if (partes.length >= 3) {
        const primerNombre = partes[0];
        const ultimoApellido = partes[partes.length - 1];
        for (const c of candidatos) {
            const n = normalizar(c.name || c.pushname || '');
            if (n.includes(primerNombre) && n.includes(ultimoApellido)) return c;
        }
    }

    return null;
}

// ---------- MODO DE OPERACIÓN ----------
const MODO = process.argv[2] || 'test';

const PRUEBAS = [
    // Test con Hernán Hamra (propio) para verificar que funciona
    { contacto: 'Hernan Hamra', nombre: 'Hernan', apellido: 'Hamra' },
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

    let yaEjecutado = false;  // evitar re-ejecución si reconecta
    client.on('ready', async () => {
        if (yaEjecutado) { console.log('Reconexión detectada, ignorando.'); return; }
        yaEjecutado = true;
        console.log('\nWhatsApp Web LISTO! Esperando sincronización...');
        await sleep(20000);  // 20 seg para que la sesión se estabilice
        console.log('Sincronización OK\n');

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

        // Aplicar límite diario
        const totalAEnviar = Math.min(envios.length, LIMITE_DIARIO);
        const enviosHoy = envios.slice(0, totalAEnviar);
        if (envios.length > LIMITE_DIARIO) {
            console.log(`\n*** LÍMITE DIARIO: enviando ${totalAEnviar} de ${envios.length} (quedan ${envios.length - totalAEnviar} para mañana) ***`);
        }

        const tandas = Math.ceil(totalAEnviar / TANDA_SIZE);
        console.log(`\nEnviando ${totalAEnviar} contactos en ${tandas} tandas de ${TANDA_SIZE}...`);
        console.log(`Delays aleatorios: ${DELAY_CONTACTO_MIN/1000}-${DELAY_CONTACTO_MAX/1000}s entre contactos, ${DELAY_TANDA_MIN/60000}-${DELAY_TANDA_MAX/60000}min entre tandas\n`);

        // --- Envío por tandas con delays aleatorios ---
        let enviados = 0;
        let errores = 0;

        for (let i = 0; i < enviosHoy.length; i++) {
            const e = enviosHoy[i];
            const nro = i + 1;

            // Pausa entre tandas (aleatoria)
            if (i > 0 && i % TANDA_SIZE === 0) {
                const tanda = Math.floor(i / TANDA_SIZE);
                const pausa = randomDelay(DELAY_TANDA_MIN, DELAY_TANDA_MAX);
                console.log(`\n--- Pausa entre tandas (tanda ${tanda} completa, ${i}/${totalAEnviar}) ---`);
                console.log(`  Esperando ${Math.round(pausa / 60000)} min...\n`);
                await sleep(pausa);
            }

            console.log(`[${nro}/${totalAEnviar}] ${e.contacto} (${e.id})`);
            try {
                // 1. Texto intro (con variaciones)
                const texto = textoIntro(e.saludo || e.nombre);
                await client.sendMessage(e.id, texto);
                console.log('  [1/3] Texto OK');
                await sleep(randomDelay(DELAY_MSG_MIN, DELAY_MSG_MAX));

                // 2. Carta JPG personalizada (inline)
                if (e.cartaPath) {
                    const tempImg = prepararImagen(e.cartaPath, e.nombre, e.apellido);
                    const media = MessageMedia.fromFilePath(tempImg);
                    await client.sendMessage(e.id, media);
                    console.log('  [2/3] Carta OK');
                } else {
                    console.log('  [2/3] Carta SKIP (no existe)');
                }
                await sleep(randomDelay(DELAY_MSG_MIN, DELAY_MSG_MAX));

                // 3. PDF Meguilat (como documento adjunto)
                if (MEGUILAT_PDF) {
                    const pdfData = readFileSync(MEGUILAT_PDF);
                    const pdfMedia = new MessageMedia('application/pdf', pdfData.toString('base64'), 'MEGUILAT ESTER PARA NINOS.pdf');
                    await client.sendMessage(e.id, pdfMedia, { sendMediaAsDocument: true });
                    console.log('  [3/3] Meguilat OK - esperando upload...');
                    await sleep(randomDelay(DELAY_POST_PDF_MIN, DELAY_POST_PDF_MAX));
                } else {
                    console.log('  [3/3] Meguilat SKIP');
                }

                // Mover a enviadas automáticamente
                moverAEnviadas(e.nombre, e.apellido);
                enviados++;
                console.log('  COMPLETADO + movido a enviadas');
            } catch (err) {
                errores++;
                console.log(`  ERROR: ${err.message}`);
            }

            // Delay aleatorio entre contactos
            const delayContacto = randomDelay(DELAY_CONTACTO_MIN, DELAY_CONTACTO_MAX);
            console.log(`  Próximo en ${Math.round(delayContacto/1000)}s...`);
            await sleep(delayContacto);
        }

        console.log(`\n=== ENVÍO FINALIZADO ===`);
        console.log(`Enviados: ${enviados} | Errores: ${errores} | No encontrados: ${noEncontrados.length}`);
        if (envios.length > LIMITE_DIARIO) {
            console.log(`Pendientes para próxima ejecución: ${envios.length - totalAEnviar}`);
        }
        console.log('Esperando 30 seg para que terminen de subir los mensajes...');
        await sleep(30000);
        process.exit(0);
    });

    client.on('auth_failure', (msg) => {
        console.log('Error de autenticacion:', msg);
        process.exit(1);
    });

    await client.initialize();
}

// ---------- LEER EXCEL (solo PENDIENTE y REENVIAR de hoja CONTACTOS) ----------
function leerExcel() {
    const tmpJson = path.resolve('./temp/contactos.json');
    if (!existsSync(path.resolve('./temp'))) mkdirSync(path.resolve('./temp'), { recursive: true });
    const pyScript = `
import openpyxl, json, sys
wb = openpyxl.load_workbook(r'${EXCEL_PATH.replace(/\\/g, '\\\\')}', data_only=True)
ws = wb['CONTACTOS']
rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is None: break
    estado = str(row[6] or '').strip()
    if estado in ('PENDIENTE', 'REENVIAR'):
        nombre = str(row[1] or '').strip()
        apellido = str(row[2] or '').strip()
        saludo = str(row[7] or '').strip() if len(row) > 7 else ''
        if nombre and apellido:
            rows.append({'nombre': nombre, 'apellido': apellido, 'contacto': nombre + ' ' + apellido, 'saludo': saludo or nombre.split()[0]})
with open(r'${tmpJson.replace(/\\/g, '\\\\')}', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False)
print(f'{len(rows)} contactos pendientes exportados')
`;
    const pyFile = path.resolve('./temp/leer_excel.py');
    writeFileSync(pyFile, pyScript, 'utf-8');
    execSync(`python "${pyFile}"`, { encoding: 'utf-8' });
    const data = readFileSync(tmpJson, 'utf-8');
    let rows = JSON.parse(data);
    // Filtrar por whitelist si está definida
    if (WHITELIST.length > 0) {
        rows = rows.filter(r => WHITELIST.includes(normalizar(r.contacto)));
        console.log(`  Filtrado por whitelist: ${rows.length} de ${WHITELIST.length}`);
    }
    return rows;
}

main().catch(console.error);
