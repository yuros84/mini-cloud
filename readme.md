# 🌩️ Mini Cloud IoT FIWARE-Ready con Docker, Flask, Postgres y Grafana

Este proyecto implementa un **mini-cloud IoT** para simular sensores que envían datos en formato **FIWARE NGSI-v2**, almacenarlos en una **base de datos PostgreSQL** y visualizarlos en **Grafana**.

---

## 🧩 Arquitectura

Servicios orquestados con **Docker Compose**:

| Servicio     | Descripción |
|---------------|-------------|
| **API (Flask)** | Recibe datos en formato FIWARE NGSI-v2 y los guarda en la base de datos |
| **DB (Postgres)** | Base de datos relacional que almacena las lecturas de los sensores |
| **Simulator** | Simula sensores enviando lecturas periódicas a la API |
| **Grafana** | Visualiza los datos de temperatura almacenados en Postgres |

---

## ⚙️ Requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚀 Instrucciones de uso

### 1. Clona el repositorio
```bash
git clone https://github.com/tu-usuario/mini-cloud.git
cd mini-cloud
```

### 2. Levantar el stack

```bash
docker-compose up --build
```
Esto construye las imágenes y levanta los contenedores:

- API: Flask app
- DB: PostgreSQL
- Simulator: envía lecturas cada 5 segundos
- Grafana: interfaz web de visualización

Para correrlos en segundo plano:

```bash
docker-compose up -d --build
```

## 🌐 Acceso a los servicios
- API: http://localhost:5000
- Grafana: http://localhost:3000 (user: admin / pass: admin)
- Postgres: interno db:5432 (user: postgres / pass: postgres)

## 🔗 API Endpoints

**POST /data**

Recibe datos de sensores en formato FIWARE NGSI-v2.

```json
{
  "id": "Sensor001",
  "type": "TemperatureSensor",
  "temperature": {
    "value": 25.6,
    "type": "Float"
  },
  "location": {
    "value": "living-room",
    "type": "Text"
  }
}
```

**GET /data**

Obtiene las últimas lecturas almacenadas

```json
[
  {
    "id": "Sensor001",
    "type": "TemperatureSensor",
    "temperature": {"value": 25.6, "type": "Float"},
    "location": {"value": "living-room", "type": "Text"},
    "created_at": "2025-10-01T10:25:00"
  }
]
```
