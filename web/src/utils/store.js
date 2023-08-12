// Import Vuex
import { createStore } from 'vuex';
import { headers } from "@/utils/api";


// Create a new Vuex store
const store = createStore({
    // State: Hold your global variables here
    state: {
        // Example global variable
        selectionsGroupsArray: [],
        selectionsGroups: {},
        typesArray: [],
        typesObject: {},
        fieldsArray: [],
        productsFields: {},
        products: [],
        username: localStorage.getItem('user'),
        role: localStorage.getItem('role'),
        favorites: [],
        colors: {},
        title: "MarketEase",
        homeDescription: "MarketEase is a platform that allows you to create your own online store in a few clicks. You can create your own products, add them to your store and let your members exchange these products.",
        // ...other global variables
    },
    // Mutations: Define methods to modify the state
    mutations: {
        setSelectionsGroupsArray(state, newSelectionsGroups) {
            console.log("setSelectionsGroupsArray", newSelectionsGroups)
            state.selectionsGroupsArray = newSelectionsGroups;
        },
        setSelectionsGroups(state, payload) {
            console.log("setSelectionsGroups", payload)
            state.selectionsGroups[`${payload.id}`] = payload.selections;
        },
        deleteSelectionsGroup(state, selectionsGroupId) {
            console.log("deleteSelectionsGroup", selectionsGroupId);
            state.selectionsGroupsArray = state.selectionsGroupsArray.filter(selectionsGroup => selectionsGroup.id !== selectionsGroupId);
            delete state.selectionsGroups[`${selectionsGroupId}`];
        },
        setTypesArray(state, newTypes) {
            console.log("setTypesArray", newTypes)
            state.typesArray = newTypes;
        },
        setTypesObject(state, newTypes) {
            console.log("setTypesObject", newTypes)
            state.typesObject = newTypes;
        },
        setFieldsArray(state, newFields) {
            console.log("setFieldsArray", newFields)
            state.fieldsArray = newFields;
        },
        setProductsFields(state, payload) {
            console.log("setProductsFields", payload)
            state.productsFields[`${payload.id}`] = payload.fields;
        },
        setProducts(state, newProducts) {
            console.log("setProducts", newProducts);
            state.products = newProducts;
        },
        deleteProduct(state, productId) {
            console.log("deleteProduct", productId);
            state.products = state.products.filter(product => product.id !== productId);
        },
        setUsername(state, username) {
            console.log("setUsername", username);
            state.username = username;
        },
        setRole(state, role) {
            console.log("setRole", role);
            state.role = role;
        },
        setFavorites(state, favorites) {
            console.log("setFavorites", favorites);
            state.favorites = favorites;
        },
        resetFavorites(state) {
            console.log("resetFavorites");
            state.favorites = [];
        },
        setColor(state, payload) {
            console.log("setColor", payload);
            state.colors[payload.id][payload.theme] = payload.color;
        },
        setColors(state, payload) {
            console.log("setColors", payload);
            state.colors = payload;
        },
        setSettings(state, payload) {
            console.log("setSettings", payload);
            state.title = payload.title;
            state.homeDescription = payload.home_description;
        },
        // ...other mutations
    },
    // Actions: Perform asynchronous tasks and commit mutations
    actions: {
        async fetchSelectionsGroupsArray({ commit, state }) {
            if(state.selectionsGroupsArray.length > 0) {
                return;
            }
            return await headers().get("/selections_groups").then((response) => {
                commit('setSelectionsGroupsArray', response.data);
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
        async fetchSelections({ commit, state }, id) {
            if (!(id && !state.selectionsGroups[`${id}`])) {
                return;
            }
            return await headers().get(`/selections_groups/${id}/selections`).then((response) => {
                commit('setSelectionsGroups', {
                    selections: response.data,
                    id: id
                });
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
        async fetchTypes({ commit, state }) {
            if(state.typesArray.length > 0) {
                return;
            }
            headers().get("/types").then((response) => {
                commit('setTypesArray', response.data);
                commit('setTypesObject', response.data.reduce((types, type) => {
                    types[type.id] = type.name;
                    return types;
                }, {}));
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
        async fetchFieldsArray({ commit, state }) {
            if (state.fieldsArray.length > 0) {
                return;
            }
            headers().get(`/fields`).then((response) => {
                commit('setFieldsArray', response.data);
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
        async fetchProductFields({ commit, dispatch, state }, productId, force = false) {
            if (!(productId && !state.productsFields[`${productId}`] && !force)) {
                return;
            }
            await headers().get(`/products/${productId}/fields`).then((response) => {
                commit('setProductsFields', {
                    fields: response.data,
                    id: productId
                });
                for(let field of response.data) {
                    dispatch('fetchSelections', field.selections_groups_id);
                }
            }).catch((error) => {
                if(error.response.status == 404) {
                    commit('setProductsFields', {
                        fields: [],
                        id: productId
                    });
                }
            });
        },
        async fetchProducts({ commit, state }, force = false) {
            if(state.products.length > 0 && !force) {
                return;
            }
            await headers().get("/products").then((response) => {
                commit('setProducts', response.data);
            }).catch((error) => {
                console.log(error);
            });
        },
        async fetchFavorites({ commit, state }, userId, force = false) {
            if(state.favorites.length > 0 && !force) {
                return;
            }
            await headers().get(`/users/${userId}/favorites`).then((response) => {
                console.log(response.data);
                commit('setFavorites', response.data);
            }).catch((error) => {
                console.log(error);
            });
        },
        async addFavorite({ state }, data) {
            console.log(data)
            await headers().post("/users/favorites", data).then((response) => {
                console.log(response.data);
                state.favorites.push(data.offer_id);
                return
            }).catch((error) => {
                console.log(error);
                return error;
            });
        },
        async removeFavorite({ commit, state }, data) {
            console.log(data)
            await headers().delete(`/users/${data.user_id}/favorites/${data.offer_id}`).then((response) => {
                console.log(response.data);
                commit('setFavorites', state.favorites.filter((id) => id!=data.offer_id));
            }).catch((error) => {
                console.log(error);
                return error;
            });
        },
        async activeColors({ state }) {
            let styles_light = "";
            let styles_dark = "";
            for (let [key, value] of Object.entries(state.colors)) {
                styles_light += `--${value.name}: ${value.value} !important;`;
                styles_dark += `--${value.name}: ${value.value_dark} !important;`;
            }
            const styles = `
                :root {
                    ${styles_light}
                }
                :root.dark-theme {
                    ${styles_dark}
                }`;
            document.getElementById("stylesheet").innerHTML = styles;
        },
        async fetchColors({ commit, state, dispatch }) {
            if(state.colors.length > 0) {
                return;
            }
            await headers().get("/sites/colors").then((response) => {
                console.log("fetchColors", response.data);
                const payload = response.data.reduce(
                    (obj, item) => Object.assign(obj, { 
                        [item.id]: {
                            'name': item.name,
                            'value': item.value,
                            'value_dark': item.value_dark,
                        } 
                    }), {});
                commit('setColors', payload);
            }).catch((error) => {
                return error;
            });
            dispatch('activeColors');
        },
        async saveColor({ state }, id) {
            headers().put(`/sites/colors/${id}`, state.colors[id]).then((response) => {
                return;
            }).catch((error) => {
                console.log(error);
                return error;
            });
        },
        async activeSettings({ state }) {
            document.getElementsByTagName("title")[0].innerHTML = state.title;
        },
        async fetchSettings({ commit, dispatch }) {
            await headers().get("/sites/settings").then((response) => {
                console.log("fetchSettings", response.data);
                commit('setSettings', response.data);
            }).catch((error) => {
                return error;
            });
            dispatch('activeSettings');
        },
        async saveSettings({ state }, id) {
            const data = { 'title': state.title, 'home_description': state.homeDescription };
            headers().put(`/sites/settings`, data).then((response) => {
                return;
            }).catch((error) => {
                console.log(error);
                return error;
            });
        },
    },
    // Getters: Derive computed properties from the state
    getters: {
        selectionsGroupById: (state) => (id) => {
            return state.selectionsGroupsArray.find(selectionsGroup => selectionsGroup.id === id);
        },
        getProductById: (state) => (id) => {
            return state.products.find(product => product.id === id);
        },
    },
});

export default store;
