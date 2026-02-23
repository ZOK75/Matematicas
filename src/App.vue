<template>
  <div style="font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto;">
    <h1>Calculadora de Métodos Numéricos</h1>
    <hr>

    <div style="margin-bottom: 20px;">
      <label><b>Selecciona el Método: </b></label>
      <select v-model="metodo" style="padding: 5px; margin-left: 10px;">
        <option value="euler">Euler Mejorado</option>
        <option value="runge_kutta">Runge-Kutta</option>
        <option value="newton">Newton-Raphson</option>
      </select>
    </div>

    <div style="display: flex; flex-direction: column; gap: 10px; max-width: 300px;">
      <input v-model="form.funcion" placeholder="Función (ej: x + y)">
      <input v-model.number="form.x0" type="number" placeholder="Valor inicial x0">

      <div v-if="metodo !== 'newton'" style="display: flex; flex-direction: column; gap: 10px;">
        <input v-model.number="form.y0" type="number" placeholder="Valor inicial y0">
        <input v-model.number="form.h" type="number" step="0.1" placeholder="Paso h">
        <input v-model.number="form.n" type="number" placeholder="Iteraciones n">
      </div>

      <button
        @click="enviarDatos"
        :disabled="loading"
        style="padding: 10px; background-color: #42b983; color: white; border: none; cursor: pointer;"
      >
        {{ loading ? 'Calculando...' : 'Calcular Ahora' }}
      </button>
    </div>

    <div v-if="resultados" style="margin-top: 30px;">
      <h3>Resultados</h3>

      <table border="1" style="width: 100%; border-collapse: collapse; text-align: center;">
        <thead>
          <tr style="background-color: #f2f2f2;">
            <th>Iteración</th>
            <th>X</th>
            <th>Y (Resultado)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in resultados.x_values" :key="i">
            <td>{{ i }}</td>
            <td>{{ Number(x).toFixed(4) }}</td>
            <td>{{ Number(resultados.y_values[i]).toFixed(4) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- GRÁFICA -->
      <canvas
        ref="graficaCanvas"
        style="margin-top: 30px;"
      ></canvas>
    </div>
  </div>
</template>

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
  n: 10
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
    console.error(err)
    alert("Error: " + (err.response?.data?.error || "No se pudo conectar con el servidor Python"))
  } finally {
    loading.value = false
  }
}

watch(resultados, async (nuevoResultado) => {
  if (!nuevoResultado) return

  await nextTick()

  if (!graficaCanvas.value) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(graficaCanvas.value, {
    type: 'line',
    data: {
      labels: nuevoResultado.x_values,
      datasets: [
        {
          label: 'Resultado Numérico',
          data: nuevoResultado.y_values,
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'X'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Y'
          }
        }
      }
    }
  })
})
</script>