#include <EEPROM.h>
#include <Adafruit_LiquidCrystal.h>
#include <Wire.h>

#define SENSORPIN 10
#define RELAYPIN 12
#define DATASPEED 19200
#define DATASIZE 3
#define INARRAYSIZE 2
#define OUTARRAYSIZE 2

const byte inArray[INARRAYSIZE + 1] = {10, 11};
const byte outArray[OUTARRAYSIZE + 1] = {7, 8};
const byte ledpin = 13;

int dataArray[DATASIZE + 1] = {200, 200, 200};
byte step = 0;
byte run = 0;
byte ledStatus = 0;

Adafruit_LiquidCrystal lcd(0);

// Time control
unsigned long lastRead = 0;

// Serial comms
boolean newData = false;
const byte numChars = 32;
char receivedChars[numChars];
String apple = "";
byte initial = 1;
byte errorLevel = 0;

unsigned int cVar = 100;          //Variable counting to
unsigned int countInterval = 0; //Current count

void setup()
{
    Serial.begin(DATASPEED);
    lcd.begin(20, 4);
    // Prepare Output pins
    for (byte k = 0; k < OUTARRAYSIZE; k++)
    {
        pinMode(outArray[k], OUTPUT);
        delay(1);
    }
    // Prepare Input pins    
    for (byte k; k < INARRAYSIZE; k++)
    {
        pinMode(inArray[k], INPUT_PULLUP);
        delay(1);
    }
    for (byte k = 0; k < DATASIZE; k++)
    {
        dataArray[k] = EEPROM.read(40 + k);
        Serial.print("ArrayLOC[");
        Serial.print(k);
        Serial.print("] Value: ");
        Serial.println(dataArray[k]);
    }
    pinMode(ledpin, OUTPUT);
    digitalWrite(outArray[0], HIGH);

    byte cVarTemp1 = EEPROM.read(21);
    byte cVarTemp2 = EEPROM.read(22);
    
    cVar = cVarTemp1 + cVarTemp2;
}

void loop()
{
    if (Serial.available() > 0)
    {
        recvWithEndMarker();
    }
    if (newData == true)
    {
        checkData();
    }
    
    if ((run == 2) && (errorLevel == 0))
    {
        byte senCheck = digitalRead(inArray[0]);
        if ((senCheck == LOW) && (millis() - lastRead >= dataArray[0]))
        {
            countInterval++;
            lcd.setCursor(0,1);
            lcd.print("C:");
            lcd.print(countInterval);
            lastRead = millis();
            Serial.print("S:");
            Serial.println(countInterval);
        }
        if (countInterval >= cVar)
        {
            Serial.println("COMPLETE");
            digitalWrite(outArray[0], HIGH);
            digitalWrite(ledpin, LOW);
            countInterval = 0;
            run = 0;
        }
    }
}

void recvWithEndMarker()
{
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;

    while (Serial.available() > 0 && newData == false)
    {
        rc = Serial.read();

        if (rc != endMarker)
        {
            receivedChars[ndx] = rc;
            ndx++;
            apple = apple += rc;
            if (ndx >= numChars)
            {
                ndx = numChars - 1;
            }
        }
        else
        {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            lcd.setCursor(0,0);
            lcd.clear();
            lcd.print(apple);
            newData = true;
        }
    }
}

void checkData()
{
    if (newData == true)
    {
        if (apple.length() >= 3)
        {
            if (apple.substring(0, 9) == "VARCHANGE")
            {
                unsigned int value = lastValue();
                cVar = value;
                lcd.setCursor(0,2);
                lcd.print(cVar);
                if ((value > 250) && (value <= 500))
                {
                    byte tempValue = value - 250;
                    EEPROM.update(21, tempValue);
                    EEPROM.update(22, 250);
                }
                if ((value >= 0) && (value <= 250))
                {
                    EEPROM.update(21, value);
                    EEPROM.update(22, 0);
                }
            }

            if (apple.substring(0, 3) == "RUN")
            {
                byte value = lastValue();
                static byte pause = 0;
                run = value;
                switch (value)
                {
                case 0:
                    run = 0;
                    lcd.clear();
                    lcd.setCursor(0,0);
                    lcd.print("Cycle Stopped");
                    digitalWrite(ledpin, LOW);
                    digitalWrite(outArray[0], HIGH);
                    break;
                case 1:
                    countInterval = 0;
                    // Intentional no break!
                case 2:
                    run = 2;
                    lcd.clear();
                    lcd.setCursor(0,0);
                    lcd.print("Cycle Running");
                    lcd.setCursor(0,2);
                    lcd.print("VAR:");
                    lcd.print(cVar);
                    digitalWrite(outArray[0], LOW);
                    digitalWrite(ledpin, HIGH);
                    lastRead = millis();
                    break;
                default:
                    reportFunction(0);
                    break;
                }
            }
            // Simple test command
            if (apple.substring(0, 4) == "TEST")
            {
                ledStatus = !ledStatus;
                digitalWrite(ledpin, ledStatus);
            }
            if (apple.substring(0, 10) == "DATACHANGE")
            {
                byte address = firstValue();
                // Protect against writing outside of EEPROM memory
                if ((address < 0) || (address >= EEPROM.length()))
                {
                    reportFunction(1);
                    return;
                }
                // Value must remain within limits
                int value = lastValue();
                if (value >= 255)
                {
                    reportFunction(0);
                    return;
                }
                dataArray[address] = value;
                EEPROM.update(address+40,value);
                Serial.print("Updated ArrayLoc[");
                Serial.print(address);
                Serial.print("] Value: ");
                Serial.println(value);
            }
        }
        newData = false;
        apple = "";
    }
}

int firstValue()
{
    char masterArray[numChars];
    byte slaveindx;
    byte value_start = apple.indexOf('.');

    byte value_end = apple.indexOf('.', value_start + 1);

    for (byte k = value_start + 1; k < value_end; k++)
    {
        masterArray[slaveindx] = receivedChars[k];
        slaveindx++;
    }
    masterArray[slaveindx] = '\0';
    Serial.println(masterArray);
    int value = atoi(masterArray);

    return value;
}

// Value after the last instance of a "." to the end of the string/array
int lastValue()
{
    char masterArray[numChars];
    byte slaveindx = 0;
    byte value_end = apple.lastIndexOf('.');

    for (byte k = value_end + 1; k < apple.length(); k++)
    {
        masterArray[slaveindx] = receivedChars[k];
        slaveindx++;
    }
    masterArray[slaveindx] = '\0';
    int lastvalue = atoi(masterArray);

    return lastvalue;
}

void reportFunction(byte code)
{
    switch (code)
    {
    case 0:
        Serial.println("Unexpected input recieved");
        break;
    case 1:
        Serial.println("EEPROM Address not found");
        break;
    }
}
