#define buzzer 9 //connect Buzzer to digital pin9
int buttonState = 0;
bool open = false;
int x = 0;

void setup() {                
 // initialize the digital pin9 as an output.
  pinMode(buzzer, OUTPUT);
  pinMode(4, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(12, OUTPUT);
  pinMode(13,OUTPUT);
  //inicia comunicacion serial
  Serial.begin(9600);
  Serial.setTimeout(5);
  digitalWrite(13, LOW);
  digitalWrite(12, LOW);
  digitalWrite(buzzer, LOW);
}

void loop() {
    //El torniquete tiene 2 estados fisicos: Abierto y Cerrado.
    //Las señales que puede recibir se resumen en Nada (x=0), Aprobado (x=1) y Denegado (x=2).
    //El sonido del buzzer no cuenta como desbloqueo/bloqueo.
    //Por defecto, está en Cerrado.
    //El boton sirve para detectar si una persona ha entrado/pasado por el torniquete.
    //Sólo el botón detector puede cambiar el torniquete de Abierto a Cerrado.
    //Sólo la señal de Aprobado puede cambiar el torniquete de Cerrado a Abierto.
    //Si recibe la señal de Denegado estando en estado Cerrado, no hará nada físico. Sólo reproducir el sonido de denegado.
    //Si recibe la señal de Aprobado estando en estado Cerrado, abrirá, cambiará a estado Abierto y reproducirá el sonido de aprobado.
    //Si recibe la señal de Aprobado estando en estado Abierto, se mantendrá abierto y no hará nada físico. Ni siquiera reproducir sonido.
    //Si recibe la señal de Denegado estando en estado Abierto, se mantendrá abierto y no hará nada físico. Ni siquiera reproducir sonido.
    //Si está en estado Abierto y detecta el botón, cerrará y cambiará a estado Cerrado. No podrá cambiar del estado Cerrado durante 3 segundos, ni reproducirá sonido.
    //Si está en estado Cerrado y detecta el botón, emitirá una alarma de emergencia durante un minuto, porque eso no debería ser posible.
    while (Serial.available()){
      x = Serial.readString().toInt();
      buttonState = digitalRead(7);
      if (!open){
        if (x == 2){
          denegado();
          delay(50);
          x = 0;
        }
        else if (x == 1){
          permitido();
          delay(50);
          open = abrir();
          delay(50);
          x = 0;
        }
      }
      if (buttonState == LOW){
        break;
      }
    }
    buttonState = digitalRead(7);
    if (buttonState == LOW){
      digitalWrite(buzzer,HIGH);
      delay(10);
      digitalWrite(buzzer,LOW);
      if (open){
        delay(5);
          if (buttonState == LOW) {
            open = cerrar();
            digitalWrite(buzzer,HIGH);
            delay(10);
            digitalWrite(buzzer,LOW);
            delay(2990);
          }
      }
      else {
        while (true){
          buttonState = digitalRead(4);
          emergencia();
          if (buttonState == LOW){
            digitalWrite(buzzer,LOW);
            break;
          }
        }
      }  
    }
    x = 0;
    delay(5);          
}

bool abrir(){
  digitalWrite(13, HIGH);
  digitalWrite(12, LOW);
  delay(300);
  digitalWrite(13, LOW);
  return true;
}

bool cerrar(){
  digitalWrite(13, LOW);
  digitalWrite(12, HIGH);
  delay(500);
  digitalWrite(12, LOW);
  return false;
}

void denegado(){
  digitalWrite(buzzer,HIGH);
  delay(1000);
  digitalWrite(buzzer,LOW);
}

void permitido(){
  digitalWrite(buzzer,HIGH);
  delay(100);
  digitalWrite(buzzer,LOW);
  delay(100);
  digitalWrite(buzzer,HIGH);
  delay(100);
  digitalWrite(buzzer,LOW);
  delay(100);
  digitalWrite(buzzer,HIGH);
  delay(500);
  digitalWrite(buzzer,LOW);
}

void emergencia(){
    digitalWrite(buzzer,HIGH);
    delay(350);
    digitalWrite(buzzer,LOW);
    delay(150);
}

