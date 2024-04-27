"""
Author: Chanakya NV (chnkya@gmail.com)
Purpose: For Twitter Coding Challenge.
Description:
    A simple tool to gather status metrics from each server and output aggregated result.

"""

# Server Settings
SERVER_FILE_LOCATION = "servers.txt"
SERVER_PORT = "80"
SERVER_PROTOCOL = "http"
SERVER_END_POINT = "status"
SERVER_SUFFIX = ".twitter.com"

# Thread Settings
MAX_THREAD_COUNT = "" #Should default to CPU threads or a tuned number.

# Results
RESULT_FILE = "result.txt"
result = {}
response_list = []

import threading
import os.path
import requests
import logging
import socket
import validators
import json

logging.basicConfig(level=logging.INFO)


class Utils:

    def get_status(self, server):
        url = SERVER_PROTOCOL + "://" + server + ":" + SERVER_PORT + "/" + SERVER_END_POINT
        status_payload = requests.get(url=url)
        assert status_payload.status_code == 200
        status_payload = status_payload.json()
        response_list.append(status_payload)
        return status_payload


    def is_server_alive(self, server):
        if validators.domain(server):
            try:
                socket.gethostbyname(server)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((server, int(SERVER_PORT)))
                if result == 0:
                    return True
                else:
                    return False
            except socket.error:
                logging.warning("Hostname Lookup Failed for "+server+", Probably Server does not exist !")
                return False
        else:
            logging.warning("Server Domain Name is not valid !")
            return False

    def aggregate_status(self,response_list):
        success_rate_sum = {}
        request_rate_sum = {}
        for server_response in response_list:
            key_set = set(["Application","Version","Success_Count","Request_Count"])
            if key_set.issubset(server_response.keys()):
                if server_response["Application"] in success_rate_sum.keys():
                    if server_response["Version"] in success_rate_sum[server_response["Application"]].keys():
                        success_rate_sum[server_response["Application"]][server_response["Version"]] = \
                            success_rate_sum[server_response["Application"]][server_response["Version"]] + server_response["Success_Count"]
                        request_rate_sum[server_response["Application"]][server_response["Version"]] = \
                            request_rate_sum[server_response["Application"]][server_response["Version"]] + server_response["Request_Count"]
                    else:
                        success_rate_sum[server_response["Application"]][server_response["Version"]] = server_response["Success_Count"]
                        request_rate_sum[server_response["Application"]][server_response["Version"]] = server_response["Request_Count"]
                else:
                    success_rate_sum[server_response["Application"]] = { server_response["Version"]: server_response["Success_Count"] }
                    request_rate_sum[server_response["Application"]] = { server_response["Version"]: server_response["Request_Count"] }
            else:
                logging.warning("Bad JSON Response:"+str(server_response))

        print("\n ----- Success Rate Details ----- ")
        for app_key in success_rate_sum:
            for ver_key in success_rate_sum[app_key]:
                success_rate = round((success_rate_sum[app_key][ver_key]/request_rate_sum[app_key][ver_key])*100,2)
                if app_key in result.keys():
                    result[app_key][ver_key] = success_rate
                    #Print out for Humans.
                    print("Aplication:"+str(app_key)+" Version:"+str(ver_key)+" has success rate of "+str(success_rate)+"%")
                else:
                    result[app_key] = {ver_key: success_rate}
                    #Print out for Humans.
                    print("Aplication:" + str(app_key) + " Version:" + str(ver_key) + " has success rate of " +str(success_rate)+"%")

    def store_result(self):
        try:
            f = open("results.txt", "w+")
        except EOFError as ex:
            logging.error("Caught the EOF error.")
            raise ex
        except IOError as ex:
            logging.error("Caught the I/O error.")
            raise ex
        except:
            raise

        result_in_json = json.dumps(result)
        f.write(result_in_json)
        f.close()

# Main Starts Here

if __name__ == "__main__":
    if os.path.isfile(SERVER_FILE_LOCATION):
        try:
            f = open(SERVER_FILE_LOCATION, 'r')
        except EOFError as ex:
            logging.error("Caught the EOF error.")
            raise ex
        except IOError as ex:
            logging.error("Caught the I/O error.")
            raise ex
        except:
            raise

        obj = Utils()

        # Running Threads for making http calls to avoid serial wait.
        thr = {}

        logging.info("Starting to status check on servers ... ")
        for server in f:
            server = server.strip()
            server = server+SERVER_SUFFIX
            if obj.is_server_alive(server):
                thr[server] = threading.Thread(target=obj.get_status, args=(server,))
                thr[server].start()
            else:
                logging.warning(server+" is not up !")

        for value in thr.values():
            value.join()
        f.close()

        obj.aggregate_status(response_list)

        #Storing result in JSON format to results.txt file for Machines.
        obj.store_result()

    else:
        logging.error(SERVER_FILE_LOCATION+' file does not exist in local directory !')
