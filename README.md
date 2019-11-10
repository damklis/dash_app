# GameMetrics DASHBOARD
![Screencast-from-10 11 2019-12_12_37](https://user-images.githubusercontent.com/43547278/68543152-b0e44280-03b3-11ea-9eb0-5f7adc00f70e.gif)

GameMetrics Dashboard is a web application build with Python Dash library.
It is a user-friendly UI showing statistics about your application (in my case FreeToPlay mobile game).

The dashboard consists of 5 different Tabs:

- TAB "FUNNEL" - shows steps, that player takes during onboarding (each click is an analytical event)
- TAB "WIN-RATIO" - created for Level Designer, shows the table with stats about games on a specific level.  
We can use that to balance the in-game economy.    
- TAB "DROP-RATE" - shows a table with information on how many users churned during achieving new levels.
- TAB "SESSIONS" - informs us about global sessions length in application
- TAB "ECONOMY" - created for Game Designer, shows how much resource player has on a given level.

You can compare the last versions of your application simply by selecting one of the radio-items in the top left corner.
Dashboard works on top of data extracted from the HIVE and then converted to pickles - serialized Python objects.

# Data Flow
Image presentation of data flow in the application.
![dataflow](https://user-images.githubusercontent.com/43547278/68486629-c76a8c80-0241-11ea-882d-a031cab24703.png)



# Running App locally
Before running the container with app we first need to build it so it becomes available in our local docker repository. Run the following command from project's root directory.

```
docker build -t <image_name>:<image_version> .
```

After application is build succesfully, image can by started with following command:
```
docker run -p 80:80 --rm -v <project_root_folder>:/app  <docker_image_name>:<image_version>
```

Information about command options:
- `--rm` removes the container after stopping it. There is always a fresh version of configuration and other features while running the app.
- `-v` In the case of bind mounts, the first field is the path to the file or directory on the host machine.
The second field is the path where the file or directory is mounted in the container.
- `-p` maps a port from container to localhost
