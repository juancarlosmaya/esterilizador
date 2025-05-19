
// LIBRERIAS WIFI
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiMulti.h>
WiFiMulti WiFiMulti;                            // objeto conexion wifi
HTTPClient client;                              // cliente http
const uint16_t port = 80;                       // servidor y puerto a donde se va a conectar el dispositivo
const char server[]= "http://esterilizacionremota.pythonanywhere.com/APIusuario/2/";
DynamicJsonDocument doc(100000);                 // objeto json para almacenar información recibida y enviada a servidor      
TaskHandle_t manejadorTareaServidor= NULL;      // manejador de tarea envío datos a servidor

int led = 2;

// VARIABLES A ENVIAR AL SRVIDOR
float frecuenciaCardiaca=34;
float SENAL[257]={15.15, 2, 3.35, 2.8, 2.15, 2, 1.2, 1.5, 1.55, 1.5, 1.45, 0.95, 1.35, 1.55, 1.3, 1.55, 1.1, 1.85, 1.9, 3.25, 2.45, 1.65, 6.95, 1.15, 1.5, 0.8, 1.35, 1.65, 3, 3.5, 4.1, 3.9, 3.3, 2.15, 2.7, 2.15, 1.7, 1.1, 0.45, 0.95, 1, 0.6, 0.7, 1.1, 0.95, 1.1, 0.65, 1.35, 2.25, 1.1, 1, 6.35, 0.1, 0.75, 1.05, 1.85, 2.75, 3, 3.75, 3.45, 3.85, 3.3, 3.6, 3.5, 2.55, 2.7, 2.55, 2.95, 2.6, 2.45, 2.55, 2.5, 2.6, 2.2, 3, 3.55, 3.55, 1.75, 3.25, 5.45, 1.45, 1.65, 2.1, 2.15, 3, 4.35, 3.9, 3.5, 2.9, 1.95, 2.25, 1.95, 1.1, 0.9, 0.85, 0.75, 1.15, 1.45, 1.25, 1.25, 1.05, 1.15, 1.25, 1.15, 0.7, 2.1, 0.95, 0.75, 5.8, 0.3, 0.3, 0.25, 0.9, 1.3, 2.25, 3, 3.4, 3.85, 2.35, 2.2, 2.2, 2.05, 1.35, 0.6, 0.8, 0.65, 1.2, 0.85, 1.05, 1.4, 0.85, 1.1, 1.9, 2.75, 0.1, 0.95, 7.4, -1.25, 0.75, 0.95, 1.1, 1.65, 3, 2.9, 3.2, 2.9, 1.7, 2.1, 1.55, 0.8, -0.3, 0.7, 0.15, -0.05, 0.4, 0.5, 0.65, 0.05, 0.9, 0, 0.15, 0.4, 1.1, 1.15, -0.65, 2.05, 1.85, -0.75, -0.75, 0.45, 0.4, 1.5, 2.25, 1.95, 3.05, 1.3, 1.75, 1.55, 1, 0.6, 0.1, 0.05, -0.2, 0.35, 0.25, 0.35, -0.15, 0, 0.4, 0.95, 0.8, -0.2, -0.3, 6.85, -1.85, -0.35, -0.4, 0.25, 0.8, 1.45, 1.45, 2.25, 1.4, 0.9, 0.5, 0.65, -0.15, -0.45, -0.85, -0.95, -1.2, -1.2, -0.95, -1, -1.95, -1.5, -1.9, -1.1, -1.35, -1.2, -2.65, -0.3, 0.6, -3.5, -2.75, -3, -2.2, -1.75, -0.3, -1, 0.1, -1.3, -1.8, -1.75, -2.55, -3, -3.3, -3.5, -3.45, -3.6, -3.45, -3.65, -3.75, -4.05, -3.6, -5.05, -4.3, -3.1, -3.2, -3.55, -2, -1, 1, 2, 3, 4,0};







void setup() {

    Serial.begin(115200);
    pinMode(led, OUTPUT);
    
    // CONEXIÓN WIFI
    WiFiMulti.addAP("juanc", "jc7303733"); // poner aquí clave y contraseña wifi
    Serial.print("Esperano conexión WIFI");
    while(WiFiMulti.run() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("");
    Serial.println("WiFi conectado");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    // CONEXIÓN CON SERVIDOR  
    Serial.print("Conectando a: ");
    Serial.println(server);
    if (!client.begin(server)) {
        Serial.println("Connection failed.");
        while (1){}
    }
/*
    // CONFIGURACIÓN DE TAREA ENVÍO DE DATOS A INTERNET
    xTaskCreatePinnedToCore(
        envioDatosServidor,             // nombre de la funcion
        "envio datos servidor",         // nombre de funcion para depuración
        10000,                          // tamaño de stack (bytes)
        NULL,                           // parametros pasados
        1,                              // prioridad de la tarea
        &manejadorTareaServidor,        // manejador de esta tarea
        1                              // nucleo en le que se ejecuta esta tarea
    );
*/
}
int k=0;

void loop() {

 int httpCode=client.GET();
    if (httpCode > 0) {
        // --------- LEER DATOS DE BASE DE DATOS
        // Get the request response payload
        String payload = client.getString(); 
        //Serial.println(payload);          
        DeserializationError error= deserializeJson(doc, payload); // deserializa y revisa errores
        if (error) {
            Serial.print(F("deserializeJson() failed with code "));
            Serial.println(error.c_str());
        }
        
        //int frecuencia_cardiaca = doc["frecuenciaCardiaca"].as<int>();
        //Serial.print("la frecuencia cardíaca es");
        //Serial.println(frecuencia_cardiaca);
        

        // -------- SOBREESCRIBIR DATOS EN BASE DE DATOS
        
        client.addHeader("Content-Type", "application/json");
        
        for (int j=0;j<257;j++){doc["pletismografia"]["senal"][j]=int(SENAL[j]);}
        doc["frecuenciaCardiaca"] = int(SENAL[k]);
        k++;
        if (k==255){
          k=0;
        }

        String message = "";
        serializeJson(doc, message);
        Serial.print(message);
        httpCode = client.PUT(message);
        Serial.println(httpCode);
    }  
    //Serial.print("El tiempo transcurrido es:");
    //Serial.print(micros()-tiempo);


}
