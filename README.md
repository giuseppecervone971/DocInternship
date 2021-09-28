# Internship project

The following GitHub repository will be used to collect the whole documentation for my internship project. The aim of this project is to create an alternative to an expensive data diode using free, open source software and two Raspoberry Pi machines connected to each other via serial cable. Then using the diode we built, catch diagnostics data of the devices on the protected network using a Zabbix Server running on the Raspberry Pi sending the data. Having caught the data, we send it from a protected to an unprotected network without risk using the diode. The final part of the project is running a Zabbix server, on the Raspberry Pi machine on the unprotected network, where we inject the data so we can have a situation as close as the situation we have on the protected network.
The repository currently is structed in two main folders, one is the documentation folder built in Latex, where I am documenting a full guide on how to get the project running, and documenting my steps, and the other folder with the file transfer files. It is suggested that you read the documentation before looking at the program itself. 

### To do list for File Transfer:
- [x] Communication between two machines.
- [x] File Transmission.
- [x] Checksum to check for correct file transmission.
- [x] Increased file size.
- [x] Increased transmission speeds.
- [x] Stress test.
### Extras for File Transfer:
- [ ] Ease of use by allowing the program to be run for any filename.
- [ ] RTS/CTS implementation or using the filesize as a parameter for more secure transmission.
- [ ] Config file for parameters


### To do list for Zabbix:
- [X] Setup on both Raspberry Pi machines
- [X] Add to the public Zabbix server the hosts and items (as trappers).
- [X] Configure Zabbix dashboard for easy access to graphs.

### To do list for Documentation:
- [ ] Zabbix installation guide

