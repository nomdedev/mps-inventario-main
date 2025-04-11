const fs = require('fs');
const readline = require('readline');

const configPath = './config/databaseConfig.json';

// Interfaz para capturar datos del usuario
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askQuestion(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function configureServer() {
  try {
    const server = await askQuestion('Ingrese el nombre del servidor: ');
    const database = await askQuestion('Ingrese el nombre de la base de datos: ');
    const user = await askQuestion('Ingrese el usuario: ');
    const password = await askQuestion('Ingrese la contraseña: ');
    const port = await askQuestion('Ingrese el puerto (default 1433): ');

    const config = {
      server,
      database,
      user,
      password,
      port: port ? parseInt(port) : 1433
    };

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log('Configuración guardada exitosamente.');
  } catch (err) {
    console.error('Error al guardar la configuración:', err);
  } finally {
    rl.close();
  }
}

configureServer();
