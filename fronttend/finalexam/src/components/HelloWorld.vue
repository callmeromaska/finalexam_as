<template>
  <div id="app">
    <h1>Student Performance Analysis</h1>
    <div class="container">
      <label class="student-label" for="student-id">Enter Student ID:</label>
      <div class="knopochki">
        <input v-model="studentId" type="number" id="student-id" />
        <button @click="fetchPerformance">Get Performance</button>
        <button @click="fetchReport">Get All Reports</button>
      </div>

      <div v-if="performance">
        <h3>Performance Details</h3>
        <p><strong>Student ID:</strong> {{ performance.student_id }}</p>
        <p><strong>Performance Score:</strong> {{ performance.performance_score }}</p>
      </div>
    </div>
    <div class="stats">
      <div v-if="reports.length > 0">
        <h3>All Students Report</h3>
        <table border="1">
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Test Scores</th>
              <th>Questions Attempted</th>
              <th>Time Spent</th>
              <th>Performance Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in reports" :key="report.student_id">
              <td>{{ report.student_id }}</td>
              <td>{{ report.test_scores }}</td>
              <td>{{ report.questions_attempted }}</td>
              <td>{{ report.time_spent }}</td>
              <td>{{ report.performance_score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <ImgBase></ImgBase>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      studentId: null,
      performance: null,
      reports: [],
    };
  },
  methods: {
    fetchPerformance() {
      if (!this.studentId) return alert("Please enter a Student ID.");
      axios
        .get(`http://127.0.0.1:5000/api/performance?student_id=${this.studentId}`)
        .then((response) => {
          this.performance = response.data;
        })
        .catch((error) => {
          alert(error.response.data.error || "An error occurred.");
        });
    },
    fetchReport() {
      axios.get("http://127.0.0.1:5000/api/report").then((response) => {
        this.reports = response.data;
      });
    },
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 20px;
}
table {
  margin: 20px auto;
  width: 80%;
}

body{
  display: flex;
  flex-direction: column;
  justify-items: center !important;
  align-content: center;
  width: 100%;
  height: -webkit-fill-available !important;
  
}

.container{
  width: fit-content;
  align-self: center;
}
.student-label{
  display: flex;
  flex-direction: inherit;
  justify-content: center;
  margin-bottom: 10px;
  max-width: 500px;
  /* min-width: 200px; */
}
.knopochki{
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 500px;
  /* min-width: 200px; */
}
</style>
