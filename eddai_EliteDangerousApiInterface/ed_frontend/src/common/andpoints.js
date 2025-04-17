const baseEndpoint = '/api/v1/';

const endpoints = {
    systems: {
        getAll: () => `${baseEndpoint}systems`,
        getById: (id) => `${baseEndpoint}systems/${id}`,
    },
}

export { endpoints};