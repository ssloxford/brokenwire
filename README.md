<p align="center"><img src="https://github.com/ssloxford/brokenwire/blob/main/data/brokenwire_logo.png" width="30%"></p>

# Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging

This repository contains the evaluation source code used in our NDSS paper [**Brokenwire: Wireless Disruption of CCS Electric Vehicle Charging**](https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_s251_paper.pdf).

Brokenwire is a novel attack against the **Combined Charging System (CCS)**, one of the most widely used DC rapid charging technologies for electric vehicles (EVs). 
The attack interrupts necessary control communication between the vehicle and charger, **causing charging sessions to abort**.
The attack can be conducted wirelessly from a distance using electromagnetic interference, allowing individual vehicles or entire fleets to be disrupted simultaneously. 
In addition, the attack can be mounted with off-the-shelf radio hardware and minimal technical knowledge. 
With a power budget of 1 W, the attack is successful from around **47 m** distance. 
The **exploited CSMA/CA behavior** is a required part of the HomePlug GreenPHY, DIN 70121 & ISO 15118 standards and all known implementations exhibit it.

Brokenwire has immediate implications for many of the **12 million** battery EVs estimated to be on the roads worldwide — and profound effects on the new wave of electrification for vehicle fleets, both for private enterprise and for crucial public 
services. 
In addition to electric cars, Brokenwire affects **electric ships, airplanes and heavy duty vehicles**. 
As such, we conducted a disclosure to industry and discuss in our paper a range of mitigation techniques that could be deployed to limit the impact.

You can also learn more about Brokenwire on our [**website**](https://brokenwire.fail).

## Structure of the Repository
This repository is organized as follows:

```
.                                         # root directory of the repository
├── code                                  # contains the evaluation source code
│   ├── lab_evaluation                    # files used for the lab evaluation
│   │   └── collect_data.py               # Python script used to evaluate Brokenwire in a controlled lab setting
│   ├── lib                               # various Python classes required for the evaluation
│   │   │── EvaluationUtils.py            # library that helps running the lab evaluation
│   │   └── IPerfEvaluation.py            # Python class used for the lab evaluation
│   ├── req                               # text file that contains all the Python requirements
│   └── scripts                           # directory that contains additional evaluation scripts
│       └── preamble_emission.py          # Python script that emits the preamble with a LimeSDR
│       └── preamble_emission.py          # Python script that emits the preamble with a OsmoSDR devices such as (USRP, BladeRF, AntSDR E200 with UHD, etc.). USRP X or N versions with a DC-30 MHz daughter board would fit well, others will need a downconverter
├── data                                  # directory that contains required files
│   └── preambles                         # directory that contains the preamble
│       └── captured_preamble.dat         # captured preamble used for the attack
├── docker-compose.yml                    # configuration file of the Docker container
├── Dockerfile                            # build instructions for the Docker container
└── README.md                             # this README file
```

## Running the Docker Container
This repository contains all configuration and source code files necessary to run the Brokenwire attack.
To ensure a quick and easy deployment, we provide a Dockerfile to build a container with all the required dependencies.
<br>**Please note**, to immediately get started with this repository, you will need `docker`, `docker-compose` and a LimeSDR.

The following steps outline how to build and run the Docker container and execute the Brokenwire attack:

 * `git clone https://github.com/ssloxford/brokenwire.git`
 * `cd brokenwire/`
 * `docker-compose build`
 * `docker-compose up -d`

Once the container is up and running, you can attach to it

`docker attach brokenwire`

and run the following command to start the attack:

`python3 /home/code/scripts/preamble_emission.py  --lime-sdr-gain LIMESDR_GAIN`

where LIMESDR_GAIN is a value between -12 and 64.


## Using other SDR devices

Initially the source was made for the LimeSDR, but an alternative using OsmoSDR block can also be used for USRP X/N version with a DC-30 MHz daughter, or a downconverter for other devices that wouldn't tune to 17 MHz frequencies:

```
python3 preamble_emission_osmosdr.py --help
usage: preamble_emission_osmosdr.py [-h] [--devicestring DEVICESTRING] [--inputfile INPUTFILE] [--txgain TXGAIN] [--var-freq VAR_FREQ]

optional arguments:
  -h, --help            show this help message and exit
  --devicestring DEVICESTRING
                        Set deviceargs [default='']
  --inputfile INPUTFILE
                        Set preamblefile [default='captured_preamble.dat']
  --txgain TXGAIN       Set txgain [default=10]
  --var-freq VAR_FREQ   Set frequency [default=17000000]
```


## Recommended Equipment

To run the Brokenwire attack, a software-defined radio that can transmit at a center frequency of 17 MHz with a sample rate >= 25MSPS is required. 
While any SDR with the these properties should work, our source code is tailored to the use of a LimeSDR.
Since Brokenwire is a very effective attack and does not require a high transmission power, testing the attack should not require any additional amplification.

## Contributors
 * [Sebastian Köhler](https://cs.ox.ac.uk/people/sebastian.kohler)
 * [Richard Baker](https://www.cs.ox.ac.uk/people/richard.baker)
 * [Martin Strohmeier](https://www.cs.ox.ac.uk/people/martin.strohmeier)
