
typedef struct{
    // GGA - Global Positioning System Fixed Data
    float nmea_longitude;
    float nmea_latitude;
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
    float mc_10p0;
    float nc_2p5;
    float nc_10p0;
    uint16_t SO_ppm;
};
typedef struct DATA
{
	struct sps30_measurement PM_Data;
	CO_t CO_Data;
	GPS_t GPS_Data;
} CollatedData;


