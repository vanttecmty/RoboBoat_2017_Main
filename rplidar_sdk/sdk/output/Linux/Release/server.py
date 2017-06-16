import socket  
  
s = socket.socket()   
s.bind(("localhost", 8893))  
s.listen(1)  
  
sc, addr = s.accept()  
  
while True:
    message = sc.recv(2000)  
    
    if message == "quit":  
        break        

    strMeasures = message.decode('utf-8');
    arrMeasures = strMeasures.split(";");
    #print(arrMeasures);

print("adios");  
sc.close();  
s.close();