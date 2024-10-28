import os
from datetime import datetime

class FileSaver:
    def __init__(self, directory: str):
        self.directory = directory
        # self.create_directory()

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print(f"")
        else:
            print(f"directory '{self.directory}' already exist")


    def _save_file(self, namefile: str, extension: str, content: str):
        self.create_directory()
        date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{namefile}_{date_time}.{extension}"
        filepath = os.path.join(self.directory, filename)

        with open(filepath, "w") as file:
            file.write(content)
        
        print(f"File saved as {filepath}")

    def save_grib(self, namefile: str, content: str):
        self._save_file(namefile, "grib", content)

    def save_hdf5(self, namefile: str, content: str):
        self._save_file(namefile, "hdf5", content)

    def save_bufr(self, namefile: str, content: str):
        self._save_file(namefile, "bufr", content)

    def save_tmds(self, namefile: str, content: str):
        self._save_file(namefile, "tmds", content)


saver = FileSaver("C:\Docs")

# saver.save_grib("weather_data", "This is GRIB file content.")
# saver.save_hdf5("climate_data", "This is HDF5 file content.")
# saver.save_bufr("forecast_data", "This is BUFR file content.")
# saver.save_tmds("sensor_data", "This is TMDS file content.")
