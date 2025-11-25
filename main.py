#This code segment is here to simulate th RPi.GPIO library
import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

import display
import embedded
import keyboard
import time


class __main:

    __buffer_measurement=None
    __sample_measurement=None
    __result=False

    __MEASUREMENT_TOLERANCE=1000

    embedded_interaction=embedded.control()
    
    def run(self):

        self.embedded_interaction.configure_components()

        is_running=True
        stages=[self.start, self.measure_buffer, self.measure_sample, self.clean]
        current_stage=1

        stages[0]()

        while(is_running):
            #if(keyboard.is_pressed('k')):
            if(self.embedded_interaction.is_button_pressed()):
                time.sleep(2) #This is just the keypress debouncing, i think for the button it should be handeled in embedded class
                stages[current_stage]() #Runs the stored function
                current_stage=(current_stage+1)%len(stages)
            
        
    def start(slef):
        print("Please input the buffer solution, then press the button")
        display.display.display_buffer_next()

    def measure_buffer(self):
        print("Measuring buffer solution, insert sample next, then press the button")
        display.display.display_graph()

        self.__buffer_measurement=self.embedded_interaction.measure_frequency()

        display.display.display_sample_next()

        

    def measure_sample(self):
        print ("Measuring sample solution, insert cleaning next, then press the button")
        display.display.display_graph()

        self.__sample_measurement=self.embedded_interaction.measure_frequency()
        self.__result=not(self.__buffer_measurement-self.__MEASUREMENT_TOLERANCE<self.__sample_measurement 
                          and self.__sample_measurement<self.__buffer_measurement+self.__MEASUREMENT_TOLERANCE)
        display.display.display_cleaning_next()


    def clean(self):
        print("Cleaning the device, perepare next sampe")
        display.display.display_cleaning()
        self.embedded_interaction.clean()
        display.display.display_result(self.__result)

    
application_instance=__main()
application_instance.run()