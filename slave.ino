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

// Time control
unsigned long lastRead = 0;

// Serial comms
boolean newData = false;
const byte numChars = 32;
char recievedChars[numChars];
String apple = "";
byte initial = 1;

unsigned int cVar = 0;          //Variable counting to
unsigned int countInterval = 0; //Current count

void setup()
{
    // Prepare Output pins
    for (byte k; k < OUTARRAYSIZE; k++)
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

    for (byte k; k < DATASIZE; k++)
    {
        dataArray[k] = EEPROM.read(40 + k)
    }
    pinMode(ledpin, OUTPUT);
    Serial.begin(DATASPEED);
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

    if ((run == 1) && (errorLevel == 0))
    {
        byte senCheck = digitialRead([inArray[0]]);
        if ((senCheck >= 1) && (millis() - lastRead >= dataArray[0]))
        {
            countInterval++;
            lastRead = millis();
        }
        if (countInterval >= cVar)
        {
            // Serial.println("Complete");
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
            if (apple.substring(0, 8) == "VARCHANGE")
            {
                unsigned int value = lastValue();
                cVar = value;
            }
            if (apple.substring(0, 3) == "RUN")
            {
                byte value = lastValue();
                run = value;
                switch (value)
                {
                case 0:
                    run = 0;
                    break;
                case 1:
                    run = 1;
                    digitalWrite(outArray[0], HIGH);
                    lastRead = millis();
                    countInterval = 0;
                    break;
                default:
                    reportFunction(0);
                    break;
                }
            }
            if (apple.substring(0, 4) == "TEST")
            {
                ledStatus = !ledStatus;
                digitalWrite(ledpin, ledStatus)
            }
            if (apple.substring(0, 3) == "DATACHANGE")
            {
                byte address = firstValue();
                int value = lastValue();
                dataArray[address] = value;
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
    if (debug >= 2)
    {
        Serial.print("V Start: ");
        Serial.println(value_start);
    }
    byte value_end = apple.indexOf('.', value_start + 1);
    if (debug >= 2)
    {
        Serial.print("V End: ");
        Serial.println(value_end);
    }
    for (byte k = value_start + 1; k < value_end; k++)
    {
        masterArray[slaveindx] = receivedChars[k];
        slaveindx++;
    }
    masterArray[slaveindx] = '\0';
    Serial.println(masterArray);
    int value = atoi(masterArray);

    if (debug >= 2)
    {
        Serial.print("fvF firstValue: ");
        Serial.println(value);
    }
    return value;
}

// Value after the last instance of a "." to the end of the string/array
int lastValue()
{
    char masterArray[numChars];
    byte slaveindx = 0;
    byte value_end = apple.lastIndexOf('.');
    if (debug >= 2)
    {
        Serial.print("V End (2): ");
        Serial.println(value_end);
    }
    for (byte k = value_end + 1; k < apple.length(); k++)
    {
        masterArray[slaveindx] = receivedChars[k];
        slaveindx++;
    }
    masterArray[slaveindx] = '\0';
    int lastvalue = atoi(masterArray);
    if (debug >= 2)
    {
        Serial.print("lvF lastValue: ");
        Serial.println(lastvalue);
    }
    return lastvalue;
}

void reportFunction(byte code)
{
    switch (code)
    {
    case 0:
        Serial.println("Unexpected input recieved") break;
    }
}
#include <EEPROM.h>
