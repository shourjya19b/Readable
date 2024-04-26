<script setup>
import InputError from "@/components/InputError.vue";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
import store from "@/store";
</script>
<template>
  <SuccessAlert
    v-show="success"
    message="Created user successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <ErrorAlert
    v-show="failure"
    message="Failed to create user"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container text-center mt-4 p-5">
    <div class="row justify-content-center p-5">
      <div class="col col-md-4 rounded-1 shadow p-5 bg-white">
        <h1 class="fs-1 mb-4 fw-semibold fst-italic">Read</h1>
        <form @submit="signup">
          <div class="mb-3 px-3">
            <input
              type="text"
              class="form-control shadow-sm bg-light"
              name="username"
              placeholder="Username"
              v-model="name"
            />
            <InputError :message="error['name']" />
          </div>
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
          <div class="mb-3 px-3">
            <input
              type="password"
              class="form-control shadow-sm bg-light"
              name="password"
              placeholder="Password"
              v-model="password"
            />
            <InputError :message="error['password']" />
          </div>
          <div class="mb-4 px-3">
            <input
              type="password"
              class="form-control shadow-sm bg-light"
              name="confirm_password"
              placeholder="Confirm Password"
              v-model="confirm_pwd"
            />
            <InputError :message="error['confirm_pwd']" />
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
            Create Account
          </button>
        </form>
        <div class="mb-2 text-secondary">
          Have an account?
          <a href="/user/login" class="text-decoration-none">Login</a>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Register",
  data() {
    return {
      name: null,
      password: null,
      confirm_pwd: null,
      email: null,
      success: false,
      failure: false,
      error: {
        name: null,
        password: null,
        confirm_pwd: null,
        email: null,
      },
    };
  },
  methods: {
    signup(event) {
      event.preventDefault();
      if (!this.validate())
        fetch(store.getters.BASEURL + "/user/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            password: this.password,
            confirm_pwd: this.confirm_pwd,
          }),
        })
          .then((response) => {
            return [response.json(), response.status];
          })
          .then((data) => {
            if (data[1] == 404) {
              this.failure = true;
              let backend_error = data[0]["error"];
              if (backend_error == "invalid_name")
                this.error["name"] = "Invalid name";
              else if (backend_error == "invalid_email")
                this.error["email"] = "Invalid email";
              else if (backend_error == "duplicate_email")
                this.error["email"] = "Email already exists";
              else if (backend_error == "invalid_password")
                this.error["password"] = "Invalid password";
            } else if (data[1] == 201) {
              this.success = true;
              this.name = null;
              this.email = null;
              this.password = null;
              this.confirm_pwd = null;
            }
          });
    },
    validate() {
      let invalid = false;
      this.error = {
        name: null,
        password: null,
        confirm_pwd: null,
        email: null,
      };
      if (!this.name || this.name.length < 2) {
        invalid = true;
        this.error["name"] = "Required field";
      }
      if (!this.password || this.password != this.confirm_pwd) {
        invalid = true;
        this.error["password"] = "Passwords don't match";
      }
      if (
        !this.email ||
        !this.email.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/)
      ) {
        invalid = true;
        this.error["email"] = "Invalid email";
      }
      return invalid;
    },
    dismissAlert() {
      this.success = false;
      this.failure = false;
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
  text-shadow: 1.5px 1.5px 0 black;
}
a {
  color: hsl(203, 55%, 38%);
}
a:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
</style>
