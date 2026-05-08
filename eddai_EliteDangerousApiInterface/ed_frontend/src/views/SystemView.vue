<template>
    <div class="system-view">
        <header class="page-header">
            <h1>
                <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="3"/>
                    <circle cx="12" cy="12" r="8" opacity="0.3"/>
                    <circle cx="12" cy="12" r="11" opacity="0.1"/>
                </svg>
                Systems Explorer
            </h1>
            <p class="header-subtitle">Cerca e filtra sistemi nella galassia di Elite Dangerous</p>
        </header>

        <form class="filters" @submit.prevent="applyFilters">
            <div class="filters-header">
                <h2>
                    <svg class="filter-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                    Filtri
                    <span v-if="activeFiltersCount > 0" class="filter-badge">{{ activeFiltersCount }}</span>
                </h2>
                <button type="button" @click="toggleFilters" class="btn-toggle-filters">
                    <span v-if="filtersExpanded">Nascondi</span>
                    <span v-else>Mostra</span>
                    <svg :class="['chevron', { 'chevron-up': filtersExpanded }]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M6 9l6 6 6-6"/>
                    </svg>
                </button>
            </div>

            <transition name="slide-fade">
                <div v-show="filtersExpanded" class="filter-grid">
                <label>
                    Search
                    <input v-model.trim="filters.search" type="text" placeholder="Nome o address" />
                </label>

                <label>
                    Allegiance
                    <select v-model.number="filters.allegiance" :disabled="isLoadingAllegiances">
                        <option :value="null">Tutte</option>
                        <option v-for="allegiance in allegiances" :key="allegiance.id" :value="allegiance.id">
                            {{ allegiance.name }}
                        </option>
                    </select>
                    <small v-if="isLoadingAllegiances">Caricamento allegiances...</small>
                    <small v-if="allegianceError" class="error-message">{{ allegianceError }}</small>
                </label>

                <label>
                    Government
                    <select v-model.number="filters.government" :disabled="isLoadingGovernments">
                        <option :value="null">Tutte</option>
                        <option v-for="government in governments" :key="government.id" :value="government.id">
                            {{ government.name }}
                        </option>
                    </select>
                    <small v-if="isLoadingGovernments">Caricamento governi...</small>
                    <small v-if="governmentError" class="error-message">{{ governmentError }}</small>
                </label>

                <label>
                    Power
                    <select v-model.number="filters.power" :disabled="isLoadingPowers">
                        <option :value="null">Tutte</option>
                        <option v-for="power in powers" :key="power.id" :value="power.id">
                            {{ power.name }}
                        </option>
                    </select>
                    <small v-if="isLoadingPowers">Caricamento poteri...</small>
                    <small v-if="powerError" class="error-message">{{ powerError }}</small>
                </label>

                <label>
                    Primary Economy
                    <select v-model.number="filters.primaryEconomy" :disabled="isLoadingPrimaryEconomies">
                        <option :value="null">Tutte</option>
                        <option v-for="economy in primaryEconomies" :key="economy.id" :value="economy.id">
                            {{ economy.name }}
                        </option>
                    </select>
                    <small v-if="isLoadingPrimaryEconomies">Caricamento economie...</small>
                    <small v-if="primaryEconomyError" class="error-message">{{ primaryEconomyError }}</small>
                </label>

                <label>
                    Secondary Economy
                    <select v-model.number="filters.secondaryEconomy" :disabled="isLoadingSecondaryEconomies">
                        <option :value="null">Tutte</option>
                        <option v-for="economy in secondaryEconomies" :key="economy.id" :value="economy.id">
                            {{ economy.name }}
                        </option>
                    </select>
                    <small v-if="isLoadingSecondaryEconomies">Caricamento economie...</small>
                    <small v-if="secondaryEconomyError" class="error-message">{{ secondaryEconomyError }}</small>
                </label>

                <label>
                    Security
                    <select v-model="filters.security">
                        <option value="">Tutte</option>
                        <option value="A">Anarchy</option>
                        <option value="H">High</option>
                        <option value="M">Medium</option>
                        <option value="L">Low</option>
                    </select>
                </label>

                <label>
                    Population
                    <input v-model.number="filters.population" type="number" min="0" />
                </label>

                <label>
                    Population &gt;
                    <input v-model.number="filters.population__gt" type="number" min="0" />
                </label>

                <label>
                    Population &lt;
                    <input v-model.number="filters.population__lt" type="number" min="0" />
                </label>

                <label>
                    Controlling Faction
                    <SearchableDropdown
                        v-model="selectedControllingFactions"
                        :endpoint="endpoints.bgsMinorFactions"
                        placeholder="Seleziona faction..."
                        search-placeholder="Cerca faction (min 3 caratteri)..."
                    />
                </label>

                <label>
                    Controlling Faction State
                    <SearchableDropdown
                        v-model="selectedControllingFactionStates"
                        :endpoint="endpoints.bgsPowerStates"
                        placeholder="Seleziona stato..."
                        search-placeholder="Cerca stato (min 3 caratteri)..."
                    />
                </label>

                <label>
                    Exclude Faction
                    <SearchableDropdown
                        v-model="selectedExcludeFactions"
                        :endpoint="endpoints.bgsMinorFactions"
                        placeholder="Seleziona faction da escludere..."
                        search-placeholder="Cerca faction (min 3 caratteri)..."
                        :maxSelections="1"
                    />
                </label>

                <label>
                    Exclude Faction State
                    <SearchableDropdown
                        v-model="selectedExcludeFactionStates"
                        :endpoint="endpoints.bgsPowerStates"
                        placeholder="Seleziona stato da escludere..."
                        search-placeholder="Cerca stato (min 3 caratteri)..."
                    />
                </label>

                <label>
                    Distance By System
                    <SearchableDropdown
                        v-model="selectedDistanceBySystem"
                        :endpoint="endpoints.systemsGetAll"
                        placeholder="Seleziona sistema..."
                        search-placeholder="Cerca sistema (min 3 caratteri)..."
                        :maxSelections="1"
                    />
                </label>

                <label>
                    Distance Min (Ly)
                    <input v-model.number="filters.filter_distance_by_system__gt" type="number" min="0" step="0.1" />
                </label>

                <label>
                    Distance Max (Ly)
                    <input v-model.number="filters.filter_distance_by_system__lt" type="number" min="0" step="0.1" />
                </label>

                <label>
                    Order Distance
                    <select v-model="filters.order_distance_by_system">
                        <option value="">Default</option>
                        <option value="distance_st">distance_st</option>
                        <option value="-distance_st">-distance_st</option>
                    </select>
                </label>

                <label>
                    Created At
                    <input v-model.trim="filters.created_at" type="datetime-local" />
                </label>

                <label>
                    Created At &gt;
                    <input v-model.trim="filters.created_at__gt" type="datetime-local" />
                </label>

                <label>
                    Created At &lt;
                    <input v-model.trim="filters.created_at__lt" type="datetime-local" />
                </label>

                <label>
                    Updated At
                    <input v-model.trim="filters.updated_at" type="datetime-local" />
                </label>

                <label>
                    Updated At &gt;
                    <input v-model.trim="filters.updated_at__gt" type="datetime-local" />
                </label>

                <label>
                    Updated At &lt;
                    <input v-model.trim="filters.updated_at__lt" type="datetime-local" />
                </label>
            </div>
            </transition>

            <div class="filter-actions">
                <button type="submit" :disabled="isLoading">Applica filtri</button>
                <button type="button" @click="resetFilters" :disabled="isLoading">Reset</button>
            </div>
        </form>

        <transition name="fade">
            <div v-if="errorMessage" class="error-message">
                <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 8v4M12 16h.01"/>
                </svg>
                {{ errorMessage }}
            </div>
        </transition>

        <div class="results-info" v-if="systems.length > 0 || isLoading">
            <div class="info-card">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M3 6h18M3 12h18M3 18h18"/>
                </svg>
                <div>
                    <span class="info-label">Sistemi caricati:</span>
                    <span class="info-value">{{ systems.length }}</span>
                </div>
            </div>
            <div v-if="totalItems > 0" class="info-card">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                <div>
                    <span class="info-label">Totale:</span>
                    <span class="info-value">{{ totalItems }}</span>
                </div>
            </div>
            <div v-if="hasNext" class="info-card info-more">
                <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 5v14M5 12l7 7 7-7"/>
                </svg>
                <span class="info-label">Altri risultati disponibili</span>
            </div>
        </div>

        <div v-if="isLoading && systems.length === 0" class="loading-initial">
            <div class="spinner"></div>
            <p>Caricamento sistemi...</p>
        </div>
        <div v-else-if="systems.length === 0 && !isLoading" class="no-results">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 15h8M9 9h.01M15 9h.01"/>
            </svg>
            <h3>Nessun sistema trovato</h3>
            <p>Prova a modificare i filtri di ricerca</p>
        </div>
        
        <div v-if="systems.length > 0 || isLoading" class="table-container">
            <table class="systems-table">
                <thead>
                    <tr>
                        <th @click="sortBy('name')" class="sortable">
                            Nome
                            <svg v-if="sortColumn === 'name'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path :d="sortDirection === 'asc' ? 'M12 5v14M19 12l-7-7-7 7' : 'M12 19V5M5 12l7 7 7-7'"/>
                            </svg>
                        </th>
                        <th>Allegiance</th>
                        <th>Government</th>
                        <th>Economia Primaria</th>
                        <th>Economia Secondaria</th>
                        <th @click="sortBy('population')" class="sortable">
                            Popolazione
                            <svg v-if="sortColumn === 'population'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path :d="sortDirection === 'asc' ? 'M12 5v14M19 12l-7-7-7 7' : 'M12 19V5M5 12l7 7 7-7'"/>
                            </svg>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <template v-if="isLoading && systems.length === 0">
                        <tr v-for="n in 10" :key="'skeleton-' + n" class="skeleton-row">
                            <td><div class="skeleton skeleton-text"></div></td>
                            <td><div class="skeleton skeleton-text skeleton-short"></div></td>
                            <td><div class="skeleton skeleton-text skeleton-short"></div></td>
                            <td><div class="skeleton skeleton-text skeleton-medium"></div></td>
                            <td><div class="skeleton skeleton-text skeleton-medium"></div></td>
                            <td><div class="skeleton skeleton-text skeleton-short"></div></td>
                        </tr>
                    </template>
                    <transition-group v-else name="list" tag="template">
                        <tr v-for="system in sortedSystems" :key="system.id" class="data-row">
                            <td class="system-name">
                                <svg class="system-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <circle cx="12" cy="12" r="3"/>
                                </svg>
                                {{ system.name }}
                            </td>
                            <td>{{ getAllegianceName(system) }}</td>
                            <td>{{ getGovernmentName(system) }}</td>
                            <td>{{ getPrimaryEconomyName(system) }}</td>
                            <td>{{ getSecondaryEconomyName(system) }}</td>
                            <td class="population">{{ formatPopulation(system.population) }}</td>
                        </tr>
                    </transition-group>
                </tbody>
            </table>
            
            <div v-if="hasNext" class="load-more-container">
                <button 
                    type="button" 
                    @click="loadMoreSystems" 
                    :disabled="isLoading"
                    class="btn-load-more"
                >
                    <span v-if="isLoading">
                        <span class="btn-spinner"></span>
                        Caricamento...
                    </span>
                    <span v-else>
                        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M12 5v14M5 12l7 7 7-7"/>
                        </svg>
                        Carica altri sistemi
                    </span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { axiox as axios } from '@/common/api.service.js';
import { endpoints } from '@/common/endpoints.js';
import SearchableDropdown from '@/components/SearchableDropdown.vue';

export default {
    name: 'SystemView',
    components: {
        SearchableDropdown
    },
    data() {
        return {
            endpoints,
            systems: [],
            errorMessage: '',
            isLoading: false,
            currentPage: 1,
            totalItems: 0,
            hasNext: false,
            hasPrevious: false,
            filtersExpanded: true,
            sortColumn: '',
            sortDirection: 'asc',
            allegiances: [],
            isLoadingAllegiances: false,
            allegianceError: '',
            governments: [],
            isLoadingGovernments: false,
            governmentError: '',
            powers: [],
            isLoadingPowers: false,
            powerError: '',
            primaryEconomies: [],
            isLoadingPrimaryEconomies: false,
            primaryEconomyError: '',
            secondaryEconomies: [],
            isLoadingSecondaryEconomies: false,
            secondaryEconomyError: '',
            selectedControllingFactions: [],
            selectedControllingFactionStates: [],
            selectedExcludeFactionStates: [],
            selectedExcludeFactions: [],
            selectedDistanceBySystem: [],
            filters: {
                allegiance: null,
                created_at: '',
                created_at__gt: '',
                created_at__lt: '',
                filter_distance_by_system__gt: null,
                filter_distance_by_system__lt: null,
                government: null,
                order_distance_by_system: '',
                population: null,
                population__gt: null,
                population__lt: null,
                power: null,
                primaryEconomy: null,
                search: '',
                secondaryEconomy: null,
                security: '',
                updated_at: '',
                updated_at__gt: '',
                updated_at__lt: '',
            },
        };
    },
    computed: {
        activeFiltersCount() {
            let count = 0;
            if (this.filters.search) count++;
            if (this.filters.allegiance) count++;
            if (this.filters.government) count++;
            if (this.filters.power) count++;
            if (this.filters.primaryEconomy) count++;
            if (this.filters.secondaryEconomy) count++;
            if (this.filters.security) count++;
            if (this.filters.population) count++;
            if (this.filters.population__gt) count++;
            if (this.filters.population__lt) count++;
            if (this.selectedControllingFactions.length > 0) count++;
            if (this.selectedControllingFactionStates.length > 0) count++;
            if (this.selectedExcludeFactions.length > 0) count++;
            if (this.selectedExcludeFactionStates.length > 0) count++;
            if (this.selectedDistanceBySystem.length > 0) count++;
            if (this.filters.filter_distance_by_system__gt) count++;
            if (this.filters.filter_distance_by_system__lt) count++;
            if (this.filters.order_distance_by_system) count++;
            if (this.filters.created_at) count++;
            if (this.filters.created_at__gt) count++;
            if (this.filters.created_at__lt) count++;
            if (this.filters.updated_at) count++;
            if (this.filters.updated_at__gt) count++;
            if (this.filters.updated_at__lt) count++;
            return count;
        },
        sortedSystems() {
            if (!this.sortColumn) {
                return this.systems;
            }
            
            const sorted = [...this.systems].sort((a, b) => {
                let aVal = a[this.sortColumn];
                let bVal = b[this.sortColumn];
                
                if (this.sortColumn === 'name') {
                    aVal = (aVal || '').toLowerCase();
                    bVal = (bVal || '').toLowerCase();
                }
                
                if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
                if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
                return 0;
            });
            
            return sorted;
        },
        allegianceMap() {
            const map = new Map();
            this.allegiances.forEach(item => map.set(item.id, item.name));
            return map;
        },
        governmentMap() {
            const map = new Map();
            this.governments.forEach(item => map.set(item.id, item.name));
            return map;
        },
        primaryEconomyMap() {
            const map = new Map();
            this.primaryEconomies.forEach(item => map.set(item.id, item.name));
            return map;
        },
        secondaryEconomyMap() {
            const map = new Map();
            this.secondaryEconomies.forEach(item => map.set(item.id, item.name));
            return map;
        }
    },
    methods: {
        normalizeDateTime(value) {
            if (!value) {
                return '';
            }
            return `${value}:00`;
        },
        buildQueryParams(page) {
            const params = { page };
            const rawFilters = {
                ...this.filters,
                created_at: this.normalizeDateTime(this.filters.created_at),
                created_at__gt: this.normalizeDateTime(this.filters.created_at__gt),
                created_at__lt: this.normalizeDateTime(this.filters.created_at__lt),
                updated_at: this.normalizeDateTime(this.filters.updated_at),
                updated_at__gt: this.normalizeDateTime(this.filters.updated_at__gt),
                updated_at__lt: this.normalizeDateTime(this.filters.updated_at__lt),
            };

            // Handle controlling factions: single ID or CSV
            if (this.selectedControllingFactions.length > 0) {
                if (this.selectedControllingFactions.length === 1) {
                    rawFilters.conrollingFaction = this.selectedControllingFactions[0].id;
                } else {
                    rawFilters.conrollingFaction__in = this.selectedControllingFactions.map(f => f.id).join(',');
                }
            }

            // Handle controlling faction states: single ID or CSV
            if (this.selectedControllingFactionStates.length > 0) {
                if (this.selectedControllingFactionStates.length === 1) {
                    rawFilters.conrollingFaction__state = this.selectedControllingFactionStates[0].id;
                } else {
                    rawFilters.conrollingFaction__in__state = this.selectedControllingFactionStates.map(s => s.id).join(',');
                }
            }

            // Handle exclude faction states: single ID or CSV
            if (this.selectedExcludeFactionStates.length > 0) {
                if (this.selectedExcludeFactionStates.length === 1) {
                    rawFilters.conrollingFaction__not__state = this.selectedExcludeFactionStates[0].id;
                } else {
                    rawFilters.conrollingFaction__not__in__state = this.selectedExcludeFactionStates.map(s => s.id).join(',');
                }
            }

            // Handle exclude factions (single selection only)
            if (this.selectedExcludeFactions.length > 0) {
                rawFilters.conrollingFaction__not = this.selectedExcludeFactions[0].id;
            }

            // Handle distance by system (single selection only)
            if (this.selectedDistanceBySystem.length > 0) {
                rawFilters.distance_by_system = this.selectedDistanceBySystem[0].id;
            }

            Object.entries(rawFilters).forEach(([key, value]) => {
                if (value !== '' && value !== null && value !== undefined) {
                    params[key] = value;
                }
            });

            return params;
        },
        async getSystems(page = 1) {
            try {
                this.isLoading = true;
                this.errorMessage = '';

                let endpoint = endpoints.systemsGetAll;
                let response = await axios.get(endpoint, {
                    params: this.buildQueryParams(page),
                });
                let payload = response.data || {};
                const newSystems = Array.isArray(payload) ? payload : (payload.results || []);
                
                // Accumula i risultati invece di sostituirli
                if (page === 1) {
                    this.systems = newSystems;
                } else {
                    this.systems = [...this.systems, ...newSystems];
                }
                
                this.totalItems = Number.isInteger(payload.count) ? payload.count : this.systems.length;
                this.hasNext = Boolean(payload.next);
                this.hasPrevious = Boolean(payload.previous);
                this.currentPage = page;
            } catch (error) {
                this.errorMessage = 'Errore durante il caricamento dei sistemi. Verifica filtri e connessione API.';
                console.error('Error fetching systems:', error);
            } finally {
                this.isLoading = false;
            }
        },
        async fetchAllegiances() {
            try {
                this.isLoadingAllegiances = true;
                this.allegianceError = '';

                const collected = [];
                let endpoint = endpoints.bgsFactions;
                let pageGuard = 0;

                while (endpoint && pageGuard < 50) {
                    const response = await axios.get(endpoint);
                    const payload = response.data || {};
                    const items = Array.isArray(payload) ? payload : (payload.results || []);

                    items.forEach((item) => {
                        if (item && item.id !== null && item.id !== undefined) {
                            collected.push({
                                id: item.id,
                                name: item.name || `Faction ${item.id}`,
                            });
                        }
                    });

                    endpoint = payload && payload.next ? payload.next : null;
                    pageGuard += 1;
                }

                const uniqueById = new Map();
                collected.forEach((item) => {
                    if (!uniqueById.has(item.id)) {
                        uniqueById.set(item.id, item);
                    }
                });
                this.allegiances = Array.from(uniqueById.values()).sort((a, b) => {
                    return String(a.name).localeCompare(String(b.name));
                });
            } catch (error) {
                this.allegianceError = 'Impossibile caricare le allegiances.';
                console.error('Error fetching allegiances:', error);
            } finally {
                this.isLoadingAllegiances = false;
            }
        },
        async fetchGovernments() {
            try {
                this.isLoadingGovernments = true;
                this.governmentError = '';

                const collected = [];
                let endpoint = endpoints.bgsGovernments;
                let pageGuard = 0;

                while (endpoint && pageGuard < 50) {
                    const response = await axios.get(endpoint);
                    const payload = response.data || {};
                    const items = Array.isArray(payload) ? payload : (payload.results || []);

                    items.forEach((item) => {
                        if (item && item.id !== null && item.id !== undefined) {
                            collected.push({
                                id: item.id,
                                name: item.name || `Government ${item.id}`,
                            });
                        }
                    });

                    endpoint = payload && payload.next ? payload.next : null;
                    pageGuard += 1;
                }

                const uniqueById = new Map();
                collected.forEach((item) => {
                    if (!uniqueById.has(item.id)) {
                        uniqueById.set(item.id, item);
                    }
                });
                this.governments = Array.from(uniqueById.values()).sort((a, b) => {
                    return String(a.name).localeCompare(String(b.name));
                });
            } catch (error) {
                this.governmentError = 'Impossibile caricare i governi.';
                console.error('Error fetching governments:', error);
            } finally {
                this.isLoadingGovernments = false;
            }
        },
        async fetchPowers() {
            try {
                this.isLoadingPowers = true;
                this.powerError = '';

                const collected = [];
                let endpoint = endpoints.bgsPowers;
                let pageGuard = 0;

                while (endpoint && pageGuard < 50) {
                    const response = await axios.get(endpoint);
                    const payload = response.data || {};
                    const items = Array.isArray(payload) ? payload : (payload.results || []);

                    items.forEach((item) => {
                        if (item && item.id !== null && item.id !== undefined) {
                            collected.push({
                                id: item.id,
                                name: item.name || `Power ${item.id}`,
                            });
                        }
                    });

                    endpoint = payload && payload.next ? payload.next : null;
                    pageGuard += 1;
                }

                const uniqueById = new Map();
                collected.forEach((item) => {
                    if (!uniqueById.has(item.id)) {
                        uniqueById.set(item.id, item);
                    }
                });
                this.powers = Array.from(uniqueById.values()).sort((a, b) => {
                    return String(a.name).localeCompare(String(b.name));
                });
            } catch (error) {
                this.powerError = 'Impossibile caricare i poteri.';
                console.error('Error fetching powers:', error);
            } finally {
                this.isLoadingPowers = false;
            }
        },
        async fetchPrimaryEconomies() {
            try {
                this.isLoadingPrimaryEconomies = true;
                this.primaryEconomyError = '';

                const collected = [];
                let endpoint = endpoints.economy;
                let pageGuard = 0;

                while (endpoint && pageGuard < 50) {
                    const response = await axios.get(endpoint);
                    const payload = response.data || {};
                    const items = Array.isArray(payload) ? payload : (payload.results || []);

                    items.forEach((item) => {
                        if (item && item.id !== null && item.id !== undefined) {
                            collected.push({
                                id: item.id,
                                name: item.name || `Economy ${item.id}`,
                            });
                        }
                    });

                    endpoint = payload && payload.next ? payload.next : null;
                    pageGuard += 1;
                }

                const uniqueById = new Map();
                collected.forEach((item) => {
                    if (!uniqueById.has(item.id)) {
                        uniqueById.set(item.id, item);
                    }
                });
                this.primaryEconomies = Array.from(uniqueById.values()).sort((a, b) => {
                    return String(a.name).localeCompare(String(b.name));
                });
            } catch (error) {
                this.primaryEconomyError = 'Impossibile caricare le economie.';
                console.error('Error fetching primary economies:', error);
            } finally {
                this.isLoadingPrimaryEconomies = false;
            }
        },
        async fetchSecondaryEconomies() {
            try {
                this.isLoadingSecondaryEconomies = true;
                this.secondaryEconomyError = '';

                const collected = [];
                let endpoint = endpoints.economy;
                let pageGuard = 0;

                while (endpoint && pageGuard < 50) {
                    const response = await axios.get(endpoint);
                    const payload = response.data || {};
                    const items = Array.isArray(payload) ? payload : (payload.results || []);

                    items.forEach((item) => {
                        if (item && item.id !== null && item.id !== undefined) {
                            collected.push({
                                id: item.id,
                                name: item.name || `Economy ${item.id}`,
                            });
                        }
                    });

                    endpoint = payload && payload.next ? payload.next : null;
                    pageGuard += 1;
                }

                const uniqueById = new Map();
                collected.forEach((item) => {
                    if (!uniqueById.has(item.id)) {
                        uniqueById.set(item.id, item);
                    }
                });
                this.secondaryEconomies = Array.from(uniqueById.values()).sort((a, b) => {
                    return String(a.name).localeCompare(String(b.name));
                });
            } catch (error) {
                this.secondaryEconomyError = 'Impossibile caricare le economie.';
                console.error('Error fetching secondary economies:', error);
            } finally {
                this.isLoadingSecondaryEconomies = false;
            }
        },
        toggleFilters() {
            this.filtersExpanded = !this.filtersExpanded;
        },
        sortBy(column) {
            if (this.sortColumn === column) {
                this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortColumn = column;
                this.sortDirection = 'asc';
            }
        },
        applyFilters() {
            this.systems = []; // Reset dei sistemi quando si applicano nuovi filtri
            this.currentPage = 1;
            this.sortColumn = '';
            this.sortDirection = 'asc';
            this.getSystems(1);
        },
        loadMoreSystems() {
            if (this.hasNext && !this.isLoading) {
                this.getSystems(this.currentPage + 1);
            }
        },
        formatPopulation(population) {
            if (!population || population === 0) return '-';
            return new Intl.NumberFormat('it-IT').format(population);
        },
        getAllegianceName(system) {
            if (!system.allegiance) return '-';
            // Se è un oggetto con name, usa quello
            if (typeof system.allegiance === 'object' && system.allegiance.name) {
                return system.allegiance.name;
            }
            // Altrimenti è un ID, cerca nella mappa
            return this.allegianceMap.get(system.allegiance) || '-';
        },
        getGovernmentName(system) {
            if (!system.government) return '-';
            if (typeof system.government === 'object' && system.government.name) {
                return system.government.name;
            }
            return this.governmentMap.get(system.government) || '-';
        },
        getPrimaryEconomyName(system) {
            // L'API ritorna primaryEconomy (camelCase)
            const economyId = system.primaryEconomy || system.primary_economy;
            if (!economyId) return '-';
            if (typeof economyId === 'object' && economyId.name) {
                return economyId.name;
            }
            return this.primaryEconomyMap.get(economyId) || '-';
        },
        getSecondaryEconomyName(system) {
            // L'API ritorna secondaryEconomy (camelCase)
            const economyId = system.secondaryEconomy || system.secondary_economy;
            if (!economyId) return '-';
            if (typeof economyId === 'object' && economyId.name) {
                return economyId.name;
            }
            return this.secondaryEconomyMap.get(economyId) || '-';
        },
        resetFilters() {
            this.filters = {
                allegiance: null,
                created_at: '',
                created_at__gt: '',
                created_at__lt: '',
                filter_distance_by_system__gt: null,
                filter_distance_by_system__lt: null,
                government: null,
                order_distance_by_system: '',
                population: null,
                population__gt: null,
                population__lt: null,
                power: null,
                primaryEconomy: null,
                search: '',
                secondaryEconomy: null,
                security: '',
                updated_at: '',
                updated_at__gt: '',
                updated_at__lt: '',
            };
            this.governments = this.governments;
            this.powers = this.powers;
            this.primaryEconomies = this.primaryEconomies;
            this.secondaryEconomies = this.secondaryEconomies;
            this.selectedControllingFactions = [];
            this.selectedControllingFactionStates = [];
            this.selectedExcludeFactionStates = [];
            this.selectedExcludeFactions = [];
            this.selectedDistanceBySystem = [];
            this.systems = []; // Reset dei sistemi
            this.currentPage = 1;
            this.getSystems(1);
        },
    },
    created() {
        document.title = 'Systems';
        this.fetchAllegiances();
        this.fetchGovernments();
        this.fetchPowers();
        this.fetchPrimaryEconomies();
        this.fetchSecondaryEconomies();
        this.getSystems();
    }
};
</script>

<style scoped>
/* ==================== EDDAI THEME - Elite Dangerous Orange ==================== */
/* Color scheme: #f36c1d (orange), #1c1b1d (dark), #2a2829 (dark-gray) */

.system-view {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    min-height: 100vh;
    background: linear-gradient(135deg, #1c1b1d 0%, #2a2829 100%);
    padding: 2rem;
    color: #f36c1d;
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ==================== PAGE HEADER ==================== */
.page-header {
    text-align: center;
    margin-bottom: 2rem;
    animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.page-header h1 {
    color: #f36c1d;
    font-weight: 700;
    letter-spacing: 1px;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.header-icon {
    width: 48px;
    height: 48px;
    stroke-width: 2;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.8;
        transform: scale(1.05);
    }
}

.header-subtitle {
    color: rgba(243, 108, 29, 0.7);
    font-size: 1rem;
    font-weight: 400;
}

/* ==================== FILTERS CARD ==================== */
.filters {
    background-color: #1c1b1d;
    border: 1px solid rgba(243, 108, 29, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.filters-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(243, 108, 29, 0.2);
}

.filters-header h2 {
    color: #f36c1d;
    font-size: 1.3rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0;
}

.filter-icon {
    width: 24px;
    height: 24px;
    stroke-width: 2;
}

.filter-badge {
    background: linear-gradient(135deg, #f36c1d, #ff8533);
    color: #1c1b1d;
    border-radius: 12px;
    padding: 0.25rem 0.75rem;
    font-size: 0.85rem;
    font-weight: 700;
    animation: pop 0.3s ease-out;
}

@keyframes pop {
    0% {
        transform: scale(0);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}

.btn-toggle-filters {
    background-color: transparent;
    color: #f36c1d;
    border: 1px solid rgba(243, 108, 29, 0.3);
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-toggle-filters:hover {
    background-color: rgba(243, 108, 29, 0.1);
    border-color: #f36c1d;
}

.chevron {
    width: 16px;
    height: 16px;
    stroke-width: 2;
    transition: transform 0.3s ease;
}

.chevron-up {
    transform: rotate(180deg);
}

/* Slide-fade transition for filters */
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateY(-10px);
    opacity: 0;
}

.filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1.25rem;
}

.filter-grid label {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.95rem;
    color: #f36c1d;
    font-weight: 500;
}

/* ==================== FORM ELEMENTS ==================== */
.filter-grid input,
.filter-grid select {
    background-color: #2a2829;
    color: #f36c1d;
    border: 1px solid rgba(243, 108, 29, 0.3);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
    font-size: 0.95rem;
}

.filter-grid input:focus,
.filter-grid select:focus {
    background-color: #2a2829;
    color: #f36c1d;
    border-color: #f36c1d;
    outline: none;
    box-shadow: 0 0 0 3px rgba(243, 108, 29, 0.1);
}

.filter-grid input::placeholder {
    color: rgba(243, 108, 29, 0.5);
}

.filter-grid input:disabled,
.filter-grid select:disabled {
    background-color: rgba(42, 40, 41, 0.5);
    color: rgba(243, 108, 29, 0.5);
    cursor: not-allowed;
}

.filter-grid small {
    color: rgba(243, 108, 29, 0.7);
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

/* ==================== BUTTONS ==================== */
.filter-actions {
    margin-top: 1.5rem;
    display: flex;
    gap: 1rem;
    justify-content: flex-start;
}

.filter-actions button {
    background-color: #f36c1b;
    color: #1c1b1d;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: inset 4px 4px 4px 0px rgba(0, 0, 0, 0.2);
}

.filter-actions button:hover:not(:disabled) {
    background-color: #ff8533;
    color: #1c1b1d;
    transform: translateY(-2px);
    box-shadow: inset 4px 4px 4px 0px rgba(0, 0, 0, 0.3);
}

.filter-actions button:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: inset 4px 4px 4px 0px rgba(0, 0, 0, 0.2);
}

.filter-actions button:disabled {
    background-color: rgba(243, 108, 29, 0.3);
    color: rgba(28, 27, 29, 0.5);
    cursor: not-allowed;
    transform: none;
}

.filter-actions button[type="button"] {
    background-color: transparent;
    color: #f36c1d;
    border: 2px solid rgba(243, 108, 29, 0.3);
    box-shadow: none;
}

.filter-actions button[type="button"]:hover:not(:disabled) {
    background-color: rgba(243, 108, 29, 0.1);
    color: #ff8533;
    border-color: #ff8533;
}

/* ==================== MESSAGES ==================== */
.error-message {
    background-color: rgba(220, 38, 38, 0.15);
    color: #ff6b6b;
    border: 1px solid rgba(220, 38, 38, 0.4);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 1rem;
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.error-icon {
    width: 24px;
    height: 24px;
    stroke-width: 2;
    flex-shrink: 0;
}

/* Fade transition for error messages */
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}

/* ==================== RESULTS INFO ==================== */
.results-info {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}

.info-card {
    background-color: #1c1b1d;
    border: 1px solid rgba(243, 108, 29, 0.2);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #f36c1d;
    font-weight: 500;
    transition: all 0.3s ease;
    animation: scaleIn 0.4s ease-out;
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.info-card:hover {
    border-color: #f36c1d;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(243, 108, 29, 0.2);
}

.info-icon {
    width: 20px;
    height: 20px;
    stroke-width: 2;
    flex-shrink: 0;
}

.info-label {
    color: rgba(243, 108, 29, 0.7);
    font-size: 0.9rem;
}

.info-value {
    color: #f36c1d;
    font-weight: 700;
    font-size: 1.1rem;
    margin-left: 0.25rem;
}

.info-more {
    background: linear-gradient(135deg, rgba(243, 108, 29, 0.1), rgba(243, 108, 29, 0.05));
    border-color: rgba(243, 108, 29, 0.3);
}

.loading-initial,
.no-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    color: rgba(243, 108, 29, 0.8);
    font-size: 1.1rem;
    text-align: center;
    padding: 4rem 2rem;
    background-color: #1c1b1d;
    border: 1px solid rgba(243, 108, 29, 0.2);
    border-radius: 12px;
    animation: fadeIn 0.5s ease-in;
}

.spinner {
    width: 48px;
    height: 48px;
    border: 4px solid rgba(243, 108, 29, 0.2);
    border-top-color: #f36c1d;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.empty-icon {
    width: 64px;
    height: 64px;
    stroke-width: 2;
    opacity: 0.5;
}

.no-results h3 {
    color: #f36c1d;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
}

.no-results p {
    color: rgba(243, 108, 29, 0.6);
    font-size: 1rem;
    margin: 0;
}

/* ==================== TABLE ==================== */
.table-container {
    background-color: #1c1b1d;
    border: 1px solid rgba(243, 108, 29, 0.2);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    animation: slideUp 0.6s ease-out 0.2s both;
}

.systems-table {
    width: 100%;
    border-collapse: collapse;
    color: #f36c1d;
}

.systems-table thead {
    background-color: rgba(243, 108, 29, 0.15);
    position: sticky;
    top: 0;
    z-index: 10;
}

.systems-table th {
    padding: 1rem 1.5rem;
    text-align: left;
    font-weight: 700;
    font-size: 0.9rem;
    color: #f36c1d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 2px solid rgba(243, 108, 29, 0.3);
    position: relative;
}

.systems-table th.sortable {
    cursor: pointer;
    user-select: none;
    transition: all 0.3s ease;
}

.systems-table th.sortable:hover {
    background-color: rgba(243, 108, 29, 0.2);
    color: #ff8533;
}

.sort-icon {
    width: 16px;
    height: 16px;
    stroke-width: 2;
    margin-left: 0.5rem;
    display: inline-block;
    vertical-align: middle;
    animation: fadeIn 0.3s ease-in;
}

/* Skeleton loaders */
.skeleton-row td {
    padding: 1rem 1.5rem;
}

.skeleton {
    background: linear-gradient(
        90deg,
        rgba(243, 108, 29, 0.1) 0%,
        rgba(243, 108, 29, 0.2) 50%,
        rgba(243, 108, 29, 0.1) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: 4px;
    height: 16px;
}

@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

.skeleton-text {
    width: 100%;
}

.skeleton-short {
    width: 60%;
}

.skeleton-medium {
    width: 80%;
}

/* Data rows */
.data-row {
    border-bottom: 1px solid rgba(243, 108, 29, 0.1);
    transition: all 0.3s ease;
}

.data-row:hover {
    background-color: rgba(243, 108, 29, 0.08);
    transform: scale(1.002);
}

.data-row:last-child {
    border-bottom: none;
}

/* List transition for rows */
.list-enter-active {
    transition: all 0.5s ease;
}

.list-leave-active {
    transition: all 0.3s ease;
}

.list-enter-from {
    opacity: 0;
    transform: translateY(-10px);
}

.list-leave-to {
    opacity: 0;
    transform: translateX(-20px);
}

.systems-table td {
    padding: 1rem 1.5rem;
    font-size: 0.95rem;
    color: rgba(243, 108, 29, 0.9);
}

.systems-table td.system-name {
    font-weight: 600;
    color: #f36c1d;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.system-icon {
    width: 16px;
    height: 16px;
    stroke-width: 2;
    flex-shrink: 0;
}

.systems-table td.population {
    text-align: right;
    font-variant-numeric: tabular-nums;
}

/* ==================== LOAD MORE BUTTON ==================== */
.load-more-container {
    padding: 2rem;
    display: flex;
    justify-content: center;
    background-color: rgba(243, 108, 29, 0.05);
    border-top: 1px solid rgba(243, 108, 29, 0.2);
}

.btn-load-more {
    background: linear-gradient(135deg, #f36c1b, #ff8533);
    color: #1c1b1d;
    border: none;
    border-radius: 8px;
    padding: 1rem 3rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(243, 108, 29, 0.3);
    min-width: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-load-more:hover:not(:disabled) {
    background: linear-gradient(135deg, #ff8533, #f36c1b);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(243, 108, 29, 0.4);
}

.btn-load-more:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(243, 108, 29, 0.3);
}

.btn-load-more:disabled {
    background: linear-gradient(135deg, rgba(243, 108, 29, 0.3), rgba(243, 108, 29, 0.2));
    color: rgba(28, 27, 29, 0.5);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.btn-icon {
    width: 20px;
    height: 20px;
    stroke-width: 2;
}

.btn-spinner {
    width: 20px;
    height: 20px;
    border: 3px solid rgba(28, 27, 29, 0.3);
    border-top-color: #1c1b1d;
    border-radius: 50%;
    display: inline-block;
    animation: spin 1s linear infinite;
}

/* ==================== RESPONSIVE DESIGN ==================== */
@media (max-width: 1200px) {
    .filter-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    }
    
    .systems-table th,
    .systems-table td {
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
    }
}

@media (max-width: 768px) {
    .system-view {
        padding: 1rem;
        gap: 1rem;
    }
    
    .page-header h1 {
        font-size: 1.75rem;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .header-icon {
        width: 36px;
        height: 36px;
    }
    
    .filter-grid {
        grid-template-columns: 1fr;
    }
    
    .filters-header {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }
    
    .filters-header h2 {
        justify-content: center;
    }
    
    .filter-actions {
        flex-direction: column;
    }
    
    .filter-actions button {
        width: 100%;
    }
    
    .results-info {
        flex-direction: column;
        align-items: stretch;
    }
    
    .info-card {
        justify-content: center;
    }
    
    .table-container {
        overflow-x: auto;
    }
    
    .systems-table {
        min-width: 800px;
    }
    
    .btn-load-more {
        width: 100%;
        padding: 1rem 2rem;
    }
}

@media (max-width: 480px) {
    .page-header h1 {
        font-size: 1.5rem;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
    }
    
    .filters {
        padding: 1rem;
    }
    
    .filter-grid {
        gap: 1rem;
    }
}

/* ==================== PRINT STYLES ==================== */
@media print {
    .filters,
    .filter-actions,
    .btn-load-more {
        display: none;
    }
    
    .system-view {
        background: white;
        color: black;
    }
    
    .systems-table {
        border: 1px solid #ccc;
    }
    
    .systems-table th,
    .systems-table td {
        border: 1px solid #ddd;
        color: black;
    }
}
</style>