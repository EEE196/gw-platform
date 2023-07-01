struct sps30_measurement_SD {
    float mc_1p0;
    float mc_2p5;
    float mc_4p0;
    float mc_10p0;
    float nc_0p5;
    float nc_1p0;
    float nc_2p5;
    float nc_4p0;
    float nc_10p0;
    float typical_particle_size;
    uint16_t SO_ppm;
};
typedef struct{
    // GGA - Global Positioning System Fixed Data
    float dec_longitude;
    float dec_latitude;
    float altitude;
    float utc_time;
    // RMC - Recommended Minimmum Specific GNS Data
    uint32_t date;
} GPS_t;
typedef struct {
		float co2_ppm;
		float temperature;
		float relative_humidity;
	} CO_t;
struct sps30_measurement {
    float mc_2p5;
    float nc_2p5;
    uint16_t SO_ppm;
};
typedef struct DATA
{
	struct sps30_measurement PM_Data;
	CO_t CO_Data;
	GPS_t GPS_Data;
} CollatedData;

typedef struct DATASD
{
	struct sps30_measurement_SD PM_Data;
	CO_t CO_Data;
	GPS_t GPS_Data;
} CollatedDataSD;


