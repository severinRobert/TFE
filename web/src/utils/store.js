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
        async fetchProducts({ commit, dispatch, state }, force = false) {
            if(state.products.length > 0 && !force) {
                return;
            }
            await headers().get("/products").then((response) => {
                commit('setProducts', response.data);
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
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
