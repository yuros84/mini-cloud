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
