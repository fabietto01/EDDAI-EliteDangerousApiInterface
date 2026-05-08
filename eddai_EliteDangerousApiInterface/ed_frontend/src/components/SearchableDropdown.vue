<template>
    <div class="searchable-dropdown" ref="dropdownContainer">
        <div class="selected-display" @click="toggleDropdown">
            <div v-if="selectedItems.length > 0" class="selected-items-inline">
                <span class="selected-chip">
                    {{ selectedItems[0].name }}
                    <span class="remove-chip-icon" @click.stop="removeItem(selectedItems[0].id)">×</span>
                </span>
                <span v-if="selectedItems.length > 1" class="count-badge">
                    +{{ selectedItems.length - 1 }}
                </span>
            </div>
            <span v-else class="placeholder-text">{{ placeholder }}</span>
            <span class="dropdown-arrow">▼</span>
        </div>
        
        <div v-if="isOpen" class="dropdown-overlay">
            <div class="dropdown-header">
                <input 
                    v-model.trim="searchQuery" 
                    @input="onSearchInput"
                    type="text" 
                    :placeholder="searchPlaceholder"
                    :disabled="isLoading"
                    ref="searchInput"
                />
            </div>
            
            <div class="dropdown-content">
                <div v-if="selectedItems.length > 0" class="selected-section">
                    <div class="section-title">Selezionate:</div>
                    <div v-for="item in selectedItems" :key="'selected-' + item.id" 
                        @click="removeItem(item.id)"
                        class="result-item selected">
                        {{ item.name }}
                        <span class="remove-icon">×</span>
                    </div>
                </div>
                
                <div v-if="isLoading" class="loading-message">
                    Ricerca in corso...
                </div>
                
                <div v-else-if="searchQuery.length >= minSearchLength">
                    <div v-if="searchResults.length > 0" class="results-section">
                        <div class="section-title">Risultati:</div>
                        <div v-for="item in searchResults" :key="'result-' + item.id" 
                            @click="addItem(item)"
                            class="result-item">
                            {{ item.name }}
                        </div>
                    </div>
                    <div v-else class="no-results">
                        Nessun risultato trovato
                    </div>
                </div>
                
                <div v-else class="info-message">
                    Inserisci almeno {{ minSearchLength }} caratteri per cercare
                    <div v-if="maxSelections" class="selection-limit-info">
                        ({{ selectedItems.length }}/{{ maxSelections }} selezionati)
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { axiox as axios } from '@/common/api.service.js';

export default {
    name: 'SearchableDropdown',
    props: {
        modelValue: {
            type: Array,
            default: () => []
        },
        placeholder: {
            type: String,
            default: 'Seleziona...'
        },
        searchPlaceholder: {
            type: String,
            default: 'Cerca (min 3 caratteri)...'
        },
        endpoint: {
            type: String,
            required: true
        },
        searchParam: {
            type: String,
            default: 'search'
        },
        minSearchLength: {
            type: Number,
            default: 3
        },
        pageSize: {
            type: Number,
            default: 10
        },
        disabled: {
            type: Boolean,
            default: false
        },
        maxSelections: {
            type: Number,
            default: null
        }
    },
    data() {
        return {
            isOpen: false,
            searchQuery: '',
            searchResults: [],
            isLoading: false,
            selectedItems: []
        };
    },
    watch: {
        modelValue: {
            immediate: true,
            handler(newValue) {
                this.selectedItems = Array.isArray(newValue) ? [...newValue] : [];
            }
        }
    },
    methods: {
        toggleDropdown() {
            if (this.disabled) return;
            
            this.isOpen = !this.isOpen;
            if (this.isOpen) {
                this.$nextTick(() => {
                    if (this.$refs.searchInput) {
                        this.$refs.searchInput.focus();
                    }
                });
            } else {
                this.searchQuery = '';
                this.searchResults = [];
            }
        },
        closeDropdown(event) {
            if (this.$refs.dropdownContainer && !this.$refs.dropdownContainer.contains(event.target)) {
                this.isOpen = false;
                this.searchQuery = '';
                this.searchResults = [];
            }
        },
        async onSearchInput() {
            if (this.searchQuery.length < this.minSearchLength) {
                this.searchResults = [];
                return;
            }

            try {
                this.isLoading = true;
                const response = await axios.get(this.endpoint, {
                    params: {
                        [this.searchParam]: this.searchQuery,
                        page_size: this.pageSize,
                    },
                });
                const payload = response.data || {};
                const items = Array.isArray(payload) ? payload : (payload.results || []);
                this.searchResults = items.map((item) => ({
                    id: item.id,
                    name: item.name || `Item ${item.id}`,
                }));
            } catch (error) {
                console.error('Error searching items:', error);
                this.searchResults = [];
            } finally {
                this.isLoading = false;
            }
        },
        addItem(item) {
            if (!this.selectedItems.find((i) => i.id === item.id)) {
                // Controlla se è stato raggiunto il limite di selezioni
                if (this.maxSelections && this.selectedItems.length >= this.maxSelections) {
                    return;
                }
                const newSelection = [...this.selectedItems, item];
                this.selectedItems = newSelection;
                this.$emit('update:modelValue', newSelection);
            }
            this.searchQuery = '';
            this.searchResults = [];
        },
        removeItem(id) {
            const newSelection = this.selectedItems.filter((i) => i.id !== id);
            this.selectedItems = newSelection;
            this.$emit('update:modelValue', newSelection);
        }
    },
    mounted() {
        document.addEventListener('click', this.closeDropdown);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.closeDropdown);
    }
};
</script>

<style scoped>
/* ==================== EDDAI THEME - Searchable Dropdown ==================== */
/* Color scheme: #f36c1d (orange), #1c1b1d (dark), #2a2829 (dark-gray) */

.searchable-dropdown {
    position: relative;
}

.selected-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    background-color: #2a2829;
    color: #f36c1d;
    border: 1px solid rgba(243, 108, 29, 0.3);
    border-radius: 6px;
    cursor: pointer;
    min-height: 48px;
    transition: all 0.3s ease;
}

.selected-display:hover {
    border-color: #f36c1d;
    box-shadow: 0 0 0 3px rgba(243, 108, 29, 0.1);
}

.selected-items-inline {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    overflow: hidden;
}

.selected-chip {
    background-color: rgba(243, 108, 29, 0.2);
    border: 1px solid rgba(243, 108, 29, 0.4);
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.9rem;
    color: #f36c1d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
}

.remove-chip-icon {
    color: #f36c1d;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    transition: color 0.2s;
    line-height: 1;
    flex-shrink: 0;
}

.remove-chip-icon:hover {
    color: #ff8533;
}

.count-badge {
    background-color: #f36c1b;
    color: #1c1b1d;
    border-radius: 50%;
    padding: 0.15rem 0.6rem;
    font-size: 0.8rem;
    font-weight: 700;
    white-space: nowrap;
}

.placeholder-text {
    color: rgba(243, 108, 29, 0.5);
    font-size: 0.95rem;
}

.dropdown-arrow {
    color: #f36c1d;
    font-size: 0.85rem;
    margin-left: 0.75rem;
    transition: transform 0.3s ease;
}

.dropdown-overlay {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    background-color: #1c1b1d;
    border: 1px solid rgba(243, 108, 29, 0.3);
    border-radius: 8px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    z-index: 1000;
    max-height: 450px;
    display: flex;
    flex-direction: column;
}

.dropdown-header {
    padding: 0.75rem;
    border-bottom: 1px solid rgba(243, 108, 29, 0.2);
}

.dropdown-header input {
    width: 100%;
    padding: 0.75rem 1rem;
    background-color: #2a2829;
    color: #f36c1d;
    border: 1px solid rgba(243, 108, 29, 0.3);
    border-radius: 6px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.dropdown-header input:focus {
    outline: none;
    border-color: #f36c1d;
    box-shadow: 0 0 0 3px rgba(243, 108, 29, 0.1);
}

.dropdown-header input::placeholder {
    color: rgba(243, 108, 29, 0.5);
}

.dropdown-content {
    overflow-y: auto;
    max-height: 380px;
}

.selected-section,
.results-section {
    padding: 0.5rem 0;
}

.section-title {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: rgba(243, 108, 29, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.result-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    font-size: 0.95rem;
    color: #f36c1d;
    transition: all 0.2s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.result-item:hover {
    background-color: rgba(243, 108, 29, 0.1);
    color: #ff8533;
}

.result-item.selected {
    background-color: rgba(243, 108, 29, 0.2);
    color: #ff8533;
    font-weight: 500;
}

.result-item.selected:hover {
    background-color: rgba(243, 108, 29, 0.3);
}

.remove-icon {
    color: #f36c1d;
    font-size: 1.3rem;
    font-weight: bold;
    transition: color 0.2s;
}

.remove-icon:hover {
    color: #ff8533;
}

.loading-message,
.info-message,
.no-results {
    padding: 1.5rem;
    text-align: center;
    color: rgba(243, 108, 29, 0.7);
    font-size: 0.95rem;
}

.selection-limit-info {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: rgba(243, 108, 29, 0.6);
    font-weight: 600;
}

.no-results {
    color: rgba(243, 108, 29, 0.5);
}

/* Scrollbar styling for dropdown */
.dropdown-content::-webkit-scrollbar {
    width: 8px;
}

.dropdown-content::-webkit-scrollbar-track {
    background: rgba(243, 108, 29, 0.05);
    border-radius: 4px;
}

.dropdown-content::-webkit-scrollbar-thumb {
    background: rgba(243, 108, 29, 0.3);
    border-radius: 4px;
}

.dropdown-content::-webkit-scrollbar-thumb:hover {
    background: rgba(243, 108, 29, 0.5);
}
</style>
