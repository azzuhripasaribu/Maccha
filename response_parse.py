def response_parser(response_mesage_raw: bytearray) -> str:
    # Put your request message decoding logic here.
    # This method return a str.
    # Anda boleh menambahkan helper fungsi/method sebanyak yang Anda butuhkan selama
    # TIDAK MENGUBAH ATAUPUN MENGHAPUS  SPEC (parameter dan return type) YANG DIMINTA.

    #PARSE HEADER
    c = response_mesage_raw
    ID=struct.unpack('!H',c[0:2])[0]
    c = c[2:]
    
    temp = bytetobin(c[0])
    QR = int(temp[0])
    OPCODE = int(temp[1:5],2)
    
    AA = int(temp[5], 2)
    TC = int(temp[6], 2)
    RD = int(temp[7], 2)
    
    temp = bytetobin(c[1])
    RA = int(temp[0], 2)
    Z = int(temp[1],2)
    AD = int(temp[2],2)
    CD = int(temp[3],2)
    RCODE = int(temp[4:], 2)
    
    c = c[2:]
    QDCOUNT,ANCOUNT,NSCOUNT,ARCOUNT = struct.unpack('!HHHH',c[0:8])
    
    ## GET NAME
    domain_name = ''
    response_byte = response_mesage_raw[12:]
    name_length = response_byte[0]
    while name_length != 0:
        response_byte = response_byte[1:]
        name = ''
        for i in range(name_length):
            name_char = chr(response_byte[i])
            name += name_char
        name += '.'
        response_byte = response_byte[name_length:]
        name_length = response_byte[0]
        domain_name += name
    domain_name = domain_name[:-1]

    response_byte = response_byte[1:]
    
    # GET TYPE
    type_byte = response_byte[0:2]
    response_byte = response_byte[2:]

    typestr = type_byte[0]*256 + type_byte[1]

    # GET CLASS
    class_byte = response_byte[0:2]
    response_byte = response_byte[2:]

    class_str = class_byte[0]*256 + type_byte[1]
    
    # GET TTL
    TTL_byte = response_byte[0:4]
    response_byte = response_byte[4:]
    
    ttl = TTL_byte[0]*256*265*256 + TTL_byte[1]*256*256 + TTL_byte[2]*256 + TTL_byte[3]

    #Get Data Length
    DL_byte = response_byte[0:2]
    response_byte = response_byte[2:]

    length = DL_byte[0]*256 + DL_byte[1]
    
    #Get Data
    ip = ''
    for i in range(4):
        ip = ip + str(response_byte[i])
        ip += '.'
    ip = ip[:-1]

    message = f"""[Response from DNS Server]\n
-------------------------------------------------------------------------\n
HEADERS\n
Request ID: {ID}\n
QR: {QR} | OPCODE: {OPCODE} | AA: {AA} | TC: {TC}> | RD: {RD} | RA: {RA} | AD: {AD} | CD: {CD} | RCODE: {RCODE}\n
Question Count: {QDCOUNT} | Answer Count: {ANCOUNT} | Authority Count: {NSCOUNT} | Additional Count: {ARCOUNT}\n
-------------------------------------------------------------------------\n
QUESTION\n
Domain Name: {domain_name} | QTYPE: {typestr} | QCLASS: {class_str}\n
-------------------------------------------------------------------------\n
ANSWER
TYPE: {typestr} | CLASS: {class_str} | TTL: {ttl} | RDLENGTH: {length}
IP Address: {ip}
==========================================================================

"""

    return(message)