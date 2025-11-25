#import qcm_data_collection
import time
import RPi.GPIO as GPIO 

class control:
    PUMP_GPIO=1
    PUMP_DIRECTION_GPIO=2
    BUTTON_GPIO=12

    __FREQUENCY_SAMPLE_SIZE=25
    __SECONDS_BETWEEN_SAMPLES=2

    __CLEANING_TIME_SECONDS=10
    
    def is_button_pressed(self): 
        is_pressed=GPIO.input(self.BUTTON_GPIO)
        #probably need to add debouncing here
        return is_pressed
    
    def __start_pump(self):
        raise NotImplementedError()
    
    def __stop_pump(self):
        raise NotImplementedError()
    
    def measure_frequency(self):
        self.__start_pump()

        sample_sums=0
        for _ in len(range(self.__FREQUENCY_SAMPLE_SIZE)):
            sample_sums+=qcm.get_qcm_frequency()
            time.sleep(self.__SECONDS_BETWEEN_SAMPLES)

        self.__stop_pump()

    def clean(self):
        self.__start_pump()
        time.sleep(self.__CLEANING_TIME_SECONDS)
        self.__stop_pump()

    def configure_components(self):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.PUMP_GPIO, GPIO.OUT)
        GPIO.setup(self.PUMP_DIRECTION_GPIO, GPIO.OUT)

        GPIO.setup(self.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class qcm:
    def get_qcm_frequency():
        raise NotImplementedError()