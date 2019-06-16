
export py4j=/usr/local/share/py4j/py4j0.10.8.1.jar
export jssc=./ECoGLink/Devices/Nexus/jssc.jar
export nexus=./ECoGLink/Devices/Nexus/nexus.jar

javac -d ./ECoGLink/Devices/Nexus -cp "${py4j}:${jssc}:${nexus}" ./java/NexusEntryPoint.java 
