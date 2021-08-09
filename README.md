# GVE_DevNet_RoomOS_Endpoints_Control
Sample prototype of a web application to control RoomOS Endpoints using xAPI commands


## Contacts
* Gerardo Chaves (gchaves@cisco.com)
* Rami Alfadel (ralfadel@cisco.com)

## Solution Components
* Cisco TelePresence endpoints
* [Cisco TelePresence end-point xAPIs](https://roomos.cisco.com/xapi/)
* Python
  - Python Module:
    - [Flask](https://flask.palletsprojects.com/)

## Solution Overview
This prototype is showing a sample way to control Cisco Collaboration Endpoints from a web dashboard, with simple functions matching what's provided in a touch-10 device.


## Installation/Configuration

### Getting Started   
 1. Choose a folder, then create a virtual environment:  
   ```python3 -m venv <name of environment>```

 2. Activate the created virtual environment:  
   ```source <name of environment>/Scripts/activate```

 3. Access the created virtual environment:  
   ```cd <name of environment>```

 4. Clone this Github repository into the virtual environment folder:  
   ```git clone [add github link here]```
   - For Github link: 
        In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
        ![/IMAGES/giturl.png](/IMAGES/giturl.png)

 5. Access the folder **GVE_DevNet_RoomOS_Endpoints_Control**:  
   ```cd GVE_DevNet_RoomOS_Endpoints_Control```

 6. Install the solution requirements:  
   ```pip3 install -r requirements.txt```

 7. Initiate the Flask application settings:  
   ```export FLASK_APP=app.py```  
   ```export FLASK_ENV=development```

 8. Start the Flask application:  
   ```flask run```

 9. Open the hosted web page in your browser:  
    (Default: [localhost:5000](localhost:5000))


## Usage
- As you open the main page, you will be asked to login with the device IP address and credintials:
    ![/IMAGES/login.png](/IMAGES/login.png)

- If the login is successful, the index page will show up:
    ![/IMAGES/index.png](/IMAGES/index.png)
    - Displaying the following buttons/options:

        - **Move Camera**:  
        ![/IMAGES/move_camera.png](/IMAGES/move_camera.png)  
        Which will invoke the xAPI call: ([Camera PositionSet](https://roomos.cisco.com/xapi/Command.Camera.PositionSet/)) and change the position of the selected camera.  
        

        - **Enable USB Mode**:  
        ![/IMAGES/usb_mode.png](/IMAGES/usb_mode.png)  
        Which will trigger USB-passthrough mode if it's avaialble on the device.  
        More details:  https://gblogs.cisco.com/ch-tech/usb-passthrough-mode-on-video-endpoints/


        - **Make a Call**:  
        ![/IMAGES/make_call.png](/IMAGES/make_call.png)  
        Which will dial a number/URI using the xAPI call: ([Dial](https://roomos.cisco.com/xapi/Command.Dial))  
        

        - **Volume Control**:  
        ![/IMAGES/volume_control.png](/IMAGES/volume_control.png)  
        Which will control the volume level of the device using using the xAPI call: ([Audio Volume Set](https://roomos.cisco.com/xapi/Command.Audio.Volume.Set/)) and provide the ability to mute/umute the mic using using the xAPI calls: ([Audio Microphones Mute](https://roomos.cisco.com/xapi/Command.Audio.Microphones.Mute/) & [Audio Microphones Unmute](https://roomos.cisco.com/xapi/Command.Audio.Microphones.Unmute/))  

        - **Change Theme**:  
        ![/IMAGES/change_theme.png](/IMAGES/change_theme.png)  
        Which will change the backgroundImage of the panel containing the buttons just in the HTML view itself. The view of the second theme:  
        ![/IMAGES/index_2.png](/IMAGES/index_2.png)  
        


## Notes

- The xAPI calls genereated from the python flask application are following the websocket methodolegy explained here: [xAPI over WebSocket](https://community.cisco.com/t5/collaboration-voice-and-video/xapi-over-websocket-xows-ce9-7-x/ba-p/3831553) 



### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.