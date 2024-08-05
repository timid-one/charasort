from datetime import date
import os
from dotenv_vault import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

load_dotenv()

def transferFileData(inputPath, outputPath, type):
    with open(inputPath, 'r') as fileReader:
        lines = fileReader.readlines()
        with open(outputPath, 'a') as fileWriter:
            for line in lines:
                lineComponents = line.split(' - ', 1)
                fileWriter.write("{name: \"" + lineComponents[0] + "\", img: href=\"" + lineComponents[1].strip('\n') + "\",opts: {status: [\"" + type + "\",]}},\n")
            


def writeLines(path, lines):
    with open(path, 'w') as fileWriter:
        fileWriter.writelines(lines)

def main(): 
    dateStr = str(date.today())
    dir = os.path.dirname(os.path.dirname(__file__))
    filePath = "{}\\{}{}".format(os.path.join(dir, 'js\\data'), dateStr, '.js')
    watchedCommand = "$mmvnisi-"
    unwatchedCommand = "$fnvisi- unwatched"
    headerLines =   [
        "dataSetVersion = \"" + dateStr + "\"; // Change this when creating a new data set version. YYYY-MM-DD format.\ndataSet[dataSetVersion] = {};\n\n",
        "dataSet[dataSetVersion].options = [\n",
        "\t{\n",
        "\t\tname: \"Filter by Watched/Unwatched status\",\n",
        "\t\tkey: \"status\",\n",
        "\t\ttooltip: \"Check this to restrict to watched/unwatched characters.\",\n",
        "\t\tchecked: false,\n",
        "\t\tsub: [\n",
        "\t\t\t{ name: \"Watched\", key: \"wch\" },\n",
        "\t\t\t{ name: \"Unwatched\", key: \"unw\" },\n",
        "\t\t]\n",
        "\t},\n",
        "];\n",
        "dataSet[dataSetVersion].characterData = [\n" 
    ]
    if(os.getenv("GETFILEDATA") == None):
        print("Must include file data option in .env file")
        return

    match os.getenv("GETFILEDATA").lower().strip():
        case "true":
            watchedPath = os.getenv("WATCHEDFILEPATH")
            unwatchedPath = os.getenv("UNWATCHEDFILEPATH")

            if(watchedPath is None):
                print("Please ensure WATCHEDFILEPATH option in .env file is present")
                return
            
            
            if(unwatchedPath is None):
                print("Please ensure UNWATCHEDFILEPATH option in .env file is present")
                return

            if(not os.path.exists(watchedPath)):
                watchedPath = os.path.join(dir, watchedPath)
                if(not os.path.exists(watchedPath)):
                    print("Failed to obtain watched file path for character names. Please ensure WATCHEDFILEPATH is valid")
                    print("Erroneous Filepath:" + watchedPath)
                    return  
            
            if(not os.path.exists(unwatchedPath)):
                unwatchedPath = os.path.join(dir, unwatchedPath)
                if(not os.path.exists(unwatchedPath)):
                    print("Failed to obtain watched file path for character names. Please ensure UNWATCHEDFILEPATH is valid")
                    print("Erroneous Filepath:" + watchedPath)
                    return  
            
            writeLines(filePath, headerLines)
            
            transferFileData(watchedPath, filePath, 'wch')
            transferFileData(unwatchedPath, filePath, 'unw')

            with open(filePath, 'a') as fileWriter:
                fileWriter.write(']')

        case "false":
            token = os.getenv("TOKEN")
            serverID = os.getenv("SERVERID")
            channelID = os.getenv("CHANNELID")
            if(token is None):
                print("Discord token not provided, please ensure the TOKEN field is not empty")
                return
            
            if(serverID is None):
                print("Waifubot server ID not provided, please ensure the SERVERID field is not empty")
                return
            
            if(channelID is None):
                print("Waifubot channel ID not provided, please ensure the CHANNELID field is not empty")
                return
            
            print(os.path.join(dir, 'geckodriver.exe'))
            cService = webdriver.FirefoxService(executable_path=os.path.join(dir, '\\scripts\\geckodriver.exe'))
            driver = webdriver.Firefox(service=cService)
            driver.get("https://discord.com")
            driver.execute_script("function login(token) {setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `\"" + token + "\"`}, 50);setTimeout(() => {location.reload();}, 2500);}login(token);")
            driver.get("https://discord.com/channels/{}/{}".format(serverID, channelID))
            
            writeLines(filePath, headerLines)
        case _:
            print("Invalid setting value provided for GETFILEDATA. Valid values are either TRUE or FALSE")
            return


        


if __name__=="__main__": 
    main() 