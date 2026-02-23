<template>

<div class="p-5">

<h1>Calculadora de Métodos Numéricos</h1>



<div class="form-group">

<label>Selecciona Método:</label>

<select v-model="metodo" class="form-control">

<option value="euler">Euler Mejorado</option>

<option value="runge_kutta">Runge-Kutta</option>

<option value="newton">Newton-Raphson</option>

</select>

</div>



<div class="inputs">

<input v-model="form.funcion" placeholder="Función (ej: x + y o x**2 - 2)">

<input v-model.number="form.x0" type="number" placeholder="x0">



<template v-if="metodo !== 'newton'">

<input v-model.number="form.y0" type="number" placeholder="y0">

<input v-model.number="form.h" type="number" step="0.1" placeholder="Paso h">

<input v-model.number="form.n" type="number" placeholder="Iteraciones n">

</template>

</div>



<button @click="enviarDatos" :disabled="loading">Calcular</button>



<div v-if="resultados" class="mt-4">

<h3>Tabla de Valores</h3>

<table border="1">

<thead>

<tr><th>i</th><th>X</th><th>Y</th></tr>

</thead>

<tbody>

<tr v-for="(x, i) in resultados.x_values" :key="i">

<td>{{ i }}</td>

<td>{{ x.toFixed(4) }}</td>

<td>{{ resultados.y_values[i].toFixed(4) }}</td>

</tr>

</tbody>

</table>

</div>

</div>

</template>



<script setup>

import { ref } from 'vue';

import axios from 'axios';



const metodo = ref('euler');

const loading = ref(false);

const resultados = ref(null);

const form = ref({

funcion: '',

x0: 0,

y0: 0,

h: 0.1,

n: 10

});



const enviarDatos = async () => {

loading.value = true;

try {

const res = await axios.post('http://localhost:5000/api/calcular', {

metodo: metodo.value,

params: form.value

});

resultados.value = res.data;

} catch (err) {

alert("Error: " + (err.response?.data?.error || "Fallo en el servidor"));

} finally {

loading.value = false;

}

};

</script>
