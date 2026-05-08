const baseEndpoint = '/api/v1/';

const endpoints = {
    atmosphereComponent: `${baseEndpoint}atmosphere-component`,
    atmosphereComponentById: (id) => `${baseEndpoint}atmosphere-component/${id}`,

    atmosphereType: `${baseEndpoint}atmosphere-type`,
    atmosphereTypeById: (id) => `${baseEndpoint}atmosphere-type/${id}`,

    bgsFactions: `${baseEndpoint}bgs/factions`,
    bgsFactionsById: (id) => `${baseEndpoint}bgs/factions/${id}`,

    bgsGovernments: `${baseEndpoint}bgs/governments`,
    bgsGovernmentsById: (id) => `${baseEndpoint}bgs/governments/${id}`,

    bgsMinorFactions: `${baseEndpoint}bgs/minor-factions`,
    bgsMinorFactionsById: (id) => `${baseEndpoint}bgs/minor-factions/${id}`,
    bgsMinorFactionsSystemsById: (id) => `${baseEndpoint}bgs/minor-factions/${id}/systems`,

    bgsMinorFactionsInSystem: `${baseEndpoint}bgs/minor-factions-in-system`,
    bgsMinorFactionsInSystemById: (id) => `${baseEndpoint}bgs/minor-factions-in-system/${id}`,
    bgsMinorFactionsInSystemStatesByMinorFactionInSystemPk: (minorfactioninsystemPk) =>
        `${baseEndpoint}bgs/minor-factions-in-system/${minorfactioninsystemPk}/states`,
    bgsMinorFactionsInSystemStatesByMinorFactionInSystemPkAndId: (minorfactioninsystemPk, id) =>
        `${baseEndpoint}bgs/minor-factions-in-system/${minorfactioninsystemPk}/states/${id}`,

    bgsPowerInSystem: `${baseEndpoint}bgs/power-in-system`,
    bgsPowerInSystemById: (id) => `${baseEndpoint}bgs/power-in-system/${id}`,

    bgsPowerStates: `${baseEndpoint}bgs/power-states`,
    bgsPowerStatesById: (id) => `${baseEndpoint}bgs/power-states/${id}`,

    bgsPowers: `${baseEndpoint}bgs/powers`,
    bgsPowersById: (id) => `${baseEndpoint}bgs/powers/${id}`,
    bgsPowersSystemsById: (id) => `${baseEndpoint}bgs/powers/${id}/systems`,

    bgsStates: `${baseEndpoint}bgs/states`,
    bgsStatesById: (id) => `${baseEndpoint}bgs/states/${id}`,

    body: `${baseEndpoint}body`,

    bodyPlanet: `${baseEndpoint}body/planet`,
    bodyPlanetById: (id) => `${baseEndpoint}body/planet/${id}`,
    bodyPlanetAtmosphereComponentByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/atmosphere-component`,
    bodyPlanetAtmosphereComponentByPlanetPkAndId: (planetPk, id) =>
        `${baseEndpoint}body/planet/${planetPk}/atmosphere-component/${id}`,
    bodyPlanetAtmosphereComponentAddsByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/atmosphere-component/adds`,
    bodyPlanetMaterialByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/material`,
    bodyPlanetMaterialByPlanetPkAndId: (planetPk, id) => `${baseEndpoint}body/planet/${planetPk}/material/${id}`,
    bodyPlanetMaterialAddsByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/material/adds`,
    bodyPlanetSampleByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/sample`,
    bodyPlanetSampleByPlanetPkAndId: (planetPk, id) => `${baseEndpoint}body/planet/${planetPk}/sample/${id}`,
    bodyPlanetSampleAddsByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/sample/adds`,
    bodyPlanetSignalByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/signal`,
    bodyPlanetSignalByPlanetPkAndId: (planetPk, id) => `${baseEndpoint}body/planet/${planetPk}/signal/${id}`,
    bodyPlanetSignalAddsByPlanetPk: (planetPk) => `${baseEndpoint}body/planet/${planetPk}/signal/adds`,

    bodyStar: `${baseEndpoint}body/star`,
    bodyStarById: (id) => `${baseEndpoint}body/star/${id}`,

    commodity: `${baseEndpoint}commodity`,
    commodityById: (id) => `${baseEndpoint}commodity/${id}`,

    economy: `${baseEndpoint}economy`,
    economyById: (id) => `${baseEndpoint}economy/${id}`,

    hotspotType: `${baseEndpoint}hotspot-type`,
    hotspotTypeById: (id) => `${baseEndpoint}hotspot-type/${id}`,

    material: `${baseEndpoint}material`,
    materialById: (id) => `${baseEndpoint}material/${id}`,

    planetType: `${baseEndpoint}planet-type`,
    planetTypeById: (id) => `${baseEndpoint}planet-type/${id}`,

    ring: `${baseEndpoint}ring`,
    ringById: (id) => `${baseEndpoint}ring/${id}`,
    ringHotspotByRingPk: (ringPk) => `${baseEndpoint}ring/${ringPk}/hotspot`,
    ringHotspotByRingPkAndId: (ringPk, id) => `${baseEndpoint}ring/${ringPk}/hotspot/${id}`,
    ringHotspotMultipleAddsByRingPk: (ringPk) => `${baseEndpoint}ring/${ringPk}/hotspot/multiple-adds`,

    sampleSignals: `${baseEndpoint}sample-signals`,
    sampleSignalsById: (id) => `${baseEndpoint}sample-signals/${id}`,

    services: `${baseEndpoint}services`,
    servicesById: (id) => `${baseEndpoint}services/${id}`,

    signalSignals: `${baseEndpoint}signal-signals`,
    signalSignalsById: (id) => `${baseEndpoint}signal-signals/${id}`,

    starLuminosity: `${baseEndpoint}star-luminosity`,
    starLuminosityById: (id) => `${baseEndpoint}star-luminosity/${id}`,

    starType: `${baseEndpoint}star-type`,
    starTypeById: (id) => `${baseEndpoint}star-type/${id}`,

    stationTypes: `${baseEndpoint}station-types`,
    stationTypesById: (id) => `${baseEndpoint}station-types/${id}`,

    stations: `${baseEndpoint}stations`,
    stationsById: (id) => `${baseEndpoint}stations/${id}`,
    stationsCommoditiesByStationPk: (stationPk) => `${baseEndpoint}stations/${stationPk}/commodities`,
    stationsCommoditiesByStationPkAndId: (stationPk, id) => `${baseEndpoint}stations/${stationPk}/commodities/${id}`,
    stationsCommoditiesAddsByStationPk: (stationPk) => `${baseEndpoint}stations/${stationPk}/commodities/adds`,
    stationsServicesByStationPk: (stationPk) => `${baseEndpoint}stations/${stationPk}/services`,
    stationsServicesByStationPkAndId: (stationPk, id) => `${baseEndpoint}stations/${stationPk}/services/${id}`,
    stationsServicesAddsByStationPk: (stationPk) => `${baseEndpoint}stations/${stationPk}/services/adds`,

    systemsGetAll: `${baseEndpoint}system`,
    systemsGetById: (id) => `${baseEndpoint}system/${id}`,
    systemMinorFactionsById: (id) => `${baseEndpoint}system/${id}/minor-factions`,
    systemPowersById: (id) => `${baseEndpoint}system/${id}/powers`,

    volcanism: `${baseEndpoint}volcanism`,
    volcanismById: (id) => `${baseEndpoint}volcanism/${id}`,

    // Backward compatibility alias.
    factionsGetAll: `${baseEndpoint}bgs/factions`,
};

export {endpoints};