import serial
import serial.tools.list_ports
import time
import string
import io
from io import StringIO
from xmodem import XMODEM, NAK, CRC, ACK

global ser

ports = list(serial.tools.list_ports.comports())
ser = serial.Serial(ports[1].device, baudrate=115200, bytesize=8, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=0, rtscts=0, dsrdtr=0)

def str_output(strcom):
    result = strcom.find('[0;37m')
    if(result > 0):
        dm = strcom.replace('[0;37m','')
        result = 0
        print(dm)

def serial_ports():
    if ser.isOpen():
        print("Com port is closed")
        ser.close()
    ser.open()
    print('Connected ' + ser.name)
    # Wait until there is data waiting in the serial buffer
    ser.write(("\r").encode())
    time.sleep(1)
    s_command = ''
    print ('Enter your commands below.\r\nInsert "exit" to leave the application.\r\n')
    while (s_command != 'exit'):
        print('Enter command>')
        s_command = input()
        if(s_command == 'exit'):
            ser.close()
        elif((s_command == '/fota/image 0') or (s_command == '/fota/image 1')):
            buffer = open("C:\\hex\\Beacon_013\\app.bin",'rb')
            #ser.readall()
            readUntil(CRC)
            #strup = c_char.decode('UTF-8')
            #print(str_output(strup))
            XMODEM(getc,putc).send(buffer, quiet = 1)
            buffer.close()
            print('ok')
        else:
            ser.write((s_command + "\r").encode('Ascii'))
            s_command = ''
            out = ser.readall()  # read_all()
            strup = out.decode('UTF-8')
            print(str_output(strup))

def readUntil(char = None):
    def serialPortWriter():
        while True:
            tmp = ser.read(1)
            if not tmp or (char and char == tmp):
                break
            yield tmp
    return ''.join(serialPortWriter())

def putc(data, timeout = 1):
    ser.write(data)
    time.sleep(0.001) # give delay to send an ACK
    
def getc(size, timeout = 1):
    return ser.read(size)

if __name__ == '__main__':
    serial_ports()
    


