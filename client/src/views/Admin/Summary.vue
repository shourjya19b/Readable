<script setup>
import store from "@/store";
</script>
<template>
  <div class="container">
    <div class="row mt-5 p-3 justify-content-center">
      <div class="col-4 me-5">
        <apexchart
          width="500"
          type="donut"
          :options="donutChartoptions"
          :series="donutChartseries"
        ></apexchart>
      </div>
    </div>
    <div class="row mt-5 p-3 justify-content-center">
      <div class="col-4">
        <apexchart
          width="500"
          type="bar"
          :options="barChartoptions"
          :series="barChartseries"
        ></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AdminSummary",
  data() {
    return {
      donutChart: {
        sections: [],
        issues: [],
      },
      barChart: {
        books: [],
        issues: [],
      },
    };
  },
  created() {
    fetch(store.getters.BASEURL + "/admin/book/statistics", {
      method: "GET",
      headers: {
        "Authentication-Token": store.getters.getToken,
      },
    })
      .then((response) => {
        if (response.status == 200) return response.json();
        else
          return {
            books: [],
            issues: [],
          };
      })
      .then((data) => (this.barChart = data));

    fetch(store.getters.BASEURL + "/admin/section/statistics", {
      method: "GET",
      headers: {
        "Authentication-Token": store.getters.getToken,
      },
    })
      .then((response) => {
        if (response.status == 200) return response.json();
        else
          return {
            sections: [],
            issues: [],
          };
      })
      .then((data) => (this.donutChart = data));
  },
  computed: {
    donutChartoptions() {
      return {
        labels: this.donutChart["sections"],
      };
    },
    donutChartseries() {
      return this.donutChart["issues"];
    },
    barChartoptions() {
      return {
        chart: {
          id: "book_stats",
        },
        xaxis: {
          categories: this.barChart["books"],
        },
      };
    },
    barChartseries() {
      return [
        {
          name: "book_series",
          data: this.barChart["issues"],
        },
      ];
    },
  },
};
</script>
