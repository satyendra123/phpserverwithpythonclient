import mysql.connector
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Enable Access Permission of particular origin
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    return response

# Read Input value of json from user [Note: json.loads converts the input value into a dictionary]
@app.route('/validate', methods=['POST'])
def validate_qr_code():
    # Read JSON data from request
    data = request.get_json()

    device_id = data.get('did', None)
    qrcode = data.get('qrcde', None)
    match_id = qrcode[3:7]
    sectorid = qrcode[7:9]

    valid_invalid = "invalid"
    connected_maingate_subgate = ""
    devID = ""
    gateID = ""
    subdevID = ""
    subgateID = ""

    # check deviceID is exists or not.
    if not device_id:
        return jsonify({'status': 'error', 'msg': 'deviceid not found'})
    elif not qrcode:
        return jsonify({'status': 'error', 'msg': 'qrcode not found'})
    else:
        # Connecting to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mohali_stad_tickets"
        )
        mycursor = mydb.cursor(dictionary=True)

        # check the device validation on FULL HEIGHT TURNSTILE
        mycursor.execute("SELECT id, machid, devicename, status FROM devices WHERE deviceid=%s", (device_id,))
        results_deviceDT = mycursor.fetchone()
        if results_deviceDT:
            devID = results_deviceDT['id']
            valid_invalid = "valid"

            # Read Connected GateID
            mycursor.execute("SELECT devices.id, pavgates.id as gateid FROM devices "
                              "INNER JOIN machines ON machines.id = devices.machid "
                              "INNER JOIN pavgates ON pavgates.id = machines.gateid "
                              "WHERE devices.deviceid=%s", (device_id,))
            results_devDT = mycursor.fetchone()
            if results_devDT:
                gateID = results_devDT['gateid']
                connected_maingate_subgate = "MainGate"
        else:
            # check the sub device validation on TURNSTILE
            mycursor.execute("SELECT id, subdevicename, status FROM subdevices WHERE subdeviceid=%s", (device_id,))
            results_subdeviceDT = mycursor.fetchone()
            if results_subdeviceDT:
                subdevID = results_subdeviceDT['id']
                valid_invalid = "valid"

                # Read Connected Sub GateID
                mycursor.execute("SELECT subdevices.id, submachines.id, pavsubgates.id as subgateid FROM subdevices "
                                  "INNER JOIN submachines ON submachines.id = subdevices.submachid "
                                  "INNER JOIN pavsubgates ON pavsubgates.id = submachines.subgateid "
                                  "INNER JOIN pavgates ON pavgates.id = pavsubgates.pavgateid "
                                  "WHERE subdevices.id=%s", (subdevID,))
                results_subdevDT = mycursor.fetchone()
                if results_subdevDT:
                    subgateID = results_subdevDT['subgateid']
                    connected_maingate_subgate = "SubGate"
            else:
                mydb.close()
                return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'invalid deviceid'})

        # Device is verified "OK"
        if valid_invalid == "valid":
            if connected_maingate_subgate == "MainGate":
                mycursor.execute("SELECT * FROM visitortickets WHERE barcode=%s AND status='Active'", (qrcode,))
                results_QR = mycursor.fetchone()
                if results_QR:
                    qrCodeTable = results_QR['barcode']
                    if qrCodeTable == qrcode:
                        mycursor.execute("SELECT * FROM sectors WHERE sectorcode=%s AND gatecode=%s AND status='Active'",
                                         (sectorid, gateID))
                        results_sector = mycursor.fetchone()
                        if results_sector:
                            ticktstatus = 'Deactive'
                            mycursor.execute("UPDATE visitortickets SET status=%s WHERE barcode=%s", (ticktstatus, qrCodeTable))
                            mydb.commit()
                            mydb.close()
                            return jsonify({'status': 'success', 'ticket': 'valid'})
                        else:
                            mydb.close()
                            return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'wrong gate entry'})
                    else:
                        mydb.close()
                        return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'ticket qr code not present'})
                else:
                    mydb.close()
                    return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'ticket qrcode not found or deactive'})
            elif connected_maingate_subgate == "SubGate":
                mydb.close()
                return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'gate not found'})
            else:
                mydb.close()
                return jsonify({'status': 'error', 'ticket': 'invalid', 'msg': 'gate not found'})

if __name__ == '__main__':
    app.run(debug=True)