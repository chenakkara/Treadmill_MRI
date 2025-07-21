// TTL pulse generation code.
// input - serial input '1' from the optical flow python script
// output - TTL pulse LOW
 
void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin as an output
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); // TTL in is active low
  // Check if there is new serial data available
  if (Serial.available() > 0) {
    // Read the latest character from the serial buffer
    char receivedChar = Serial.read();
    
    // Process the received character immediately
    if (receivedChar == '1') {
      digitalWrite(LED_BUILTIN, LOW); // Turn on the LED
      delay(50); // Keep the LED on for 50 milliseconds
      digitalWrite(LED_BUILTIN, HIGH); // Turn off the LED
      delay(950); // wait for 1 TR after triggering - change this according to the TR of the MR imaging sequence 
      // Print acknowledgment message via serial
      Serial.println("Received '1', LED turned ON");
    }
    // Add additional conditions for other characters if needed
    else {
      digitalWrite(LED_BUILTIN, HIGH); // Turn off the LED
    }
    
    // Clear any remaining data in the serial buffer (optional)
    while (Serial.available() > 0) {
      char clearChar = Serial.read(); // Read and discard any extra characters
    } 
  }
}
