// Import Vuex
import { createStore } from 'vuex';
import { headers } from "@/utils/api";


// Create a new Vuex store
const store = createStore({
    // State: Hold your global variables here
    state: {
        // Example global variable
        selectionsGroups: {},
        types: [],
        productsFields: {},
        // ...other global variables
    },
    // Mutations: Define methods to modify the state
    mutations: {
        setSelectionsGroups(state, payload) {
            console.log("setSelectionsGroups", payload);
            state.selectionsGroups[`${payload.id}`] = payload.selections;
        },
        setTypes(state, newTypes) {
            console.log("setTypes", newTypes);
            state.types = newTypes;
        },
        setProductsFields(state, payload) {
            console.log("setProductsFields", payload);
            state.productsFields[`${payload.id}`] = payload.fields;
        },
        // ...other mutations
    },
    // Actions: Perform asynchronous tasks and commit mutations
    actions: {
        async fetchSelections({ commit, state }, id) {
            if (!(id && !state.selectionsGroups[`${id}`])) {
                return;
            }
            headers().get(`/selections_groups/${id}/selections`).then((response) => {
                commit('setSelectionsGroups', {
                    selections: response.data,
                    id: id
                });
            }).catch((error) => {
                this.error = error;
            });
        },
        async fetchTypes({ commit, state }) {
            if(state.types.length > 0) {
                return;
            }
            headers().get("/types").then((response) => {
                commit('setTypes', response.data);
            }).catch((error) => {
                this.error = error;
            });
        },
        async fetchFields({ commit, dispatch, state }, productId) {
            if (!(productId && !state.productsFields[`${productId}`])) {
                return;
            }
            headers().get(`/products/${productId}/fields`).then((response) => {
                commit('setProductsFields', {
                    fields: response.data,
                    id: productId
                });
                for(let field of response.data) {
                    dispatch('fetchSelections', field.selections_groups_id);
                }
            }).catch((error) => {
                this.error = error;
            });
        },
    },
    // Getters: Derive computed properties from the state
    getters: {
        // ...getters if needed
    },
});

export default store;
