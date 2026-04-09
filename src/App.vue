<template>
  <div class="main-container">
    <div class="calculator-card">
      <header class="header">
        <h1>Calculadora Unidad 3</h1>
        <h2>Juan Victor Solis Hernandez</h2>
      </header>

      <div class="form-container">
        <div class="input-group full-width">
          <label class="label-title">Selecciona el Método</label>
          <select v-model="metodo" class="custom-select">
            <option value="euler">Euler Mejorado</option>
            <option value="runge_kutta">Runge-Kutta</option>
            <option value="newton">Newton-Raphson</option>
          </select>
        </div>

        <div class="input-group full-width">
          <label class="label-title">Ecuación Matemática</label>
          <span class="input-hint">{{ metodo === 'newton' ? 'Ingresa f(x)' : 'Ingresa f(x, y)' }}</span>
          <input
            v-model="form.funcion"
            :placeholder="metodo === 'newton' ? 'ej: x**2 - 4' : 'ej: x + y'"
            class="custom-input"
          >
        </div>

        <div class="input-group">
          <label class="label-title">{{ metodo === 'newton' ? 'Aproximación inicial' : 'Punto inicial' }}</label>
          <span class="input-hint">Valor de x₀</span>
          <input v-model.number="form.x0" type="number" step="any" class="custom-input">
        </div>

        <template v-if="metodo !== 'newton'">
          <div class="input-group">
            <label class="label-title">Valor inicial y₀</label>
            <span class="input-hint">Condición inicial</span>
            <input v-model.number="form.y0" type="number" step="any" class="custom-input">
          </div>

          <div class="input-group">
            <label class="label-title">Tamaño del paso</label>
            <span class="input-hint">Valor de h</span>
            <input v-model.number="form.h" type="number" step="0.001" class="custom-input">
          </div>

          <div class="input-group">
            <label class="label-title">Iteraciones</label>
            <span class="input-hint">Número n</span>
            <input v-model.number="form.n" type="number" class="custom-input">
          </div>
        </template>

        <template v-else>
          <div class="input-group">
            <label class="label-title">Tolerancia</label>
            <span class="input-hint">Margen de error</span>
            <input v-model.number="form.tol" type="number" step="0.0000001" class="custom-input">
          </div>
        </template>

        <button @click="enviarDatos" :disabled="loading" class="btn-calculate">
          <span v-if="!loading">Calcular Ahora</span>
          <span v-else class="loader"></span>
        </button>
      </div>

      <div v-if="resultados" class="results-section">
        <hr class="divider">

        <div v-if="metodo === 'newton' && resultados.root !== undefined" class="root-badge">
          <span class="badge-label">Raíz encontrada:</span>
          <span class="badge-value">{{ resultados.root.toFixed(8) }}</span>
        </div>

        <h3>Tabla de Resultados</h3>
        <div class="table-wrapper">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Iteración</th>
                <th>{{ metodo === 'newton' ? 'X (Aproximación)' : 'X' }}</th>
                <th>{{ metodo === 'newton' ? 'f(X) / Valor Y' : 'Y (Resultado)' }}</th>

                <th v-if="metodo === 'newton'">Error Absoluto</th>

                <template v-if="metodo === 'euler'">
                  <th style="color: #2980b9;">Yr (Predictor)</th>
                  <th style="color: #c0392b;">Margen de Error</th>
                </template>

                <template v-if="metodo === 'runge_kutta'">
                  <th style="color: #8e44ad;">K1</th>
                  <th style="color: #8e44ad;">K2</th>
                  <th style="color: #8e44ad;">K3</th>
                  <th style="color: #8e44ad;">K4</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <template v-if="metodo === 'newton'">
                <tr v-for="item in resultados.historial_completo" :key="item.iter">
                  <td>{{ item.iter }}</td>
                  <td>{{ item.x.toFixed(6) }}</td>
                  <td>{{ item.y.toFixed(6) }}</td>
                  <td class="error-col">
                    {{ item.error === 0 ? '-' : item.error.toFixed(8) }}
                  </td>
                </tr>
              </template>

              <template v-else>
                <tr v-for="(val, i) in resultados.x_values" :key="i">
                  <td>{{ i }}</td>
                  <td>{{ Number(val).toFixed(6) }}</td>
                  <td>{{ Number(resultados.y_values[i]).toFixed(6) }}</td>

                  <template v-if="metodo === 'euler'">
                    <td style="color: #2980b9;">
                      {{ (resultados.detalles?.[i] && i !== 0) ? resultados.detalles[i].y_pred.toFixed(6) : '—' }}
                    </td>
                    <td style="color: #c0392b; font-family: monospace;">

                      {{ (resultados.detalles?.[i] && i !== 0) ? resultados.detalles[i].error.toFixed(4) : '0.0000' }}
                    </td>
                  </template>

                  <template v-if="metodo === 'runge_kutta'">
                    <template v-if="resultados.ks && resultados.ks[i]">
                      <td style="color: #8e44ad; font-family: monospace;">{{ resultados.ks[i].k1.toFixed(5) }}</td>
                      <td style="color: #8e44ad; font-family: monospace;">{{ resultados.ks[i].k2.toFixed(5) }}</td>
                      <td style="color: #8e44ad; font-family: monospace;">{{ resultados.ks[i].k3.toFixed(5) }}</td>
                      <td style="color: #8e44ad; font-family: monospace;">{{ resultados.ks[i].k4.toFixed(5) }}</td>
                    </template>
                    <template v-else>
                      <td>-</td><td>-</td><td>-</td><td>-</td>
                    </template>
                  </template>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <div class="chart-container">
          <canvas ref="graficaCanvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* (Estilos se mantienen iguales para conservar tu diseño) */
.main-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  padding: 40px 20px;
}
.calculator-card {
  background: white;
  width: 100%;
  max-width: 950px;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.header { text-align: center; margin-bottom: 30px; }
.header h1 { color: #2c3e50; margin: 0; font-size: 26px; }
.subtitle { color: #7f8c8d; font-size: 14px; margin-top: 5px; }
.form-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.full-width { grid-column: span 2; }
.input-group { display: flex; flex-direction: column; }
.label-title { font-weight: 600; color: #34495e; font-size: 14px; margin-bottom: 4px; }
.input-hint { font-size: 11px; color: #95a5a6; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
.custom-input, .custom-select { padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; transition: all 0.3s ease; }
.custom-input:focus, .custom-select:focus { outline: none; border-color: #42b983; box-shadow: 0 0 8px rgba(66, 185, 131, 0.2); }
.btn-calculate { grid-column: span 2; padding: 14px; background-color: #42b983; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.3s; margin-top: 10px; font-size: 16px; }
.btn-calculate:hover { background-color: #3aa876; }
.divider { margin: 40px 0; border: 0; border-top: 1px solid #eee; }
.root-badge { background: #e8f5e9; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #c8e6c9; margin-bottom: 25px; }
.badge-label { color: #2e7d32; margin-right: 10px; }
.badge-value { font-weight: bold; color: #1b5e20; font-size: 20px; }
.table-wrapper { max-height: 400px; overflow-y: auto; border-radius: 12px; border: 1px solid #eee; margin-bottom: 30px; }
.custom-table { width: 100%; border-collapse: collapse; }
.custom-table th { background: #f8f9fa; padding: 15px; font-size: 13px; color: #2c3e50; position: sticky; top: 0; border-bottom: 2px solid #eee; z-index: 10; }
.custom-table td { padding: 12px; border-top: 1px solid #eee; font-size: 14px; color: #34495e; text-align: center; }
.error-col { font-family: monospace; color: #e67e22; font-weight: 600; }
.chart-container { margin-top: 20px; background: #fafafa; padding: 20px; border-radius: 12px; }
</style>

<script setup>
import { ref, watch, nextTick } from 'vue'
import axios from 'axios'
import { Chart } from 'chart.js/auto'

const metodo = ref('euler')
const loading = ref(false)
const resultados = ref(null)
const graficaCanvas = ref(null)
let chartInstance = null

const form = ref({
  funcion: '',
  x0: 0,
  y0: 0,
  h: 0.1,
  n: 10,
  tol: 0.0000001
})

const enviarDatos = async () => {
  if (!form.value.funcion) {
    alert("Por favor escribe una función")
    return
  }
  loading.value = true
  resultados.value = null

  try {
    const res = await axios.post('http://localhost:5000/api/calcular', {
      metodo: metodo.value,
      params: form.value
    })
    resultados.value = res.data
  } catch (err) {
    alert("Error: " + (err.response?.data?.error || "Error en el servidor"))
  } finally {
    loading.value = false
  }
}

watch(resultados, async (newVal) => {
  if (!newVal) return
  await nextTick()
  if (!graficaCanvas.value) return

  if (chartInstance) chartInstance.destroy()

  let labels, dataPoints, labelName;

  if (metodo.value === 'newton') {
    const historial = newVal.historial_completo;
    labels = historial.map(h => `Iter ${h.iter}`);
    dataPoints = historial.map(h => h.x);
    labelName = 'Convergencia de la Raíz (Xn)';
  } else {
    labels = newVal.x_values.map(v => Number(v).toFixed(2));
    dataPoints = newVal.y_values;
    labelName = 'Solución de la EDO';
  }

  chartInstance = new Chart(graficaCanvas.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: labelName,
        data: dataPoints,
        borderColor: metodo.value === 'newton' ? '#3498db' : '#42b983',
        backgroundColor: metodo.value === 'newton' ? 'rgba(52, 152, 219, 0.1)' : 'rgba(66, 185, 131, 0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 5,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: { title: { display: true, text: metodo.value === 'newton' ? 'Valor Aproximado Xn' : 'Valor Y' } },
        x: { title: { display: true, text: metodo.value === 'newton' ? 'Nro de Iteración' : 'Valor X' } }
      }
    }
  })
})
</script>