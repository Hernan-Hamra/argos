const { Client, LocalAuth } = require('whatsapp-web.js');
const { readFileSync, readdirSync } = require('fs');
const path = require('path');

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: path.resolve('./wwjs_auth') }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox'],
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    }
});

const sleep = ms => new Promise(r => setTimeout(r, ms));

let yaEjecutado = false;

client.on('qr', qr => console.log('QR recibido (no debería pasar, ya autenticado)'));
client.on('authenticated', () => console.log('Autenticado!'));

client.on('ready', async () => {
    if (yaEjecutado) return;
    yaEjecutado = true;
    console.log('WhatsApp listo, esperando sync...');
    await sleep(15000);

    try {
        // Obtener mi propio número (mensaje a mí misma)
        const me = client.info.wid._serialized;
        console.log(`Enviando a: ${me}\n`);

        // Leer archivos de mensajes
        const tempDir = path.resolve('./temp');
        const msgFiles = [
            'msg_no_encontrados.txt',
            'msg_tanda_4.txt',
            'msg_tanda_5.txt',
            'msg_tanda_6.txt',
            'msg_tanda_7.txt',
            'msg_tanda_8.txt',
        ];

        for (const file of msgFiles) {
            const filePath = path.join(tempDir, file);
            const texto = readFileSync(filePath, 'utf-8');
            await client.sendMessage(me, texto);
            console.log(`Enviado: ${file}`);
            await sleep(3000);
        }

        console.log('\nTodos los mensajes enviados!');
    } catch (err) {
        console.error('Error:', err);
    }

    await sleep(10000);
    process.exit(0);
});

client.initialize();
