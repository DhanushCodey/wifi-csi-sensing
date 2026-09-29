# This docs is about the CSI(Channel State Information)

## CSI DATA
- CSI_DATA (app_main.c)
    - #if and #else is used for preprocessor directive controls the portion of source file.

- (#if CONFIG_IDF_TARGET_ESP32C5 || CONFIG_IDF_TARGET_ESP32C6 || CONFIG_IDF_TARGET_ESP32C61)
    - Compile only for these chips
    - these CONFIG_IDF_TARGET* comes from the sdkconfig idf.py set-target esp32 cmd.

- s_count : No of packets has been processed. true if s_count == 0, so the first packet trigger's the header

- uint32_t rx_id = *(uint32_t *)(info->payload + 15);
    -  info->payload : calculates the memeory address
       -  moves 15 bytes into it

## Wifi CSI initalization
- wifi_csi_init (app_main.c)
    - So basiaclly both sender and reciever agrees on a known pattern in order to recieve and transmit packets.
    - [what was sent (known)  →  [ the room ]  →  what arrived (measured)]
    - CSI = arrived / sent
- CSI : is not a measurment its a by product of radio computes every single packet

    ### The two training fields
    - LLTF (Legacy Long Training Field) : Every wifi devices understands it and it covers 64 sub-carriers.
    - HT-LTF (High Troughput Long Training Field) : Comes after legacy and cover full modern band-width, inculding the
                                                    extra sub-carriers 40MHz hence 128.

    why it used? to nullify the echo.

    ### STBC and the merge
    - STBC (Space time block coding) : Used to send the same message again and again in a loop. so if one packet is                                 damaged the other is recieved.
    - stbc_htltf2_en = true says "capture that second one too." this is triggered when stbc is in use.
    - ltf_merge_en avg's the lltf + htltf = 128 + stbc_hltf = 128 = 256 / 2 = 128

## CONFIG_GAIN_CONTROL
    - A set of code which responsible to lock the gain. AGC automatic gain control
    - Strong signal give low volume, weak signals give high volume
    */ 
    esp_csi_gain_ctrl_get_rx_gain(...)     // what gain did we just use?
    if (s_count < 100)  record_rx_gain()   // packets 0–99: write it down
    else if (s_count == 100)               // exactly at packet 100:
    get_rx_gain_baseline(...)          //   what's the typical value?
    set_rx_force_gain(...)             //   lock it there forever
    */
    1. watch the first hundred packets
    2. write down what observed in the first 100
    3. lock the gain

## first_word_invalid
- It's a warning flag the hardware sets. Nothing more.
- Value 0 = the CSI data is fine, read it all.
- Value 1 = the first four bytes of the array are garbage — a known ESP32 hardware quirk where the very start of the buffer comes out corrupted.
- values = values[4:] -> discard the first 4 vals

## The callback rx_cb
- So basically the digits that we see are called by a call-back funtion
- on, every time a packet arrives with CSI attached, the driver calls it and hands you the data.


## Espressif data's

    DATA_COLUMNS_NAMES_C5C6 : describes the data of C5C6 model esp32.
    DATA_COLUMNS_NAMES : describes our esp32 data

   ### Adding img and real number
        csi_data_complex[-1][i] = complex(csi_raw_data[i * 2 + 1], csi_raw_data[i * 2])
        -  reason is simple, the signal has both amplitude and phase where the img_no is used as the real and the phase is real number

   ### usleep(1000 * 1000 / CONFIG_SEND_FREQUENCY);
        - Calculates the packet rate.
    
   ### ESP-NOW
        esp_now_send(peer.peer_addr, (const uint8_t *)&count, sizeof(count));
        - the communication happen by esp-now a communication bridge between esp's.
        - a 4 byte counter that lands in the 15 byte payload. that's why we have calculation of memory address + 15
        box:   0   1   2   3  ...  15  16  17  18  19  20 ...
        [ ] [ ] [ ] [ ]     [ ] [ ] [ ] [ ] [ ] [ ]
                                    └───────────────┘
                                    the counter lives here



    

