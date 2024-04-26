<script setup>
import InputError from "@/components/InputError.vue";
import ValidationError from "@/components/ValidationError.vue";
import store from "@/store";
import router from "@/router";
</script>
<template>
  <div class="container text-center mt-5 p-5">
    <div class="row justify-content-center p-5">
      <div class="col col-md-4 rounded-1 shadow p-5 bg-white">
        <h1 class="fs-1 mb-4 fw-bold fst-italic">Read</h1>
        <ValidationError :invalid="error['validation']" />
        <form @submit="signin">
          <div class="mb-3 px-3">
            <input
              type="email"
              class="form-control shadow-sm bg-light"
              name="email"
              placeholder="Email"
              v-model="email"
            />
            <InputError :message="error['email']" />
          </div>
          <div class="mb-4 px-3">
            <input
              type="password"
              class="form-control shadow-sm bg-light"
              name="password"
              placeholder="Password"
              v-model="password"
            />
            <InputError :message="error['password']" />
          </div>
          <button
            type="submit"
            class="btn btn-lg mb-4 shadow rounded-pill fw-semibold"
            style="
              --bs-btn-padding-y: 0.25rem;
              --bs-btn-padding-x: 2.5rem;
              --bs-btn-font-size: 1.25rem;
            "
          >
            Login
          </button>
        </form>
        <div class="mb-2 text-secondary">
          Don't have an account?
          <a href="/user/register" class="text-decoration-none">Sign up</a>
        </div>
        <div class="mb-2 text-secondary">
          <a href="/admin/login" class="adm-link text-decoration-none"
            >Admin Login</a
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "UserLogin",
  data() {
    return {
      email: null,
      password: null,
      error: {
        email: null,
        password: null,
        validation: false,
      },
    };
  },
  methods: {
    signin(event) {
      event.preventDefault();
      if (!this.validate())
        fetch(store.getters.BASEURL + "/user/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        })
          .then((response) => {
            return [response.json(), response.status];
          })
          .then((data) => {
            if (data[1] == 404) {
              this.error["validation"] = true;
              return data[0];
            } else if (data[1] == 200) {
              return data[0];
            }
          })
          .then((data) => {
            if (data) {
              if (Object.keys(data).includes("token")) {
                store.commit("setUser", data);
                router.push("/user/board");
              }
            }
          });
    },
    validate() {
      let invalid = false;
      this.error = {
        email: null,
        password: null,
        validation: false,
      };
      if (
        !this.email ||
        !this.email.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)
      ) {
        invalid = true;
        this.error["email"] = "Invalid email";
      }
      if (!this.password) {
        invalid = true;
        this.error["password"] = "Invalid password";
      }
      return invalid;
    },
  },
};
</script>
<style scoped>
h1 {
  color: #ed7966;
  font-family: Sacramento;
}
.btn {
  background: hsl(203, 55%, 38%);
  color: white;
}
.btn:hover {
  text-shadow: 2px 2px 0 black;
}

a {
  color: hsl(203, 55%, 38%);
}
a:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
.adm-link {
  color: #ed7966;
}
.adm-link:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
</style>
