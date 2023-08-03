# CQSim GUI

The CQSim GUI is an interactive graphical user interface for CQSim, a simulation program. This GUI provides users with an alternative way to interact with CQSim instead of entering parameters through the terminal. Additionally, it offers the option to view real-time graph analysis while the simulation is running. The GUI allows users to select between graphing Utilization, Max Wait Time, or Average Wait Time of the simulation. It was implemented by Sean Dudo <seanpdudo@gmail.com> when Sean attended the NSF REU program at Illinois Tech in the summer of 2023.

## Running the GUI

To run the CQSim GUI, follow these steps:

1. Make sure you have Python 3 installed on your system.

2. Open a terminal or command prompt.

3. Navigate to the directory where the CQSim files are located.

4. Execute the following command to run the GUI:

```
python3 GUI_cqsim.py
```

## How to Use the GUI

Once you have launched the GUI, you will see a graphical interface with various options and controls.

### Simulation Parameters

The GUI provides input fields and options to set simulation parameters. You can enter these values directly into the provided fields.

### Real-Time Graph Analysis

The GUI allows you to select real-time graph analysis while the simulation is running. You can choose to view graphs for Utilization, Max Wait Time, or Average Wait Time. The graphs will update dynamically as the simulation progresses.

### Interaction with the Simulation

As the simulation is running, the graph pages 'back' button will be grey. When the simulation completes, it will turn blue again. However, if you hit back before the simulation is done, it will stop the simulation in the background as well.


### Additional Notes

- The GUI provides a more user-friendly way to interact with CQSim and visualize simulation results in real-time.

- The GUI_cqsim.py file should be located in the same directory as the CQSim program files to ensure proper execution.

- You can modify the code in GUI_cqsim.py to add more features or customize the user interface based on your requirements.

Enjoy using the CQSim GUI to simulate and analyze queuing systems efficiently! If you encounter any issues or have suggestions for improvement, feel free to contribute or contact the developers.
