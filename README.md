# Automatisation d'un spectrophotomètre Varian 634 avec Python


Ce programme Python permet d'automatiser un ancien spectrophotomètre Varian 634 en utilisant différentes bibliothèques telles que serial, Phidget22, time, matplotlib, numpy, csv, pandas, re et scipy.signal. Il permet d'acquérir la tension de la photodiode à l'aide d'un Phidget, de piloter le réseau de diffration du spectrophotomètre avec un moteur, de configurer le spectrophotomètre en mode simple faisceau et de traiter le signal d'absorbance de la solution pour enlever le bruit de mesure.


python main.py --arg1 valeur1 --arg2 valeur2

$ cat image.txt
  _____  ____  _   _ _____ _____ _____ _   _  ____   ____   ____  
 |  __ \|  _ \| \ | | ____|_   _| ____| \ | |/ ___| / ___| / ___| 
 | |  | | |_) |  \| |  _|   | | |  _| |  \| | |  _  \___ \| |     
 | |__| |  __/| |\  | |___  | | | |___| |\  | |_| |  ___) | |___  
 |_____/|_|   |_| \_|_____| |_| |_____|_| \_|\____| |____/ \____|
