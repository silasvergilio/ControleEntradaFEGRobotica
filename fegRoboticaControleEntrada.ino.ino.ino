#include <SPI.h> //Adiciona a biblioteca para comunicação SPI com o Arduino
#include <MFRC522.h> //Biblioteca para interpretar leitura do leitor de RFID
#include <SoftwareSerial.h> //Biblioteca para uso da serial por software para o bluetooth

SoftwareSerial HC05(10,6); //Cria objeto da serial por software para o bluetooth

 //Define pinos para o leitor de RFID
#define SS_PIN 53
#define RST_PIN 9
#define relePin 2
//Constroi objeto do leitor de RFID
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.
char charLido;
 
//Função que é executada uma vez
void setup() 
{
  //Inicializa a comunicação bluetooth com 9600 bps
  HC05.begin(9600);
  SPI.begin(); // Inicia  SPI bus
  mfrc522.PCD_Init(); // Inicia MFRC522
  Serial.begin(9600); //Inicia comunicação serial (com computador)
  pinMode(relePin,OUTPUT); //Declara o pino do rolê como saída
  
}
 
void loop() 
{

  //Garante que o rele irá estar fechado a todo momento, a não ser que um cartão apareça
  digitalWrite(relePin,HIGH);
  

  
  //Verifica se um cartão foi apresentado
  
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }

  //Inicializa string com a UID do cartão
  String conteudo= "";

  //Cria a string do conteudo do cartão
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {   
     conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
   //Normaliza todos os chars
   conteudo.toUpperCase();
   //Manda por bluetooth a substring com a ID do cartão

  
   HC05.print(conteudo.substring(1));

   //Imprime na serial o codigo do cartão
  // Serial.println(conteudo.substring(1));

  
   while(HC05.read() != 'a')
   {
   }

   digitalWrite(relePin,LOW);
   delay(1000);
   digitalWrite(relePin,HIGH);
    
}

