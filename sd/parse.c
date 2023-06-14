
// C program to read particular bytes
// from the existing file
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <dirent.h>
#include "../common/convert.h"
void writeCollatedData(FILE* file, const CollatedDataSD* data) {
    
    // Write GPS data
    fprintf(file, "%f,%f,%f,%d,", data->GPS_Data.nmea_longitude, data->GPS_Data.nmea_latitude, data->GPS_Data.utc_time, data->GPS_Data.date);

    // Write CO data
    fprintf(file, "%f,%d,%f,%f,", data->CO_Data.co2_ppm, data->PM_Data.SO_ppm, data->CO_Data.temperature, data->CO_Data.relative_humidity);

    // Write PM data
    fprintf(file, "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n", data->PM_Data.mc_1p0, data->PM_Data.mc_2p5, data->PM_Data.mc_4p0, data->PM_Data.mc_10p0, data->PM_Data.nc_0p5, data->PM_Data.nc_1p0, data->PM_Data.nc_2p5, data->PM_Data.nc_4p0, data->PM_Data.nc_10p0, data->PM_Data.typical_particle_size);
}

int main(int argc, char* argv[])
{
	CollatedDataSD collatedData;
	// Pointer to the file to be
	// read from
	DIR* d;
	struct dirent *dir;
	FILE* fileptr;
	long filelen;
	char buffer[sizeof(collatedData)];

	d = opendir(".");
	if (d) 
	{
		while ((dir = readdir(d)) != NULL)
		{
			/* On linux/Unix we don't want current and parent directories
         		* If you're on Windows machine remove this two lines
         		*/
			if (!strcmp (dir->d_name, "."))
			    continue;
			if (!strcmp (dir->d_name, ".."))    
			    continue;
			if(!strcmp (dir->d_name, "a.exe"))
			    continue;
			fileptr = fopen(dir->d_name, "rb");
			if (fileptr != NULL)
			{
				// Get the filename
				char* filename = dir->d_name;

				// Rename the file extension to ".csv"
				char* extension = strrchr(filename, '.');
				if (extension != NULL) {
				    strcpy(extension, ".csv");
				} else {
				    strcat(filename, ".csv");
				}

				fseek(fileptr, 0, SEEK_END);          // Jump to the end of the file
				filelen = ftell(fileptr);             // Get the current byte offset in the file
				rewind(fileptr);                      // Jump back to the beginning of the file
	

				// Write column names
            			FILE* dataFile = fopen(filename, "w");
				fprintf(dataFile, "Longitude E,Latitude N,UTC Time,Date,CO2 ppm,SO2 ppm,Temperature °,Relative Humidity,MC1.0 #/cm^3,MC2.5 #/cm^3,MC4.0 #/cm^3,MC10.0 #/cm^3,NC0.5 #/cm^3,NC1.0 #/cm^3,NC2.5 #/cm^3,NC4.0 #/cm^3,NC10.0 #/cm^3,Typical Particle Size\n");

 				while (fread(buffer, sizeof(char), sizeof(collatedData), fileptr) == sizeof(collatedData)) {
                    			memcpy(&collatedData, buffer, sizeof(collatedData));
                   			writeCollatedData(dataFile, &collatedData);
              			}
				fclose(fileptr);
				fclose(dataFile);
			}
		}
	}
}
