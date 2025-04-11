const fs = require('fs');
const sql = require('mssql');

// Lee la configuración desde el archivo JSON
const configPath = './config/databaseConfig.json';
const dbConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Configuración de la conexión
const sqlConfig = {
  user: dbConfig.user,
  password: dbConfig.password,
  server: dbConfig.server,
  database: dbConfig.database,
  port: dbConfig.port,
  options: {
    encrypt: true, // Usa true si estás usando Azure
    trustServerCertificate: true // Cambia según sea necesario
  }
};

// Función para conectarse a la base de datos
async function connectToDatabase() {
  try {
    const pool = await sql.connect(sqlConfig);
    console.log('Conexión exitosa a la base de datos');
    return pool;
  } catch (err) {
    console.error('Error al conectar a la base de datos:', err);
    throw err;
  }
}

module.exports = { connectToDatabase };
