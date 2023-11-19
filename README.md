# Octopus Intelligent Tesla Powerwall Integration
A python script to automate updating of time of use tarrif data to the Tesla cloud API for the Tesla Powerwall based on variable tariffs from Octopus Intelligent

After joining Octopus Intelligent the other day I couldn't find a way to update my Tesla Powerwall automatically to notify it of the change in the scheduled times when the charging tariffs are in effect.

It relies on two different projects:

io.py from https://github.com/liamjvs/intelligent-octopus-scheduler

cli.py from https://github.com/tdorssers/TeslaPy

These two need to be set up in the same folder the iotesla.py script. The only change needed to be made in the script is the email address at the top myemail = "my@email.com"

I've set these up in Home Assistant by copying all the files to a folder called python_scripts in the config folder making sure all the .json files are there.

Then running

```docker exec -it $(docker ps -f name=homeassistant -q) bash```

Within the Advanced SSH & Web Terminal by Frenck to get to the actual run environment on the shell to install the telsapy modules
(From my understanding the python modules will get wiped everytime the core is updated.)

```pip install teslapy```

Then I created an automation to run the update whenever changes are detected using the Octopus Intelligent integration: https://github.com/megakid/ha_octopus_intelligent

Plus a second trigger using the standard Octopus Energy Integration: https://github.com/BottlecapDave/HomeAssistant-OctopusEnergy/ (replacing the sensor with your actual sensor!)

```
alias: Call IO Tesla On Change
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.octopus_intelligent_next_offpeak_start
    for:
      hours: 0
      minutes: 0
      seconds: 0
  - platform: state
    entity_id:
      - sensor.octopus_energy_electricity_XXXXXX_XXXXXXX_current_rate
condition: []
action:
  - service: shell_command.iotesla
    data: {}
mode: single
```

Which calls the shell command added to the configuration.yaml
```
shell_command:
  iotesla: "cd python_scripts; python iotesla.py"
```
An example of a sucessfull POST to the API can be found here: https://www.reddit.com/r/TeslaSolar/comments/uijh6i/any_success_with_using_the_powerwall_time_of_use/   
