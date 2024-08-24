# EPICS GUI for TRIUMF

<img src="/img/triumf_bcit.png" alt="TRIUMF and BCIT" width="250"/>

## Table of Contents

- [Description](#description) - Why was this project created? Who is it for?
- [Features](#features) - What does this GUI offer?
- [Installation](#installation) - How to set up the GUI on your system.
- [Usage](#usage) - How to use the GUI after installation.
- [Contributors](#contributors) - Who contributed to this project?

## <a name="description"></a> Description

The EPICS GUI for TRIUMF project aims to build a cost-effective control system for tabletop experiments by leveraging a Raspberry Pi cluster running the Experimental Physics and Industrial Control System (EPICS). This project is designed to:

- **Create a Raspberry Pi Cluster Running EPICS**: Utilize a low-cost, scalable solution for controlling experiments.
- **Control Tabletop Experiments with ER-PCC**: Integrate with ER-PCC for streamlined experiment management.
- **Offer a Cost-Effective Alternative**: Provide a more affordable control system compared to existing solutions at TRIUMF.

## <a name="features"></a> Features

- **Raspberry Pi Integration**: Seamlessly integrates with Raspberry Pi clusters for versatile deployment options.
- **EPICS Compatibility**: Fully supports EPICS, ensuring compatibility with existing control systems and standards.
- **ER-PCC Support**: Includes support for ER-PCC, making it suitable for a range of experimental setups.
- **User-Friendly Interface**: Provides an intuitive GUI for easy control and monitoring of experiments.

## <a name="installation"></a> Installation

To install and set up the EPICS GUI for TRIUMF, follow these steps:

1. **Clone the Repository**: Download the project files from GitHub.
   ```bash
   git clone https://github.com/MattiasHenders/epics-gui-triumf.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd epics-gui-triumf
   ```

3. **Run the EPICS Server**: Execute the startup script to initialize the EPICS server.
   ```bash
   bash ./start_server.sh
   ```

4. **Configuration**: Review the configuration files in the `config` directory to ensure proper setup for your environment.

## <a name="usage"></a> Usage

Once installed, you can use the EPICS GUI to control and monitor your experiments. The main features include:

- **Experiment Control**: Use the GUI to start, stop, and manage experiments.
- **Data Monitoring**: View real-time data and logs from your experiments.
- **Configuration Management**: Adjust settings and configurations through the user-friendly interface.

For detailed usage instructions, refer to the [Documentation](#documentation) or consult the `docs` directory within the project.

## <a name="contributors"></a> Contributors

This project was made possible by the contributions of many developers. You can view the list of contributors on GitHub:

<a href="https://github.com/MattiasHenders/epics-gui-triumf/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MattiasHenders/epics-gui-triumf" />
</a>

## <a name="documentation"></a> Documentation

For more information, including detailed installation and usage instructions, visit the [Documentation](#documentation) section in the `docs` directory.

---

Thank you for your interest in the EPICS GUI for TRIUMF project! If you have any questions or need further assistance, please feel free to reach out.
