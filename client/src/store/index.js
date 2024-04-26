import { createStore } from "vuex";

const store = createStore({
  state() {
    return {
      BASEURL: "http://127.0.0.1:5000",
      sections: [],
      books: [],
      user: {
        role: null,
        token: null,
      },
    };
  },
  getters: {
    BASEURL(state) {
      return state.BASEURL;
    },
    getToken(state) {
      return state.user["token"];
    },
    getRole(state) {
      return state.user["role"];
    },
    getSections(state) {
      return state.sections;
    },
    getBooks(state) {
      return state.books;
    },
  },
  mutations: {
    setUser(state, value) {
      state.user = value;
      sessionStorage.setItem("user", JSON.stringify(value));
    },
    setSections(state, value) {
      state.sections = value;
    },
    setBooks(state, value) {
      state.books = value;
    },
  },
  actions: {
    getSections({ commit, state }, { search }) {
      const query = new URLSearchParams();
      if (search) query.append("search", search);
      fetch(state.BASEURL + "/sections?" + query.toString(), {
        method: "GET",
        headers: {
          "Authentication-Token": state.user["token"],
        },
      })
        .then((response) => {
          if (response.status == 200) return response.json();
          return [];
        })
        .then((data) => {
          commit("setSections", data);
        });
    },
    getBooks({ commit, state }, { search, rating, author, section }) {
      const query = new URLSearchParams();
      if (search) query.append("title", search);
      if (author) query.append("author", author);
      if (rating) query.append("rating", rating);
      if (section) query.append("section", section);

      fetch(state.BASEURL + "/books?" + query.toString(), {
        method: "GET",
        headers: {
          "Authentication-Token": state.user["token"],
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          commit("setBooks", data);
        });
    },
  },
});

export default store;
