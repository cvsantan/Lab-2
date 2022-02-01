# Step Response Plots!

This file contains the results from the step respoinse tests conducted on our motor. We utilized a proportional closed loop controller to get the motor to stop afetr exactly one revolution. Three different proportional gain values were tested (0.835, 4, 2.35). Althogh all of the gain values provided a highly accurate staedy state value, we found that a value of 0.835 proveided the quickest response with no overshoot. In an ideal system this would be the preferred value, however if any sort of disturbance was introduced into the system, using one of the higher gain values could provide some needed correction.

![This graph contains step responses](https://github.com/cvsantan/Lab-2/blob/main/KP_0.835.png)
