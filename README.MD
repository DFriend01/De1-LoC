# The De1-LoC by Haddware (Team L2A-06)

For our CPEN 391 Project we implemented a smart lock with a multitude of customizable unlock options, including pinpad entry and FaceID. The lock also support notification of anomalous unlocks. The project was comrpised of 3 main parts: [the backend](backend/BACKEND.md), [the user app](UserApp/APP.MD), and [the embedded system](). 

Management of unlock methods is initiated through the user app, with most information being stored in the backend. The hardware was integrated to make API requests to the backend when prompted by a user triggered interrupt. Full documentation of the systems are provided at the link above, including instructions on how to set up the system for yourself. 

# Contributions
Members of our group contributed as follows:
## Aswin
- Performed paired programming with Harshil for the embedded system (files in `embedded_system/`)
    - Hardware: Pinpad reader, pinpad avalon interface, servo motor controller, 
    servo motor avalon interface, RFS daughtercard connection
    - Embedded software: Coordinates the servo and pinpad from the Nios2 processor, 
    with the backend using wifi. Original code mainly in [main.c](embedded_system/software/embedded_software/main.c), 
    [requests.h](embedded_system/software/embedded_software/requests.h).
- Individual debugging and validation of servo motor controller

## Declan
- Sole Frontend Developer, contributed all files within `UserApp/`
- Machine Learning Development, authored code in `outlier-detection/` and the KNN and RandomForest models.
- Worked with Devon on facial recognition pipeline

## Devon
- Backend Developer, implemented code in `backend/` unless otherwise specified.
- Worked with Declan on facial recogntion pipeline
- Validated Hyperparameters for ML models and augmented data

## Harshil
- Performed paired programming with Aswin for the embedded system (files in `embedded_system/`)
    - Hardware: Pinpad reader, pinpad avalon interface, servo motor controller, 
    servo motor avalon interface, RFS daughtercard connection
    - Embedded software: Coordinates the servo and pinpad from the Nios2 processor, 
    with the backend using wifi. Original code mainly in [main.c](embedded_system/software/embedded_software/main.c), 
    [requests.h](embedded_system/software/embedded_software/requests.h).